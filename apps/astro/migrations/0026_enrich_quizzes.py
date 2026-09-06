# -*- coding: utf-8 -*-
from django.db import migrations
from django.utils.text import slugify


# Preguntas extra para llegar a >=5 por leccion. q = (texto, tipo, [(op, correcta)])
ADD_QUESTIONS = {
    'planetas-rocosos': [
        ('Cual es el planeta rojo?', 'single',
         [('Marte', True), ('Venus', False), ('Mercurio', False), ('La Tierra', False)]),
        ('Venus gira al reves que la mayoria de los planetas.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'gigantes-gaseosos': [
        ('De que estan hechos sobre todo los gigantes gaseosos?', 'single',
         [('Gas (hidrogeno y helio)', True), ('Roca', False), ('Hielo', False), ('Metal', False)]),
        ('Que es la Gran Mancha Roja de Jupiter?', 'single',
         [('Una tormenta gigante', True), ('Un volcan', False), ('Un oceano', False), ('Un crater', False)]),
        ('Saturno es tan poco denso que flotaria en el agua.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'gigantes-helados': [
        ('Que le da a Urano y Neptuno su color azulado?', 'single',
         [('El metano de su atmosfera', True), ('El agua', False), ('El oxigeno', False), ('El hielo seco', False)]),
        ('Cual es el planeta mas lejano del Sol?', 'single',
         [('Neptuno', True), ('Urano', False), ('Saturno', False), ('Pluton', False)]),
        ('Urano gira casi de lado, como acostado.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'la-luna': [
        ('Que teoria explica el origen de la Luna?', 'single',
         [('El gran impacto', True), ('La captura de un cometa', False),
          ('Una explosion solar', False), ('El Big Bang', False)]),
        ('La Luna siempre nos muestra la misma cara.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'fases-de-la-luna': [
        ('En que fase no se ve la Luna?', 'single',
         [('Luna nueva', True), ('Luna llena', False), ('Cuarto creciente', False), ('Cuarto menguante', False)]),
        ('Escribe cuantas fases principales tiene la Luna (numero).', 'text',
         [('4', True), ('cuatro', True)]),
        ('Las fases de la Luna se deben a la sombra de la Tierra.', 'truefalse',
         [('Falso', True), ('Verdadero', False)]),
    ],
    'eclipses': [
        ('Cuando ocurre un eclipse lunar?', 'single',
         [('Cuando la Tierra se pone entre el Sol y la Luna', True),
          ('Cuando la Luna tapa al Sol', False), ('Solo de dia', False), ('Nunca', False)]),
        ('Por que la Luna se ve rojiza en un eclipse lunar?', 'single',
         [('Por la luz que filtra la atmosfera de la Tierra', True),
          ('Porque se calienta', False), ('Por el polvo lunar', False), ('Por Marte', False)]),
        ('Es seguro mirar un eclipse solar directamente sin proteccion.', 'truefalse',
         [('Falso', True), ('Verdadero', False)]),
    ],
    'que-es-una-estrella': [
        ('Que elemento fusiona una estrella como el Sol en su nucleo?', 'single',
         [('Hidrogeno', True), ('Oxigeno', False), ('Carbono', False), ('Hierro', False)]),
        ('Escribe el nombre de la estrella mas cercana a la Tierra.', 'text',
         [('El Sol', True), ('Sol', True)]),
        ('Las estrellas tienen luz propia.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'tipos-de-estrellas': [
        ('Que determina el color de una estrella?', 'single',
         [('Su temperatura', True), ('Su edad', False), ('Su distancia', False), ('Su nombre', False)]),
        ('Una estrella mucho mas grande que el Sol es una...', 'single',
         [('Gigante o supergigante', True), ('Enana', False), ('Planeta', False), ('Luna', False)]),
        ('Cuanto mas masiva es una estrella, mas rapido vive y muere.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
    'vida-y-muerte-de-una-estrella': [
        ('En que termina una estrella como el Sol?', 'single',
         [('En una enana blanca', True), ('En un agujero negro', False),
          ('En una supernova', False), ('En un planeta', False)]),
        ('Que puede quedar tras la supernova de una estrella muy masiva?', 'single',
         [('Un agujero negro o una estrella de neutrones', True),
          ('Un planeta nuevo', False), ('Un cometa', False), ('Nada', False)]),
        ('Escribe como se llaman las nubes de gas donde nacen las estrellas.', 'text',
         [('nebulosas', True), ('nebulosa', True)]),
    ],
    'la-via-lactea': [
        ('Donde esta el Sol dentro de la Via Lactea?', 'single',
         [('En uno de sus brazos espirales', True), ('En el centro exacto', False),
          ('Fuera de ella', False), ('En otra galaxia', False)]),
        ('Que hay en el centro de la Via Lactea?', 'single',
         [('Un agujero negro supermasivo', True), ('Una estrella gigante', False),
          ('Un planeta', False), ('Nada', False)]),
        ('Escribe el nombre de nuestra galaxia.', 'text',
         [('Via Lactea', True), ('vialactea', True)]),
    ],
    'tipos-de-galaxias': [
        ('Que tipo de galaxia tiene brazos que giran?', 'single',
         [('Espiral', True), ('Eliptica', False), ('Irregular', False), ('Cuadrada', False)]),
        ('Las galaxias con forma de balon y estrellas viejas son...', 'single',
         [('Elipticas', True), ('Espirales', False), ('Irregulares', False), ('Enanas', False)]),
        ('La Via Lactea chocara con la galaxia de Andromeda en el futuro.', 'truefalse',
         [('Verdadero', True), ('Falso', False)]),
    ],
}

# Tarjetas extra para lecciones flojas. c = (titulo, subtitulo, resumen, dato)
ADD_CARDS = {
    'gigantes-gaseosos': [
        ('Un monton de lunas', 'Mundos propios',
         'Jupiter y Saturno tienen decenas de lunas. Algunas, como Europa o Encelado, podrian esconder oceanos de agua bajo el hielo.',
         'Europa podria tener mas agua que toda la Tierra.')],
    'gigantes-helados': [
        ('Lejos y helados', 'Los confines del sistema',
         'Estan tan lejos del Sol que reciben muy poca luz y son gelidos. Neptuno tarda 165 anos en dar una sola vuelta al Sol.', '')],
    'fases-de-la-luna': [
        ('Truco para reconocerlas', 'Creciente o menguante',
         'En el hemisferio norte: si la Luna parece una "D" esta creciendo, y si parece una "C" esta menguando.', '')],
    'eclipses': [
        ('No pasan cada mes', 'La orbita inclinada',
         'La orbita de la Luna esta un poco inclinada, por eso no hay un eclipse en cada luna nueva o llena, solo cuando se alinean.', '')],
    'que-es-una-estrella': [
        ('Soles lejanos', 'Puntos en la noche',
         'Las estrellas parecen puntitos por la enorme distancia, pero en realidad son soles gigantes, muchos mayores que el nuestro.', '')],
    'tipos-de-estrellas': [
        ('Enanas y supergigantes', 'Tamanos extremos',
         'El Sol es una enana amarilla. Betelgeuse es una supergigante roja: si estuviera en el centro del Sistema Solar, se tragaria varios planetas.', '')],
    'vida-y-muerte-de-una-estrella': [
        ('Polvo de estrellas', 'De donde vienes',
         'El calcio de tus huesos y el hierro de tu sangre se forjaron dentro de estrellas hace miles de millones de anos.', '')],
    'la-via-lactea': [
        ('Una banda en el cielo', 'Por que se llama asi',
         'En cielos muy oscuros, la Via Lactea se ve como una banda lechosa cruzando el cielo: son sus millones de estrellas juntas.', '')],
    'tipos-de-galaxias': [
        ('Miles de millones', 'Un universo enorme',
         'Se calcula que hay billones de galaxias en el universo observable, cada una con miles de millones de estrellas.', '')],
}


def forwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')
    Card = apps.get_model('astro', 'Card')

    for slug, cards in ADD_CARDS.items():
        try:
            lesson = Lesson.objects.get(slug=slug)
        except Lesson.DoesNotExist:
            continue
        base = lesson.cards.count()
        for i, (title, subtitle, summary, fun) in enumerate(cards, start=base + 1):
            if Card.objects.filter(lesson=lesson, slug=slugify(title)).exists():
                continue
            Card.objects.create(lesson=lesson, category=lesson.category, slug=slugify(title),
                                title=title, subtitle=subtitle, summary=summary, fun_fact=fun,
                                icon=lesson.icon, order=i)

    for slug, questions in ADD_QUESTIONS.items():
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
    # Reversion simple: borra las preguntas/cartas añadidas por texto/slug.
    Question = apps.get_model('astro', 'Question')
    Card = apps.get_model('astro', 'Card')
    texts = [q[0] for qs in ADD_QUESTIONS.values() for q in qs]
    Question.objects.filter(text__in=texts).delete()
    slugs = [slugify(c[0]) for cs in ADD_CARDS.values() for c in cs]
    Card.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0025_alter_shopitem_effect'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
