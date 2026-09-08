"""Vistas: public."""

from .common import *  # noqa: F401,F403

# ---------- Publico ----------


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured = categories.first()
    featured_cards = featured.cards.filter(is_active=True) if featured else []
    return render(
        request,
        "astro/home.html",
        {
            "categories": categories,
            "featured": featured,
            "featured_cards": featured_cards,
        },
    )


@login_required(login_url=LOGIN_URL)
def certificate(request, slug):
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return redirect("astro:ruta")
    last = (
        LessonProgress.objects.filter(user=request.user, lesson__in=lessons, completed=True)
        .order_by("-completed_at")
        .first()
    )
    exam = UnitExam.objects.filter(user=request.user, category=unit).first()
    return render(
        request,
        "astro/app/certificate.html",
        {
            "unit": unit,
            "date": last.completed_at if last else None,
            "n_lessons": len(lessons),
            "n_cards": unit.card_count,
            "exam": exam,
        },
    )


def public_certificate(request, username, slug):
    """Certificado verificable, visible sin sesion (para compartir)."""
    User = get_user_model()
    owner = get_object_or_404(User, username=username, is_active=True)
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(owner, unit)
    if not complete:
        raise Http404("Certificado no disponible")
    last = (
        LessonProgress.objects.filter(user=owner, lesson__in=lessons, completed=True)
        .order_by("-completed_at")
        .first()
    )
    exam = UnitExam.objects.filter(user=owner, category=unit).first()
    return render(
        request,
        "astro/public_certificate.html",
        {
            "owner": owner,
            "unit": unit,
            "date": last.completed_at if last else None,
            "n_lessons": len(lessons),
            "n_cards": unit.card_count,
            "exam": exam,
        },
    )


@login_required(login_url=LOGIN_URL)
def glossary(request):
    """Explorar/buscar todas las tarjetas del contenido (glosario libre)."""
    q = request.GET.get("q", "").strip()
    cards = Card.objects.filter(is_active=True, category__is_active=True).select_related(
        "category", "lesson"
    )
    if q:
        cards = cards.filter(
            Q(title__icontains=q)
            | Q(subtitle__icontains=q)
            | Q(summary__icontains=q)
            | Q(content__icontains=q)
            | Q(fun_fact__icontains=q)
        )
    cards = list(cards.order_by("category__order", "lesson__order", "order")[:120])
    return render(
        request,
        "astro/app/glossary.html",
        {
            "cards": cards,
            "q": q,
            "total": len(cards),
            "apod": _get_apod() if not q else None,  # hero solo sin busqueda
            "active_nav": "glossary",
        },
    )
