"""Vistas: social."""

from .common import *  # noqa: F401,F403


@login_required(login_url=LOGIN_URL)
def pub_profile(request, username):
    """Perfil publico de otro usuario, con boton de seguir."""
    User = get_user_model()
    target = get_object_or_404(User, username=username, is_active=True)
    if target == request.user:
        return redirect("astro:profile")
    stats = _user_public_stats(target)
    stats["is_following"] = Follow.objects.filter(follower=request.user, following=target).exists()
    stats["followers"] = Follow.objects.filter(following=target).count()
    stats["following"] = Follow.objects.filter(follower=target).count()
    stats["active_nav"] = "friends"
    return render(request, "astro/app/pub_profile.html", stats)


@login_required(login_url=LOGIN_URL)
@require_POST
def follow_toggle(request, username):
    User = get_user_model()
    target = get_object_or_404(User, username=username, is_active=True)
    if target != request.user:
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if created:
            Notification.push(
                target,
                f"{request.user.username} te empezo a seguir.",
                icon="user",
                url=reverse("astro:pub_profile", args=[request.user.username]),
            )
        else:
            obj.delete()
    return redirect("astro:pub_profile", username=username)


@login_required(login_url=LOGIN_URL)
def friends(request):
    """Amigos: a quienes sigues + clasificacion semanal entre amigos."""
    wk = timezone.localdate().strftime("%G-%V")
    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
    )
    following = [
        _user_public_stats(p.user)
        for p in Profile.objects.filter(user_id__in=following_ids).select_related("user")
    ]
    following.sort(key=lambda s: -s["profile"].xp)

    # Clasificacion semanal: amigos + tu, por XP de la semana
    board_profiles = list(
        Profile.objects.filter(user_id__in=following_ids + [request.user.id]).select_related("user")
    )
    for p in board_profiles:
        p.eff = _weekly_of(p, wk)
    board_profiles.sort(key=lambda p: (-p.eff, p.user.username.lower()))
    board = [
        {"pos": i, "p": p, "me": p.user_id == request.user.id, "rank": get_rank(p.xp)}
        for i, p in enumerate(board_profiles, start=1)
    ]

    return render(
        request,
        "astro/app/friends.html",
        {
            "following": following,
            "board": board,
            "n_following": len(following_ids),
            "n_followers": Follow.objects.filter(following=request.user).count(),
            "active_nav": "friends",
        },
    )


@login_required(login_url=LOGIN_URL)
def duels(request):
    """Lista de duelos: por jugar, pendientes y terminados."""
    mine = list(
        Duel.objects.filter(Q(challenger=request.user) | Q(opponent=request.user)).select_related(
            "challenger", "opponent"
        )[:40]
    )
    to_play, pending, done = [], [], []
    for d in mine:
        role = _duel_role(d, request.user)
        my_done = d.challenger_done if role == "challenger" else d.opponent_done
        rival = d.opponent if role == "challenger" else d.challenger
        my_score = d.challenger_score if role == "challenger" else d.opponent_score
        rival_score = d.opponent_score if role == "challenger" else d.challenger_score
        info = {
            "d": d,
            "rival": rival,
            "my_score": my_score,
            "rival_score": rival_score,
            "won": d.winner_id == request.user.id,
            "tie": d.status == "complete" and d.winner_id is None,
        }
        if not my_done:
            to_play.append(info)
        elif d.status != "complete":
            pending.append(info)
        else:
            done.append(info)
    return render(
        request,
        "astro/app/duels.html",
        {
            "to_play": to_play,
            "pending": pending,
            "done": done,
            "active_nav": "duels",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def create_duel(request, username):
    """Reta a otro usuario: crea el duelo y lleva al retador a jugar."""
    User = get_user_model()
    target = get_object_or_404(User, username=username, is_active=True)
    if target == request.user:
        return redirect("astro:duels")
    ids = list(Question.objects.filter(is_active=True).values_list("id", flat=True))
    if len(ids) < DUEL_QUESTIONS:
        messages.error(request, "No hay suficientes preguntas para un duelo.")
        return redirect("astro:pub_profile", username=username)
    chosen = random.sample(ids, DUEL_QUESTIONS)
    duel = Duel.objects.create(challenger=request.user, opponent=target, question_ids=chosen)
    Notification.push(
        target,
        f"{request.user.username} te reto a un duelo!",
        icon="flame",
        url=reverse("astro:duels"),
    )
    return redirect("astro:play_duel", pk=duel.id)


@login_required(login_url=LOGIN_URL)
def play_duel(request, pk):
    duel = get_object_or_404(Duel, pk=pk)
    role = _duel_role(duel, request.user)
    if not role:
        return redirect("astro:duels")
    my_done = duel.challenger_done if role == "challenger" else duel.opponent_done
    if my_done:
        return redirect("astro:duels")
    rival = duel.opponent if role == "challenger" else duel.challenger
    return render(
        request,
        "astro/app/duel_play.html",
        {
            "duel": duel,
            "rival": rival,
            "questions": _duel_questions(duel),
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_duel(request, pk):
    duel = get_object_or_404(Duel, pk=pk)
    role = _duel_role(duel, request.user)
    if not role:
        return JsonResponse({"error": "forbidden"}, status=403)
    my_done = duel.challenger_done if role == "challenger" else duel.opponent_done
    if my_done:
        return JsonResponse({"error": "done"}, status=400)

    try:
        answers = json.loads(request.body or "{}").get("answers", {})
    except (ValueError, AttributeError):
        answers = {}

    correct = 0
    for q in _duel_questions(duel):
        val = answers.get(str(q.id), "")
        ok = services.grade_question(q, val)
        if ok:
            correct += 1
        _record_answer(request.user, q, ok)

    if role == "challenger":
        duel.challenger_score = correct
        duel.challenger_done = True
    else:
        duel.opponent_score = correct
        duel.opponent_done = True

    both = duel.challenger_done and duel.opponent_done
    if both and duel.status != "complete":
        duel.status = "complete"
        duel.completed_at = timezone.now()
    duel.save()

    result = {"my_score": correct, "total": len(duel.question_ids), "both_done": both}
    if both:
        winner = duel.winner_id
        result["outcome"] = (
            "tie" if winner is None else ("win" if winner == request.user.id else "lose")
        )
        result["rival_score"] = (
            duel.opponent_score if role == "challenger" else duel.challenger_score
        )
        # Notificar a ambos
        c, o = duel.challenger, duel.opponent
        if winner is None:
            Notification.push(
                c, f"Empate en tu duelo con {o.username}.", icon="flame", url=reverse("astro:duels")
            )
            Notification.push(
                o, f"Empate en tu duelo con {c.username}.", icon="flame", url=reverse("astro:duels")
            )
        else:
            win_u = c if winner == c.id else o
            lose_u = o if winner == c.id else c
            Notification.push(
                win_u,
                f"Ganaste el duelo contra {lose_u.username}!",
                icon="trophy",
                url=reverse("astro:duels"),
            )
            Notification.push(
                lose_u,
                f"Perdiste el duelo contra {win_u.username}. Revancha?",
                icon="flame",
                url=reverse("astro:duels"),
            )
    return JsonResponse(result)
