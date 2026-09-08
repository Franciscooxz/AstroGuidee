"""Progreso del usuario: tarjetas, lecciones, repaso (SM-2), estadistica y examenes."""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class CardProgress(models.Model):
    """Progreso de un usuario sobre una tarjeta."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="card_progress", on_delete=models.CASCADE
    )
    card = models.ForeignKey("Card", related_name="progress", on_delete=models.CASCADE)
    known = models.BooleanField("Dominada", default=False)
    updated_at = models.DateTimeField("Actualizada", auto_now=True)

    class Meta:
        verbose_name = "Progreso de tarjeta"
        verbose_name_plural = "Progreso de tarjetas"
        unique_together = ("user", "card")

    def __str__(self):
        estado = "dominada" if self.known else "vista"
        return f"{self.user} · {self.card} · {estado}"


class LessonProgress(models.Model):
    """Progreso de un usuario sobre una leccion (para el desbloqueo secuencial)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="lesson_progress", on_delete=models.CASCADE
    )
    lesson = models.ForeignKey("Lesson", related_name="progress", on_delete=models.CASCADE)
    completed = models.BooleanField("Completada", default=False)
    completed_at = models.DateTimeField("Completada el", null=True, blank=True)
    updated_at = models.DateTimeField("Actualizada", auto_now=True)

    class Meta:
        verbose_name = "Progreso de leccion"
        verbose_name_plural = "Progreso de lecciones"
        unique_together = ("user", "lesson")

    def __str__(self):
        estado = "completada" if self.completed else "en curso"
        return f"{self.user} · {self.lesson.title} · {estado}"


class ReviewItem(models.Model):
    """Programacion de repaso espaciado (SM-2) de una pregunta para un usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE
    )
    question = models.ForeignKey("Question", related_name="reviews", on_delete=models.CASCADE)
    ease = models.FloatField("Facilidad", default=2.5)
    interval = models.PositiveIntegerField("Intervalo (dias)", default=0)
    reps = models.PositiveIntegerField("Repeticiones", default=0)
    lapses = models.PositiveIntegerField("Fallos", default=0)
    due = models.DateField("Proximo repaso", default=timezone.localdate)
    last_reviewed = models.DateTimeField("Ultimo repaso", null=True, blank=True)

    class Meta:
        verbose_name = "Repaso"
        verbose_name_plural = "Repasos"
        unique_together = ("user", "question")
        ordering = ["due"]

    def __str__(self):
        return f"{self.user} · {self.question} · vence {self.due}"

    def schedule(self, correct):
        """Actualiza el intervalo segun SM-2 (respuesta binaria correcto/incorrecto)."""
        today = timezone.localdate()
        if correct:
            if self.reps == 0:
                self.interval = 1
            elif self.reps == 1:
                self.interval = 3
            else:
                self.interval = max(1, round(self.interval * self.ease))
            self.reps += 1
            self.ease = min(3.0, self.ease + 0.1)
        else:
            self.reps = 0
            self.interval = 1
            self.lapses += 1
            self.ease = max(1.3, self.ease - 0.2)
        self.due = today + timedelta(days=self.interval)
        self.last_reviewed = timezone.now()


class QuestionStat(models.Model):
    """Estadistica acumulada de un usuario sobre una pregunta (analitica y repaso de flojos)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="question_stats", on_delete=models.CASCADE
    )
    question = models.ForeignKey("Question", related_name="stats", on_delete=models.CASCADE)
    seen = models.PositiveIntegerField("Veces respondida", default=0)
    correct = models.PositiveIntegerField("Aciertos", default=0)
    last_seen = models.DateTimeField("Ultima vez", null=True, blank=True)

    class Meta:
        verbose_name = "Estadistica de pregunta"
        verbose_name_plural = "Estadisticas de preguntas"
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user} · {self.question} · {self.correct}/{self.seen}"

    @property
    def accuracy(self):
        return round(self.correct / self.seen * 100) if self.seen else 0


class UnitExam(models.Model):
    """Resultado del examen final de una unidad para un usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="unit_exams", on_delete=models.CASCADE
    )
    category = models.ForeignKey("Category", related_name="exams", on_delete=models.CASCADE)
    passed = models.BooleanField("Aprobado", default=False)
    best_score = models.PositiveSmallIntegerField("Mejor nota (%)", default=0)
    attempts = models.PositiveIntegerField("Intentos", default=0)
    passed_at = models.DateTimeField("Aprobado el", null=True, blank=True)

    class Meta:
        verbose_name = "Examen de unidad"
        verbose_name_plural = "Examenes de unidad"
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user} · {self.category} · {self.best_score}%"
