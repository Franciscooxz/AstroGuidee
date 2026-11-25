"""Aviso diario por correo para volver al repaso.

En producción se ejecuta cada hora:
    python manage.py send_reminders

Usa la hora local del servidor (America/Bogota) y el correo configurado
en Django. Cada persona elige la hora en Ajustes.
"""

import os

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone

from apps.astro.models import Notification, Profile, ReviewItem


class Command(BaseCommand):
    help = "Envía el aviso del día a quien lo tiene activo en esta hora."

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()
        base = os.environ.get("APP_BASE_URL", "").rstrip("/")
        if not base and os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
            base = "https://" + os.environ["RENDER_EXTERNAL_HOSTNAME"]
        path = reverse("astro:review")
        link = f"{base}{path}" if base else path

        due = Profile.objects.filter(reminder_on=True, reminder_hour=now.hour).select_related("user")
        sent = 0
        for profile in due:
            if profile.last_reminded == today:
                continue
            email = (profile.user.email or "").strip()
            has_review = ReviewItem.objects.filter(user=profile.user).exists()
            text = (
                "Tienes un repaso esperando en AstroGuide."
                if has_review
                else "Tu ruta de AstroGuide te espera."
            )
            Notification.push(profile.user, text, icon="progress", url=path)
            if email:
                try:
                    send_mail(
                        "Tu repaso de AstroGuide",
                        f"{text}\n\n{link}",
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as exc:
                    self.stderr.write(f"{profile.user.username}: {exc}")
                    continue
            profile.last_reminded = today
            profile.save(update_fields=["last_reminded"])
            sent += 1
        self.stdout.write(f"Avisos enviados: {sent}")
