"""Logica de dominio de AstroGuide: calificacion de respuestas y estadistica.

Se extrae de las vistas para evitar duplicacion (los endpoints finish_* la
compartian) y facilitar los tests unitarios.
"""

import math
import unicodedata

from django.utils import timezone

from .models import QuestionStat

# Umbral de aprobado por nivel de dificultad de la unidad (1 facil -> 5 dificil).
PASS_RATIO = {1: 0.60, 2: 0.67, 3: 0.75, 4: 0.85, 5: 0.90}


def norm_text(s):
    """Normaliza texto para comparar respuestas: sin acentos, minusculas, sin espacios extra."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()


def grade_question(question, value):
    """True si `value` (id de opcion o texto escrito) responde bien la pregunta.

    Unifica los tres tipos de pregunta: en 'text' compara sin acentos contra las
    opciones correctas; en el resto, por id de opcion marcada como correcta.
    """
    if question.qtype == "text":
        typed = norm_text(str(value))
        accepted = [norm_text(o.text) for o in question.options.all() if o.is_correct]
        return bool(typed) and typed in accepted
    return any(o.is_correct and str(o.id) == str(value) for o in question.options.all())


def pass_ratio(difficulty):
    return PASS_RATIO.get(difficulty, 0.60)


def needed_correct(total, difficulty):
    """Aciertos minimos para aprobar segun el nivel."""
    return math.ceil(pass_ratio(difficulty) * total) if total else 0


def record_answer(user, question, correct):
    """Acumula la estadistica del usuario sobre una pregunta (precision / temas flojos)."""
    stat, _ = QuestionStat.objects.get_or_create(user=user, question=question)
    stat.seen += 1
    if correct:
        stat.correct += 1
    stat.last_seen = timezone.now()
    stat.save(update_fields=["seen", "correct", "last_seen"])
