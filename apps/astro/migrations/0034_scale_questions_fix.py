# -*- coding: utf-8 -*-
from django.db import migrations

# Completa 3 lecciones que quedaron 1 pregunta corta (una propuesta coincidia
# con una ya existente y se omitio). Cierra el cupo de su nivel.
ADD = {
    'galaxias-asombrosas': [  # nivel 3 -> 7
        ("Que separa a unas galaxias de otras en el espacio?", 'single',
         [("Enormes vacios casi sin materia", True), ("Aire", False),
          ("Agua", False), ("Muros solidos", False)]),
    ],
    'el-horizonte-de-sucesos': [  # nivel 3 -> 7
        ("Visto desde fuera, que parece pasarle al tiempo cerca del horizonte de sucesos?", 'single',
         [("Parece transcurrir cada vez mas lento", True), ("Se acelera", False),
          ("Desaparece de golpe", False), ("No cambia nada", False)]),
    ],
    'famosos-y-ondas-gravitacionales': [  # nivel 4 -> 8
        ("Ademas de agujeros negros, que otros objetos al fusionarse emiten ondas gravitacionales?", 'single',
         [("Estrellas de neutrones", True), ("Planetas rocosos", False),
          ("Asteroides", False), ("Cometas", False)]),
    ],
}


def forwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')
    for slug, questions in ADD.items():
        try:
            lesson = Lesson.objects.get(slug=slug)
        except Lesson.DoesNotExist:
            continue
        base = lesson.questions.count()
        for qi, (text, qtype, options) in enumerate(questions, start=base + 1):
            if Question.objects.filter(lesson=lesson, text=text).exists():
                continue
            q = Question.objects.create(lesson=lesson, text=text, qtype=qtype, order=qi)
            for oi, (otext, correct) in enumerate(options, start=1):
                Option.objects.create(question=q, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    texts = [q[0] for qs in ADD.values() for q in qs]
    Question.objects.filter(text__in=texts).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0033_scale_questions'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
