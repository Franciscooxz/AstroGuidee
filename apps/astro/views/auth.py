"""Vistas: auth."""

from .common import *  # noqa: F401,F403

# ---------- Autenticacion ----------


def register(request):
    if request.user.is_authenticated:
        return redirect("astro:ruta")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("astro:onboarding")  # a la bienvenida
    else:
        form = RegisterForm()
    return render(request, "astro/auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("astro:ruta")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get("next") or request.GET.get("next") or "astro:ruta")
    else:
        form = LoginForm(request)
    return render(
        request, "astro/auth/login.html", {"form": form, "next": request.GET.get("next", "")}
    )


def logout_view(request):
    logout(request)
    return redirect("astro:home")
