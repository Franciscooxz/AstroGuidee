import time

from django.conf import settings

from .models import Notification, Profile

# Version de assets para cache-busting: en desarrollo cambia en cada arranque
# del servidor (para no ver CSS/JS cacheado); en produccion es estable.
_ASSET_VERSION = str(int(time.time())) if settings.DEBUG else "1"


def astro_profile(request):
    """Perfil del usuario + version de assets, disponibles en todas las plantillas."""
    ctx = {"ASSET_VERSION": _ASSET_VERSION}
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        ctx["astro_profile"] = profile
        ctx["unread_notifications"] = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
    return ctx
