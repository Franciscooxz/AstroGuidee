"""Vistas: learning."""

from ..models import CardProgress
from ..security import rate_limit
from .common import *  # noqa: F401,F403

# ---------- App (requiere sesion) ----------


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

    started_ids = set(
        LessonProgress.objects.filter(user=request.user, completed=False).values_list(
            "lesson_id", flat=True
        )
    )
    started_ids.update(
        CardProgress.objects.filter(
            user=request.user, known=True, card__lesson_id__isnull=False
        ).values_list("card__lesson_id", flat=True)
    )
    for i, u in enumerate(units, start=1):
        u["index"] = i
        u["complete"] = u["total"] > 0 and u["done"] == u["total"]
        u["pct"] = round(100 * u["done"] / u["total"]) if u["total"] else 0
        for n, lesson in enumerate(u["lessons"], start=1):
            lesson.n = n
            lesson.side = "left" if n % 2 else "right"
            lesson.started = lesson.id in started_ids

    current_index = next(
        (i for i, u in enumerate(units) if any(l.status == "current" for l in u["lessons"])),
        None,
    )
    if current_index is None and units:
        current_index = len(units) - 1 if all(u["complete"] for u in units) else 0
    for i, u in enumerate(units):
        if current_index is None:
            u["fold"] = "locked"
        elif i < current_index:
            u["fold"] = "done"
        elif i == current_index:
            u["fold"] = "current"
        elif i == current_index + 1:
            u["fold"] = "next"
        else:
            u["fold"] = "locked"
    featured = units[current_index] if current_index is not None else None
    earlier = [u for u in units if u["fold"] == "done"]
    upcoming = [u for u in units if u["fold"] in ("next", "locked")]

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
            "featured": featured,
            "earlier": earlier,
            "upcoming": upcoming,
            "current_lesson": current_lesson,
            "reviews_due": reviews_due,
            "can_practice": bool(
                reviews_due
                or ReviewItem.objects.filter(user=request.user).exists()
                or QuestionStat.objects.filter(
                    user=request.user, seen__gt=0, correct__lt=F("seen")
                ).exists()
            ),
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


def _can_open_lesson(request, lesson_obj):
    """La primera lección se puede ver sin cuenta. El resto pide sesión y desbloqueo."""
    first = _first_lesson()
    if not request.user.is_authenticated:
        return bool(first and lesson_obj.id == first.id)
    status, _ = _lesson_status(request.user)
    return status.get(lesson_obj.id) != "locked"


def lesson(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    if not _can_open_lesson(request, lesson_obj):
        if not request.user.is_authenticated:
            return redirect("astro:register")
        return redirect("astro:ruta")

    cards = lesson_obj.cards.filter(is_active=True)
    is_completed = False
    if request.user.is_authenticated:
        status, _ = _lesson_status(request.user)
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


def quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    if not _can_open_lesson(request, lesson_obj):
        if not request.user.is_authenticated:
            return redirect("astro:register")
        return redirect("astro:ruta")

    questions = list(lesson_obj.questions.filter(is_active=True).prefetch_related("options"))
    if not questions:
        return redirect("astro:lesson", slug=lesson_obj.slug)

    free_hearts = _is_first_unit(lesson_obj) or not request.user.is_authenticated
    hearts = 0
    if request.user.is_authenticated and not free_hearts:
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
        hearts = profile.hearts

    difficulty = lesson_obj.category.difficulty
    return render(
        request,
        "astro/app/quiz.html",
        {
            "lesson": lesson_obj,
            "questions": questions,
            "hearts": hearts,
            "hearts_max": HEARTS_MAX,
            "free_hearts": free_hearts,
            "difficulty": difficulty,
            "difficulty_name": lesson_obj.category.difficulty_name,
            "needed": _needed_correct(len(questions), difficulty),
        },
    )


def _clean_answers(raw):
    clean = {}
    if not isinstance(raw, dict):
        return clean
    for key, val in raw.items():
        if isinstance(val, (str, int)):
            clean[str(key)] = val
    return clean


@require_POST
@rate_limit("quiz", limit=30, window=60)  # anti-farmeo: 30 envios / min por IP
def finish_quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    try:
        raw = json.loads(request.body or "{}").get("answers", {})
    except (ValueError, AttributeError):
        raw = {}
    answers = _clean_answers(raw)

    if not request.user.is_authenticated:
        first = _first_lesson()
        if not first or lesson_obj.id != first.id:
            return JsonResponse({"error": "auth"}, status=401)
        request.session["guest_quiz"] = {"slug": lesson_obj.slug, "answers": answers}
        graded = _grade_lesson(lesson_obj, answers)
        graded.pop("questions", None)
        graded.update(
            {
                "saved": False,
                "signup_url": reverse("astro:register"),
                "xp_earned": 0,
                "coins_earned": 0,
                "daily_bonus": 0,
                "hearts_lost": 0,
                "hearts": 0,
                "hearts_max": HEARTS_MAX,
                "doubled": False,
                "streak": 0,
                "total_xp": 0,
                "total_coins": 0,
                "newly_achievements": [],
            }
        )
        return JsonResponse(graded)

    if not _can_open_lesson(request, lesson_obj):
        return JsonResponse({"error": "locked"}, status=403)

    return JsonResponse(_commit_quiz(request.user, lesson_obj, answers))


def claim_guest_quiz(request):
    """Si aprobó la primera lección sin cuenta, la guarda al entrar."""
    payload = request.session.pop("guest_quiz", None)
    if not payload or not request.user.is_authenticated:
        return
    lesson = Lesson.objects.filter(slug=payload.get("slug"), is_active=True).first()
    first = _first_lesson()
    if not lesson or not first or lesson.id != first.id:
        return
    _commit_quiz(request.user, lesson, _clean_answers(payload.get("answers")))


def _grade_lesson(lesson_obj, answers):
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
    difficulty = lesson_obj.category.difficulty
    needed = _needed_correct(total, difficulty)
    return {
        "correct": correct,
        "total": total,
        "needed": needed,
        "passed": total > 0 and correct >= needed,
        "perfect": total > 0 and correct == total,
        "questions": questions,
    }


def _commit_quiz(user, lesson_obj, answers):
    graded = _grade_lesson(lesson_obj, answers)
    questions = graded.pop("questions")
    correct = graded["correct"]
    total = graded["total"]
    passed = graded["passed"]
    perfect = graded["perfect"]
    for q in questions:
        val = answers.get(str(q.id), "")
        if q.qtype == "text":
            typed = _norm_text(str(val))
            accepted = [_norm_text(o.text) for o in q.options.all() if o.is_correct]
            ok = bool(typed) and typed in accepted
        else:
            ok = any(o.is_correct and str(o.id) == str(val) for o in q.options.all())
        _record_answer(user, q, ok)

    already_completed = LessonProgress.objects.filter(
        user=user, lesson=lesson_obj, completed=True
    ).exists()

    profile = _get_profile(user)
    _refill_hearts(profile)
    hearts_lost = 0
    if not _is_first_unit(lesson_obj):
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

        prog, _ = LessonProgress.objects.get_or_create(user=user, lesson=lesson_obj)
        if not prog.completed:
            prog.completed = True
            prog.completed_at = timezone.now()
            prog.save()
        _seed_reviews(user, lesson_obj)

        level_after = profile.xp // 100 + 1
        if level_after > level_before:
            Notification.push(
                user,
                f"¡Subiste al nivel {level_after}! Sigue así.",
                icon="star",
                url=reverse("astro:profile"),
            )

        newly = _award_achievements(user)

    # Meta diaria: si cumpliste la meta de hoy y no la habias cobrado, bono de Cosmos
    daily_bonus = 0
    today = timezone.localdate()
    done_today = _lessons_done_today(user)
    if passed and done_today >= profile.daily_goal and profile.daily_claimed != today:
        profile.daily_claimed = today
        profile.add_coins(DAILY_BONUS)
        daily_bonus = DAILY_BONUS
        Notification.push(
            user,
            f"Meta diaria cumplida! +{DAILY_BONUS} Cosmos.",
            icon="coin",
            url=reverse("astro:store"),
        )

    profile.save()  # persiste vidas, meta diaria y demas

    return {
            "correct": correct,
            "total": total,
            "needed": graded["needed"],
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
