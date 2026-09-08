"""Vistas: auth."""

from django.conf import settings

from ..security import honeypot_tripped, rate_limit, turnstile_ok
from .common import *  # noqa: F401,F403

# ---------- Autenticacion ----------


@rate_limit("register", limit=6, window=600)  # 6 registros / 10 min por IP
def register(request):
    if request.user.is_authenticated:
        return redirect("astro:ruta")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        bot = honeypot_tripped(request) or not turnstile_ok(request)
        if not bot and form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("astro:onboarding")  # a la bienvenida
        if bot:
            form.add_error(None, "No pudimos verificar que eres humano. Vuelve a intentarlo.")
    else:
        form = RegisterForm()
    return render(
        request,
        "astro/auth/register.html",
        {"form": form, "turnstile_sitekey": settings.TURNSTILE_SITEKEY},
    )


@rate_limit("login", limit=12, window=300)  # 12 intentos / 5 min por IP
def login_view(request):
    if request.user.is_authenticated:
        return redirect("astro:ruta")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if not honeypot_tripped(request) and form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get("next") or request.GET.get("next") or "astro:ruta")
        if honeypot_tripped(request):
            form.add_error(None, "No pudimos verificar que eres humano.")
    else:
        form = LoginForm(request)
    return render(
        request, "astro/auth/login.html", {"form": form, "next": request.GET.get("next", "")}
    )


def logout_view(request):
    logout(request)
    return redirect("astro:home")
