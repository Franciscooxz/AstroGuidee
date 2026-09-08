# -*- coding: utf-8 -*-
"""Relleno de huecos del roadmap (Fase R5): lecciones nuevas en unidades existentes."""
from django.db import migrations
from django.db.models import Max
from django.utils.text import slugify

# cada leccion se anade al final de su unidad destino
ADD = [
    {'unit': 'sistema-solar', 'slug': 'cuerpos-menores', 'title': 'Cuerpos menores', 'icon': 'planet',
     'subtitle': 'Asteroides, cometas y enanos',
     'cards': [
        ('No solo planetas', 'Los pequenos habitantes',
         'Ademas de los 8 planetas, el Sistema Solar esta lleno de cuerpos menores: planetas enanos, asteroides y cometas. Son restos de la formacion del Sistema Solar.',
         'Pluton fue reclasificado como planeta enano en 2006.'),
        ('Asteroides y cometas', 'Roca y hielo',
         'Los asteroides son rocosos y se concentran sobre todo en un cinturon entre Marte y Jupiter. Los cometas son bolas de hielo y polvo que, al acercarse al Sol, desarrollan una cola brillante.',
         'La cola de un cometa siempre apunta lejos del Sol.'),
        ('Los confines: Kuiper y Oort', 'El borde del Sistema Solar',
         'Mas alla de Neptuno esta el Cinturon de Kuiper (donde vive Pluton) y, aun mas lejos, la Nube de Oort: una capa esferica de cometas que rodea todo el Sistema Solar.', ''),
     ],
     'questions': [
        ('Que son los cuerpos menores del Sistema Solar?', 'single',
         'Son restos de la formacion del Sistema Solar: cuerpos mas pequenos que los planetas.',
         [('Planetas enanos, asteroides y cometas', True), ('Solo los 8 planetas', False),
          ('Las estrellas', False), ('Las galaxias', False)]),
        ('Donde esta el principal cinturon de asteroides?', 'single',
         'El cinturon principal de asteroides orbita entre Marte y Jupiter.',
         [('Entre Marte y Jupiter', True), ('Mas alla de Neptuno', False),
          ('Entre la Tierra y la Luna', False), ('Dentro del Sol', False)]),
        ('De que estan hechos sobre todo los cometas?', 'single',
         'Al acercarse al Sol, su hielo se sublima y forma la cola brillante del cometa.',
         [('Hielo y polvo', True), ('Hierro puro', False), ('Gas caliente', False), ('Lava', False)]),
        ('La cola de un cometa apunta hacia el Sol.', 'truefalse',
         'Es al reves: el viento solar empuja la cola siempre en direccion contraria al Sol.',
         [('Falso', True), ('Verdadero', False)]),
        ('Como se clasifica Pluton hoy?', 'single',
         'Desde 2006 Pluton es un planeta enano; vive en el Cinturon de Kuiper.',
         [('Planeta enano', True), ('Planeta principal', False), ('Estrella', False), ('Cometa', False)]),
        ('Que hay mas alla de Neptuno, en los confines del Sistema Solar?', 'single',
         'El Cinturon de Kuiper (donde esta Pluton) y, mucho mas lejos, la esferica Nube de Oort de cometas.',
         [('El Cinturon de Kuiper y la Nube de Oort', True), ('Otro Sol', False),
          ('Nada en absoluto', False), ('El cinturon de asteroides', False)]),
     ]},
    {'unit': 'galaxias', 'slug': 'el-medio-interestelar', 'title': 'El medio interestelar', 'icon': 'galaxy',
     'subtitle': 'Entre las estrellas',
     'cards': [
        ('El espacio no esta vacio', 'Gas y polvo entre estrellas',
         'Entre las estrellas de una galaxia no hay vacio total: hay gas (sobre todo hidrogeno) y polvo muy fino. Es el medio interestelar, la materia prima de las estrellas.',
         'Ese polvo es el que oscurece partes de la Via Lactea en el cielo.'),
        ('Nebulosas: cunas de estrellas', 'Donde nacen los soles',
         'Cuando una nube de gas del medio interestelar se contrae por gravedad, nacen estrellas nuevas. Esas nubes brillantes son las nebulosas, autenticas fabricas de estrellas.', ''),
        ('El ciclo de la materia', 'Polvo de estrellas',
         'Las estrellas nacen del gas y, al morir, devuelven material enriquecido al medio interestelar, que formara nuevas estrellas y planetas. Estamos hechos de ese material reciclado.',
         'El calcio de tus huesos se forjo dentro de estrellas.'),
     ],
     'questions': [
        ('Que es el medio interestelar?', 'single',
         'Es la materia (gas de hidrogeno y polvo fino) que llena el espacio entre las estrellas; la materia prima estelar.',
         [('El gas y el polvo que hay entre las estrellas', True), ('El nucleo de una estrella', False),
          ('Un planeta', False), ('El espacio totalmente vacio', False)]),
        ('De que esta hecho sobre todo el gas interestelar?', 'single',
         'El hidrogeno es el elemento mas abundante del universo y domina el medio interestelar.',
         [('Hidrogeno', True), ('Hierro', False), ('Oxigeno', False), ('Oro', False)]),
        ('Donde nacen las estrellas?', 'single',
         'Cuando una nube de gas se contrae por gravedad, se encienden estrellas nuevas.',
         [('En las nebulosas del medio interestelar', True), ('En los agujeros negros', False),
          ('En los planetas', False), ('En el Sol', False)]),
        ('El espacio entre las estrellas esta completamente vacio.', 'truefalse',
         'Contiene gas y polvo: el medio interestelar, del que nacen las estrellas.',
         [('Falso', True), ('Verdadero', False)]),
        ('Que hacen las estrellas con su material al morir?', 'single',
         'Ese material reciclado formara nuevas estrellas y planetas; por eso somos polvo de estrellas.',
         [('Lo devuelven enriquecido al medio interestelar', True), ('Lo destruyen para siempre', False),
          ('Lo convierten en oro puro', False), ('Nada', False)]),
        ('El polvo interestelar puede oscurecer partes de la Via Lactea.', 'truefalse',
         'Las manchas oscuras que cruzan la Via Lactea son nubes de polvo que bloquean la luz de fondo.',
         [('Verdadero', True), ('Falso', False)]),
     ]},
    {'unit': 'agujeros-negros', 'slug': 'estrellas-de-neutrones-y-pulsares',
     'title': 'Estrellas de neutrones y pulsares', 'icon': 'star',
     'subtitle': 'Restos extremos de supernova',
     'cards': [
        ('Lo que queda de una supernova', 'Materia aplastada',
         'Cuando una estrella masiva explota como supernova, su nucleo puede quedar aplastado en una estrella de neutrones: un objeto diminuto (una ciudad de ancho) pero con mas masa que el Sol.',
         'Una cucharadita de estrella de neutrones pesaria miles de millones de toneladas.'),
        ('Pulsares', 'Faros del cosmos',
         'Algunas estrellas de neutrones giran vertiginosamente y emiten haces de radiacion como un faro. Si ese haz barre la Tierra, lo recibimos como pulsos regulares: son los pulsares.',
         'Al primer pulsar lo apodaron LGM-1, por si era una senal alienigena.'),
        ('Magnetars', 'Los imanes mas potentes',
         'Un magnetar es una estrella de neutrones con un campo magnetico brutal, el mas intenso conocido en el universo. Puede liberar estallidos de energia colosales.', ''),
     ],
     'questions': [
        ('Que queda tras la supernova de una estrella masiva, si no es un agujero negro?', 'single',
         'El nucleo colapsado forma una estrella de neutrones: diminuta pero mas masiva que el Sol.',
         [('Una estrella de neutrones', True), ('Un planeta', False), ('Una enana blanca', False), ('Nada', False)]),
        ('Como es una estrella de neutrones?', 'single',
         'Del tamano de una ciudad pero con materia tan comprimida que supera la masa del Sol.',
         [('Diminuta pero con mas masa que el Sol', True), ('Enorme y ligera', False),
          ('Igual que el Sol', False), ('Un gas frio', False)]),
        ('Que es un pulsar?', 'single',
         'Su haz de radiacion barre el espacio como un faro; si nos apunta, lo recibimos como pulsos regulares.',
         [('Una estrella de neutrones que gira y emite pulsos de radiacion', True),
          ('Un planeta que parpadea', False), ('Una galaxia', False), ('Un cometa', False)]),
        ('Una cucharadita de estrella de neutrones pesaria muy poco.', 'truefalse',
         'Al contrario: pesaria miles de millones de toneladas, por su densidad extrema.',
         [('Falso', True), ('Verdadero', False)]),
        ('Que es un magnetar?', 'single',
         'Tiene el campo magnetico mas intenso conocido y puede lanzar estallidos de energia enormes.',
         [('Una estrella de neutrones con un campo magnetico brutal', True), ('Un iman de la Tierra', False),
          ('Un tipo de planeta', False), ('Una nebulosa', False)]),
        ('De donde vienen las estrellas de neutrones?', 'single',
         'Son el resto denso que deja el colapso del nucleo de una estrella muy masiva.',
         [('Del nucleo colapsado de una estrella masiva tras una supernova', True),
          ('De la fusion de dos planetas', False), ('Del Big Bang directamente', False), ('De un cometa', False)]),
     ]},
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    for data in ADD:
        if Lesson.objects.filter(slug=data['slug']).exists():
            continue
        try:
            unit = Category.objects.get(slug=data['unit'])
        except Category.DoesNotExist:
            continue
        order = (Lesson.objects.filter(category=unit).aggregate(m=Max('order'))['m'] or 0) + 1
        lesson = Lesson.objects.create(
            category=unit, title=data['title'], slug=data['slug'], subtitle=data['subtitle'],
            icon=data['icon'], order=order, is_active=True)
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
    Lesson = apps.get_model('astro', 'Lesson')
    Lesson.objects.filter(slug__in=[d['slug'] for d in ADD]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0051_seed_nivel2'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
