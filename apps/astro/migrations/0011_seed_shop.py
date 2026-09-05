from django.db import migrations


ITEMS = [
    {
        'key': 'streak-freeze', 'name': 'Congelar racha', 'effect': 'streak_freeze',
        'icon': 'flame', 'price': 30, 'order': 1,
        'description': 'Protege tu racha si te saltas un dia. Se usa solo cuando lo necesitas.',
    },
    {
        'key': 'double-xp', 'name': 'Doble XP', 'effect': 'double_xp',
        'icon': 'star', 'price': 20, 'order': 2,
        'description': 'Duplica el XP que ganes en tu proximo quiz.',
    },
]


def forwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    for data in ITEMS:
        ShopItem.objects.get_or_create(key=data['key'], defaults=data)


def backwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    ShopItem.objects.filter(key__in=[i['key'] for i in ITEMS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0010_shop'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
