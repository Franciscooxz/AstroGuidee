# -*- coding: utf-8 -*-
from django.db import migrations
from django.utils.text import slugify


DATA = [
    {
        'unit': {'name': 'Agujeros negros', 'order': 5, 'icon': 'blackhole', 'accent': '#7c5cff',
                 'subtitle': 'Donde ni la luz escapa.',
                 'description': 'Los objetos mas extremos del universo. Veras que son, como se '
                                'forman y que es el misterioso horizonte de sucesos.'},
        'lessons': [
            {'title': 'Que es un agujero negro', 'icon': 'blackhole', 'order': 1,
             'cards': [
                 ('Un agujero negro', 'Gravedad extrema',
                  'Es una region del espacio con una gravedad tan intensa que nada, ni siquiera la luz, '
                  'puede escapar de ella.', 'Por eso es "negro": no emite ni refleja luz.'),
                 ('Como se forman', 'El final de una estrella gigante',
                  'La mayoria nace cuando una estrella muy masiva agota su combustible y colapsa sobre '
                  'si misma bajo su propia gravedad.', ''),
                 ('No se lo tragan todo', 'Un mito comun',
                  'Un agujero negro no "aspira" todo a su alrededor: solo caes si te acercas demasiado. '
                  'Si el Sol fuera uno del mismo tamano, la Tierra seguiria en orbita.', ''),
             ],
             'questions': [
                 ('Que puede escapar de un agujero negro?', 'single',
                  [('Nada, ni la luz', True), ('Solo la luz', False), ('El sonido', False), ('Los planetas cercanos', False)]),
                 ('Como nace la mayoria de los agujeros negros?', 'single',
                  [('Al colapsar una estrella muy masiva', True), ('Al chocar dos planetas', False),
                   ('Por un cometa', False), ('Por el viento solar', False)]),
                 ('Un agujero negro aspira absolutamente todo lo que hay a su alrededor.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('Por que se llama "negro"?', 'single',
                  [('Porque no emite ni refleja luz', True), ('Porque esta pintado', False),
                   ('Porque es frio', False), ('Porque es pequeno', False)]),
                 ('Escribe que fuerza es la responsable de un agujero negro.', 'text',
                  [('gravedad', True), ('la gravedad', True)]),
             ]},
            {'title': 'El horizonte de sucesos', 'icon': 'blackhole', 'order': 2,
             'cards': [
                 ('El punto de no retorno', 'El borde del agujero',
                  'Es la frontera alrededor de un agujero negro: una vez la cruzas, ya no hay forma de '
                  'volver ni de enviar informacion hacia afuera.', ''),
                 ('La singularidad', 'El corazon',
                  'En el centro, toda la masa se concentra en un punto donde las leyes de la fisica que '
                  'conocemos dejan de funcionar.', ''),
                 ('Se pueden "fotografiar"', 'La primera imagen',
                  'En 2019 se publico la primera imagen de un agujero negro: no se ve el, sino la luz de '
                  'la materia caliente girando a su alrededor.', 'Era el agujero negro de la galaxia M87.'),
             ],
             'questions': [
                 ('Que es el horizonte de sucesos?', 'single',
                  [('El punto de no retorno', True), ('El centro del agujero', False),
                   ('Una estrella', False), ('Una galaxia', False)]),
                 ('Una vez cruzas el horizonte de sucesos, puedes volver.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('Que hay en el centro de un agujero negro?', 'single',
                  [('Una singularidad', True), ('Un planeta', False), ('Una estrella', False), ('Un tunel a otra ciudad', False)]),
                 ('Que muestra la imagen de 2019 de un agujero negro?', 'single',
                  [('La luz de la materia girando a su alrededor', True), ('El interior del agujero', False),
                   ('Un planeta', False), ('Una estrella nueva', False)]),
                 ('En que ano se publico la primera imagen de un agujero negro? (numero)', 'text',
                  [('2019', True)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'El Universo', 'order': 6, 'icon': 'galaxy', 'accent': '#4f7cff',
                 'subtitle': 'El origen y el destino de todo.',
                 'description': 'De donde viene el universo, como crece y de que esta hecho en realidad.'},
        'lessons': [
            {'title': 'El Big Bang', 'icon': 'rocket', 'order': 1,
             'cards': [
                 ('El principio de todo', 'Hace 13.800 millones de anos',
                  'El universo comenzo desde un estado extremadamente denso y caliente, y desde entonces '
                  'no ha parado de expandirse y enfriarse.', 'No fue una explosion en el espacio: fue el espacio mismo estirandose.'),
                 ('No fue una explosion normal', 'Un error comun',
                  'El Big Bang no ocurrio "en" un lugar: todo el espacio estaba junto y empezo a estirarse '
                  'a la vez, en todas partes.', ''),
                 ('El eco del Big Bang', 'La radiacion de fondo',
                  'Todavia podemos detectar un debil resplandor que sobro del universo primitivo: la '
                  'radiacion de fondo de microondas.', ''),
             ],
             'questions': [
                 ('Que describe el Big Bang?', 'single',
                  [('El inicio y la expansion del universo', True), ('El fin del universo', False),
                   ('La muerte del Sol', False), ('Una galaxia', False)]),
                 ('El Big Bang fue una explosion en un punto concreto del espacio.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('Que edad tiene el universo aproximadamente?', 'single',
                  [('Unos 13.800 millones de anos', True), ('Unos 6.000 anos', False),
                   ('Unos 100 millones', False), ('Unos mil anos', False)]),
                 ('Que es la radiacion de fondo de microondas?', 'single',
                  [('El resplandor que sobro del universo primitivo', True), ('Una estrella', False),
                   ('Un planeta', False), ('Una galaxia', False)]),
                 ('Desde el Big Bang, el universo esta...', 'single',
                  [('Expandiendose', True), ('Encogiendose', False), ('Quieto', False), ('Girando en circulo', False)]),
             ]},
            {'title': 'La expansion del universo', 'icon': 'galaxy', 'order': 2,
             'cards': [
                 ('Todo se aleja', 'Las galaxias se separan',
                  'Las galaxias se alejan unas de otras: cuanto mas lejos estan, mas rapido se alejan. '
                  'El universo se hace cada vez mas grande.', ''),
                 ('Quien lo descubrio', 'Edwin Hubble',
                  'En 1929, Edwin Hubble observo que casi todas las galaxias se alejan de nosotros: la '
                  'prueba de que el universo se expande.', 'El telescopio espacial Hubble lleva su nombre.'),
                 ('No hay un centro', 'Como un globo',
                  'Imagina puntos dibujados en un globo que se infla: todos se alejan entre si sin que '
                  'haya un centro. Asi es la expansion del universo.', ''),
             ],
             'questions': [
                 ('Que hacen las galaxias en el universo?', 'single',
                  [('Se alejan unas de otras', True), ('Se acercan', False), ('Estan quietas', False), ('Chocan siempre', False)]),
                 ('Quien descubrio la expansion del universo?', 'single',
                  [('Edwin Hubble', True), ('Isaac Newton', False), ('Galileo', False), ('Colon', False)]),
                 ('El universo tiene un centro desde el que todo se aleja.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('Cuanto mas lejos esta una galaxia...', 'single',
                  [('Mas rapido se aleja', True), ('Mas lento se aleja', False), ('Mas cerca esta', False), ('No se mueve', False)]),
                 ('Escribe el apellido del astronomo que descubrio la expansion.', 'text',
                  [('Hubble', True)]),
             ]},
            {'title': 'Materia y energia oscura', 'icon': 'atom', 'order': 3,
             'cards': [
                 ('Lo que no vemos', 'La mayor parte del universo',
                  'Casi todo el universo es materia y energia oscura: no las vemos, pero notamos sus '
                  'efectos en como se mueven las galaxias.', 'Lo que vemos (estrellas, planetas) es menos del 5% del universo.'),
                 ('Materia oscura', 'Pegamento invisible',
                  'Es una materia invisible cuya gravedad mantiene unidas a las galaxias. Sin ella, se '
                  'desharian al girar.', ''),
                 ('Energia oscura', 'Acelera la expansion',
                  'Es una energia misteriosa que empuja al universo a expandirse cada vez mas rapido.', ''),
             ],
             'questions': [
                 ('Cuanto del universo es materia y energia oscura?', 'single',
                  [('La mayor parte (mas del 90%)', True), ('La mitad', False), ('Un 10%', False), ('Casi nada', False)]),
                 ('Que hace la materia oscura?', 'single',
                  [('Su gravedad mantiene unidas las galaxias', True), ('Da luz', False),
                   ('Enfria el universo', False), ('Crea planetas', False)]),
                 ('Que hace la energia oscura?', 'single',
                  [('Acelera la expansion del universo', True), ('Frena el universo', False),
                   ('Apaga las estrellas', False), ('Nada', False)]),
                 ('Todo lo que vemos (estrellas, planetas) es la mayor parte del universo.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('La materia invisible que une a las galaxias se llama materia...', 'single',
                  [('Oscura', True), ('Brillante', False), ('Solida', False), ('Gaseosa', False)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Astrofisica', 'order': 7, 'icon': 'atom', 'accent': '#d16bff',
                 'subtitle': 'La fisica del cosmos.',
                 'description': 'Las ideas que explican como funciona el universo: la gravedad, la luz '
                                'y las nociones de la relatividad de Einstein.'},
        'lessons': [
            {'title': 'La gravedad', 'icon': 'orbit', 'order': 1,
             'cards': [
                 ('La fuerza que atrae', 'Une el universo',
                  'La gravedad es la fuerza con la que toda materia atrae a otra materia. Mantiene los '
                  'planetas en orbita y a ti pegado al suelo.', ''),
                 ('Newton y la manzana', 'La ley de la gravedad',
                  'Isaac Newton describio como la gravedad depende de la masa y la distancia: mas masa y '
                  'menos distancia, mas fuerza de atraccion.', ''),
                 ('Einstein la reinvento', 'Espacio-tiempo curvo',
                  'Einstein mostro que la gravedad no es solo una fuerza: la masa curva el espacio-tiempo, '
                  'y los objetos siguen esa curva.', ''),
             ],
             'questions': [
                 ('Que hace la gravedad?', 'single',
                  [('Atrae la materia hacia otra materia', True), ('La repele', False), ('La calienta', False), ('La ilumina', False)]),
                 ('La gravedad mantiene a los planetas...', 'single',
                  [('En orbita alrededor del Sol', True), ('Quietos en el espacio', False),
                   ('Chocando entre si', False), ('Fuera del sistema', False)]),
                 ('Quien describio la ley clasica de la gravedad?', 'single',
                  [('Isaac Newton', True), ('Galileo', False), ('Colon', False), ('Hubble', False)]),
                 ('Segun Einstein, la gravedad es...', 'single',
                  [('La curvatura del espacio-tiempo por la masa', True), ('Un tipo de luz', False),
                   ('Un sonido', False), ('Un gas', False)]),
                 ('Escribe el apellido del cientifico de la manzana y la gravedad.', 'text',
                  [('Newton', True)]),
             ]},
            {'title': 'La luz y el espectro', 'icon': 'star', 'order': 2,
             'cards': [
                 ('La luz nos trae informacion', 'Mensajeros del cosmos',
                  'Casi todo lo que sabemos del universo nos llega en forma de luz. Analizarla nos dice '
                  'muchisimo de objetos lejanisimos.', ''),
                 ('El espectro', 'La luz descompuesta',
                  'Al descomponer la luz de una estrella (como un arcoiris) aparecen lineas que revelan de '
                  'que elementos esta hecha.', 'Asi supimos de que estan hechas las estrellas sin ir a ellas.'),
                 ('Luz que no vemos', 'Mas alla del arcoiris',
                  'Existe luz invisible: infrarrojo, ultravioleta, rayos X... Los telescopios la "ven" '
                  'para descubrir cosas ocultas.', ''),
             ],
             'questions': [
                 ('Que nos permite saber la luz de las estrellas?', 'single',
                  [('De que estan hechas', True), ('Su nombre', False), ('Su edad en dias', False), ('Nada', False)]),
                 ('Que es el espectro de la luz?', 'single',
                  [('La luz descompuesta en sus colores', True), ('Un tipo de estrella', False),
                   ('Un planeta', False), ('Un sonido', False)]),
                 ('Existe luz que el ojo humano no puede ver, como los rayos X o el infrarrojo.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('Como supimos de que estan hechas las estrellas sin viajar a ellas?', 'single',
                  [('Analizando su luz y su espectro', True), ('Preguntando', False), ('Adivinando', False), ('Con un microscopio', False)]),
                 ('Como se llama la luz descompuesta en colores? (una palabra)', 'text',
                  [('espectro', True), ('el espectro', True)]),
             ]},
            {'title': 'Nociones de relatividad', 'icon': 'atom', 'order': 3,
             'cards': [
                 ('El espacio-tiempo', 'Todo conectado',
                  'Einstein unio el espacio y el tiempo en un solo concepto: el espacio-tiempo. La masa lo '
                  'deforma como una bola pesada sobre una cama elastica.', ''),
                 ('El tiempo no es fijo', 'Es relativo',
                  'El tiempo pasa un poco mas lento donde la gravedad es mas fuerte o cuando te mueves muy '
                  'rapido. Los GPS lo tienen en cuenta.', 'Sin corregir la relatividad, el GPS fallaria por kilometros.'),
                 ('Nada mas rapido que la luz', 'El limite del universo',
                  'La velocidad de la luz es el limite de velocidad del universo: nada con masa puede '
                  'alcanzarla.', ''),
             ],
             'questions': [
                 ('Que unio Einstein en un solo concepto?', 'single',
                  [('El espacio y el tiempo', True), ('El agua y el aire', False),
                   ('La luz y el sonido', False), ('La Tierra y la Luna', False)]),
                 ('Donde pasa el tiempo un poco mas lento?', 'single',
                  [('Donde la gravedad es mas fuerte', True), ('Donde hace frio', False),
                   ('Solo de noche', False), ('En las montanas', False)]),
                 ('Algo con masa puede viajar mas rapido que la luz.', 'truefalse',
                  [('Falso', True), ('Verdadero', False)]),
                 ('Por que el GPS necesita la relatividad?', 'single',
                  [('Porque el tiempo pasa distinto en los satelites', True), ('Por las nubes', False),
                   ('Por el viento', False), ('Por la Luna', False)]),
                 ('Cual es el limite de velocidad del universo?', 'single',
                  [('La velocidad de la luz', True), ('La velocidad del sonido', False),
                   ('La de un cohete', False), ('No hay limite', False)]),
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
            for ci, (title, subtitle, summary, fun) in enumerate(ldata['cards'], start=1):
                Card.objects.get_or_create(
                    lesson=lesson, slug=slugify(title),
                    defaults={'category': unit, 'title': title, 'subtitle': subtitle,
                              'summary': summary, 'fun_fact': fun, 'icon': lesson.icon, 'order': ci},
                )
            for qi, (text, qtype, options) in enumerate(ldata['questions'], start=1):
                if Question.objects.filter(lesson=lesson, text=text).exists():
                    continue
                q = Question.objects.create(lesson=lesson, text=text, qtype=qtype, order=qi)
                for oi, (otext, correct) in enumerate(options, start=1):
                    Option.objects.create(question=q, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Category.objects.filter(slug__in=[slugify(b['unit']['name']) for b in DATA]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0026_enrich_quizzes'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
