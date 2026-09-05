from django.db import migrations


CARD_ICONS = {
    'el-sol': 'sun',
    'mercurio': 'mercury',
    'venus': 'venus',
    'la-tierra': 'earth',
    'marte': 'mars',
    'jupiter': 'jupiter',
    'saturno': 'saturn',
    'urano': 'uranus',
    'neptuno': 'neptune',
}


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Card = apps.get_model('astro', 'Card')

    Category.objects.filter(slug='sistema-solar').update(icon='orbit')
    for slug, icon in CARD_ICONS.items():
        Card.objects.filter(slug=slug).update(icon=icon)


def backwards(apps, schema_editor):
    Card = apps.get_model('astro', 'Card')
    Category = apps.get_model('astro', 'Category')
    Card.objects.update(icon='')
    Category.objects.update(icon='')


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0003_add_icon'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
