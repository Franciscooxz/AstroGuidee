"""Vuelve a cargar la ruta pedagógica sin borrar el progreso.

    python manage.py load_learning_path
"""

from django.core.management.base import BaseCommand

from apps.astro.path_build import load_learning_path


class Command(BaseCommand):
    help = "Actualiza las 6 etapas y las 24 unidades de la ruta."

    def handle(self, *args, **options):
        load_learning_path()
        self.stdout.write(self.style.SUCCESS("Ruta actualizada."))
