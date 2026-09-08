# -*- coding: utf-8 -*-
"""Nivel 2 'Observacion' (Fase R4): unidad nueva."""
from django.db import migrations
from django.utils.text import slugify

UNIT = {'slug': 'observacion-astronomica', 'name': 'Observacion',
        'subtitle': 'Encuentra y mira el cielo', 'icon': 'star',
        'accent': '#b18bff', 'order': 3, 'difficulty': 2}

LESSONS = [
    {'slug': 'prepararte-para-observar', 'title': 'Prepararte para observar', 'icon': 'moon',
     'subtitle': 'Cielo oscuro y ojos listos', 'order': 1,
     'cards': [
        ('El enemigo: la luz de la ciudad', 'Contaminacion luminica',
         'Las luces de las ciudades iluminan el cielo y borran las estrellas mas debiles. Por eso desde una ciudad ves pocas, y desde el campo oscuro, miles. Buscar cielos oscuros es el primer paso.',
         'Mucha gente de ciudad nunca ha visto la Via Lactea a simple vista.'),
        ('Deja que tus ojos se adapten', 'Vision nocturna',
         'Tus ojos tardan unos 20-30 minutos en adaptarse a la oscuridad y ver estrellas debiles. Una luz blanca lo arruina en un segundo; por eso los astronomos usan luz roja.', ''),
        ('El seeing', 'La atmosfera tiembla',
         'El seeing es la estabilidad del aire. Cuando la atmosfera tiembla, las estrellas titilan y las imagenes se ven borrosas. Con buen seeing el cielo esta mas quieto y nitido.',
         'Por eso los grandes telescopios se ponen en montanas altas y secas.'),
     ],
     'questions': [
        ('Que es la contaminacion luminica?', 'single',
         'Las luces de las ciudades iluminan el cielo y ocultan las estrellas mas debiles; desde el campo oscuro ves muchas mas.',
         [('El exceso de luz artificial que borra las estrellas', True), ('Un gas venenoso', False),
          ('La luz de la Luna', False), ('Un tipo de estrella', False)]),
        ('Cuanto tardan tus ojos en adaptarse a la oscuridad?', 'single',
         'Unos 20-30 minutos; una luz blanca arruina esa adaptacion al instante.',
         [('Unos 20-30 minutos', True), ('1 segundo', False), ('Varias horas', False), ('No se adaptan', False)]),
        ('Que color de luz usan los astronomos para no perder la vision nocturna?', 'single',
         'La luz roja apenas afecta a la adaptacion de los ojos a la oscuridad.',
         [('Roja', True), ('Blanca', False), ('Azul', False), ('Verde', False)]),
        ('Que es el seeing?', 'single',
         'Con buen seeing el aire esta quieto y las imagenes se ven nitidas; con mal seeing, todo tiembla.',
         [('La estabilidad de la atmosfera al observar', True), ('El tamano del telescopio', False),
          ('El brillo de la Luna', False), ('Un planeta', False)]),
        ('Desde una ciudad se ven muchas mas estrellas que desde el campo oscuro.', 'truefalse',
         'Es al reves: la contaminacion luminica de la ciudad borra las estrellas debiles.',
         [('Falso', True), ('Verdadero', False)]),
        ('Por que titilan las estrellas?', 'single',
         'El aire en movimiento desvia su luz; en el espacio, sin atmosfera, no titilarian.',
         [('Por la turbulencia de la atmosfera', True), ('Porque se encienden y apagan', False),
          ('Por la Luna', False), ('Por su color', False)]),
     ]},
    {'slug': 'binoculares-y-telescopios', 'title': 'Binoculares y telescopios', 'icon': 'star',
     'subtitle': 'Tus herramientas', 'order': 2,
     'cards': [
        ('Empieza con binoculares', 'Mas de lo que crees',
         'No hace falta un telescopio caro para empezar. Unos binoculares normales ya te muestran los crateres de la Luna, las lunas de Jupiter y muchos cumulos de estrellas.',
         'Galileo cambio la historia con un telescopio peor que tus binoculares.'),
        ('Lo que importa: la apertura', 'Cuanta luz recoge',
         'En un telescopio, lo mas importante NO es cuanto aumenta, sino su apertura: el diametro de su lente o espejo. A mas apertura, mas luz recoge y mas objetos debiles ves.', ''),
        ('Aumento y distancia focal', 'No te obsesiones con el zoom',
         'El aumento depende del ocular y de la distancia focal. Mucho aumento con poca apertura da imagenes oscuras y borrosas. Vale mas ver nitido que ver grande.', ''),
     ],
     'questions': [
        ('Con que puedes empezar a observar sin gastar mucho?', 'single',
         'Unos binoculares ya muestran crateres de la Luna, lunas de Jupiter y cumulos de estrellas.',
         [('Con unos binoculares', True), ('Solo con un telescopio carisimo', False),
          ('Con un microscopio', False), ('Con nada', False)]),
        ('Que es lo mas importante en un telescopio?', 'single',
         'La apertura determina cuanta luz recoge; a mas apertura, mas objetos debiles se ven.',
         [('La apertura (diametro del espejo o lente)', True), ('Cuanto aumenta', False),
          ('Su color', False), ('Su peso', False)]),
        ('Mas aumento siempre significa mejor imagen.', 'truefalse',
         'Mucho aumento con poca apertura da imagenes oscuras y borrosas. Vale mas nitidez que tamano.',
         [('Falso', True), ('Verdadero', False)]),
        ('Que puedes ver de Jupiter con unos simples binoculares?', 'single',
         'Sus lunas mas grandes se ven como puntitos al lado, igual que las vio Galileo.',
         [('Sus lunas mas grandes', True), ('Su nucleo', False), ('Nada', False), ('Su interior', False)]),
        ('De que depende cuanta luz recoge un telescopio?', 'single',
         'A mayor diametro del espejo o lente, mas luz capta y mas debil es lo que alcanzas a ver.',
         [('De su apertura', True), ('De su ocular', False), ('De su tripode', False), ('De su color', False)]),
        ('Escribe la parte del telescopio que determina cuanta luz recoge (una palabra).', 'text',
         'La apertura (el diametro del espejo o la lente) es lo que manda para captar luz.',
         [('apertura', True), ('la apertura', True), ('diametro', True)]),
     ]},
    {'slug': 'que-observar', 'title': 'Que observar', 'icon': 'galaxy',
     'subtitle': 'De la Luna al cielo profundo', 'order': 3,
     'cards': [
        ('La Luna y los planetas', 'Los reyes del principiante',
         'Lo mas facil y espectacular para empezar: los crateres de la Luna, los anillos de Saturno, las fases de Venus y las lunas de Jupiter. Con poco equipo ya impresionan.', ''),
        ('Cielo profundo', 'Cumulos y nebulosas',
         'Mas alla del Sistema Solar estan los objetos de cielo profundo: cumulos de estrellas, nebulosas (nubes de gas donde nacen estrellas) y galaxias. Necesitan cielos oscuros y paciencia.',
         'La nebulosa de Orion se ve incluso con binoculares.'),
        ('Estrellas dobles', 'Dos por el precio de una',
         'Muchas estrellas son en realidad dos que orbitan juntas: estrellas dobles. Separarlas con un telescopio, a veces con colores distintos, es un clasico de la observacion.', ''),
     ],
     'questions': [
        ('Cual es un objeto ideal para empezar a observar?', 'single',
         'La Luna, Saturno con sus anillos o las lunas de Jupiter son faciles y espectaculares con poco equipo.',
         [('La Luna y sus crateres', True), ('Un agujero negro', False),
          ('Una galaxia lejana muy debil', False), ('El nucleo del Sol', False)]),
        ('Que son los objetos de cielo profundo?', 'single',
         'Cumulos de estrellas, nebulosas y galaxias mas alla del Sistema Solar; piden cielos oscuros.',
         [('Cumulos, nebulosas y galaxias mas alla del Sistema Solar', True), ('Los planetas', False),
          ('Las fases de la Luna', False), ('Los satelites artificiales', False)]),
        ('Que es una estrella doble?', 'single',
         'Muchas estrellas son en realidad dos que orbitan juntas; separarlas con un telescopio es un clasico.',
         [('Dos estrellas que orbitan juntas', True), ('Una estrella muy grande', False),
          ('Una estrella y un planeta', False), ('Dos galaxias', False)]),
        ('La nebulosa de Orion se puede ver incluso con binoculares.', 'truefalse',
         'Es de los objetos de cielo profundo mas faciles; se ve como una manchita difusa.',
         [('Verdadero', True), ('Falso', False)]),
        ('Que planeta es famoso por sus anillos, visibles con un telescopio pequeno?', 'single',
         'Los anillos de Saturno son uno de los espectaculos favoritos de los observadores.',
         [('Saturno', True), ('Marte', False), ('Mercurio', False), ('La Tierra', False)]),
        ('Que son las nebulosas?', 'single',
         'En muchas nebulosas nacen estrellas nuevas a partir del gas y el polvo.',
         [('Nubes de gas y polvo, muchas veces cunas de estrellas', True), ('Estrellas muy calientes', False),
          ('Planetas gaseosos', False), ('Lunas heladas', False)]),
     ]},
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    unit, _ = Category.objects.get_or_create(slug=UNIT['slug'], defaults={
        'name': UNIT['name'], 'subtitle': UNIT['subtitle'], 'icon': UNIT['icon'],
        'accent': UNIT['accent'], 'order': UNIT['order'], 'difficulty': UNIT['difficulty'],
        'is_active': True})
    Category.objects.filter(pk=unit.pk).update(
        name=UNIT['name'], order=UNIT['order'], difficulty=UNIT['difficulty'], is_active=True)

    for data in LESSONS:
        if Lesson.objects.filter(slug=data['slug']).exists():
            continue
        lesson = Lesson.objects.create(
            category=unit, title=data['title'], slug=data['slug'], subtitle=data['subtitle'],
            icon=data['icon'], order=data['order'], is_active=True)
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
    Lesson.objects.filter(slug__in=[d['slug'] for d in LESSONS]).delete()
    Category.objects.filter(slug=UNIT['slug']).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0050_seed_nivel1'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
