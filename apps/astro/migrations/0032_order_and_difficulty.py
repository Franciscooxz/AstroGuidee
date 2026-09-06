# -*- coding: utf-8 -*-
from django.db import migrations

# (slug, nuevo_orden, dificultad) — orden facil -> dificil aprobado por el usuario.
UNITS = [
    ('sistema-solar', 1, 1),
    ('la-luna-y-los-eclipses', 2, 1),
    ('las-estrellas', 3, 2),
    ('galaxias', 4, 2),
    ('exoplanetas', 5, 3),
    ('galaxias-del-universo', 6, 3),
    ('agujeros-negros', 7, 3),
    ('agujeros-negros-tipos-y-famosos', 8, 4),
    ('el-universo', 9, 4),
    ('descubrimientos-y-exploracion', 10, 4),
    ('astrofisica', 11, 5),
]


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    for slug, order, diff in UNITS:
        Category.objects.filter(slug=slug).update(order=order, difficulty=diff)


def backwards(apps, schema_editor):
    # Restaura el orden anterior (dificultad vuelve a 1); orden previo conocido.
    prev = {
        'sistema-solar': 1, 'la-luna-y-los-eclipses': 2, 'las-estrellas': 3,
        'galaxias': 4, 'agujeros-negros': 5, 'el-universo': 6, 'astrofisica': 7,
        'exoplanetas': 8, 'galaxias-del-universo': 9,
        'agujeros-negros-tipos-y-famosos': 10, 'descubrimientos-y-exploracion': 11,
    }
    Category = apps.get_model('astro', 'Category')
    for slug, order in prev.items():
        Category.objects.filter(slug=slug).update(order=order, difficulty=1)


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0031_category_difficulty'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
