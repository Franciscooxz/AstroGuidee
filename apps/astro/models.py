from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Un tema de estudio: Sistema Solar, Estrellas, Agujeros Negros, Galaxias..."""
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    subtitle = models.CharField('Subtitulo', max_length=200, blank=True)
    description = models.TextField('Descripcion', blank=True)
    emoji = models.CharField('Emoji (respaldo)', max_length=8, blank=True, default='')
    icon = models.CharField('Icono', max_length=40, blank=True, default='orbit',
                            help_text='Nombre del icono SVG, ej. orbit, star, galaxy, blackhole.')
    accent = models.CharField('Color de acento (hex)', max_length=7, blank=True, default='#8b5cff',
                              help_text='Color principal de la categoria, ej. #8b5cff')
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def card_count(self):
        return self.cards.filter(is_active=True).count()

    @property
    def lesson_count(self):
        return self.lessons.filter(is_active=True).count()


class Lesson(models.Model):
    """Una leccion dentro de una unidad. Agrupa unas cuantas tarjetas."""
    category = models.ForeignKey(Category, related_name='lessons', on_delete=models.CASCADE,
                                 verbose_name='Unidad')
    title = models.CharField('Titulo', max_length=120)
    slug = models.SlugField('Slug', max_length=140, unique=True, blank=True)
    subtitle = models.CharField('Subtitulo', max_length=200, blank=True)
    icon = models.CharField('Icono', max_length=40, blank=True, default='')
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Leccion'
        verbose_name_plural = 'Lecciones'
        ordering = ['category__order', 'order']

    def __str__(self):
        return f'{self.category.name} · {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            self.slug = base
        super().save(*args, **kwargs)

    @property
    def card_count(self):
        return self.cards.filter(is_active=True).count()

    @property
    def question_count(self):
        return self.questions.filter(is_active=True).count()

    @property
    def has_quiz(self):
        return self.questions.filter(is_active=True).exists()


class Card(models.Model):
    """Una tarjeta de estudio (flashcard) dentro de una categoria."""
    category = models.ForeignKey(Category, related_name='cards', on_delete=models.CASCADE,
                                 verbose_name='Unidad')
    lesson = models.ForeignKey('Lesson', related_name='cards', on_delete=models.CASCADE,
                               verbose_name='Leccion', null=True, blank=True)
    title = models.CharField('Titulo', max_length=120)
    slug = models.SlugField('Slug', max_length=140, blank=True)
    subtitle = models.CharField('Subtitulo', max_length=200, blank=True,
                                help_text='Ej. "Planeta rocoso", "Gigante gaseoso"')
    summary = models.TextField('Resumen (reverso de la tarjeta)',
                               help_text='Texto breve que se ve al girar la tarjeta.')
    content = models.TextField('Contenido ampliado', blank=True)
    fun_fact = models.CharField('Dato curioso', max_length=250, blank=True)
    emoji = models.CharField('Emoji (respaldo)', max_length=8, blank=True)
    icon = models.CharField('Icono', max_length=40, blank=True, default='',
                            help_text='Nombre del icono SVG, ej. sun, earth, mars, saturn.')
    image = models.ImageField('Imagen', upload_to='astro/cards/', blank=True, null=True)
    image_credit = models.CharField('Credito de imagen', max_length=200, blank=True)
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Mantener la unidad sincronizada con la leccion
        if self.lesson_id:
            self.category = self.lesson.category
        super().save(*args, **kwargs)


class CardProgress(models.Model):
    """Progreso de un usuario sobre una tarjeta."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='card_progress',
                             on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='progress', on_delete=models.CASCADE)
    known = models.BooleanField('Dominada', default=False)
    updated_at = models.DateTimeField('Actualizada', auto_now=True)

    class Meta:
        verbose_name = 'Progreso de tarjeta'
        verbose_name_plural = 'Progreso de tarjetas'
        unique_together = ('user', 'card')

    def __str__(self):
        estado = 'dominada' if self.known else 'vista'
        return f'{self.user} · {self.card} · {estado}'


class LessonProgress(models.Model):
    """Progreso de un usuario sobre una leccion (para el desbloqueo secuencial)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_progress',
                             on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed = models.BooleanField('Completada', default=False)
    completed_at = models.DateTimeField('Completada el', null=True, blank=True)
    updated_at = models.DateTimeField('Actualizada', auto_now=True)

    class Meta:
        verbose_name = 'Progreso de leccion'
        verbose_name_plural = 'Progreso de lecciones'
        unique_together = ('user', 'lesson')

    def __str__(self):
        estado = 'completada' if self.completed else 'en curso'
        return f'{self.user} · {self.lesson.title} · {estado}'


class Question(models.Model):
    """Una pregunta del quiz de una leccion."""
    QTYPES = [
        ('single', 'Opcion multiple'),
        ('truefalse', 'Verdadero / Falso'),
        ('text', 'Escribir respuesta'),
    ]
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE,
                               verbose_name='Leccion')
    text = models.CharField('Pregunta', max_length=300)
    qtype = models.CharField('Tipo', max_length=20, choices=QTYPES, default='single',
                             help_text='En "Escribir respuesta", las opciones marcadas como correctas '
                                       'son las respuestas aceptadas.')
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text[:60]


class Option(models.Model):
    """Una opcion de respuesta de una pregunta."""
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE,
                                 verbose_name='Pregunta')
    text = models.CharField('Opcion', max_length=200)
    is_correct = models.BooleanField('Es correcta', default=False)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class Profile(models.Model):
    """Progreso global del usuario: XP, racha diaria y monedas."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',
                                on_delete=models.CASCADE)
    xp = models.PositiveIntegerField('XP', default=0)
    streak = models.PositiveIntegerField('Racha', default=0)
    best_streak = models.PositiveIntegerField('Mejor racha', default=0)
    last_active = models.DateField('Ultima actividad', null=True, blank=True)
    coins = models.PositiveIntegerField('Cosmos (monedas)', default=0)
    streak_freezes = models.PositiveIntegerField('Congeladores de racha', default=0)
    double_xp_pending = models.BooleanField('Doble XP pendiente', default=False)
    perfect_quizzes = models.PositiveIntegerField('Quizzes perfectos', default=0)
    avatar = models.CharField('Avatar (icono)', max_length=40, blank=True, default='')
    weekly_xp = models.PositiveIntegerField('XP de la semana', default=0)
    week_key = models.CharField('Semana', max_length=10, blank=True, default='')
    frame = models.CharField('Marco de avatar', max_length=40, blank=True, default='')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'{self.user} · {self.xp} XP · racha {self.streak} · {self.coins} Cosmos'

    def register_activity(self):
        """Actualiza la racha diaria segun la ultima actividad."""
        today = timezone.localdate()
        if self.last_active == today:
            return  # ya conto hoy
        if self.last_active == today - timedelta(days=1):
            self.streak += 1
        elif self.last_active == today - timedelta(days=2) and self.streak_freezes > 0:
            self.streak_freezes -= 1  # el congelador cubrio el dia perdido
            self.streak += 1
        else:
            self.streak = 1
        self.last_active = today
        self.best_streak = max(self.best_streak, self.streak)

    def add_xp(self, amount):
        self.xp += max(0, amount)

    def add_coins(self, amount):
        self.coins += max(0, amount)

    def add_weekly_xp(self, amount):
        wk = timezone.localdate().strftime('%G-%V')
        if self.week_key != wk:
            self.week_key = wk
            self.weekly_xp = 0
        self.weekly_xp += max(0, amount)


class ShopItem(models.Model):
    """Un articulo de la tienda que se compra con Cosmos."""
    EFFECTS = [
        ('streak_freeze', 'Congelar racha'),
        ('double_xp', 'Doble XP en el proximo quiz'),
        ('frame', 'Marco de avatar (cosmetico)'),
    ]
    key = models.SlugField('Clave', max_length=40, unique=True)
    name = models.CharField('Nombre', max_length=100)
    description = models.CharField('Descripcion', max_length=200, blank=True)
    icon = models.CharField('Icono', max_length=40, blank=True, default='coin')
    price = models.PositiveIntegerField('Precio (Cosmos)', default=10)
    effect = models.CharField('Efecto', max_length=30, choices=EFFECTS)
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Articulo de tienda'
        verbose_name_plural = 'Tienda'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.name} ({self.price} Cosmos)'


class Purchase(models.Model):
    """Registro de un cosmetico comprado por un usuario (para saber que posee)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases',
                             on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, related_name='purchases', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        unique_together = ('user', 'item')

    def __str__(self):
        return f'{self.user} · {self.item.name}'


class Achievement(models.Model):
    """Un logro/insignia que se desbloquea al cumplir un hito."""
    CONDITIONS = [
        ('lessons_completed', 'Lecciones completadas'),
        ('streak', 'Racha (dias)'),
        ('xp', 'XP total'),
        ('perfect_quizzes', 'Quizzes perfectos'),
    ]
    key = models.SlugField('Clave', max_length=40, unique=True)
    name = models.CharField('Nombre', max_length=100)
    description = models.CharField('Descripcion', max_length=200, blank=True)
    icon = models.CharField('Icono', max_length=40, blank=True, default='star')
    condition_type = models.CharField('Condicion', max_length=30, choices=CONDITIONS)
    threshold = models.PositiveIntegerField('Meta', default=1)
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Logro'
        verbose_name_plural = 'Logros'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Registro de un logro desbloqueado por un usuario."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='achievements',
                             on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, related_name='unlocked_by',
                                    on_delete=models.CASCADE)
    earned_at = models.DateTimeField('Desbloqueado el', auto_now_add=True)

    class Meta:
        verbose_name = 'Logro de usuario'
        verbose_name_plural = 'Logros de usuarios'
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f'{self.user} · {self.achievement.name}'
