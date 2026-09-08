"""Vistas: review_exam."""

from .common import *  # noqa: F401,F403


@login_required(login_url=LOGIN_URL)
def exam(request, slug):
    """Examen final de una unidad: todas sus preguntas, disponible al completarla."""
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return redirect("astro:ruta")
    questions = list(
        Question.objects.filter(lesson__in=lessons, is_active=True).prefetch_related("options")
    )
    if not questions:
        return redirect("astro:certificate", slug=unit.slug)
    return render(
        request,
        "astro/app/exam.html",
        {
            "unit": unit,
            "questions": questions,
            "needed": math.ceil(EXAM_PASS * len(questions)),
            "active_nav": "ruta",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_exam(request, slug):
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return JsonResponse({"error": "locked"}, status=403)

    try:
        answers = json.loads(request.body or "{}").get("answers", {})
    except (ValueError, AttributeError):
        answers = {}

    questions = list(
        Question.objects.filter(lesson__in=lessons, is_active=True).prefetch_related("options")
    )
    total = len(questions)
    correct = 0
    for q in questions:
        val = answers.get(str(q.id), "")
        ok = services.grade_question(q, val)
        if ok:
            correct += 1
        _record_answer(request.user, q, ok)

    pct = round(correct / total * 100) if total else 0
    passed = pct >= round(EXAM_PASS * 100)
    honors = pct >= EXAM_HONORS

    ex, _ = UnitExam.objects.get_or_create(user=request.user, category=unit)
    ex.attempts += 1
    ex.best_score = max(ex.best_score, pct)
    newly_passed = passed and not ex.passed
    bonus = 0
    if passed:
        ex.passed = True
        if not ex.passed_at:
            ex.passed_at = timezone.now()
    ex.save()

    if newly_passed:
        profile = _get_profile(request.user)
        bonus = EXAM_BONUS
        profile.add_coins(bonus)
        profile.save(update_fields=["coins"])
        Notification.push(
            request.user,
            f"Examen final de {unit.name} superado! +{bonus} Cosmos.",
            icon="trophy",
            url=reverse("astro:certificate", args=[unit.slug]),
        )

    return JsonResponse(
        {
            "correct": correct,
            "total": total,
            "pct": pct,
            "passed": passed,
            "honors": honors,
            "bonus": bonus,
            "best_score": ex.best_score,
            "cert_url": reverse("astro:certificate", args=[unit.slug]),
        }
    )


@login_required(login_url=LOGIN_URL)
def review(request):
    """Repaso inteligente: presenta las preguntas vencidas (repeticion espaciada)."""
    due = list(_due_reviews(request.user)[:REVIEW_BATCH])
    total_due = _due_reviews(request.user).count()
    next_item = (
        ReviewItem.objects.filter(user=request.user, due__gt=timezone.localdate())
        .order_by("due")
        .first()
    )
    total_items = ReviewItem.objects.filter(user=request.user).count()
    weak_available = QuestionStat.objects.filter(
        user=request.user, seen__gt=0, correct__lt=F("seen")
    ).exists()
    return render(
        request,
        "astro/app/review.html",
        {
            "items": due,
            "questions": [it.question for it in due],
            "total_due": total_due,
            "next_due": next_item.due if next_item else None,
            "total_items": total_items,
            "weak_available": weak_available,
            "active_nav": "review",
        },
    )


@login_required(login_url=LOGIN_URL)
def review_weak(request):
    """Practica dirigida: prioriza las preguntas donde mas fallas."""
    questions = _weak_questions(request.user)
    return render(
        request,
        "astro/app/review.html",
        {
            "items": questions,
            "questions": questions,
            "weak": True,
            "active_nav": "review",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_review(request):
    """Corrige una sesion de repaso: reprograma (SM-2) y acumula estadisticas.

    Califica las preguntas realmente enviadas, asi sirve tanto al repaso por
    vencimiento como al modo 'practicar temas flojos'.
    """
    try:
        answers = json.loads(request.body or "{}").get("answers", {})
    except (ValueError, AttributeError):
        answers = {}

    qids = [k for k in answers.keys()][:REVIEW_BATCH]
    questions = Question.objects.filter(id__in=qids, is_active=True).prefetch_related("options")
    correct = 0
    total = 0
    for q in questions:
        val = answers.get(str(q.id), "")
        ok = services.grade_question(q, val)
        item, _ = ReviewItem.objects.get_or_create(user=request.user, question=q)
        item.schedule(ok)
        item.save()
        _record_answer(request.user, q, ok)
        total += 1
        if ok:
            correct += 1

    xp_earned = correct * XP_PER_REVIEW
    profile = _get_profile(request.user)
    if xp_earned:
        profile.add_xp(xp_earned)
        profile.add_weekly_xp(xp_earned)
    if total:
        profile.register_activity()
        _check_streak_chest(profile)
    profile.save()

    return JsonResponse(
        {
            "correct": correct,
            "total": total,
            "xp_earned": xp_earned,
            "total_xp": profile.xp,
            "streak": profile.streak,
        }
    )
