# -*- coding: utf-8 -*-
from django.db import migrations
from django.utils.text import slugify


DATA = [
    {
        'unit': {'name': 'Exoplanetas', 'order': 8, 'icon': 'planet', 'accent': '#3ddc84',
                 'subtitle': 'Planetas de otras estrellas.',
                 'description': 'Mas alla del Sistema Solar hay miles de planetas orbitando otras '
                                'estrellas. Veras que son, como se descubren y algunos mundos famosos.'},
        'lessons': [
            {'title': 'Que es un exoplaneta', 'icon': 'planet', 'order': 1,
             'cards': [
                 ('Planetas de otras estrellas', 'Mundos lejanos',
                  'Un exoplaneta es un planeta que orbita otra estrella, no el Sol. Ya se han confirmado '
                  'miles de ellos.', 'El primero alrededor de una estrella como el Sol se descubrio en 1995.'),
                 ('Los hay de todo tipo', 'Variedad enorme',
                  'Gigantes gaseosos pegados a su estrella ("jupiteres calientes"), super-Tierras rocosas, '
                  'mundos de lava o de hielo... el catalogo es asombroso.', ''),
                 ('La zona habitable', 'Ni muy caliente ni muy frio',
                  'Es la distancia a una estrella donde podria haber agua liquida en la superficie: la '
                  'mejor apuesta para buscar vida.', ''),
             ],
             'questions': [
                 ('Que es un exoplaneta?', 'single',
                  [('Un planeta que orbita otra estrella, no el Sol', True), ('Una estrella', False),
                   ('Una galaxia', False), ('Una luna del Sol', False)]),
                 ('Que es la zona habitable?', 'single',
                  [('La distancia donde podria haber agua liquida', True), ('El centro de la estrella', False),
                   ('El borde de la galaxia', False), ('Una nave', False)]),
                 ('Ya se han descubierto miles de exoplanetas.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('En que ano se hallo el primer exoplaneta en una estrella como el Sol?', 'single',
                  [('1995', True), ('1700', False), ('2020', False), ('1900', False)]),
                 ('Escribe como se llaman los planetas fuera del Sistema Solar (una palabra).', 'text',
                  [('exoplanetas', True), ('exoplaneta', True)]),
             ]},
            {'title': 'Como se descubren', 'icon': 'star', 'order': 2,
             'cards': [
                 ('El transito', 'Un mini-eclipse',
                  'Cuando un planeta pasa por delante de su estrella, la atenua un poquito. Midiendo ese '
                  'parpadeo se detectan planetas.', ''),
                 ('El bamboleo', 'La estrella se mueve',
                  'La gravedad de un planeta hace que su estrella se bambolee un poco. Ese movimiento '
                  'delata al planeta aunque no lo veamos.', ''),
                 ('Telescopios cazadores', 'Kepler y TESS',
                  'Telescopios espaciales como Kepler y TESS vigilan miles de estrellas buscando esos '
                  'parpadeos.', 'El telescopio Kepler descubrio miles de planetas el solo.'),
             ],
             'questions': [
                 ('En que consiste el metodo del transito?', 'single',
                  [('Detectar el parpadeo cuando el planeta pasa frente a su estrella', True),
                   ('Escuchar el planeta', False), ('Fotografiarlo de cerca', False), ('Tocarlo', False)]),
                 ('Que telescopios se dedican a cazar exoplanetas?', 'single',
                  [('Kepler y TESS', True), ('Voyager', False), ('Apolo', False), ('El Titanic', False)]),
                 ('La gravedad de un planeta puede hacer que su estrella se bambolee.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('Como delata un planeta a su estrella en el metodo del bamboleo?', 'single',
                  [('Haciendo que la estrella se mueva un poco', True), ('Apagandola', False),
                   ('Cambiandole el color para siempre', False), ('Explotando', False)]),
                 ('Escribe el telescopio cazador de planetas que empieza por K.', 'text',
                  [('Kepler', True)]),
             ]},
            {'title': 'Mundos famosos', 'icon': 'planet', 'order': 3,
             'cards': [
                 ('TRAPPIST-1', 'Siete Tierras',
                  'Un pequeno sistema con siete planetas del tamano de la Tierra, varios en la zona '
                  'habitable, a unos 40 anos luz.', ''),
                 ('Super-Tierras', 'Mas grandes que la nuestra',
                  'Planetas rocosos mas grandes que la Tierra, muy comunes en la galaxia; algunos podrian '
                  'ser habitables.', ''),
                 ('En busca de vida', 'La gran pregunta',
                  'Analizando la atmosfera de los exoplanetas buscamos gases que podrian indicar vida. El '
                  'telescopio James Webb ya lo hace.', ''),
             ],
             'questions': [
                 ('Que tiene de especial el sistema TRAPPIST-1?', 'single',
                  [('Siete planetas del tamano de la Tierra', True), ('Un solo planeta gigante', False),
                   ('No tiene planetas', False), ('Es una galaxia', False)]),
                 ('Que es una super-Tierra?', 'single',
                  [('Un planeta rocoso mas grande que la Tierra', True), ('Una estrella', False),
                   ('Una galaxia', False), ('Una nave', False)]),
                 ('Analizando su atmosfera se pueden buscar senales de vida en un exoplaneta.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('Que telescopio analiza atmosferas de exoplanetas?', 'single',
                  [('El James Webb', True), ('El Titanic', False), ('El Voyager', False), ('El Apolo', False)]),
                 ('Cuantos planetas tiene el sistema TRAPPIST-1? (numero)', 'text',
                  [('7', True), ('siete', True)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Galaxias del universo', 'order': 9, 'icon': 'galaxy', 'accent': '#b18bff',
                 'subtitle': 'Vecinas, cumulos y cuasares.',
                 'description': 'La Via Lactea no esta sola. Conoceras a Andromeda, los cumulos de '
                                'galaxias y los brillantes cuasares.'},
        'lessons': [
            {'title': 'Andromeda y el Grupo Local', 'icon': 'galaxy', 'order': 1,
             'cards': [
                 ('Andromeda', 'La galaxia vecina',
                  'Es la gran galaxia espiral mas cercana a la Via Lactea, a unos 2,5 millones de anos '
                  'luz. Se ve a simple vista como una manchita.', 'Su luz que ves hoy salio hace 2,5 millones de anos.'),
                 ('El Grupo Local', 'Nuestro vecindario',
                  'La Via Lactea, Andromeda y decenas de galaxias mas pequenas forman un grupo unido por '
                  'la gravedad: el Grupo Local.', ''),
                 ('El gran choque', 'En 4.500 millones de anos',
                  'Andromeda se acerca a nosotros y chocara con la Via Lactea, formando una galaxia '
                  'gigante. Las estrellas casi no chocaran entre si.', ''),
             ],
             'questions': [
                 ('Que es Andromeda?', 'single',
                  [('La gran galaxia espiral mas cercana', True), ('Una estrella', False),
                   ('Un planeta', False), ('Un cometa', False)]),
                 ('A que distancia esta Andromeda, aproximadamente?', 'single',
                  [('Unos 2,5 millones de anos luz', True), ('100 km', False),
                   ('1 ano luz', False), ('En el Sistema Solar', False)]),
                 ('Andromeda chocara con la Via Lactea en el futuro lejano.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('Que es el Grupo Local?', 'single',
                  [('El grupo de galaxias al que pertenece la Via Lactea', True), ('Un club', False),
                   ('Una estrella', False), ('Un planeta', False)]),
                 ('Escribe la galaxia grande mas cercana a la nuestra.', 'text',
                  [('Andromeda', True)]),
             ]},
            {'title': 'Galaxias asombrosas', 'icon': 'galaxy', 'order': 2,
             'cards': [
                 ('Cumulos de galaxias', 'Ciudades de galaxias',
                  'Las galaxias se agrupan en cumulos de cientos o miles, unidos por la gravedad. Son de '
                  'las estructuras mas grandes que existen.', ''),
                 ('La red cosmica', 'El universo es una telarana',
                  'A gran escala, las galaxias forman filamentos y enormes vacios, como una gigantesca '
                  'telarana cosmica.', ''),
                 ('Galaxias activas', 'Nucleos brillantisimos',
                  'Algunas galaxias tienen un nucleo que brilla mas que todas sus estrellas juntas: un '
                  'agujero negro devorando materia (un cuasar).', 'Los cuasares estan entre los objetos mas brillantes del universo.'),
             ],
             'questions': [
                 ('Que es un cumulo de galaxias?', 'single',
                  [('Un grupo de cientos o miles de galaxias unidas por gravedad', True),
                   ('Una estrella', False), ('Un planeta', False), ('Una nave', False)]),
                 ('Como se distribuyen las galaxias a gran escala?', 'single',
                  [('En filamentos y vacios, como una red cosmica', True), ('En linea recta', False),
                   ('Al azar sin ningun patron', False), ('En un cuadrado', False)]),
                 ('Que es un cuasar?', 'single',
                  [('Un nucleo galactico brillantisimo con un agujero negro devorando materia', True),
                   ('Una estrella pequena', False), ('Un planeta', False), ('Una luna', False)]),
                 ('Los cuasares estan entre los objetos mas brillantes del universo.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('La estructura a gran escala del universo se parece a una...', 'single',
                  [('Telarana (red cosmica)', True), ('Linea recta', False),
                   ('Bola solida', False), ('Caja vacia', False)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Agujeros negros: tipos y famosos', 'order': 10, 'icon': 'blackhole', 'accent': '#7c5cff',
                 'subtitle': 'Estelares, supermasivos y famosos.',
                 'description': 'No todos los agujeros negros son iguales. Veras sus tipos, los mas '
                                'famosos y las ondas gravitacionales.'},
        'lessons': [
            {'title': 'Tipos de agujeros negros', 'icon': 'blackhole', 'order': 1,
             'cards': [
                 ('Estelares', 'De una estrella',
                  'Los mas comunes: nacen del colapso de una estrella masiva. Tienen unas pocas veces la '
                  'masa del Sol.', ''),
                 ('Supermasivos', 'Gigantes en el centro',
                  'En el centro de casi todas las galaxias hay uno con millones o miles de millones de '
                  'veces la masa del Sol.', ''),
                 ('Intermedios', 'El eslabon perdido',
                  'De tamano medio, mas raros y dificiles de encontrar. Los astronomos aun estudian como '
                  'se forman.', ''),
             ],
             'questions': [
                 ('Cuales son los tipos de agujero negro por su masa?', 'single',
                  [('Estelares, intermedios y supermasivos', True), ('Solo uno', False),
                   ('Diez tipos', False), ('Ninguno', False)]),
                 ('Donde suele haber un agujero negro supermasivo?', 'single',
                  [('En el centro de casi todas las galaxias', True), ('En cada planeta', False),
                   ('En la Luna', False), ('En el Sol', False)]),
                 ('De que nace un agujero negro estelar?', 'single',
                  [('Del colapso de una estrella masiva', True), ('De un planeta', False),
                   ('De un cometa', False), ('De una galaxia', False)]),
                 ('Un agujero negro supermasivo puede tener miles de millones de veces la masa del Sol.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('El agujero negro del centro de una galaxia es de tipo...', 'single',
                  [('Supermasivo', True), ('Estelar', False), ('Pequeno', False), ('Frio', False)]),
             ]},
            {'title': 'Famosos y ondas gravitacionales', 'icon': 'blackhole', 'order': 2,
             'cards': [
                 ('Sagitario A*', 'El de nuestra casa',
                  'Es el agujero negro supermasivo en el centro de la Via Lactea. Se logro fotografiar en '
                  '2022.', ''),
                 ('M87*', 'La primera foto',
                  'El agujero negro de la galaxia M87 fue el primero en ser fotografiado, en 2019: un '
                  'anillo de luz rodeando la oscuridad.', ''),
                 ('Ondas gravitacionales', 'Temblores del espacio-tiempo',
                  'Cuando dos agujeros negros chocan, crean ondas en el espacio-tiempo. Se detectaron por '
                  'primera vez en 2015.', 'Ese descubrimiento gano el Nobel de Fisica en 2017.'),
             ],
             'questions': [
                 ('Que es Sagitario A*?', 'single',
                  [('El agujero negro supermasivo del centro de la Via Lactea', True),
                   ('Una estrella', False), ('Un planeta', False), ('Un cometa', False)]),
                 ('Que se fotografio por primera vez en 2019?', 'single',
                  [('El agujero negro de la galaxia M87', True), ('Un planeta nuevo', False),
                   ('El Sol', False), ('La Luna', False)]),
                 ('Que son las ondas gravitacionales?', 'single',
                  [('Ondas en el espacio-tiempo, p.ej. al chocar agujeros negros', True),
                   ('Ondas de radio', False), ('Olas del mar', False), ('Un sonido', False)]),
                 ('Las ondas gravitacionales se detectaron por primera vez en 2015.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('En que ano se fotografio Sagitario A*? (numero)', 'text',
                  [('2022', True)]),
             ]},
        ],
    },
    {
        'unit': {'name': 'Descubrimientos y exploracion', 'order': 11, 'icon': 'rocket', 'accent': '#4f7cff',
                 'subtitle': 'Telescopios, sondas y hallazgos.',
                 'description': 'Como exploramos el cosmos y algunos de los mayores descubrimientos '
                                'recientes: telescopios, misiones y sorpresas.'},
        'lessons': [
            {'title': 'Telescopios que cambiaron todo', 'icon': 'star', 'order': 1,
             'cards': [
                 ('El Hubble', 'El ojo en el cielo',
                  'El telescopio espacial Hubble, en orbita desde 1990, nos dio imagenes increibles de '
                  'galaxias, nebulosas y el universo profundo.', ''),
                 ('El James Webb', 'Ver el pasado',
                  'Lanzado en 2021, ve en infrarrojo y capta la luz de las primeras galaxias, formadas '
                  'hace mas de 13.000 millones de anos.', 'Mira tan lejos que casi ve el principio del universo.'),
                 ('Por que en el espacio', 'Sin atmosfera estorbando',
                  'Desde el espacio, los telescopios ven sin la distorsion de la atmosfera terrestre: '
                  'imagenes mucho mas nitidas.', ''),
             ],
             'questions': [
                 ('Desde cuando esta en orbita el telescopio Hubble?', 'single',
                  [('Desde 1990', True), ('Desde 1700', False), ('Desde 2020', False), ('Nunca ha estado', False)]),
                 ('Que capta el telescopio James Webb?', 'single',
                  [('Luz infrarroja de las primeras galaxias', True), ('Solo la Luna', False),
                   ('El fondo del mar', False), ('Nada', False)]),
                 ('Los telescopios espaciales ven mejor porque no tienen la atmosfera estorbando.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('En que ano se lanzo el telescopio James Webb?', 'single',
                  [('2021', True), ('1990', False), ('1500', False), ('2000', False)]),
                 ('Escribe el famoso telescopio espacial que empieza por H.', 'text',
                  [('Hubble', True)]),
             ]},
            {'title': 'Misiones que exploran', 'icon': 'rocket', 'order': 2,
             'cards': [
                 ('Las Voyager', 'Los viajeros',
                  'Lanzadas en 1977, las sondas Voyager exploraron los planetas gigantes y hoy viajan por '
                  'el espacio interestelar, mas alla del Sistema Solar.', 'Voyager 1 es el objeto humano mas lejano.'),
                 ('Robots en Marte', 'Rovers exploradores',
                  'Vehiculos como Perseverance recorren Marte buscando senales de vida antigua y '
                  'estudiando su suelo.', ''),
                 ('Volver a la Luna', 'El programa Artemis',
                  'La humanidad planea volver a la Luna y, algun dia, llegar a Marte con personas.', ''),
             ],
             'questions': [
                 ('Que hacen hoy las sondas Voyager?', 'single',
                  [('Viajan por el espacio interestelar, mas alla del Sistema Solar', True),
                   ('Estan en la Luna', False), ('Se quedaron en la Tierra', False), ('Orbitan el Sol de cerca', False)]),
                 ('Que hace el rover Perseverance?', 'single',
                  [('Explora Marte buscando senales de vida', True), ('Explora el Sol', False),
                   ('Orbita la Tierra', False), ('Esta en Venus', False)]),
                 ('Voyager 1 es el objeto hecho por humanos mas lejano.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('En que ano se lanzaron las sondas Voyager?', 'single',
                  [('1977', True), ('2020', False), ('1500', False), ('1990', False)]),
                 ('En que planeta trabaja el rover Perseverance?', 'text',
                  [('Marte', True)]),
             ]},
            {'title': 'Grandes descubrimientos', 'icon': 'star', 'order': 3,
             'cards': [
                 ('Agua por todas partes', 'No solo en la Tierra',
                  'Se ha encontrado agua (helada) en la Luna, en Marte y en lunas de Jupiter y Saturno. El '
                  'agua es mas comun de lo que se creia.', ''),
                 ('Ondas gravitacionales', 'Una nueva forma de mirar',
                  'Detectarlas en 2015 abrio una manera nueva de estudiar el universo: "escuchando" los '
                  'choques de agujeros negros.', ''),
                 ('Cada vez sabemos mas', 'La ciencia avanza',
                  'Con nuevos telescopios y sondas, descubrimos planetas, galaxias y fenomenos nuevos casi '
                  'cada ano.', ''),
             ],
             'questions': [
                 ('Donde se ha encontrado agua, ademas de la Tierra?', 'single',
                  [('En la Luna, Marte y lunas de Jupiter y Saturno', True), ('En el Sol', False),
                   ('En ningun sitio mas', False), ('Solo en la Tierra', False)]),
                 ('Que abrio la deteccion de ondas gravitacionales en 2015?', 'single',
                  [('Una forma nueva de estudiar el universo', True), ('Un agujero en la Tierra', False),
                   ('Un planeta', False), ('Una galaxia', False)]),
                 ('El agua en el espacio es mas comun de lo que se creia antes.', 'truefalse',
                  [('Verdadero', True), ('Falso', False)]),
                 ('Como avanza nuestro conocimiento del universo?', 'single',
                  [('Con nuevos telescopios y sondas', True), ('Adivinando', False),
                   ('No avanza', False), ('Con magia', False)]),
                 ('En que ano se detectaron por primera vez las ondas gravitacionales? (numero)', 'text',
                  [('2015', True)]),
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
        ('astro', '0027_seed_contenido_avanzado'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
