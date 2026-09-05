from django.db import migrations
from django.utils.text import slugify


CATEGORY = {
    'name': 'Sistema Solar',
    'subtitle': 'Nuestro vecindario cosmico: el Sol y sus planetas.',
    'description': 'El Sistema Solar es el conjunto formado por el Sol y todos los cuerpos '
                   'que orbitan a su alrededor: ocho planetas, sus lunas, planetas enanos, '
                   'asteroides y cometas. Toca cada tarjeta para descubrir sus secretos.',
    'emoji': '🪐',
    'accent': '#8b5cff',
    'order': 1,
}

CARDS = [
    {
        'title': 'El Sol', 'subtitle': 'Estrella — enana amarilla', 'emoji': '☀️', 'order': 1,
        'summary': 'Es la estrella del centro del Sistema Solar. Una enorme esfera de gas caliente '
                   '(hidrogeno y helio) que genera luz y calor mediante fusion nuclear. Contiene el '
                   '99,8% de toda la masa del sistema.',
        'fun_fact': 'Cabe mas de un millon de Tierras dentro del Sol.',
    },
    {
        'title': 'Mercurio', 'subtitle': 'Planeta rocoso — el mas cercano', 'emoji': '☿️', 'order': 2,
        'summary': 'El planeta mas pequeno y el mas cercano al Sol. No tiene atmosfera que retenga el '
                   'calor, asi que pasa de un calor extremo de dia a un frio helado de noche.',
        'fun_fact': 'Un ano en Mercurio dura solo 88 dias terrestres.',
    },
    {
        'title': 'Venus', 'subtitle': 'Planeta rocoso — el mas caliente', 'emoji': '♀️', 'order': 3,
        'summary': 'Similar en tamano a la Tierra, pero cubierto por una densa atmosfera de dioxido de '
                   'carbono que atrapa el calor. Es el planeta mas caliente, mas incluso que Mercurio.',
        'fun_fact': 'En Venus, un dia dura mas que un ano.',
    },
    {
        'title': 'La Tierra', 'subtitle': 'Planeta rocoso — nuestro hogar', 'emoji': '🌍', 'order': 4,
        'summary': 'El unico planeta conocido con vida. Tiene agua liquida, una atmosfera respirable y '
                   'un campo magnetico que nos protege de la radiacion solar.',
        'fun_fact': 'El 71% de su superficie esta cubierta de agua.',
    },
    {
        'title': 'Marte', 'subtitle': 'Planeta rocoso — el planeta rojo', 'emoji': '♂️', 'order': 5,
        'summary': 'Su color rojizo viene del oxido de hierro (herrumbre) en su superficie. Tiene los '
                   'volcanes mas grandes y canones mas profundos del Sistema Solar.',
        'fun_fact': 'El Monte Olimpo, en Marte, es 3 veces mas alto que el Everest.',
    },
    {
        'title': 'Jupiter', 'subtitle': 'Gigante gaseoso — el mas grande', 'emoji': '🪐', 'order': 6,
        'summary': 'El planeta mas grande del Sistema Solar. Es una bola gigante de gas con una enorme '
                   'tormenta llamada la Gran Mancha Roja, mas grande que la Tierra entera.',
        'fun_fact': 'Tiene mas de 90 lunas conocidas.',
    },
    {
        'title': 'Saturno', 'subtitle': 'Gigante gaseoso — el de los anillos', 'emoji': '💫', 'order': 7,
        'summary': 'Famoso por sus espectaculares anillos, formados por miles de millones de trozos de '
                   'hielo y roca. Es tan poco denso que flotaria en el agua.',
        'fun_fact': 'Sus anillos miden hasta 280.000 km de ancho pero solo unos metros de grosor.',
    },
    {
        'title': 'Urano', 'subtitle': 'Gigante helado — el inclinado', 'emoji': '🔵', 'order': 8,
        'summary': 'Un gigante de hielo de color azul-verdoso por el metano de su atmosfera. Gira casi '
                   'de lado, como si rodara sobre su orbita.',
        'fun_fact': 'Su eje esta inclinado 98 grados: practicamente gira acostado.',
    },
    {
        'title': 'Neptuno', 'subtitle': 'Gigante helado — el mas lejano', 'emoji': '🌀', 'order': 9,
        'summary': 'El planeta mas alejado del Sol. Un mundo azul, frio y ventoso, con los vientos mas '
                   'rapidos del Sistema Solar.',
        'fun_fact': 'Sus vientos pueden superar los 2.000 km/h.',
    },
]


def seed(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Card = apps.get_model('astro', 'Card')

    cat, _ = Category.objects.get_or_create(
        slug=slugify(CATEGORY['name']),
        defaults={
            'name': CATEGORY['name'],
            'subtitle': CATEGORY['subtitle'],
            'description': CATEGORY['description'],
            'emoji': CATEGORY['emoji'],
            'accent': CATEGORY['accent'],
            'order': CATEGORY['order'],
        },
    )
    for data in CARDS:
        Card.objects.get_or_create(
            category=cat,
            slug=slugify(data['title']),
            defaults={
                'title': data['title'],
                'subtitle': data['subtitle'],
                'summary': data['summary'],
                'fun_fact': data['fun_fact'],
                'emoji': data['emoji'],
                'order': data['order'],
            },
        )


def unseed(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Category.objects.filter(slug=slugify(CATEGORY['name'])).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
