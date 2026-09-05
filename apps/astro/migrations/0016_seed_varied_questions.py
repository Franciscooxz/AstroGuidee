from django.db import migrations


# Preguntas de demostracion de los nuevos tipos, en la leccion 'el-sol'
DEMO = [
    {
        'text': 'El Sol es una estrella.', 'qtype': 'truefalse', 'order': 10,
        'options': [('Verdadero', True), ('Falso', False)],
    },
    {
        'text': 'Escribe el elemento mas abundante en el Sol (una palabra).',
        'qtype': 'text', 'order': 11,
        'options': [('Hidrogeno', True), ('H', True)],  # respuestas aceptadas
    },
]


def forwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')
    try:
        lesson = Lesson.objects.get(slug='el-sol')
    except Lesson.DoesNotExist:
        return
    for data in DEMO:
        if Question.objects.filter(lesson=lesson, text=data['text']).exists():
            continue
        q = Question.objects.create(lesson=lesson, text=data['text'],
                                    qtype=data['qtype'], order=data['order'])
        for i, (otext, correct) in enumerate(data['options'], start=1):
            Option.objects.create(question=q, text=otext, is_correct=correct, order=i)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    Question.objects.filter(text__in=[d['text'] for d in DEMO]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0015_question_types'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
