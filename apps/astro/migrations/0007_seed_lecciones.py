from django.db import migrations
from django.utils.text import slugify


# Lecciones del Sistema Solar: (titulo, icono, orden, [slugs de tarjetas en orden])
LESSONS = [
    ('El Sol', 'sun', 1, ['el-sol']),
    ('Planetas rocosos', 'mars', 2, ['mercurio', 'venus', 'la-tierra', 'marte']),
    ('Gigantes gaseosos', 'jupiter', 3, ['jupiter', 'saturno']),
    ('Gigantes helados', 'neptune', 4, ['urano', 'neptuno']),
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')

    try:
        unit = Category.objects.get(slug='sistema-solar')
    except Category.DoesNotExist:
        return

    for title, icon, order, card_slugs in LESSONS:
        lesson, _ = Lesson.objects.get_or_create(
            slug=slugify(title),
            defaults={'category': unit, 'title': title, 'icon': icon, 'order': order},
        )
        for i, cslug in enumerate(card_slugs, start=1):
            Card.objects.filter(slug=cslug).update(lesson=lesson, order=i)


def backwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')
    Card.objects.update(lesson=None)
    Lesson.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0006_lessons'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
