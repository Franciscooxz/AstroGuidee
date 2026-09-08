# -*- coding: utf-8 -*-
"""Nivel 1 'El cielo a simple vista' (Fase R3): unidad nueva."""
from django.db import migrations
from django.utils.text import slugify

UNIT = {'slug': 'el-cielo-a-simple-vista', 'name': 'El cielo a simple vista',
        'subtitle': 'Orientate bajo las estrellas', 'icon': 'star',
        'accent': '#6ea8ff', 'order': 2, 'difficulty': 1}

# c=(titulo,subtitulo,resumen,dato) ; q=(texto,tipo,explicacion,[(opcion,correcta)])
LESSONS = [
    {'slug': 'la-esfera-celeste', 'title': 'La esfera celeste', 'icon': 'orbit',
     'subtitle': 'La boveda del cielo', 'order': 1,
     'cards': [
        ('La boveda del cielo', 'Una esfera imaginaria',
         'Aunque las estrellas estan a distancias muy distintas, a simple vista parecen pegadas a una gran esfera que nos rodea: la esfera celeste. Es un modelo comodo para ubicar los astros.',
         'Los antiguos creian que era una boveda solida de verdad.'),
        ('Cardinales y horizonte', 'Orientarte en el cielo',
         'El horizonte es la linea donde el cielo parece tocar la tierra. Los puntos cardinales (Norte, Sur, Este, Oeste) te orientan: el Sol y casi todos los astros salen por el Este y se ponen por el Oeste.', ''),
        ('El cenit', 'Justo sobre tu cabeza',
         'El cenit es el punto del cielo que queda exactamente encima de ti. Su opuesto, bajo tus pies, es el nadir.', ''),
     ],
     'questions': [
        ('Que es la esfera celeste?', 'single',
         'Es un modelo: las estrellas estan a distancias muy distintas, pero a simple vista parecen pegadas a una esfera que nos rodea.',
         [('Una esfera imaginaria donde parecen estar los astros', True), ('Un planeta gigante', False),
          ('La atmosfera de la Tierra', False), ('Una nave espacial', False)]),
        ('Por donde salen el Sol y la mayoria de los astros?', 'single',
         'Por el Este, y se ponen por el Oeste, debido a la rotacion de la Tierra.',
         [('Por el Este', True), ('Por el Oeste', False), ('Por el Norte', False), ('Por el cenit', False)]),
        ('Como se llama el punto del cielo justo sobre tu cabeza?', 'single',
         'El cenit esta justo encima de ti; su opuesto, bajo tus pies, es el nadir.',
         [('El cenit', True), ('El horizonte', False), ('El nadir', False), ('El polo', False)]),
        ('El horizonte es la linea donde el cielo parece tocar la tierra.', 'truefalse',
         'Es tu limite de vision: por debajo del horizonte no ves el cielo.',
         [('Verdadero', True), ('Falso', False)]),
        ('Escribe el punto cardinal por donde sale el Sol.', 'text',
         'El Sol sale aproximadamente por el Este (oriente).',
         [('este', True), ('el este', True), ('oriente', True)]),
     ]},
    {'slug': 'las-constelaciones', 'title': 'Las constelaciones', 'icon': 'star',
     'subtitle': 'Dibujos en el cielo', 'order': 2,
     'cards': [
        ('Dibujos en el cielo', 'Uniendo estrellas',
         'Una constelacion es un grupo de estrellas que, vistas desde la Tierra, forman una figura. En realidad esas estrellas no estan juntas: solo lo parecen desde nuestro punto de vista.',
         'Hay 88 constelaciones oficiales reconocidas hoy.'),
        ('Mapas para orientarte', 'Guias del cielo',
         'Las constelaciones sirven de mapa: si reconoces algunas, puedes encontrar planetas, estrellas brillantes y otros objetos. La Osa Mayor o el Cinturon de Orion son puntos de partida faciles.', ''),
        ('Cada cultura, sus figuras', 'No son universales',
         'Las figuras son un invento humano: distintas culturas vieron dibujos diferentes en las mismas estrellas. Las que usamos hoy vienen sobre todo de la tradicion griega.', ''),
     ],
     'questions': [
        ('Que es una constelacion?', 'single',
         'Las estrellas de una constelacion no estan juntas en el espacio; solo lo parecen desde nuestro punto de vista.',
         [('Un grupo de estrellas que forman una figura vista desde la Tierra', True),
          ('Un planeta con anillos', False), ('Una galaxia', False), ('Una nave', False)]),
        ('Las estrellas de una constelacion estan realmente juntas en el espacio.', 'truefalse',
         'Pueden estar a distancias muy distintas; la figura es un efecto de perspectiva.',
         [('Falso', True), ('Verdadero', False)]),
        ('Cuantas constelaciones oficiales se reconocen hoy?', 'single',
         'Son 88 constelaciones oficiales que, juntas, cubren todo el cielo.',
         [('88', True), ('12', False), ('500', False), ('Solo 1', False)]),
        ('Para que sirven las constelaciones al observar?', 'single',
         'Reconociendolas puedes localizar planetas, estrellas brillantes y otros objetos.',
         [('Como mapa para orientarte y encontrar otros astros', True), ('Para predecir el futuro', False),
          ('Para medir la temperatura', False), ('Para nada', False)]),
        ('Escribe la constelacion famosa por su cinturon de 3 estrellas.', 'text',
         'Orion, con su Cinturon de tres estrellas alineadas, es de las mas faciles de reconocer.',
         [('orion', True), ('orion la del cinturon', True)]),
     ]},
    {'slug': 'coordenadas-celestes', 'title': 'Coordenadas celestes', 'icon': 'progress',
     'subtitle': 'Direcciones en el cielo', 'order': 3,
     'cards': [
        ('Como el mapa de la Tierra', 'Ubicar un astro',
         'Igual que en la Tierra usamos latitud y longitud, en el cielo usamos coordenadas para decir donde esta un astro. Las mas usadas son la ascension recta y la declinacion.', ''),
        ('Ascension recta y declinacion', 'Las coordenadas del cielo',
         'La declinacion es como la latitud (cuan al norte o al sur esta un astro). La ascension recta es como la longitud (su posicion de este a oeste). Juntas fijan un punto en la esfera celeste.', ''),
        ('La ecliptica', 'El camino del Sol',
         'La ecliptica es la linea por la que el Sol parece recorrer el cielo a lo largo del ano. Los planetas y la Luna se mueven siempre cerca de ella.',
         'Las constelaciones del zodiaco son justo las que cruza la ecliptica.'),
     ],
     'questions': [
        ('Para que sirven las coordenadas celestes?', 'single',
         'Como la latitud y la longitud en la Tierra, fijan donde esta un astro en la esfera celeste.',
         [('Para indicar la posicion de un astro en el cielo', True), ('Para medir su temperatura', False),
          ('Para pesar una estrella', False), ('Para nada', False)]),
        ('La declinacion en el cielo se parece a la... de la Tierra.', 'single',
         'La declinacion mide cuan al norte o al sur esta un astro, igual que la latitud.',
         [('Latitud', True), ('Longitud', False), ('Altitud', False), ('Temperatura', False)]),
        ('Que es la ecliptica?', 'single',
         'Es el camino aparente del Sol por el cielo durante el ano; los planetas y la Luna van cerca de ella.',
         [('La linea por la que el Sol parece recorrer el cielo en un ano', True),
          ('El ecuador de la Tierra', False), ('Una constelacion', False), ('Un tipo de eclipse', False)]),
        ('Los planetas y la Luna se mueven cerca de la ecliptica.', 'truefalse',
         'Por eso las constelaciones del zodiaco, que cruza la ecliptica, son por donde vemos pasar a los planetas.',
         [('Verdadero', True), ('Falso', False)]),
        ('La ascension recta se parece a la longitud terrestre.', 'truefalse',
         'Indica la posicion este-oeste, como la longitud; la declinacion marca la norte-sur.',
         [('Verdadero', True), ('Falso', False)]),
     ]},
    {'slug': 'el-movimiento-del-cielo', 'title': 'El movimiento del cielo', 'icon': 'orbit',
     'subtitle': 'Por que el cielo gira', 'order': 4,
     'cards': [
        ('El cielo gira', 'Movimiento aparente',
         'Durante la noche, las estrellas parecen girar lentamente. No se mueven ellas: es la Tierra la que rota. Por eso los astros salen y se ponen.',
         'En una foto de larga exposicion, las estrellas dejan circulos alrededor del polo.'),
        ('La estrella Polar', 'El punto que no se mueve',
         'En el hemisferio norte, la estrella Polar queda casi fija sobre el Norte mientras las demas giran a su alrededor. Por eso guiaba a los navegantes.', ''),
        ('La precesion', 'Un bamboleo lento',
         'El eje de la Tierra hace un lento bamboleo, como una peonza, que tarda unos 26.000 anos en completarse: la precesion. Por eso la estrella polar no siempre ha sido la misma.', ''),
     ],
     'questions': [
        ('Por que las estrellas parecen girar durante la noche?', 'single',
         'Es un movimiento aparente: la Tierra gira sobre su eje y por eso los astros salen y se ponen.',
         [('Porque la Tierra rota', True), ('Porque las estrellas se mueven rapido', False),
          ('Por el viento', False), ('Por la Luna', False)]),
        ('Que estrella queda casi fija sobre el Norte?', 'single',
         'La Polar apenas se mueve porque queda casi alineada con el eje de la Tierra; guiaba a los navegantes.',
         [('La estrella Polar', True), ('El Sol', False), ('Sirio', False), ('La Luna', False)]),
        ('Que es la precesion?', 'single',
         'El eje de la Tierra se bambolea como una peonza cada ~26.000 anos; por eso la estrella polar cambia con los milenios.',
         [('Un lento bamboleo del eje de la Tierra', True), ('La rotacion diaria', False),
          ('Un tipo de eclipse', False), ('El viento solar', False)]),
        ('Las estrellas se mueven realmente muy rapido cada noche.', 'truefalse',
         'El movimiento nocturno es aparente: lo causa la rotacion de la Tierra, no las estrellas.',
         [('Falso', True), ('Verdadero', False)]),
        ('Cuantos anos tarda aproximadamente un ciclo de precesion? (numero)', 'text',
         'Unos 26.000 anos; por eso hace miles de anos la estrella polar era otra distinta.',
         [('26000', True), ('26.000', True), ('26 mil', True)]),
     ]},
    {'slug': 'brillo-y-color-de-las-estrellas', 'title': 'Brillo y color de las estrellas', 'icon': 'star',
     'subtitle': 'Magnitud y temperatura', 'order': 5,
     'cards': [
        ('No todas brillan igual', 'La magnitud',
         'El brillo de una estrella se mide con la magnitud. Cuanto menor es el numero, mas brilla: las mas brillantes tienen magnitud negativa, y a simple vista llegamos hasta magnitud 6 en cielos oscuros.',
         'Es una escala al reves: 1 brilla mas que 6.'),
        ('Brillo aparente vs real', 'Cerca o potente',
         'Una estrella puede verse brillante por estar cerca o por ser muy potente. La magnitud aparente es como la vemos; la absoluta seria su brillo real a una misma distancia.', ''),
        ('El color cuenta la temperatura', 'Azul caliente, rojo frio',
         'El color de una estrella depende de su temperatura: las azules son las mas calientes y las rojas las mas frias. El Sol, amarillo, esta en un punto intermedio.', ''),
     ],
     'questions': [
        ('Que mide la magnitud de una estrella?', 'single',
         'La magnitud indica cuanto brilla. Ojo: cuanto menor el numero, mas brilla.',
         [('Su brillo', True), ('Su temperatura exacta', False), ('Su distancia', False), ('Su edad', False)]),
        ('En la escala de magnitud, cual brilla mas?', 'single',
         'Es una escala al reves: 1 brilla mas que 6. Las mas brillantes tienen incluso magnitud negativa.',
         [('Una de magnitud 1', True), ('Una de magnitud 6', False), ('Da igual', False), ('Ninguna brilla', False)]),
        ('De que depende el color de una estrella?', 'single',
         'Azul = caliente, rojo = frio. El Sol, amarillo, esta en un punto intermedio.',
         [('De su temperatura', True), ('De su edad', False), ('De su nombre', False), ('De su distancia', False)]),
        ('Una estrella puede verse brillante solo por estar cerca, sin ser muy potente.', 'truefalse',
         'El brillo aparente mezcla potencia y distancia; la magnitud absoluta separaria su brillo real.',
         [('Verdadero', True), ('Falso', False)]),
        ('Que color tiene una estrella mas caliente?', 'single',
         'Cuanto mas caliente, mas azul; cuanto mas fria, mas roja.',
         [('Azul', True), ('Rojo', False), ('Amarillo', False), ('Verde', False)]),
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
        ('astro', '0049_seed_nivel0'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
