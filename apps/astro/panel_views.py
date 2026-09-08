from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Achievement,
    Card,
    Category,
    Lesson,
    LessonProgress,
    Notification,
    Profile,
    Question,
    QuestionReport,
    QuestionStat,
    ShopItem,
    UserAchievement,
)
from .panel_forms import (
    AchievementForm,
    CardForm,
    LessonForm,
    OptionFormSet,
    QuestionForm,
    ShopItemForm,
    UnitForm,
)

LOGIN = "astro:login"
User = get_user_model()


# ---------- Inicio ----------


@staff_member_required(login_url=LOGIN)
def dashboard(request):
    return render(
        request,
        "astro/panel/dashboard.html",
        {
            "n_units": Category.objects.count(),
            "n_lessons": Lesson.objects.count(),
            "n_cards": Card.objects.count(),
            "n_questions": Question.objects.count(),
            "n_users": User.objects.count(),
            "active": "inicio",
        },
    )


# ---------- Estadisticas ----------


@staff_member_required(login_url=LOGIN)
def stats(request):
    User = get_user_model()
    week_ago = timezone.localdate() - timedelta(days=7)

    lessons = list(
        Lesson.objects.filter(is_active=True)
        .annotate(completions=Count("progress", filter=Q(progress__completed=True)))
        .select_related("category")
    )
    top_lessons = sorted(lessons, key=lambda l: l.completions, reverse=True)[:6]
    hardest = sorted(lessons, key=lambda l: l.completions)[:6]

    return render(
        request,
        "astro/panel/stats.html",
        {
            "n_users": User.objects.count(),
            "active_week": Profile.objects.filter(last_active__gte=week_ago).count(),
            "total_completions": LessonProgress.objects.filter(completed=True).count(),
            "total_xp": Profile.objects.aggregate(s=Sum("xp"))["s"] or 0,
            "total_achievements": UserAchievement.objects.count(),
            "perfect_quizzes": Profile.objects.aggregate(s=Sum("perfect_quizzes"))["s"] or 0,
            "top_lessons": top_lessons,
            "hardest": hardest,
            "active": "stats",
        },
    )


# ---------- Calidad (reportes) ----------


@staff_member_required(login_url=LOGIN)
def quality(request):
    """Preguntas reportadas por los usuarios (posibles errores)."""
    reports = (
        QuestionReport.objects.filter(resolved=False)
        .select_related("question", "question__lesson", "user")
        .order_by("-created_at")
    )
    grouped = {}
    for r in reports:
        g = grouped.setdefault(
            r.question_id, {"question": r.question, "count": 0, "reasons": {}, "last": r.created_at}
        )
        g["count"] += 1
        label = r.get_reason_display()
        g["reasons"][label] = g["reasons"].get(label, 0) + 1
    reported = sorted(grouped.values(), key=lambda g: g["count"], reverse=True)

    # Preguntas mas falladas (precision agregada de todos los usuarios)
    MIN_SEEN = 5
    agg = list(
        QuestionStat.objects.values("question")
        .annotate(seen=Sum("seen"), correct=Sum("correct"))
        .filter(seen__gte=MIN_SEEN)
    )
    for a in agg:
        a["acc"] = round(a["correct"] / a["seen"] * 100) if a["seen"] else 0
    lowest = sorted(agg, key=lambda a: a["acc"])[:15]
    qmap = Question.objects.select_related("lesson").in_bulk([a["question"] for a in lowest])
    hardest = [
        {"question": qmap[a["question"]], "acc": a["acc"], "seen": a["seen"]}
        for a in lowest
        if a["question"] in qmap
    ]

    return render(
        request,
        "astro/panel/quality.html",
        {
            "reported": reported,
            "n_reports": reports.count(),
            "hardest": hardest,
            "min_seen": MIN_SEEN,
            "active": "calidad",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def resolve_reports(request, qid):
    """Marca como resueltos todos los reportes de una pregunta."""
    QuestionReport.objects.filter(question_id=qid).update(resolved=True)
    messages.success(request, "Reportes marcados como resueltos.")
    return redirect("gestion:quality")


# ---------- Anuncios ----------


@staff_member_required(login_url=LOGIN)
def announcements(request):
    """Envia una notificacion (anuncio) a todos los usuarios activos."""
    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        icon = (request.POST.get("icon") or "rocket").strip()
        if not text:
            messages.error(request, "Escribe el texto del anuncio.")
        else:
            users = User.objects.filter(is_active=True)
            Notification.objects.bulk_create(
                [Notification(user=u, text=text[:250], icon=icon) for u in users]
            )
            messages.success(request, f"Anuncio enviado a {users.count()} usuarios.")
            return redirect("gestion:announcements")

    recent = Notification.objects.filter(url="").values("text", "icon").order_by("-created_at")[:20]
    # Anuncios recientes (agrupados por texto): mostramos los ultimos distintos
    seen, distinct = set(), []
    for n in recent:
        if n["text"] not in seen:
            seen.add(n["text"])
            distinct.append(n)
    return render(
        request,
        "astro/panel/announcements.html",
        {
            "recent": distinct,
            "icons": ["rocket", "star", "trophy", "coin", "heart", "galaxy", "orbit"],
            "active": "anuncios",
        },
    )


# ---------- Unidades ----------


@staff_member_required(login_url=LOGIN)
def units(request):
    return render(
        request,
        "astro/panel/units_list.html",
        {
            "units": Category.objects.all(),
            "active": "unidades",
        },
    )


@staff_member_required(login_url=LOGIN)
def unit_edit(request, pk=None):
    obj = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == "POST":
        form = UnitForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("gestion:units")
    else:
        form = UnitForm(instance=obj)
    return render(
        request,
        "astro/panel/form.html",
        {
            "form": form,
            "title": "Editar unidad" if obj else "Nueva unidad",
            "back": "gestion:units",
            "active": "unidades",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def unit_delete(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect("gestion:units")


# ---------- Lecciones ----------


@staff_member_required(login_url=LOGIN)
def lessons(request):
    return render(
        request,
        "astro/panel/lessons_list.html",
        {
            "lessons": Lesson.objects.select_related("category").all(),
            "active": "lecciones",
        },
    )


@staff_member_required(login_url=LOGIN)
def lesson_edit(request, pk=None):
    obj = get_object_or_404(Lesson, pk=pk) if pk else None
    if request.method == "POST":
        form = LessonForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("gestion:lessons")
    else:
        form = LessonForm(instance=obj)
    return render(
        request,
        "astro/panel/form.html",
        {
            "form": form,
            "title": "Editar leccion" if obj else "Nueva leccion",
            "back": "gestion:lessons",
            "active": "lecciones",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def lesson_delete(request, pk):
    get_object_or_404(Lesson, pk=pk).delete()
    return redirect("gestion:lessons")


# ---------- Tarjetas ----------


@staff_member_required(login_url=LOGIN)
def cards(request):
    qs = Card.objects.select_related("lesson", "category").all()
    lesson_id = request.GET.get("lesson")
    if lesson_id:
        qs = qs.filter(lesson_id=lesson_id)
    return render(
        request,
        "astro/panel/cards_list.html",
        {
            "cards": qs,
            "all_lessons": Lesson.objects.select_related("category").all(),
            "lesson_filter": lesson_id,
            "active": "tarjetas",
        },
    )


@staff_member_required(login_url=LOGIN)
def card_edit(request, pk=None):
    obj = get_object_or_404(Card, pk=pk) if pk else None
    if request.method == "POST":
        form = CardForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("gestion:cards")
    else:
        form = CardForm(instance=obj)
    return render(
        request,
        "astro/panel/form.html",
        {
            "form": form,
            "title": "Editar tarjeta" if obj else "Nueva tarjeta",
            "back": "gestion:cards",
            "active": "tarjetas",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def card_delete(request, pk):
    get_object_or_404(Card, pk=pk).delete()
    return redirect("gestion:cards")


# ---------- Quizzes (preguntas) ----------


@staff_member_required(login_url=LOGIN)
def questions(request):
    qs = Question.objects.select_related("lesson", "lesson__category").all()
    return render(
        request,
        "astro/panel/questions_list.html",
        {
            "questions": qs,
            "active": "quizzes",
        },
    )


@staff_member_required(login_url=LOGIN)
def question_edit(request, pk=None):
    obj = get_object_or_404(Question, pk=pk) if pk else None
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=obj)
        formset = OptionFormSet(request.POST, instance=obj)
        if form.is_valid() and formset.is_valid():
            question = form.save()
            formset.instance = question
            formset.save()
            return redirect("gestion:questions")
    else:
        form = QuestionForm(instance=obj)
        formset = OptionFormSet(instance=obj)
    return render(
        request,
        "astro/panel/question_form.html",
        {
            "form": form,
            "formset": formset,
            "title": "Editar pregunta" if obj else "Nueva pregunta",
            "active": "quizzes",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def question_delete(request, pk):
    get_object_or_404(Question, pk=pk).delete()
    return redirect("gestion:questions")


# ---------- Tienda ----------


@staff_member_required(login_url=LOGIN)
def shop(request):
    return render(
        request,
        "astro/panel/shop_list.html",
        {
            "items": ShopItem.objects.all(),
            "active": "tienda",
        },
    )


@staff_member_required(login_url=LOGIN)
def shop_edit(request, pk=None):
    obj = get_object_or_404(ShopItem, pk=pk) if pk else None
    if request.method == "POST":
        form = ShopItemForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("gestion:shop")
    else:
        form = ShopItemForm(instance=obj)
    return render(
        request,
        "astro/panel/form.html",
        {
            "form": form,
            "title": "Editar articulo" if obj else "Nuevo articulo",
            "back": "gestion:shop",
            "active": "tienda",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def shop_delete(request, pk):
    get_object_or_404(ShopItem, pk=pk).delete()
    return redirect("gestion:shop")


# ---------- Logros ----------


@staff_member_required(login_url=LOGIN)
def achievements(request):
    return render(
        request,
        "astro/panel/achievements_list.html",
        {
            "items": Achievement.objects.all(),
            "active": "logros",
        },
    )


@staff_member_required(login_url=LOGIN)
def achievement_edit(request, pk=None):
    obj = get_object_or_404(Achievement, pk=pk) if pk else None
    if request.method == "POST":
        form = AchievementForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("gestion:achievements")
    else:
        form = AchievementForm(instance=obj)
    return render(
        request,
        "astro/panel/form.html",
        {
            "form": form,
            "title": "Editar logro" if obj else "Nuevo logro",
            "back": "gestion:achievements",
            "active": "logros",
        },
    )


@staff_member_required(login_url=LOGIN)
@require_POST
def achievement_delete(request, pk):
    get_object_or_404(Achievement, pk=pk).delete()
    return redirect("gestion:achievements")
