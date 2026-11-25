"""Contenido de aprendizaje: unidades, lecciones, tarjetas y preguntas."""

from django.db import models
from django.utils.text import slugify


class Stage(models.Model):
    """Etapa de la ruta. Agrupa unidades; no es un currículo oficial."""

    code = models.SlugField("Código", max_length=20, unique=True)
    name = models.CharField("Nombre", max_length=80)
    summary = models.CharField("Resumen", max_length=240, blank=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Category(models.Model):
    """Una unidad de la ruta. El progreso se guarda por lección, no por el orden."""

    STATUS = [
        ("published", "Publicada"),
        ("draft", "Borrador"),
        ("archived", "Archivada"),
    ]

    name = models.CharField("Nombre", max_length=100)
    stage = models.ForeignKey(
        Stage,
        related_name="units",
        on_delete=models.PROTECT,
        verbose_name="Etapa",
        null=True,
        blank=True,
    )
    code = models.SlugField(
        "Código estable",
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="Identificador de la unidad, por ejemplo u01. No cambia si se reordena.",
    )
    status = models.CharField(
        "Estado editorial",
        max_length=20,
        choices=STATUS,
        default="published",
    )
    slug = models.SlugField("Slug", max_length=120, unique=True, blank=True)
    subtitle = models.CharField("Subtitulo", max_length=200, blank=True)
    description = models.TextField("Descripcion", blank=True)
    emoji = models.CharField("Emoji (respaldo)", max_length=8, blank=True, default="")
    icon = models.CharField(
        "Icono",
        max_length=40,
        blank=True,
        default="orbit",
        help_text="Nombre del icono SVG, ej. orbit, star, galaxy, blackhole.",
    )
    accent = models.CharField(
        "Color de acento (hex)",
        max_length=7,
        blank=True,
        default="#8b5cff",
        help_text="Color principal de la categoria, ej. #8b5cff",
    )
    order = models.PositiveIntegerField("Orden", default=0)
    difficulty = models.PositiveSmallIntegerField(
        "Dificultad",
        default=1,
        choices=[
            (1, "Nivel 1 · Introductorio"),
            (2, "Nivel 2 · Basico"),
            (3, "Nivel 3 · Intermedio"),
            (4, "Nivel 4 · Avanzado"),
            (5, "Nivel 5 · Experto"),
        ],
        help_text="1 = mas facil de aprobar. A mayor nivel, se exige acertar mas.",
    )
    is_active = models.BooleanField("Activa", default=True)

    DIFFICULTY_NAMES = {
        1: "Introductorio",
        2: "Basico",
        3: "Intermedio",
        4: "Avanzado",
        5: "Experto",
    }

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def difficulty_name(self):
        return self.DIFFICULTY_NAMES.get(self.difficulty, "Introductorio")

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

    REVIEW = [
        ("unverified", "Sin comprobación documental"),
        ("sources_checked", "Fuentes comprobadas; sin revisión experta"),
        ("expert_reviewed", "Revisión humana experta"),
    ]

    category = models.ForeignKey(
        Category, related_name="lessons", on_delete=models.CASCADE, verbose_name="Unidad"
    )
    title = models.CharField("Titulo", max_length=120)
    slug = models.SlugField("Slug", max_length=140, unique=True, blank=True)
    subtitle = models.CharField("Subtitulo", max_length=200, blank=True)
    objective = models.TextField("Objetivo", blank=True)
    prerequisites = models.CharField("Conocimientos previos", max_length=240, blank=True)
    summary = models.TextField("Resumen", blank=True)
    connections = models.CharField("Conexiones con lo anterior", max_length=240, blank=True)
    references = models.TextField(
        "Referencias",
        blank=True,
        help_text="Una fuente por línea, con el enlace de la página consultada.",
    )
    source_checked = models.DateField("Fecha de comprobación", null=True, blank=True)
    review_state = models.CharField(
        "Revisión",
        max_length=24,
        choices=REVIEW,
        default="unverified",
    )
    duration_min = models.PositiveSmallIntegerField("Minutos estimados", default=4)
    icon = models.CharField("Icono", max_length=40, blank=True, default="")
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activa", default=True)

    class Meta:
        verbose_name = "Leccion"
        verbose_name_plural = "Lecciones"
        ordering = ["category__order", "order"]

    def __str__(self):
        return f"{self.category.name} · {self.title}"

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

    category = models.ForeignKey(
        Category, related_name="cards", on_delete=models.CASCADE, verbose_name="Unidad"
    )
    lesson = models.ForeignKey(
        "Lesson",
        related_name="cards",
        on_delete=models.CASCADE,
        verbose_name="Leccion",
        null=True,
        blank=True,
    )
    title = models.CharField("Titulo", max_length=120)
    slug = models.SlugField("Slug", max_length=140, blank=True)
    subtitle = models.CharField(
        "Subtitulo", max_length=200, blank=True, help_text='Ej. "Planeta rocoso", "Gigante gaseoso"'
    )
    summary = models.TextField(
        "Resumen (reverso de la tarjeta)", help_text="Texto breve que se ve al girar la tarjeta."
    )
    content = models.TextField("Contenido ampliado", blank=True)
    fun_fact = models.CharField("Dato curioso", max_length=250, blank=True)
    emoji = models.CharField("Emoji (respaldo)", max_length=8, blank=True)
    icon = models.CharField(
        "Icono",
        max_length=40,
        blank=True,
        default="",
        help_text="Nombre del icono SVG, ej. sun, earth, mars, saturn.",
    )
    image = models.ImageField("Imagen", upload_to="astro/cards/", blank=True, null=True)
    image_credit = models.CharField("Credito de imagen", max_length=200, blank=True)
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activa", default=True)

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Mantener la unidad sincronizada con la leccion
        if self.lesson_id:
            self.category = self.lesson.category
        super().save(*args, **kwargs)


class Question(models.Model):
    """Una pregunta del quiz de una leccion."""

    QTYPES = [
        ("single", "Opcion multiple"),
        ("truefalse", "Verdadero / Falso"),
        ("text", "Escribir respuesta"),
    ]
    lesson = models.ForeignKey(
        Lesson, related_name="questions", on_delete=models.CASCADE, verbose_name="Leccion"
    )
    text = models.CharField("Pregunta", max_length=300)
    qtype = models.CharField(
        "Tipo",
        max_length=20,
        choices=QTYPES,
        default="single",
        help_text='En "Escribir respuesta", las opciones marcadas como correctas '
        "son las respuestas aceptadas.",
    )
    explanation = models.TextField(
        "Explicacion",
        blank=True,
        help_text="Se muestra tras responder: el porque de la respuesta "
        "(convierte el fallo en aprendizaje).",
    )
    image = models.ImageField(
        "Imagen",
        upload_to="questions/",
        blank=True,
        null=True,
        help_text='Opcional: p.ej. "identifica este planeta".',
    )
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activa", default=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]


class Option(models.Model):
    """Una opcion de respuesta de una pregunta."""

    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE, verbose_name="Pregunta"
    )
    text = models.CharField("Opcion", max_length=200)
    is_correct = models.BooleanField("Es correcta", default=False)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Opcion"
        verbose_name_plural = "Opciones"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text
