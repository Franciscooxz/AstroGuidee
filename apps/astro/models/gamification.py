"""Perfil del usuario, economia (tienda/compras), logros, notificaciones y misiones."""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Progreso global del usuario: XP, racha diaria y monedas."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    xp = models.PositiveIntegerField("XP", default=0)
    streak = models.PositiveIntegerField("Racha", default=0)
    best_streak = models.PositiveIntegerField("Mejor racha", default=0)
    last_active = models.DateField("Ultima actividad", null=True, blank=True)
    coins = models.PositiveIntegerField("Cosmos (monedas)", default=0)
    streak_freezes = models.PositiveIntegerField("Congeladores de racha", default=0)
    double_xp_pending = models.BooleanField("Doble XP pendiente", default=False)
    perfect_quizzes = models.PositiveIntegerField("Quizzes perfectos", default=0)
    avatar = models.CharField("Avatar (icono)", max_length=40, blank=True, default="")
    weekly_xp = models.PositiveIntegerField("XP de la semana", default=0)
    week_key = models.CharField("Semana", max_length=10, blank=True, default="")
    week_perfect = models.PositiveIntegerField("Quizzes perfectos de la semana", default=0)
    division = models.PositiveSmallIntegerField("Division de liga", default=0)
    streak_reward_max = models.PositiveIntegerField("Ultimo hito de racha premiado", default=0)
    pending_chest = models.PositiveIntegerField("Cofre de racha por abrir", default=0)
    daily_goal = models.PositiveSmallIntegerField("Meta diaria (lecciones)", default=1)
    frame = models.CharField("Marco de avatar", max_length=40, blank=True, default="")
    onboarded = models.BooleanField("Vio la bienvenida", default=False)
    daily_claimed = models.DateField("Meta diaria cobrada el", null=True, blank=True)
    hearts = models.PositiveIntegerField("Vidas", default=5)
    hearts_updated = models.DateTimeField("Vidas actualizadas", null=True, blank=True)
    reminder_on = models.BooleanField("Aviso diario", default=True)
    reminder_hour = models.PositiveSmallIntegerField("Hora del aviso", default=19)
    last_reminded = models.DateField("Ultimo aviso", null=True, blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.user} · {self.xp} XP · racha {self.streak} · {self.coins} Cosmos"

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

    def _ensure_week(self, wk):
        """Reinicia los contadores semanales si cambio la semana ISO."""
        if self.week_key != wk:
            self.week_key = wk
            self.weekly_xp = 0
            self.week_perfect = 0

    def add_weekly_xp(self, amount):
        self._ensure_week(timezone.localdate().strftime("%G-%V"))
        self.weekly_xp += max(0, amount)

    def add_week_perfect(self):
        self._ensure_week(timezone.localdate().strftime("%G-%V"))
        self.week_perfect += 1


class ShopItem(models.Model):
    """Un articulo de la tienda que se compra con Cosmos."""

    EFFECTS = [
        ("streak_freeze", "Congelar racha"),
        ("double_xp", "Doble XP en el proximo quiz"),
        ("refill_hearts", "Recargar vidas"),
        ("frame", "Marco de avatar (cosmetico)"),
    ]
    key = models.SlugField("Clave", max_length=40, unique=True)
    name = models.CharField("Nombre", max_length=100)
    description = models.CharField("Descripcion", max_length=200, blank=True)
    icon = models.CharField("Icono", max_length=40, blank=True, default="coin")
    price = models.PositiveIntegerField("Precio (Cosmos)", default=10)
    effect = models.CharField("Efecto", max_length=30, choices=EFFECTS)
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = "Articulo de tienda"
        verbose_name_plural = "Tienda"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} ({self.price} Cosmos)"


class Purchase(models.Model):
    """Registro de un cosmetico comprado por un usuario (para saber que posee)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE
    )
    item = models.ForeignKey(ShopItem, related_name="purchases", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        unique_together = ("user", "item")

    def __str__(self):
        return f"{self.user} · {self.item.name}"


class Notification(models.Model):
    """Notificacion para el centro de notificaciones (campana)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE
    )
    text = models.CharField("Texto", max_length=250)
    icon = models.CharField("Icono", max_length=40, blank=True, default="rocket")
    url = models.CharField("Enlace", max_length=200, blank=True)
    is_read = models.BooleanField("Leida", default=False)
    created_at = models.DateTimeField("Creada", auto_now_add=True)

    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} · {self.text[:40]}"

    @classmethod
    def push(cls, user, text, icon="rocket", url=""):
        """Crea una notificacion para el usuario (helper central)."""
        return cls.objects.create(user=user, text=text[:250], icon=icon, url=url)


class Achievement(models.Model):
    """Un logro/insignia que se desbloquea al cumplir un hito."""

    CONDITIONS = [
        ("lessons_completed", "Lecciones completadas"),
        ("streak", "Racha (dias)"),
        ("xp", "XP total"),
        ("perfect_quizzes", "Quizzes perfectos"),
    ]
    key = models.SlugField("Clave", max_length=40, unique=True)
    name = models.CharField("Nombre", max_length=100)
    description = models.CharField("Descripcion", max_length=200, blank=True)
    icon = models.CharField("Icono", max_length=40, blank=True, default="star")
    condition_type = models.CharField("Condicion", max_length=30, choices=CONDITIONS)
    threshold = models.PositiveIntegerField("Meta", default=1)
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = "Logro"
        verbose_name_plural = "Logros"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Registro de un logro desbloqueado por un usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="achievements", on_delete=models.CASCADE
    )
    achievement = models.ForeignKey(
        Achievement, related_name="unlocked_by", on_delete=models.CASCADE
    )
    earned_at = models.DateTimeField("Desbloqueado el", auto_now_add=True)

    class Meta:
        verbose_name = "Logro de usuario"
        verbose_name_plural = "Logros de usuarios"
        unique_together = ("user", "achievement")

    def __str__(self):
        return f"{self.user} · {self.achievement.name}"


class MissionClaim(models.Model):
    """Registro de una mision semanal cuya recompensa ya reclamo el usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="mission_claims", on_delete=models.CASCADE
    )
    mission_key = models.CharField("Mision", max_length=40)
    week_key = models.CharField("Semana", max_length=10)
    claimed_at = models.DateTimeField("Reclamada", auto_now_add=True)

    class Meta:
        verbose_name = "Mision reclamada"
        verbose_name_plural = "Misiones reclamadas"
        unique_together = ("user", "mission_key", "week_key")

    def __str__(self):
        return f"{self.user} · {self.mission_key} · {self.week_key}"
