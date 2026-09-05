from django.db import migrations


# { slug_leccion: [ (pregunta, [(opcion, es_correcta), ...]), ... ] }
QUIZZES = {
    'el-sol': [
        ('Que tipo de cuerpo celeste es el Sol?', [
            ('Una estrella', True), ('Un planeta', False),
            ('Un cometa', False), ('Una luna', False)]),
        ('Que proceso genera la energia del Sol?', [
            ('Fusion nuclear', True), ('Combustion de madera', False),
            ('Electricidad', False), ('Friccion', False)]),
        ('Que porcentaje de la masa del Sistema Solar tiene el Sol?', [
            ('Mas del 99%', True), ('Un 50%', False),
            ('Un 10%', False), ('Menos del 1%', False)]),
    ],
    'planetas-rocosos': [
        ('Cual es el planeta mas cercano al Sol?', [
            ('Mercurio', True), ('Venus', False), ('Tierra', False), ('Marte', False)]),
        ('Por que Marte se ve rojo?', [
            ('Por el oxido de hierro de su superficie', True),
            ('Porque esta en llamas', False), ('Por el agua', False), ('Por el hielo', False)]),
        ('Cual es el planeta mas caliente del Sistema Solar?', [
            ('Venus', True), ('Mercurio', False), ('Marte', False), ('Tierra', False)]),
    ],
    'gigantes-gaseosos': [
        ('Cual es el planeta mas grande del Sistema Solar?', [
            ('Jupiter', True), ('Saturno', False), ('Tierra', False), ('Neptuno', False)]),
        ('Que planeta es famoso por sus espectaculares anillos?', [
            ('Saturno', True), ('Jupiter', False), ('Marte', False), ('Venus', False)]),
    ],
    'gigantes-helados': [
        ('Cual es el planeta mas alejado del Sol?', [
            ('Neptuno', True), ('Urano', False), ('Saturno', False), ('Jupiter', False)]),
        ('Que tiene de especial la rotacion de Urano?', [
            ('Gira casi de lado', True), ('Gira al reves del tiempo', False),
            ('No gira', False), ('Gira mas rapido que la luz', False)]),
    ],
}


def forwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    for lesson_slug, questions in QUIZZES.items():
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
        except Lesson.DoesNotExist:
            continue
        if lesson.questions.exists():
            continue  # ya sembrado
        for qi, (qtext, options) in enumerate(questions, start=1):
            q = Question.objects.create(lesson=lesson, text=qtext, order=qi)
            for oi, (otext, correct) in enumerate(options, start=1):
                Option.objects.create(question=q, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    Question.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0008_quiz_xp'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
