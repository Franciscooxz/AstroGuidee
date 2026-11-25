"""Carga la ruta de 24 unidades y aparta el contenido anterior.

No borra lecciones ni progresos viejos: las unidades sin código quedan
inactivas, así que dejan de salir en la ruta y sus datos siguen en la base.
"""

from django.db import migrations


def load_path(apps, schema_editor):
    from apps.astro.path_build import load_learning_path

    load_learning_path(apps, schema_editor)


def hide_path(apps, schema_editor):
    Category = apps.get_model("astro", "Category")
    Category.objects.exclude(code__isnull=True).update(is_active=False, status="draft")


class Migration(migrations.Migration):
    dependencies = [
        ("astro", "0056_learning_path_schema"),
    ]

    operations = [
        migrations.RunPython(load_path, hide_path),
    ]
