"""Vistas: account."""

from .common import *  # noqa: F401,F403


@login_required(login_url=LOGIN_URL)
def profile(request):
    p = _get_profile(request.user)
    total_lessons = Lesson.objects.filter(is_active=True, category__is_active=True).count()
    done = LessonProgress.objects.filter(
        user=request.user, completed=True, lesson__is_active=True
    ).count()

    level = p.xp // 100 + 1
    xp_in_level = p.xp % 100

    earned_ids = set(
        UserAchievement.objects.filter(user=request.user).values_list("achievement_id", flat=True)
    )
    achievements = [
        {"a": a, "earned": a.id in earned_ids} for a in Achievement.objects.filter(is_active=True)
    ]
    return render(
        request,
        "astro/app/profile.html",
        {
            "profile": p,
            "total_lessons": total_lessons,
            "done_lessons": done,
            "pct": round(done / total_lessons * 100) if total_lessons else 0,
            "level": level,
            "xp_in_level": xp_in_level,
            "xp_to_next": 100 - xp_in_level,
            "rank": get_rank(p.xp),
            "achievements": achievements,
            "earned_count": len(earned_ids),
            "certificates": _user_certificates(request.user),
            "active_nav": "profile",
        },
    )


@login_required(login_url=LOGIN_URL)
def stats(request):
    """Estadisticas personales del usuario: precision, temas flojos, actividad, racha."""
    from django.db.models import Sum

    user = request.user
    p = _get_profile(user)

    # Precision por unidad (a partir de QuestionStat)
    agg = {
        row["question__lesson__category"]: row
        for row in QuestionStat.objects.filter(user=user)
        .values("question__lesson__category")
        .annotate(seen=Sum("seen"), correct=Sum("correct"))
    }

    # Progreso (lecciones completadas) por unidad
    done_ids = set(
        LessonProgress.objects.filter(user=user, completed=True).values_list("lesson_id", flat=True)
    )

    units = []
    total_seen = total_correct = 0
    for unit in Category.objects.filter(is_active=True).order_by("order"):
        lessons = list(unit.lessons.filter(is_active=True))
        row = agg.get(unit.id)
        seen = row["seen"] if row else 0
        corr = row["correct"] if row else 0
        total_seen += seen
        total_correct += corr
        done = sum(1 for l in lessons if l.id in done_ids)
        units.append(
            {
                "unit": unit,
                "seen": seen,
                "accuracy": round(corr / seen * 100) if seen else None,
                "done": done,
                "total": len(lessons),
                "progress": round(done / len(lessons) * 100) if lessons else 0,
            }
        )

    global_acc = round(total_correct / total_seen * 100) if total_seen else None
    # Temas mas flojos: unidades con precision mas baja (con datos suficientes)
    weak = sorted(
        [u for u in units if u["seen"] >= 3 and u["accuracy"] is not None],
        key=lambda u: u["accuracy"],
    )[:3]

    # Actividad: lecciones completadas por dia en los ultimos 14 dias
    today = timezone.localdate()
    start = today - timedelta(days=13)
    per_day = {}
    for d in LessonProgress.objects.filter(
        user=user, completed=True, completed_at__date__gte=start
    ).values_list("completed_at", flat=True):
        key = timezone.localtime(d).date() if timezone.is_aware(d) else d.date()
        per_day[key] = per_day.get(key, 0) + 1
    activity = [
        {"date": start + timedelta(days=i), "count": per_day.get(start + timedelta(days=i), 0)}
        for i in range(14)
    ]
    act_max = max((a["count"] for a in activity), default=0)

    level = p.xp // 100 + 1
    return render(
        request,
        "astro/app/stats.html",
        {
            "profile": p,
            "level": level,
            "rank": get_rank(p.xp),
            "global_acc": global_acc,
            "total_seen": total_seen,
            "units": units,
            "weak": weak,
            "activity": activity,
            "act_max": act_max,
            "active_nav": "stats",
        },
    )


@login_required(login_url=LOGIN_URL)
def settings_view(request):
    profile = _get_profile(request.user)
    pw_form = StyledPasswordChangeForm(request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            email = request.POST.get("email", "").strip()
            avatar = request.POST.get("avatar", "").strip()
            valid = True
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    messages.error(request, "El correo no es valido.")
                    valid = False
            if valid:
                request.user.email = email
                request.user.save(update_fields=["email"])
                profile.avatar = avatar if avatar in AVATAR_ICONS else ""
                profile.save(update_fields=["avatar"])
                messages.success(request, "Perfil actualizado.")
                return redirect("astro:settings")
        elif "save_goal" in request.POST:
            try:
                goal = int(request.POST.get("daily_goal", 1))
            except (TypeError, ValueError):
                goal = 1
            if goal in [g for g, _ in DAILY_GOALS]:
                profile.daily_goal = goal
                profile.save(update_fields=["daily_goal"])
                messages.success(request, "Meta diaria actualizada.")
                return redirect("astro:settings")
        elif "change_password" in request.POST:
            pw_form = StyledPasswordChangeForm(request.user, request.POST)
            if pw_form.is_valid():
                user = pw_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Contrasena cambiada correctamente.")
                return redirect("astro:settings")

    return render(
        request,
        "astro/app/settings.html",
        {
            "profile": profile,
            "pw_form": pw_form,
            "avatar_icons": AVATAR_ICONS,
            "daily_goals": DAILY_GOALS,
            "active_nav": "profile",
        },
    )


@login_required(login_url=LOGIN_URL)
def notifications(request):
    """Centro de notificaciones: lista el historial y marca todo como leido."""
    qs = Notification.objects.filter(user=request.user)
    items = list(qs[:100])
    qs.filter(is_read=False).update(is_read=True)
    return render(
        request,
        "astro/app/notifications.html",
        {
            "items": items,
            "active_nav": "notifications",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def report_question(request, qid):
    """Registra un reporte del usuario sobre una pregunta (posible error)."""
    question = get_object_or_404(Question, id=qid)
    try:
        reason = json.loads(request.body or "{}").get("reason", "otro")
    except (ValueError, AttributeError):
        reason = "otro"
    valid = {k for k, _ in QuestionReport.REASONS}
    if reason not in valid:
        reason = "otro"
    QuestionReport.objects.update_or_create(
        user=request.user, question=question, defaults={"reason": reason, "resolved": False}
    )
    return JsonResponse({"ok": True})


@login_required(login_url=LOGIN_URL)
@require_POST
def clear_notifications(request):
    """Borra todo el historial de notificaciones del usuario."""
    Notification.objects.filter(user=request.user).delete()
    messages.success(request, "Notificaciones borradas.")
    return redirect("astro:notifications")
