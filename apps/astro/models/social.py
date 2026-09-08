"""Social y calidad: seguir usuarios, duelos 1v1 y reportes de preguntas."""

from django.conf import settings
from django.db import models


class Follow(models.Model):
    """Relacion social: un usuario sigue a otro."""

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="following_set", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="followers_set", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField("Desde", auto_now_add=True)

    class Meta:
        verbose_name = "Seguimiento"
        verbose_name_plural = "Seguimientos"
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} -> {self.following}"


class Duel(models.Model):
    """Duelo 1v1 asincrono: ambos responden el mismo set de preguntas."""

    challenger = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="duels_sent", on_delete=models.CASCADE
    )
    opponent = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="duels_received", on_delete=models.CASCADE
    )
    question_ids = models.JSONField("Preguntas", default=list)
    challenger_score = models.PositiveSmallIntegerField(default=0)
    opponent_score = models.PositiveSmallIntegerField(default=0)
    challenger_done = models.BooleanField(default=False)
    opponent_done = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        default="pending",
        choices=[("pending", "Pendiente"), ("complete", "Terminado")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Duelo"
        verbose_name_plural = "Duelos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.challenger} vs {self.opponent}"

    @property
    def winner_id(self):
        if self.status != "complete":
            return None
        if self.challenger_score > self.opponent_score:
            return self.challenger_id
        if self.opponent_score > self.challenger_score:
            return self.opponent_id
        return None  # empate


class QuestionReport(models.Model):
    """Reporte de un usuario sobre una pregunta con posible error."""

    REASONS = [
        ("opcion", "La respuesta correcta esta mal"),
        ("confusa", "La pregunta es confusa"),
        ("datos", "Error en los datos"),
        ("otro", "Otro"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="question_reports", on_delete=models.CASCADE
    )
    question = models.ForeignKey("Question", related_name="reports", on_delete=models.CASCADE)
    reason = models.CharField("Motivo", max_length=20, choices=REASONS, default="otro")
    resolved = models.BooleanField("Resuelto", default=False)
    created_at = models.DateTimeField("Reportado", auto_now_add=True)

    class Meta:
        verbose_name = "Reporte de pregunta"
        verbose_name_plural = "Reportes de preguntas"
        unique_together = ("user", "question")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.question} · {self.get_reason_display()}"
