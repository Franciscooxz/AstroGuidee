# -*- coding: utf-8 -*-
"""Nivel 0 'Bienvenido al universo': lecciones de arranque (Fase R2)."""
from django.db import migrations
from django.db.models import F
from django.utils.text import slugify

UNIT_SLUG = 'la-luna-y-los-eclipses'  # unidad Nivel 0 (renombrada a "Bienvenido al universo")

# Nuevas lecciones al inicio (ordenes 1-3). c=(titulo,subtitulo,resumen,dato)
# q=(texto, tipo, explicacion, [(opcion, correcta)])
LESSONS = [
    {
        'slug': 'que-es-la-astronomia', 'title': 'Que es la astronomia', 'icon': 'orbit',
        'subtitle': 'La ciencia del cielo', 'order': 1,
        'cards': [
            ('La ciencia del cielo', 'Mirar mas alla de la Tierra',
             'La astronomia es la ciencia que estudia todo lo que hay mas alla de la Tierra: planetas, estrellas, galaxias y el universo entero. Se apoya en la observacion y la fisica.',
             'Es una de las ciencias mas antiguas: hace miles de anos ya se observaban los astros.'),
            ('Astronomia vs astrologia', 'No son lo mismo',
             'La astronomia es ciencia: mide, predice y se comprueba. La astrologia (los horoscopos) no es ciencia: no hay prueba de que los astros influyan en tu personalidad o tu futuro.',
             'Comparten origen historico, pero se separaron hace siglos.'),
            ('Como sabemos lo que sabemos', 'La luz lo cuenta todo',
             'Casi todo lo que sabemos del universo viene de analizar la luz que nos llega. No hemos tocado una estrella, pero su luz revela de que esta hecha, su temperatura y su movimiento.',
             ''),
        ],
        'questions': [
            ('Que estudia la astronomia?', 'single',
             'La astronomia estudia los astros y el universo: planetas, estrellas, galaxias y su fisica.',
             [('Todo lo que hay mas alla de la Tierra', True), ('Solo los horoscopos', False),
              ('Solo la Tierra', False), ('Solo el clima', False)]),
            ('La astrologia (los horoscopos) es una ciencia.', 'truefalse',
             'No lo es: no hay evidencia de que los astros influyan en tu vida. La astronomia si es ciencia.',
             [('Falso', True), ('Verdadero', False)]),
            ('De donde sacamos casi toda la informacion del universo?', 'single',
             'Analizando la luz sabemos de que estan hechos los astros, su temperatura y su movimiento, sin viajar a ellos.',
             [('De la luz que nos llega de los astros', True), ('Tocando las estrellas', False),
              ('De los horoscopos', False), ('Adivinando', False)]),
            ('La astronomia es una de las ciencias mas antiguas.', 'truefalse',
             'Desde hace miles de anos, muchas culturas observaban y registraban el cielo.',
             [('Verdadero', True), ('Falso', False)]),
            ('Escribe la ciencia que estudia los astros (una palabra).', 'text',
             'Astronomia: del griego astron (astro) y nomos (ley u orden).',
             [('astronomia', True), ('la astronomia', True)]),
        ],
    },
    {
        'slug': 'escalas-y-distancias', 'title': 'Escalas y distancias', 'icon': 'progress',
        'subtitle': 'Como se mide el universo', 'order': 2,
        'cards': [
            ('El universo es enorme', 'Los km se quedan cortos',
             'Las distancias en el espacio son tan gigantescas que el kilometro se queda corto. Por eso los astronomos usan unidades especiales para no manejar numeros imposibles.',
             'La luz, lo mas rapido que existe, tarda 8 minutos en llegar del Sol a la Tierra.'),
            ('Unidad Astronomica (UA)', 'La regla del Sistema Solar',
             '1 UA es la distancia media de la Tierra al Sol (unos 150 millones de km). Sirve para medir comodo dentro del Sistema Solar: Jupiter esta a unas 5 UA.',
             ''),
            ('El ano luz', 'Distancia, no tiempo',
             'Un ano luz es la distancia que recorre la luz en un ano (unos 9,5 billones de km). Ojo: mide distancia, no tiempo. La estrella mas cercana esta a algo mas de 4 anos luz.',
             'Ver una estrella a 100 anos luz es ver su luz de hace 100 anos: miras al pasado.'),
            ('El parsec', 'La unidad de los profesionales',
             'El parsec (unos 3,26 anos luz) es la unidad que mas usan los astronomos. Viene de medir el ligero desplazamiento aparente de una estrella cercana (la paralaje).',
             ''),
        ],
        'questions': [
            ('Que mide un ano luz?', 'single',
             'Aunque suene a tiempo, el ano luz es la DISTANCIA que la luz recorre en un ano (unos 9,5 billones de km).',
             [('Una distancia', True), ('Un tiempo', False), ('Una temperatura', False), ('Un peso', False)]),
            ('Que es una Unidad Astronomica (UA)?', 'single',
             '1 UA es la distancia media Tierra-Sol (unos 150 millones de km). Se usa dentro del Sistema Solar.',
             [('La distancia media Tierra-Sol', True), ('La distancia a la Luna', False),
              ('Un ano luz', False), ('El tamano del Sol', False)]),
            ('Cuanto tarda la luz del Sol en llegar a la Tierra?', 'single',
             'Unos 8 minutos: ves el Sol como era hace 8 minutos.',
             [('Unos 8 minutos', True), ('1 segundo', False), ('Un ano', False), ('Un dia', False)]),
            ('Ver una estrella muy lejana es como mirar al pasado.', 'truefalse',
             'Su luz tardo anos en llegar, asi que la ves como era cuando esa luz salio, no como es hoy.',
             [('Verdadero', True), ('Falso', False)]),
            ('Que unidad usan mas los astronomos para grandes distancias?', 'single',
             'El parsec (unos 3,26 anos luz), derivado del metodo de la paralaje.',
             [('El parsec', True), ('El kilometro', False), ('La UA', False), ('El metro', False)]),
        ],
    },
    {
        'slug': 'tierra-sol-y-luna', 'title': 'Tierra, Sol y Luna', 'icon': 'earth',
        'subtitle': 'Dia, noche y estaciones', 'order': 3,
        'cards': [
            ('El dia y la noche', 'La Tierra gira',
             'La Tierra gira sobre si misma una vez cada 24 horas (rotacion). La mitad iluminada por el Sol tiene dia; la otra, noche. El Sol no "sale": somos nosotros los que giramos.',
             'En el ecuador giras a mas de 1.600 km/h sin notarlo.'),
            ('Las estaciones', 'No es la distancia',
             'Las estaciones no se deben a estar mas cerca o lejos del Sol, sino a que el eje de la Tierra esta inclinado. Por eso cuando es verano en un hemisferio, es invierno en el otro.',
             'La Tierra esta mas cerca del Sol en enero, pleno invierno en el norte.'),
            ('El ano', 'La Tierra viaja alrededor del Sol',
             'La Tierra tarda un ano (unos 365 dias) en dar una vuelta completa al Sol (traslacion). Ese viaje, con el eje inclinado, produce las estaciones.',
             ''),
        ],
        'questions': [
            ('Por que hay dia y noche?', 'single',
             'La rotacion de la Tierra (una vuelta cada 24 h) hace que una mitad tenga dia y la otra noche.',
             [('Porque la Tierra gira sobre si misma', True), ('Porque el Sol se apaga', False),
              ('Porque la Luna tapa el Sol', False), ('Porque la Tierra se aleja del Sol', False)]),
            ('A que se deben las estaciones del ano?', 'single',
             'A la inclinacion del eje de la Tierra; la distancia al Sol casi no influye.',
             [('A la inclinacion del eje de la Tierra', True),
              ('A que la Tierra se acerca y aleja del Sol', False), ('A la Luna', False), ('Al viento solar', False)]),
            ('Cuando es verano en el hemisferio norte, en el sur es...', 'single',
             'Los hemisferios tienen estaciones opuestas por la inclinacion del eje.',
             [('Invierno', True), ('Verano tambien', False), ('Primavera', False), ('Siempre igual', False)]),
            ('La Tierra tarda un ano en dar una vuelta al Sol.', 'truefalse',
             'La traslacion dura unos 365 dias; de ahi la duracion del ano.',
             [('Verdadero', True), ('Falso', False)]),
            ('El Sol gira alrededor de la Tierra cada dia.', 'truefalse',
             'Es un movimiento aparente: en realidad la Tierra rota. El Sol no sale ni se pone, giramos nosotros.',
             [('Falso', True), ('Verdadero', False)]),
        ],
    },
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    try:
        unit = Category.objects.get(slug=UNIT_SLUG)
    except Category.DoesNotExist:
        return

    # Desplazar las lecciones existentes (Luna/Fases/Eclipses) para hacer sitio al inicio
    Lesson.objects.filter(category=unit).update(order=F('order') + len(LESSONS))

    for data in LESSONS:
        if Lesson.objects.filter(slug=data['slug']).exists():
            continue
        lesson = Lesson.objects.create(
            category=unit, title=data['title'], slug=data['slug'],
            subtitle=data['subtitle'], icon=data['icon'], order=data['order'], is_active=True)
        for i, (title, subtitle, summary, fun) in enumerate(data['cards'], start=1):
            Card.objects.create(lesson=lesson, category=unit, slug=slugify(title), title=title,
                                subtitle=subtitle, summary=summary, fun_fact=fun,
                                icon=data['icon'], order=i, is_active=True)
        for qi, (text, qtype, expl, options) in enumerate(data['questions'], start=1):
            q = Question.objects.create(lesson=lesson, text=text, qtype=qtype,
                                        explanation=expl, order=qi, is_active=True)
            for oi, (otext, correct) in enumerate(options, start=1):
                Option.objects.create(question=q, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    slugs = [d['slug'] for d in LESSONS]
    Lesson.objects.filter(slug__in=slugs).delete()
    try:
        unit = Category.objects.get(slug=UNIT_SLUG)
        Lesson.objects.filter(category=unit).update(order=F('order') - len(LESSONS))
    except Category.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0048_reorg_roadmap'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
