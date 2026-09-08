"""Vistas: gamification."""

from .common import *  # noqa: F401,F403


@login_required(login_url=LOGIN_URL)
def missions(request):
    items, _ = _build_missions(request.user)
    return render(
        request,
        "astro/app/missions.html",
        {
            "missions": items,
            "active_nav": "missions",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def open_chest(request):
    """Abre el cofre de racha pendiente y otorga su recompensa."""
    profile = _get_profile(request.user)
    if profile.pending_chest <= 0:
        messages.info(request, "No tienes cofres por abrir.")
        return redirect("astro:ruta")
    day = profile.pending_chest
    reward = dict(STREAK_REWARDS).get(day, 15)
    profile.add_coins(reward)
    freeze = 1 if day >= 7 else 0
    profile.streak_freezes += freeze
    profile.pending_chest = 0
    profile.save()
    extra = " y 1 congelador de racha" if freeze else ""
    messages.success(request, f"Cofre de {day} dias abierto: +{reward} Cosmos{extra}!")
    return redirect("astro:ruta")


@login_required(login_url=LOGIN_URL)
@require_POST
def claim_mission(request, key):
    items, wk = _build_missions(request.user)
    mission = next((m for m in items if m["key"] == key), None)
    if not mission:
        messages.error(request, "Mision no encontrada.")
    elif mission["claimed"]:
        messages.info(request, "Ya reclamaste esa mision.")
    elif not mission["done"]:
        messages.error(request, "Aun no completaste esa mision.")
    else:
        MissionClaim.objects.get_or_create(user=request.user, mission_key=key, week_key=wk)
        profile = _get_profile(request.user)
        profile.add_coins(mission["reward"])
        profile.save(update_fields=["coins"])
        messages.success(request, f'Mision completada: +{mission["reward"]} Cosmos.')
    return redirect("astro:missions")


@login_required(login_url=LOGIN_URL)
def league(request):
    wk = timezone.localdate().strftime("%G-%V")
    profile = _get_profile(request.user)
    div = get_division(profile.division)

    # Cohorte = todos los de tu division, ordenados por XP de esta semana
    cohort = list(Profile.objects.filter(division=profile.division).select_related("user"))
    for p in cohort:
        p.eff = _weekly_of(p, wk)
    cohort.sort(key=lambda p: (-p.eff, p.user.username.lower()))

    total = len(cohort)
    promote_n = 0 if div["is_top"] else LEAGUE_PROMOTE
    relegate_n = 0 if div["is_bottom"] else LEAGUE_RELEGATE
    # Solo tiene sentido zona de descenso si la cohorte es mayor que las dos zonas
    relegate_cut = (total - relegate_n) if total > promote_n + relegate_n else total

    rows, my_rank = [], None
    for i, p in enumerate(cohort, start=1):
        zone = "up" if i <= promote_n else ("down" if i > relegate_cut else "")
        if p.user_id == request.user.id:
            my_rank = i
        if i <= LEAGUE_SHOW or p.user_id == request.user.id:
            rows.append(
                {
                    "pos": i,
                    "p": p,
                    "eff": p.eff,
                    "zone": zone,
                    "me": p.user_id == request.user.id,
                    "rank": get_rank(p.xp),
                }
            )

    relegate_start = relegate_cut + 1 if relegate_n and total > promote_n + relegate_n else None
    return render(
        request,
        "astro/app/league.html",
        {
            "division": div,
            "rows": rows,
            "my_rank": my_rank,
            "my_weekly": _weekly_of(profile, wk),
            "total": total,
            "promote_n": promote_n,
            "relegate_n": relegate_n,
            "relegate_start": relegate_start,
            "active_nav": "league",
        },
    )


@login_required(login_url=LOGIN_URL)
def store(request):
    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=["hearts", "hearts_updated"])
    items = ShopItem.objects.filter(is_active=True)
    owned = set(Purchase.objects.filter(user=request.user).values_list("item__key", flat=True))
    return render(
        request,
        "astro/app/store.html",
        {
            "powerups": [i for i in items if i.effect != "frame"],
            "frames": [i for i in items if i.effect == "frame"],
            "owned": owned,
            "profile": profile,
            "hearts_max": HEARTS_MAX,
            "active_nav": "store",
        },
    )


@login_required(login_url=LOGIN_URL)
@require_POST
def buy_item(request, key):
    item = get_object_or_404(ShopItem, key=key, is_active=True)
    profile = _get_profile(request.user)

    if item.effect == "frame":
        if Purchase.objects.filter(user=request.user, item=item).exists():
            messages.info(request, f'Ya tienes "{item.name}".')
            return redirect("astro:store")

    if profile.coins < item.price:
        messages.error(request, f'Te faltan Cosmos para comprar "{item.name}".')
        return redirect("astro:store")

    if item.effect == "refill_hearts" and profile.hearts >= HEARTS_MAX:
        messages.info(request, "Ya tienes todas tus vidas.")
        return redirect("astro:store")

    profile.coins -= item.price
    if item.effect == "streak_freeze":
        profile.streak_freezes += 1
    elif item.effect == "double_xp":
        profile.double_xp_pending = True
    elif item.effect == "refill_hearts":
        profile.hearts = HEARTS_MAX
        profile.hearts_updated = timezone.now()
    elif item.effect == "frame":
        Purchase.objects.create(user=request.user, item=item)
        profile.frame = item.key  # lo equipa al comprarlo
    profile.save()
    messages.success(request, f'Compraste "{item.name}". Te quedan {profile.coins} Cosmos.')
    return redirect("astro:store")


@login_required(login_url=LOGIN_URL)
@require_POST
def equip_frame(request, key):
    profile = _get_profile(request.user)
    if key == "none":
        profile.frame = ""
        profile.save()
        messages.success(request, "Marco quitado.")
        return redirect("astro:store")
    item = get_object_or_404(ShopItem, key=key, effect="frame", is_active=True)
    if not Purchase.objects.filter(user=request.user, item=item).exists():
        messages.error(request, "No tienes ese marco.")
        return redirect("astro:store")
    profile.frame = item.key
    profile.save()
    messages.success(request, f'Marco "{item.name}" equipado.')
    return redirect("astro:store")
