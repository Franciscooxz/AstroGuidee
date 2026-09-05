from django.db import migrations


FRAMES = [
    {'key': 'frame-gold', 'name': 'Marco Dorado', 'effect': 'frame', 'icon': 'star',
     'price': 60, 'order': 10, 'description': 'Un aro dorado brillante para tu avatar.'},
    {'key': 'frame-nebula', 'name': 'Marco Nebulosa', 'effect': 'frame', 'icon': 'galaxy',
     'price': 60, 'order': 11, 'description': 'Un halo azul-morado de nebulosa.'},
    {'key': 'frame-ember', 'name': 'Marco Solar', 'effect': 'frame', 'icon': 'flame',
     'price': 60, 'order': 12, 'description': 'Un anillo ardiente color fuego.'},
]


def forwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    for data in FRAMES:
        ShopItem.objects.get_or_create(key=data['key'], defaults=data)


def backwards(apps, schema_editor):
    ShopItem = apps.get_model('astro', 'ShopItem')
    ShopItem.objects.filter(key__in=[f['key'] for f in FRAMES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0018_frames'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
