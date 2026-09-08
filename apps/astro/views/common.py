import json
import math
import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import F, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .. import services
from ..forms import LoginForm, RegisterForm, StyledPasswordChangeForm
from ..models import (
    Achievement,
    Card,
    Category,
    Duel,
    Follow,
    Lesson,
    LessonProgress,
    MissionClaim,
    Notification,
    Profile,
    Purchase,
    Question,
    QuestionReport,
    QuestionStat,
    ReviewItem,
    ShopItem,
    UnitExam,
    UserAchievement,
)

LOGIN_URL = "astro:login"
AVATAR_ICONS = [
    "orbit",
    "sun",
    "earth",
    "saturn",
    "galaxy",
    "blackhole",
    "star",
    "rocket",
    "atom",
    "planet",
    "coin",
    "flame",
]
XP_PER_CORRECT = 10
XP_PERFECT_BONUS = 20
COINS_PER_LESSON = 5
COINS_PERFECT_BONUS = 5
DAILY_GOAL = 1  # meta diaria por defecto (lecciones)
DAILY_GOALS = [  # opciones configurables: (lecciones, etiqueta)
    (1, "Casual"),
    (2, "Constante"),
    (3, "En serio"),
    (5, "Intenso"),
]
DAILY_BONUS = 15  # Cosmos de recompensa al cumplirla
HEARTS_MAX = 5  # vidas maximas
HEART_REFILL_MIN = 30  # minutos para recuperar 1 vida
XP_PER_REVIEW = 3  # XP por cada repaso acertado
REVIEW_BATCH = 15  # preguntas maximas por sesion de repaso

# Logica de dominio (calificacion, estadistica, umbrales) en services.py.
# Se mantienen los nombres privados como alias para no tocar las llamadas.
PASS_RATIO = services.PASS_RATIO
_pass_ratio = services.pass_ratio
_needed_correct = services.needed_correct
_record_answer = services.record_answer


def _seed_reviews(user, lesson):
    """Crea items de repaso para las preguntas de una leccion recien completada."""
    qs = lesson.questions.filter(is_active=True)
    existing = set(
        ReviewItem.objects.filter(user=user, question__in=qs).values_list("question_id", flat=True)
    )
    nuevos = [
        ReviewItem(user=user, question=q, due=timezone.localdate() + timedelta(days=1))
        for q in qs
        if q.id not in existing
    ]
    if nuevos:
        ReviewItem.objects.bulk_create(nuevos)


def _due_reviews(user):
    """Items de repaso vencidos (hoy o antes) del usuario, con la pregunta y opciones."""
    return (
        ReviewItem.objects.filter(
            user=user, due__lte=timezone.localdate(), question__is_active=True
        )
        .select_related("question", "question__lesson")
        .prefetch_related("question__options")
    )


def _refill_hearts(profile):
    """Recupera vidas segun el tiempo transcurrido (1 cada HEART_REFILL_MIN)."""
    now = timezone.now()
    if profile.hearts >= HEARTS_MAX:
        profile.hearts_updated = now
        return profile
    last = profile.hearts_updated or now
    gained = int((now - last).total_seconds() // 60 // HEART_REFILL_MIN)
    if gained > 0:
        profile.hearts = min(HEARTS_MAX, profile.hearts + gained)
        profile.hearts_updated = (
            now
            if profile.hearts >= HEARTS_MAX
            else last + timedelta(minutes=gained * HEART_REFILL_MIN)
        )
        if profile.hearts >= HEARTS_MAX:
            Notification.push(
                profile.user,
                "Tus vidas se recargaron al máximo. ¡A seguir aprendiendo!",
                icon="heart",
                url=reverse("astro:ruta"),
            )
    return profile


def _next_heart_minutes(profile):
    """Minutos aproximados hasta recuperar la proxima vida (0 si estan al maximo)."""
    if profile.hearts >= HEARTS_MAX or not profile.hearts_updated:
        return 0
    nxt = profile.hearts_updated + timedelta(minutes=HEART_REFILL_MIN)
    return max(0, int(round((nxt - timezone.now()).total_seconds() / 60)))


# Divisiones de liga (ascendentes): (key, nombre, color, icono). Distintas de RANKS.
DIVISIONS = [
    ("cometa", "Cometa", "#8ea2ff", "rocket"),
    ("luna", "Luna", "#c0c8d8", "planet"),
    ("estrella", "Estrella", "#f5b301", "star"),
    ("nebulosa", "Nebulosa", "#b18bff", "orbit"),
    ("galaxia", "Galaxia", "#4f7cff", "galaxy"),
    ("cosmos", "Cosmos", "#6ee7ff", "sun"),
]
# Misiones semanales: metric in {xp, lessons, streak, perfect}. reward = Cosmos.
MISSIONS = [
    {
        "key": "xp150",
        "name": "Coleccionista de XP",
        "desc": "Gana 150 XP esta semana",
        "icon": "star",
        "metric": "xp",
        "target": 150,
        "reward": 20,
    },
    {
        "key": "lessons5",
        "name": "Maratón de lecciones",
        "desc": "Completa 5 lecciones esta semana",
        "icon": "cards",
        "metric": "lessons",
        "target": 5,
        "reward": 25,
    },
    {
        "key": "perfect3",
        "name": "Sin fallos",
        "desc": "Consigue 3 quizzes perfectos esta semana",
        "icon": "check",
        "metric": "perfect",
        "target": 3,
        "reward": 30,
    },
    {
        "key": "streak5",
        "name": "Constancia",
        "desc": "Mantén una racha de 5 días",
        "icon": "flame",
        "metric": "streak",
        "target": 5,
        "reward": 15,
    },
]

# Cofres por hitos de racha: dias -> recompensa en Cosmos. >=7 dan tambien un congelador.
STREAK_REWARDS = [(3, 15), (7, 30), (14, 50), (30, 100), (60, 150), (100, 300)]


def _check_streak_chest(profile):
    """Si la racha alcanza un nuevo hito, deja un cofre pendiente por abrir."""
    changed = False
    for day, _reward in STREAK_REWARDS:
        if profile.streak >= day > profile.streak_reward_max:
            profile.streak_reward_max = day
            profile.pending_chest = day  # se guarda el hito mas alto alcanzado
            changed = True
    if changed:
        Notification.push(
            profile.user,
            "¡Cofre de racha desbloqueado! Ábrelo en tu ruta.",
            icon="trophy",
            url=reverse("astro:ruta"),
        )
    return changed


LEAGUE_PROMOTE = 7  # top N ascienden de division
LEAGUE_RELEGATE = 7  # ultimos N descienden de division
LEAGUE_SHOW = 30  # cuantos mostrar en la tabla


def get_division(index):
    """Devuelve datos de una division por su indice (0 = mas baja)."""
    i = max(0, min(index, len(DIVISIONS) - 1))
    key, name, color, icon = DIVISIONS[i]
    return {
        "index": i,
        "key": key,
        "name": name,
        "color": color,
        "icon": icon,
        "is_top": i == len(DIVISIONS) - 1,
        "is_bottom": i == 0,
        "next_name": DIVISIONS[i + 1][1] if i + 1 < len(DIVISIONS) else None,
        "prev_name": DIVISIONS[i - 1][1] if i > 0 else None,
    }


# Rangos por XP total: (key, nombre, xp_minimo, color)
RANKS = [
    ("bronce", "Bronce", 0, "#cd7f32"),
    ("plata", "Plata", 250, "#c0c8d8"),
    ("oro", "Oro", 750, "#f5b301"),
    ("zafiro", "Zafiro", 1500, "#4f7cff"),
    ("rubi", "Rubi", 3000, "#ff4d6d"),
    ("diamante", "Diamante", 6000, "#6ee7ff"),
]


def get_rank(xp):
    """Devuelve el rango actual y el progreso hacia el siguiente segun el XP total."""
    current, nxt = RANKS[0], None
    for i, r in enumerate(RANKS):
        if xp >= r[2]:
            current = r
            nxt = RANKS[i + 1] if i + 1 < len(RANKS) else None
    key, name, minimum, color = current
    data = {
        "key": key,
        "name": name,
        "color": color,
        "min": minimum,
        "next_name": None,
        "next_min": None,
        "pct": 100,
        "to_next": 0,
    }
    if nxt:
        span = nxt[2] - minimum
        data["next_name"] = nxt[1]
        data["next_min"] = nxt[2]
        data["to_next"] = nxt[2] - xp
        data["pct"] = round((xp - minimum) / span * 100) if span else 0
    return data


_norm_text = services.norm_text


def _get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def _lessons_done_today(user):
    return LessonProgress.objects.filter(
        user=user, completed=True, completed_at__date=timezone.localdate()
    ).count()


def _user_certificates(user):
    """Unidades totalmente completadas por el usuario (con su fecha)."""
    done = set(
        LessonProgress.objects.filter(user=user, completed=True).values_list("lesson_id", flat=True)
    )
    certs = []
    for unit in Category.objects.filter(is_active=True).order_by("order"):
        lessons = list(unit.lessons.filter(is_active=True))
        if lessons and all(l.id in done for l in lessons):
            last = (
                LessonProgress.objects.filter(user=user, lesson__in=lessons, completed=True)
                .order_by("-completed_at")
                .first()
            )
            certs.append({"unit": unit, "date": last.completed_at if last else None})
    return certs


def _award_achievements(user):
    """Evalua los logros del usuario y desbloquea los nuevos. Devuelve los recien ganados."""
    profile = _get_profile(user)
    stats = {
        "lessons_completed": LessonProgress.objects.filter(
            user=user, completed=True, lesson__is_active=True
        ).count(),
        "streak": max(profile.streak, profile.best_streak),
        "xp": profile.xp,
        "perfect_quizzes": profile.perfect_quizzes,
    }
    earned_keys = set(
        UserAchievement.objects.filter(user=user).values_list("achievement__key", flat=True)
    )
    newly = []
    for ach in Achievement.objects.filter(is_active=True):
        if ach.key in earned_keys:
            continue
        if stats.get(ach.condition_type, 0) >= ach.threshold:
            _, created = UserAchievement.objects.get_or_create(user=user, achievement=ach)
            if created:
                Notification.push(
                    user,
                    f"Logro desbloqueado: {ach.name}",
                    icon=ach.icon or "trophy",
                    url=reverse("astro:profile"),
                )
                newly.append(ach)
    return newly


# ---------- Logica de desbloqueo secuencial ----------


def _ordered_lessons():
    return list(
        Lesson.objects.filter(is_active=True, category__is_active=True)
        .select_related("category")
        .order_by("category__order", "order")
    )


def _lesson_status(user, lessons=None):
    """Devuelve (status_por_id, completed_ids). status: completed / current / locked."""
    if lessons is None:
        lessons = _ordered_lessons()
    completed = set(
        LessonProgress.objects.filter(user=user, completed=True).values_list("lesson_id", flat=True)
    )
    status = {}
    prev_completed = True  # la primera leccion siempre esta desbloqueada
    for lesson in lessons:
        is_done = lesson.id in completed
        if is_done:
            status[lesson.id] = "completed"
        elif prev_completed:
            status[lesson.id] = "current"
        else:
            status[lesson.id] = "locked"
        prev_completed = is_done
    return status, completed


def _unit_complete(user, unit):
    """True si el usuario completo todas las lecciones activas de la unidad."""
    lessons = list(unit.lessons.filter(is_active=True))
    if not lessons:
        return False, []
    done = set(
        LessonProgress.objects.filter(user=user, lesson__in=lessons, completed=True).values_list(
            "lesson_id", flat=True
        )
    )
    return all(l.id in done for l in lessons), lessons


EXAM_PASS = 0.8  # % para aprobar el examen final
EXAM_HONORS = 100  # % para "con honores"
EXAM_BONUS = 50  # Cosmos la primera vez que se aprueba


def _get_apod():
    """Imagen astronomica del dia (NASA APOD), cacheada 6h. None si falla."""
    import json
    import os
    import urllib.request

    from django.core.cache import cache

    cached = cache.get("apod")
    if cached is not None:
        return cached or None  # '' guardado = fallo reciente, no reintentar
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.load(r)
        apod = {
            "title": d.get("title", ""),
            "explanation": d.get("explanation", ""),
            "date": d.get("date", ""),
            "media_type": d.get("media_type", "image"),
            "url": d.get("url", ""),
            "hdurl": d.get("hdurl", ""),
            "copyright": d.get("copyright", ""),
        }
        cache.set("apod", apod, 60 * 60 * 6)
        return apod
    except Exception:
        cache.set("apod", "", 60 * 30)  # evita reintentar cada carga durante 30 min
        return None


def _user_public_stats(user):
    """Datos publicos de un usuario para su perfil/tarjeta social."""
    p = _get_profile(user)
    done = LessonProgress.objects.filter(user=user, completed=True, lesson__is_active=True).count()
    achievements = UserAchievement.objects.filter(user=user).count()
    return {
        "user": user,
        "profile": p,
        "level": p.xp // 100 + 1,
        "rank": get_rank(p.xp),
        "division": get_division(p.division),
        "done_lessons": done,
        "achievements": achievements,
        "certificates": len(_user_certificates(user)),
    }


DUEL_QUESTIONS = 5  # preguntas por duelo


def _duel_role(duel, user):
    if duel.challenger_id == user.id:
        return "challenger"
    if duel.opponent_id == user.id:
        return "opponent"
    return None


def _duel_questions(duel):
    qmap = Question.objects.filter(id__in=duel.question_ids).prefetch_related("options").in_bulk()
    return [qmap[i] for i in duel.question_ids if i in qmap]


def _weekly_of(profile, wk):
    """XP de la semana actual del perfil (0 si su week_key no es la actual)."""
    return profile.weekly_xp if profile.week_key == wk else 0


def _week_monday():
    today = timezone.localdate()
    return today - timedelta(days=today.isoweekday() - 1)


def _lessons_this_week(user):
    return LessonProgress.objects.filter(
        user=user, completed=True, completed_at__date__gte=_week_monday()
    ).count()


def _mission_metric(profile, metric, wk, week_lessons):
    if metric == "xp":
        return _weekly_of(profile, wk)
    if metric == "lessons":
        return week_lessons
    if metric == "perfect":
        return profile.week_perfect if profile.week_key == wk else 0
    if metric == "streak":
        return profile.streak
    return 0


def _build_missions(user):
    """Devuelve las misiones semanales con su progreso y estado de reclamo."""
    profile = _get_profile(user)
    wk = timezone.localdate().strftime("%G-%V")
    week_lessons = _lessons_this_week(user)
    claimed = set(
        MissionClaim.objects.filter(user=user, week_key=wk).values_list("mission_key", flat=True)
    )
    out = []
    for m in MISSIONS:
        value = _mission_metric(profile, m["metric"], wk, week_lessons)
        done = value >= m["target"]
        out.append(
            {
                **m,
                "value": min(value, m["target"]),
                "raw": value,
                "done": done,
                "pct": min(100, round(value / m["target"] * 100)) if m["target"] else 0,
                "claimed": m["key"] in claimed,
                "claimable": done and m["key"] not in claimed,
            }
        )
    return out, wk


def _weak_questions(user):
    """Preguntas donde el usuario mas falla (menor precision), peor primero."""
    stats = list(
        QuestionStat.objects.filter(user=user, seen__gt=0, correct__lt=F("seen"))
        .select_related("question", "question__lesson")
        .prefetch_related("question__options")
    )
    stats.sort(key=lambda s: (s.correct / s.seen, -s.seen))
    return [s.question for s in stats[:REVIEW_BATCH]]


__all__ = [
    "AVATAR_ICONS",
    "Achievement",
    "COINS_PERFECT_BONUS",
    "COINS_PER_LESSON",
    "Card",
    "Category",
    "DAILY_BONUS",
    "DAILY_GOAL",
    "DAILY_GOALS",
    "DIVISIONS",
    "DUEL_QUESTIONS",
    "Duel",
    "EXAM_BONUS",
    "EXAM_HONORS",
    "EXAM_PASS",
    "F",
    "Follow",
    "HEARTS_MAX",
    "HEART_REFILL_MIN",
    "Http404",
    "JsonResponse",
    "LEAGUE_PROMOTE",
    "LEAGUE_RELEGATE",
    "LEAGUE_SHOW",
    "LOGIN_URL",
    "Lesson",
    "LessonProgress",
    "LoginForm",
    "MISSIONS",
    "MissionClaim",
    "Notification",
    "PASS_RATIO",
    "Profile",
    "Purchase",
    "Q",
    "Question",
    "QuestionReport",
    "QuestionStat",
    "RANKS",
    "REVIEW_BATCH",
    "RegisterForm",
    "ReviewItem",
    "STREAK_REWARDS",
    "ShopItem",
    "StyledPasswordChangeForm",
    "UnitExam",
    "UserAchievement",
    "ValidationError",
    "XP_PERFECT_BONUS",
    "XP_PER_CORRECT",
    "XP_PER_REVIEW",
    "_award_achievements",
    "_build_missions",
    "_check_streak_chest",
    "_due_reviews",
    "_duel_questions",
    "_duel_role",
    "_get_apod",
    "_get_profile",
    "_lesson_status",
    "_lessons_done_today",
    "_lessons_this_week",
    "_mission_metric",
    "_needed_correct",
    "_next_heart_minutes",
    "_norm_text",
    "_ordered_lessons",
    "_pass_ratio",
    "_record_answer",
    "_refill_hearts",
    "_seed_reviews",
    "_unit_complete",
    "_user_certificates",
    "_user_public_stats",
    "_weak_questions",
    "_week_monday",
    "_weekly_of",
    "get_division",
    "get_object_or_404",
    "get_rank",
    "get_user_model",
    "json",
    "login",
    "login_required",
    "logout",
    "math",
    "messages",
    "random",
    "redirect",
    "render",
    "require_POST",
    "reverse",
    "services",
    "timedelta",
    "timezone",
    "update_session_auth_hash",
    "validate_email",
]
