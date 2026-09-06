# -*- coding: utf-8 -*-
from django.db import migrations

# Explicaciones (el porque) para las unidades iniciales Sistema Solar + La Luna.
# { lesson_slug: { texto_pregunta: explicacion } }
EXPL = {
    'el-sol': {
        "Que tipo de cuerpo celeste es el Sol?":
            "El Sol es una estrella: una enorme esfera de gas que produce su propia luz y calor. "
            "Los planetas, en cambio, no brillan por si mismos.",
        "Que proceso genera la energia del Sol?":
            "En su nucleo, el Sol fusiona hidrogeno en helio a millones de grados. Esa fusion "
            "nuclear libera la energia que nos llega como luz y calor.",
        "Que porcentaje de la masa del Sistema Solar tiene el Sol?":
            "El Sol concentra mas del 99% de toda la masa del Sistema Solar. Por eso su gravedad "
            "domina y mantiene a los planetas en orbita.",
        "El Sol es una estrella.":
            "Verdadero. Nos parece distinto solo porque esta muchisimo mas cerca que las demas "
            "estrellas, que vemos como simples puntos por la distancia.",
        "Escribe el elemento mas abundante en el Sol (una palabra).":
            "El hidrogeno es el elemento mas abundante del Sol (unas tres cuartas partes de su "
            "masa), seguido del helio. Es el combustible de su fusion.",
    },
    'planetas-rocosos': {
        "Cual es el planeta mas cercano al Sol?":
            "Mercurio es el planeta mas cercano al Sol. Es pequeno, rocoso y casi sin atmosfera, "
            "con temperaturas extremas entre el dia y la noche.",
        "Por que Marte se ve rojo?":
            "El suelo de Marte es rico en oxido de hierro (basicamente herrumbre), y eso le da "
            "su caracteristico tono rojizo.",
        "Cual es el planeta mas caliente del Sistema Solar?":
            "Venus es el mas caliente (unos 460 grados C), incluso mas que Mercurio, por su densa "
            "atmosfera de CO2 que atrapa el calor: un efecto invernadero desbocado.",
        "Cual es el planeta rojo?":
            "Marte es conocido como el planeta rojo por el oxido de hierro de su superficie.",
        "Venus gira al reves que la mayoria de los planetas.":
            "Verdadero. Venus rota en sentido retrogrado, asi que alli el Sol saldria por el "
            "oeste. Ademas gira muy despacio.",
    },
    'gigantes-gaseosos': {
        "Cual es el planeta mas grande del Sistema Solar?":
            "Jupiter es el mayor: cabrian mas de 1.300 Tierras en su interior. Es un gigante "
            "gaseoso, sin superficie solida.",
        "Que planeta es famoso por sus espectaculares anillos?":
            "Saturno destaca por sus brillantes anillos, hechos de miles de millones de trozos de "
            "hielo y roca. Otros gigantes tienen anillos, pero mucho mas tenues.",
        "De que estan hechos sobre todo los gigantes gaseosos?":
            "Sobre todo de hidrogeno y helio, los mismos gases que forman las estrellas. No tienen "
            "una superficie solida donde posarse.",
        "Que es la Gran Mancha Roja de Jupiter?":
            "Es una tormenta gigantesca, mas grande que la Tierra, que lleva siglos girando en la "
            "atmosfera de Jupiter.",
        "Saturno es tan poco denso que flotaria en el agua.":
            "Verdadero. Su densidad es menor que la del agua, asi que en una tina lo bastante "
            "grande, Saturno flotaria.",
    },
    'gigantes-helados': {
        "Cual es el planeta mas alejado del Sol?":
            "Neptuno es el planeta mas lejano del Sol. Tarda unos 165 anos terrestres en completar "
            "una sola orbita.",
        "Que tiene de especial la rotacion de Urano?":
            "Urano gira casi de lado, con su eje inclinado unos 98 grados, probablemente por un "
            "gran impacto en el pasado. Sus estaciones son extremas.",
        "Que le da a Urano y Neptuno su color azulado?":
            "El metano de su atmosfera absorbe la luz roja y refleja la azul, por eso ambos se "
            "ven azulados.",
        "Cual es el planeta mas lejano del Sol?":
            "Neptuno, el ultimo de los ocho planetas, es el mas alejado del Sol.",
        "Urano gira casi de lado, como acostado.":
            "Verdadero. Su eje esta tan inclinado que rueda practicamente tumbado sobre su orbita.",
    },
    'la-luna': {
        "Que es la Luna?":
            "La Luna es un satelite natural: un cuerpo que orbita la Tierra. No tiene luz propia; "
            "brilla porque refleja la del Sol.",
        "La Luna tiene luz propia.":
            "Falso. La Luna no emite luz: la vemos porque refleja la luz del Sol, como un espejo.",
        "Que causa principalmente las mareas?":
            "La gravedad de la Luna tira del agua de los oceanos y provoca las mareas. El Sol "
            "tambien influye, pero menos.",
        "Que teoria explica el origen de la Luna?":
            "La teoria del gran impacto: hace unos 4.500 millones de anos un cuerpo del tamano de "
            "Marte choco con la Tierra, y los restos formaron la Luna.",
        "La Luna siempre nos muestra la misma cara.":
            "Verdadero. La Luna tarda lo mismo en girar sobre si misma que en dar una vuelta a la "
            "Tierra (rotacion sincrona), asi que siempre vemos la misma cara.",
    },
    'fases-de-la-luna': {
        "Por que la Luna tiene fases?":
            "Segun la posicion de la Luna respecto al Sol y la Tierra, vemos iluminada una porcion "
            "distinta de su cara: eso son las fases.",
        "Cuanto dura aproximadamente un ciclo lunar? (numero de dias)":
            "El ciclo completo de fases dura unos 29,5 dias, algo mas que una vuelta de la Luna "
            "alrededor de la Tierra.",
        "En que fase no se ve la Luna?":
            "En luna nueva la cara iluminada apunta al lado contrario a nosotros, asi que "
            "practicamente no se ve.",
        "Escribe cuantas fases principales tiene la Luna (numero).":
            "Se suelen contar 4 fases principales: nueva, cuarto creciente, llena y cuarto menguante.",
        "Las fases de la Luna se deben a la sombra de la Tierra.":
            "Falso. Las fases dependen de que parte iluminada vemos; la sombra de la Tierra solo "
            "interviene en los eclipses lunares.",
    },
    'eclipses': {
        "En un eclipse solar, que tapa al Sol?":
            "En un eclipse solar es la Luna la que se interpone entre el Sol y la Tierra, tapando "
            "su luz.",
        "En un eclipse lunar la Luna se ve rojiza.":
            "Verdadero. La atmosfera terrestre desvia algo de luz roja hacia la Luna, dandole ese "
            "tono cobrizo (la Luna de sangre).",
        "Cuando ocurre un eclipse lunar?":
            "Cuando la Tierra se coloca entre el Sol y la Luna, y su sombra cae sobre la Luna.",
        "Por que la Luna se ve rojiza en un eclipse lunar?":
            "La atmosfera de la Tierra filtra y desvia la luz roja del Sol hacia la Luna; por eso "
            "se tine de rojo en vez de apagarse del todo.",
        "Es seguro mirar un eclipse solar directamente sin proteccion.":
            "Falso. Mirar al Sol directamente, incluso en eclipse, puede danar los ojos de forma "
            "permanente. Hay que usar filtros solares certificados.",
    },
}


def forwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    for slug, mapping in EXPL.items():
        for text, exp in mapping.items():
            Question.objects.filter(lesson__slug=slug, text=text).update(explanation=exp)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    texts = [t for m in EXPL.values() for t in m]
    Question.objects.filter(text__in=texts).update(explanation='')


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0035_question_explanation'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
