from django.db import migrations


ACHIEVEMENTS = [
    {'key': 'primer-paso', 'name': 'Primer paso', 'icon': 'check', 'order': 1,
     'condition_type': 'lessons_completed', 'threshold': 1,
     'description': 'Completa tu primera leccion.'},
    {'key': 'explorador', 'name': 'Explorador', 'icon': 'rocket', 'order': 2,
     'condition_type': 'lessons_completed', 'threshold': 3,
     'description': 'Completa 3 lecciones.'},
    {'key': 'sistema-dominado', 'name': 'Sistema dominado', 'icon': 'orbit', 'order': 3,
     'condition_type': 'lessons_completed', 'threshold': 4,
     'description': 'Completa todas las lecciones del Sistema Solar.'},
    {'key': 'en-racha', 'name': 'En racha', 'icon': 'flame', 'order': 4,
     'condition_type': 'streak', 'threshold': 3,
     'description': 'Manten una racha de 3 dias.'},
    {'key': 'imparable', 'name': 'Imparable', 'icon': 'flame', 'order': 5,
     'condition_type': 'streak', 'threshold': 7,
     'description': 'Manten una racha de 7 dias.'},
    {'key': 'perfeccionista', 'name': 'Perfeccionista', 'icon': 'star', 'order': 6,
     'condition_type': 'perfect_quizzes', 'threshold': 3,
     'description': 'Consigue 3 quizzes perfectos.'},
    {'key': 'cosmonauta', 'name': 'Cosmonauta', 'icon': 'galaxy', 'order': 7,
     'condition_type': 'xp', 'threshold': 200,
     'description': 'Acumula 200 XP.'},
]


def forwards(apps, schema_editor):
    Achievement = apps.get_model('astro', 'Achievement')
    for data in ACHIEVEMENTS:
        Achievement.objects.get_or_create(key=data['key'], defaults=data)


def backwards(apps, schema_editor):
    Achievement = apps.get_model('astro', 'Achievement')
    Achievement.objects.filter(key__in=[a['key'] for a in ACHIEVEMENTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0012_achievements'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
