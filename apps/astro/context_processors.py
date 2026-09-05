from .models import Profile


def astro_profile(request):
    """Deja el perfil del usuario disponible en todas las plantillas (nav, avatar...)."""
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return {'astro_profile': profile}
    return {}
