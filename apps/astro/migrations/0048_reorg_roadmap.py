# -*- coding: utf-8 -*-
"""Reorganizacion del contenido segun el roadmap 0-9 (Fase R1, sin contenido nuevo).

- Disuelve 'Astrofisica': gravedad->Sistema Solar, luz->Estrellas, relatividad->AN.
- Fusiona 'Galaxias del universo' en 'Galaxias' y 'AN: tipos y famosos' en 'Agujeros negros'.
- Renombra unidades a su nivel del roadmap y reordena + ajusta dificultad.
"""
from django.db import migrations
from django.db.models import Max

# lecciones a mover: (lesson_slug, unidad_destino_slug)
MOVES = [
    ('la-gravedad', 'sistema-solar'),
    ('la-luz-y-el-espectro', 'las-estrellas'),
    ('nociones-de-relatividad', 'agujeros-negros'),
    ('andromeda-y-el-grupo-local', 'galaxias'),
    ('galaxias-asombrosas', 'galaxias'),
    ('tipos-de-agujeros-negros', 'agujeros-negros'),
    ('famosos-y-ondas-gravitacionales', 'agujeros-negros'),
]
# de donde venia cada leccion (para revertir)
ORIGIN = {
    'la-gravedad': 'astrofisica', 'la-luz-y-el-espectro': 'astrofisica',
    'nociones-de-relatividad': 'astrofisica',
    'andromeda-y-el-grupo-local': 'galaxias-del-universo',
    'galaxias-asombrosas': 'galaxias-del-universo',
    'tipos-de-agujeros-negros': 'agujeros-negros-tipos-y-famosos',
    'famosos-y-ondas-gravitacionales': 'agujeros-negros-tipos-y-famosos',
}
RENAMES = {
    'la-luna-y-los-eclipses': ('La Luna y los eclipses', 'Bienvenido al universo'),
    'galaxias': ('Galaxias', 'Galaxias y el cosmos'),
    'agujeros-negros': ('Agujeros negros', 'Objetos extremos'),
    'el-universo': ('El Universo', 'Cosmologia'),
    'descubrimientos-y-exploracion': ('Descubrimientos y exploracion', 'Exploracion del espacio'),
}
# unidades vaciadas -> desactivar
EMPTIED = ['astrofisica', 'galaxias-del-universo', 'agujeros-negros-tipos-y-famosos']
# estado final: slug -> (order, difficulty)
FINAL = {
    'la-luna-y-los-eclipses': (1, 1),   # Nivel 0 (los 2,3 quedan para N1/N2)
    'sistema-solar': (4, 2),            # Nivel 3
    'exoplanetas': (5, 3),             # Nivel 3 (ext.)
    'las-estrellas': (6, 3),           # Nivel 4
    'galaxias': (7, 3),                # Nivel 5
    'agujeros-negros': (8, 4),         # Nivel 7
    'el-universo': (9, 5),             # Nivel 8
    'descubrimientos-y-exploracion': (10, 3),  # transversal
}
# estado previo conocido: slug -> (order, difficulty, is_active)
PREV = {
    'sistema-solar': (1, 1), 'la-luna-y-los-eclipses': (2, 1), 'las-estrellas': (3, 2),
    'galaxias': (4, 2), 'exoplanetas': (5, 3), 'galaxias-del-universo': (6, 3),
    'agujeros-negros': (7, 3), 'agujeros-negros-tipos-y-famosos': (8, 4),
    'el-universo': (9, 4), 'descubrimientos-y-exploracion': (10, 4), 'astrofisica': (11, 5),
}


def _move(Lesson, Card, Category, lesson_slug, cat_slug):
    try:
        lesson = Lesson.objects.get(slug=lesson_slug)
        cat = Category.objects.get(slug=cat_slug)
    except (Lesson.DoesNotExist, Category.DoesNotExist):
        return
    nxt = (Lesson.objects.filter(category=cat).aggregate(m=Max('order'))['m'] or 0) + 1
    Lesson.objects.filter(id=lesson.id).update(category=cat, order=nxt)
    Card.objects.filter(lesson=lesson).update(category=cat)


def forwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')

    for slug, dest in MOVES:
        _move(Lesson, Card, Category, slug, dest)
    for slug, (old, new) in RENAMES.items():
        Category.objects.filter(slug=slug).update(name=new)
    for slug in EMPTIED:
        Category.objects.filter(slug=slug).update(is_active=False)
    for slug, (order, diff) in FINAL.items():
        Category.objects.filter(slug=slug).update(order=order, difficulty=diff, is_active=True)


def backwards(apps, schema_editor):
    Category = apps.get_model('astro', 'Category')
    Lesson = apps.get_model('astro', 'Lesson')
    Card = apps.get_model('astro', 'Card')

    for slug, dest in MOVES:  # devolver cada leccion a su unidad original
        _move(Lesson, Card, Category, slug, ORIGIN[slug])
    for slug, (old, new) in RENAMES.items():
        Category.objects.filter(slug=slug).update(name=old)
    for slug, (order, diff) in PREV.items():
        Category.objects.filter(slug=slug).update(order=order, difficulty=diff, is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0047_duel'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
