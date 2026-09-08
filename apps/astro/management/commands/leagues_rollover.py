"""Cierre semanal de ligas: aplica ascensos/descensos y reinicia la semana.

En produccion se ejecuta con un cron los lunes (inicio de la semana ISO):
    python manage.py leagues_rollover
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.astro.models import Notification, Profile
from apps.astro.views import DIVISIONS, LEAGUE_PROMOTE, LEAGUE_RELEGATE, get_division


class Command(BaseCommand):
    help = "Aplica ascensos/descensos de liga y reinicia la XP semanal."

    def handle(self, *args, **options):
        wk = timezone.localdate().strftime("%G-%V")
        top_i = len(DIVISIONS) - 1

        profiles = list(Profile.objects.select_related("user"))
        by_div = {}
        for p in profiles:
            p.eff = p.weekly_xp if p.week_key == wk else 0
            by_div.setdefault(p.division, []).append(p)

        changes = {}  # profile.id -> nueva division
        for i in range(len(DIVISIONS)):
            members = sorted(by_div.get(i, []), key=lambda p: (-p.eff, p.user.username.lower()))
            n = len(members)
            promote_n = 0 if i == top_i else LEAGUE_PROMOTE
            relegate_n = 0 if i == 0 else LEAGUE_RELEGATE
            relegate_cut = (n - relegate_n) if n > promote_n + relegate_n else n
            for rank, p in enumerate(members, start=1):
                if promote_n and rank <= promote_n:
                    changes[p.id] = i + 1
                elif relegate_n and rank > relegate_cut:
                    changes[p.id] = i - 1

        up = down = 0
        for p in profiles:
            if p.id in changes:
                new_div = changes[p.id]
                d = get_division(new_div)
                if new_div > p.division:
                    up += 1
                    Notification.push(
                        p.user,
                        f'Ascendiste a la liga {d["name"]}! Enhorabuena.',
                        icon=d["icon"],
                        url="/app/ligas/",
                    )
                else:
                    down += 1
                    Notification.push(
                        p.user,
                        f'Bajaste a la liga {d["name"]}. A recuperar el puesto!',
                        icon=d["icon"],
                        url="/app/ligas/",
                    )
                p.division = new_div
            p.weekly_xp = 0
            p.week_perfect = 0
            p.week_key = wk
            p.save(update_fields=["division", "weekly_xp", "week_perfect", "week_key"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Ligas actualizadas: {len(profiles)} perfiles, {up} ascensos, {down} descensos."
            )
        )
