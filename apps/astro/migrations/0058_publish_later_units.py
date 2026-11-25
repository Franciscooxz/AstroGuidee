"""Publica las unidades 9 a 24 con lecciones comprobadas.

Vuelve a cargar la ruta. Es idempotente: actualiza por código y por slug
y no borra el progreso de las lecciones que ya existían.
"""

from django.db import migrations


def load_path(apps, schema_editor):
    from apps.astro.path_build import load_learning_path

    load_learning_path(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [
        ("astro", "0057_learning_path_content"),
    ]

    operations = [
        migrations.RunPython(load_path, migrations.RunPython.noop),
    ]
