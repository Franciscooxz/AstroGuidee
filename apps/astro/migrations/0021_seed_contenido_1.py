# -*- coding: utf-8 -*-
from django.db import migrations
from django.utils.text import slugify


# Estructura: unidades (orden 2,3,4) -> lecciones -> tarjetas + preguntas.
# q = (texto, tipo, [(opcion, es_correcta), ...])
DATA = [
    {
        'unit': {'name': 'La Luna y los eclipses', 'order': 2, 'icon': 'planet', 'accent': '#9aa7c7',
                 'subtitle': 'Nuestro satelite y sus fenomenos.',
                 'description': 'La Luna es el objeto mas cercano a la Tierra y el que mejor conocemos. '
                                'Aqui veras que es, por que cambia de forma y como ocurren los eclipses.'},
        'lessons': [
            {'title': 'La Luna', 'icon': 'planet', 'order': 1,
             'cards': [
                 ('La Luna', 'El satelite de la Tierra',
                  'Es el unico satelite natural de la Tierra y el quinto mas grande del Sistema Solar. '
                  'No tiene luz propia: brilla porque refleja la luz del Sol.',
                  'La Luna se aleja de la Tierra unos 3,8 cm cada ano.'),
                 ('De donde salio la Luna', 'La teoria del gran impacto',
                  'La idea mas aceptada es que hace 4.500 millones de anos un cuerpo del tamano de Marte '
                  'choco con la Tierra, y de los restos se formo la Luna.',
                  'Por eso la Luna y la Tierra tienen composiciones muy parecidas.'),
                 ('Las mareas', 'La Luna mueve el mar',
                  'La gravedad de la Luna tira del agua de los oceanos y provoca las mareas: el sube y '
                  'baja del nivel del mar dos veces al dia.', ''),
             ],
             'questions': [
                 ('Que es la Luna?', 'single', [('Un satelite natural', True), ('Un planeta', False),
                                                ('Una estrella', False), ('Un cometa', False)]),
                 ('La Luna tiene luz propia.', 'truefalse', [('Verdadero', False), ('Falso', True)]),
                 ('Que causa principalmente las mareas?', 'single',
                  [('La gravedad de la Luna', True), ('El viento', False),
                   ('La rotacion de las nubes', False), ('El calor del Sol', False)]),
             ]},
            {'title': 'Fases de la Luna', 'icon': 'planet', 'order': 2,
             'cards': [
                 ('Por que cambia de forma', 'Las fases',
                  'Siempre vemos la mitad de la Luna iluminada por el Sol, pero desde la Tierra la vemos '
                  'desde distintos angulos segun su posicion. Por eso parece cambiar de forma.', ''),
                 ('Las 4 fases principales', 'Nueva, creciente, llena, menguante',
                  'Luna nueva (no se ve), cuarto creciente, luna llena (completa) y cuarto menguante. '
                  'El ciclo completo dura unos 29,5 dias.',
                  'De ahi viene la palabra "mes": un ciclo lunar.'),
             ],
             'questions': [
                 ('Por que la Luna tiene fases?', 'single',
                  [('Por su posicion relativa entre el Sol y la Tierra', True),
                   ('Porque se apaga y se enciende', False),
                   ('Por las nubes', False), ('Porque gira muy rapido', False)]),
                 ('Cuanto dura aproximadamente un ciclo lunar? (numero de dias)', 'text',
                  [('29', True), ('30', True), ('29.5', True)]),
             ]},
            {'title': 'Eclipses', 'icon': 'sun', 'order': 3,
             'cards': [
                 ('Eclipse solar', 'La Luna tapa al Sol',
                  'Ocurre cuando la Luna se pone entre el Sol y la Tierra y proyecta su sombra sobre '
                  'nosotros, tapando al Sol por unos minutos.',
                  'Nunca mires un eclipse solar directamente sin proteccion.'),
                 ('Eclipse lunar', 'La Tierra tapa la luz',
                  'Ocurre cuando la Tierra se pone entre el Sol y la Luna, y su sombra cae sobre la Luna. '
                  'La Luna se ve rojiza: la "luna de sangre".', ''),
             ],
             'questions': [
                 ('En un eclipse solar, que tapa al Sol?', 'single',
                  [('La Luna', True), ('La Tierra', False), ('Una nube', False), ('Marte', False)]),
                 ('En un eclipse lunar la Luna se ve rojiza.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Las estrellas', 'order': 3, 'icon': 'star', 'accent': '#ffce4d',
                 'subtitle': 'Los soles del universo.',
                 'description': 'Las estrellas son gigantescas esferas de gas que producen luz y calor. '
                                'Veras que son, por que tienen distintos colores y como nacen y mueren.'},
        'lessons': [
            {'title': 'Que es una estrella', 'icon': 'star', 'order': 1,
             'cards': [
                 ('Una estrella', 'Una esfera de gas que brilla',
                  'Es una enorme bola de gas (sobre todo hidrogeno) tan caliente que su nucleo fusiona '
                  'atomos y libera muchisima energia: luz y calor.', 'El Sol es la estrella mas cercana.'),
                 ('Fusion nuclear', 'El motor de las estrellas',
                  'En el nucleo, la presion y el calor unen atomos de hidrogeno formando helio. Ese '
                  'proceso, la fusion nuclear, es lo que hace brillar a una estrella.', ''),
             ],
             'questions': [
                 ('De que estan hechas principalmente las estrellas?', 'single',
                  [('Gas (hidrogeno y helio)', True), ('Roca', False), ('Hielo', False), ('Metal', False)]),
                 ('Que proceso da energia a una estrella?', 'single',
                  [('La fusion nuclear', True), ('La combustion', False),
                   ('La electricidad', False), ('La friccion', False)]),
             ]},
            {'title': 'Tipos de estrellas', 'icon': 'star', 'order': 2,
             'cards': [
                 ('El color y la temperatura', 'El color revela el calor',
                  'El color de una estrella indica su temperatura: las azules y blancas son las mas '
                  'calientes, y las rojas las mas frias. El Sol, amarillo, esta en medio.',
                  'Al reves que el agua: aqui el azul es lo mas caliente.'),
                 ('Tamanos', 'De enanas a supergigantes',
                  'Hay estrellas enanas (pequenas), como el Sol, y supergigantes cientos de veces mas '
                  'grandes. Cuanto mas masiva, mas rapido vive y muere.', ''),
             ],
             'questions': [
                 ('Que color de estrella es el mas caliente?', 'single',
                  [('Azul', True), ('Rojo', False), ('Amarillo', False), ('Naranja', False)]),
                 ('Las estrellas rojas son las mas frias.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
             ]},
            {'title': 'Vida y muerte de una estrella', 'icon': 'flame', 'order': 3,
             'cards': [
                 ('Como nacen', 'En nubes de gas',
                  'Las estrellas nacen dentro de enormes nubes de gas y polvo llamadas nebulosas, cuando '
                  'la gravedad junta la materia hasta encender la fusion.', ''),
                 ('Como mueren', 'Depende de su masa',
                  'Una estrella como el Sol termina como enana blanca. Las muy masivas explotan como '
                  'supernova y pueden dejar una estrella de neutrones o un agujero negro.',
                  'Los atomos de tu cuerpo se formaron dentro de estrellas.'),
             ],
             'questions': [
                 ('Donde nacen las estrellas?', 'single',
                  [('En nebulosas (nubes de gas y polvo)', True), ('En los planetas', False),
                   ('En los agujeros negros', False), ('En los cometas', False)]),
                 ('Como se llama la explosion de una estrella muy masiva al morir?', 'text',
                  [('Supernova', True)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Galaxias', 'order': 4, 'icon': 'galaxy', 'accent': '#b18bff',
                 'subtitle': 'Islas de miles de millones de estrellas.',
                 'description': 'Una galaxia es un enorme conjunto de estrellas, gas y polvo unido por la '
                                'gravedad. Conoceras la nuestra, la Via Lactea, y los tipos que existen.'},
        'lessons': [
            {'title': 'La Via Lactea', 'icon': 'galaxy', 'order': 1,
             'cards': [
                 ('Nuestra galaxia', 'La Via Lactea',
                  'Es la galaxia donde vivimos. Tiene forma de espiral y contiene entre 100.000 y 400.000 '
                  'millones de estrellas. El Sol es solo una de ellas, en uno de sus brazos.',
                  'Tardariamos 100.000 anos en cruzarla a la velocidad de la luz.'),
                 ('El centro', 'Un agujero negro gigante',
                  'En el centro de la Via Lactea hay un agujero negro supermasivo llamado Sagitario A*, '
                  'millones de veces mas masivo que el Sol.', ''),
             ],
             'questions': [
                 ('Como se llama nuestra galaxia?', 'text', [('Via Lactea', True)]),
                 ('Que forma tiene la Via Lactea?', 'single',
                  [('Espiral', True), ('Cubica', False), ('Triangular', False), ('Plana y recta', False)]),
             ]},
            {'title': 'Tipos de galaxias', 'icon': 'galaxy', 'order': 2,
             'cards': [
                 ('Espirales', 'Con brazos que giran',
                  'Como la Via Lactea: un disco con brazos en espiral donde nacen muchas estrellas nuevas.', ''),
                 ('Elipticas e irregulares', 'Otras formas',
                  'Las elipticas tienen forma de balon y estrellas viejas; las irregulares no tienen una '
                  'forma definida, a menudo por choques entre galaxias.',
                  'Las galaxias tambien chocan: la Via Lactea chocara con Andromeda en unos 4.000 millones de anos.'),
             ],
             'questions': [
                 ('Cual de estos NO es un tipo de galaxia?', 'single',
                  [('Cuadrada', True), ('Espiral', False), ('Eliptica', False), ('Irregular', False)]),
                 ('Dos galaxias pueden chocar entre si.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
             ]},
        ],
    },
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    for block in DATA:
        u = block['unit']
        unit, _ = Category.objects.get_or_create(
            slug=slugify(u['name']),
            defaults={'name': u['name'], 'subtitle': u['subtitle'], 'description': u['description'],
                      'emoji': '', 'icon': u['icon'], 'accent': u['accent'], 'order': u['order']},
        )
        for ldata in block['lessons']:
            lesson, _ = Lesson.objects.get_or_create(
                slug=slugify(ldata['title']),
                defaults={'category': unit, 'title': ldata['title'],
                          'icon': ldata['icon'], 'order': ldata['order']},
            )
            for ci, card in enumerate(ldata['cards'], start=1):
                title, subtitle, summary, fun = card
                Card.objects.get_or_create(
                    lesson=lesson, slug=slugify(title),
                    defaults={'category': unit, 'title': title, 'subtitle': subtitle,
                              'summary': summary, 'fun_fact': fun, 'icon': lesson.icon, 'order': ci},
                )
            for qi, q in enumerate(ldata['questions'], start=1):
                text, qtype, options = q
                if Question.objects.filter(lesson=lesson, text=text).exists():
                    continue
                question = Question.objects.create(lesson=lesson, text=text, qtype=qtype, order=qi)
                for oi, (otext, correct) in enumerate(options, start=1):
                    Option.objects.create(question=question, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    slugs = [slugify(b['unit']['name']) for b in DATA]
    Category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0020_onboarding'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
