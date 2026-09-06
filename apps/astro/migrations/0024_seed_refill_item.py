from django.db import migrations


def forwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    ShopItem.objects.get_or_create(key='refill-hearts', defaults={
        'name': 'Recargar vidas', 'effect': 'refill_hearts', 'icon': 'flame',
        'price': 40, 'order': 3,
        'description': 'Rellena todas tus vidas al instante.',
    })


def backwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    ShopItem.objects.filter(key='refill-hearts').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0023_hearts'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
