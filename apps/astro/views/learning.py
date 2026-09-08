"""Vistas: learning."""

from ..security import rate_limit
from .common import *  # noqa: F401,F403

# ---------- App (requiere sesion) ----------


# Mapa de ruta = constelacion. Posiciones deterministas de cada estrella dentro
# de su unidad: patron de X (%) que zigzaguea sin pegarse a los bordes (para que
# las etiquetas no se corten) y una Y (px) con ritmo fijo. Las lineas que unen las
# estrellas las dibuja astro.js midiendo los centros (responsive).
# Patron 2D compacto (cumulo), no una columna. Cada bloque de 6 estrellas forma
# un racimo; los bloques siguientes se apilan debajo. X en % (lejos de bordes
# para que las etiquetas no se corten), desplazamiento Y en px dentro del bloque.
CST_XS = (30, 60, 44, 72, 26, 52)
CST_DY = (0, 40, 118, 152, 214, 250)
CST_BLOCK = 300  # alto de un bloque de 6 estrellas (px)
CST_TOP = 40


def _place_constellation(unit):
    lessons = unit["lessons"]
    maxy = 0
    for i, lesson in enumerate(lessons):
        block, k = divmod(i, len(CST_XS))
        lesson.cx = CST_XS[k]
        lesson.cy = CST_TOP + block * CST_BLOCK + CST_DY[k]
        maxy = max(maxy, lesson.cy)
    unit["h"] = maxy + 78


@login_required(login_url=LOGIN_URL)
def ruta(request):
    lessons = _ordered_lessons()
    status, completed = _lesson_status(request.user, lessons)

    # Agrupar por unidad conservando el orden
    units, current_unit = [], None
    current_lesson = None
    for lesson in lessons:
        lesson.status = status[lesson.id]
        if lesson.status == "current" and current_lesson is None:
            current_lesson = lesson
        if current_unit is None or current_unit["unit"].id != lesson.category_id:
            current_unit = {"unit": lesson.category, "lessons": [], "done": 0, "total": 0}
            units.append(current_unit)
        current_unit["lessons"].append(lesson)
        current_unit["total"] += 1
        if lesson.status == "completed":
            current_unit["done"] += 1

    for u in units:
        u["complete"] = u["total"] > 0 and u["done"] == u["total"]
        _place_constellation(u)

    total = len(lessons)
    done = len(completed)
    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=["hearts", "hearts_updated"])
    daily_done = _lessons_done_today(request.user)
    reviews_due = _due_reviews(request.user).count()
    mission_items, _ = _build_missions(request.user)
    missions_claimable = sum(1 for m in mission_items if m["claimable"])
    return render(
        request,
        "astro/app/ruta.html",
        {
            "units": units,
            "current_lesson": current_lesson,
            "reviews_due": reviews_due,
            "missions_claimable": missions_claimable,
            "pending_chest": profile.pending_chest,
            "chest_reward": dict(STREAK_REWARDS).get(profile.pending_chest, 0),
            "all_done": total > 0 and done == total,
            "total": total,
            "done": done,
            "pct": round(done / total * 100) if total else 0,
            "xp": profile.xp,
            "streak": profile.streak,
            "coins": profile.coins,
            "hearts": profile.hearts,
            "hearts_max": HEARTS_MAX,
            "next_heart": _next_heart_minutes(profile),
            "daily_done": min(daily_done, profile.daily_goal),
            "daily_goal": profile.daily_goal,
            "daily_met": daily_done >= profile.daily_goal,
            "active_nav": "ruta",
        },
    )


@login_required(login_url=LOGIN_URL)
def onboarding(request):
    profile = _get_profile(request.user)
    if request.method == "POST":
        profile.onboarded = True
        profile.save(update_fields=["onboarded"])
        return redirect("astro:ruta")
    if profile.onboarded:
        return redirect("astro:ruta")
    return render(request, "astro/app/onboarding.html", {})


@login_required(login_url=LOGIN_URL)
def lesson(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == "locked":
        return redirect("astro:ruta")

    cards = lesson_obj.cards.filter(is_active=True)
    is_completed = status.get(lesson_obj.id) == "completed"
    return render(
        request,
        "astro/app/lesson.html",
        {
            "lesson": lesson_obj,
            "cards": cards,
            "is_completed": is_completed,
            "has_quiz": lesson_obj.has_quiz,
        },
    )


@login_required(login_url=LOGIN_URL)
def quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == "locked":
        return redirect("astro:ruta")

    questions = list(lesson_obj.questions.filter(is_active=True).prefetch_related("options"))
    if not questions:
        return redirect("astro:lesson", slug=lesson_obj.slug)

    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=["hearts", "hearts_updated"])
    if profile.hearts < 1:
        return render(
            request,
            "astro/app/no_hearts.html",
            {
                "lesson": lesson_obj,
                "next_heart": _next_heart_minutes(profile),
                "coins": profile.coins,
            },
        )

    difficulty = lesson_obj.category.difficulty
    return render(
        request,
        "astro/app/quiz.html",
        {
            "lesson": lesson_obj,
            "questions": questions,
            "hearts": profile.hearts,
            "hearts_max": HEARTS_MAX,
            "difficulty": difficulty,
            "difficulty_name": lesson_obj.category.difficulty_name,
            "needed": _needed_correct(len(questions), difficulty),
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
@rate_limit("quiz", limit=30, window=60)  # anti-farmeo: 30 envios / min por IP
def finish_quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == "locked":
        return JsonResponse({"error": "locked"}, status=403)

    try:
        answers = json.loads(request.body or "{}").get("answers", {})
    except (ValueError, AttributeError):
        answers = {}

    questions = list(lesson_obj.questions.filter(is_active=True).prefetch_related("options"))
    total = len(questions)
    correct = 0
    for q in questions:
        val = answers.get(str(q.id), "")
        if q.qtype == "text":
            typed = _norm_text(str(val))
            accepted = [_norm_text(o.text) for o in q.options.all() if o.is_correct]
            ok = bool(typed) and typed in accepted
        else:
            chosen = str(val)
            ok = any(o.is_correct and str(o.id) == chosen for o in q.options.all())
        if ok:
            correct += 1
        _record_answer(request.user, q, ok)

    difficulty = lesson_obj.category.difficulty
    needed = _needed_correct(total, difficulty)
    passed = total > 0 and correct >= needed
    perfect = total > 0 and correct == total

    already_completed = LessonProgress.objects.filter(
        user=request.user, lesson=lesson_obj, completed=True
    ).exists()

    profile = _get_profile(request.user)
    _refill_hearts(profile)
    hearts_lost = min(total - correct, profile.hearts)
    profile.hearts -= hearts_lost

    xp_earned = 0
    coins_earned = 0
    doubled = False
    newly = []
    level_before = profile.xp // 100 + 1
    if passed:
        if perfect:
            profile.perfect_quizzes += 1
            profile.add_week_perfect()
        if not already_completed:
            xp_earned = correct * XP_PER_CORRECT + (XP_PERFECT_BONUS if perfect else 0)
            if profile.double_xp_pending:
                xp_earned *= 2
                profile.double_xp_pending = False
                doubled = True
            profile.add_xp(xp_earned)
            profile.add_weekly_xp(xp_earned)
            coins_earned = COINS_PER_LESSON + (COINS_PERFECT_BONUS if perfect else 0)
            profile.add_coins(coins_earned)
        profile.register_activity()
        _check_streak_chest(profile)
        profile.save()

        prog, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson_obj)
        if not prog.completed:
            prog.completed = True
            prog.completed_at = timezone.now()
            prog.save()
        _seed_reviews(request.user, lesson_obj)

        level_after = profile.xp // 100 + 1
        if level_after > level_before:
            Notification.push(
                request.user,
                f"¡Subiste al nivel {level_after}! Sigue así.",
                icon="star",
                url=reverse("astro:profile"),
            )

        newly = _award_achievements(request.user)

    # Meta diaria: si cumpliste la meta de hoy y no la habias cobrado, bono de Cosmos
    daily_bonus = 0
    today = timezone.localdate()
    done_today = _lessons_done_today(request.user)
    if passed and done_today >= profile.daily_goal and profile.daily_claimed != today:
        profile.daily_claimed = today
        profile.add_coins(DAILY_BONUS)
        daily_bonus = DAILY_BONUS
        Notification.push(
            request.user,
            f"Meta diaria cumplida! +{DAILY_BONUS} Cosmos.",
            icon="coin",
            url=reverse("astro:store"),
        )

    profile.save()  # persiste vidas, meta diaria y demas

    return JsonResponse(
        {
            "correct": correct,
            "total": total,
            "needed": needed,
            "passed": passed,
            "perfect": perfect,
            "xp_earned": xp_earned,
            "doubled": doubled,
            "coins_earned": coins_earned,
            "daily_bonus": daily_bonus,
            "hearts": profile.hearts,
            "hearts_lost": hearts_lost,
            "hearts_max": HEARTS_MAX,
            "total_xp": profile.xp,
            "total_coins": profile.coins,
            "streak": profile.streak,
            "newly_achievements": [{"name": a.name, "icon": a.icon} for a in newly],
        }
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def complete_lesson(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == "locked":
        return redirect("astro:ruta")

    prog, _created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson_obj)
    if not prog.completed:
        prog.completed = True
        prog.completed_at = timezone.now()
        prog.save()
        profile = _get_profile(request.user)
        profile.register_activity()
        _check_streak_chest(profile)
        profile.save()
        _seed_reviews(request.user, lesson_obj)
        _award_achievements(request.user)
    return redirect("astro:ruta")
