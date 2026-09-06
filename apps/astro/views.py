import json
import math
import unicodedata
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, StyledPasswordChangeForm
from .models import (Achievement, Category, Lesson, LessonProgress, Profile,
                     Purchase, ShopItem, UserAchievement)

LOGIN_URL = 'astro:login'
AVATAR_ICONS = ['orbit', 'sun', 'earth', 'saturn', 'galaxy', 'blackhole',
                'star', 'rocket', 'atom', 'planet', 'coin', 'flame']
XP_PER_CORRECT = 10
XP_PERFECT_BONUS = 20
COINS_PER_LESSON = 5
COINS_PERFECT_BONUS = 5
DAILY_GOAL = 1          # lecciones por dia para cumplir la meta
DAILY_BONUS = 15        # Cosmos de recompensa al cumplirla
HEARTS_MAX = 5          # vidas maximas
HEART_REFILL_MIN = 30   # minutos para recuperar 1 vida


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
        profile.hearts_updated = (now if profile.hearts >= HEARTS_MAX
                                  else last + timedelta(minutes=gained * HEART_REFILL_MIN))
    return profile


def _next_heart_minutes(profile):
    """Minutos aproximados hasta recuperar la proxima vida (0 si estan al maximo)."""
    if profile.hearts >= HEARTS_MAX or not profile.hearts_updated:
        return 0
    nxt = profile.hearts_updated + timedelta(minutes=HEART_REFILL_MIN)
    return max(0, int(round((nxt - timezone.now()).total_seconds() / 60)))

# Rangos por XP total: (key, nombre, xp_minimo, color)
RANKS = [
    ('bronce', 'Bronce', 0, '#cd7f32'),
    ('plata', 'Plata', 250, '#c0c8d8'),
    ('oro', 'Oro', 750, '#f5b301'),
    ('zafiro', 'Zafiro', 1500, '#4f7cff'),
    ('rubi', 'Rubi', 3000, '#ff4d6d'),
    ('diamante', 'Diamante', 6000, '#6ee7ff'),
]


def get_rank(xp):
    """Devuelve el rango actual y el progreso hacia el siguiente segun el XP total."""
    current, nxt = RANKS[0], None
    for i, r in enumerate(RANKS):
        if xp >= r[2]:
            current = r
            nxt = RANKS[i + 1] if i + 1 < len(RANKS) else None
    key, name, minimum, color = current
    data = {'key': key, 'name': name, 'color': color, 'min': minimum,
            'next_name': None, 'next_min': None, 'pct': 100, 'to_next': 0}
    if nxt:
        span = nxt[2] - minimum
        data['next_name'] = nxt[1]
        data['next_min'] = nxt[2]
        data['to_next'] = nxt[2] - xp
        data['pct'] = round((xp - minimum) / span * 100) if span else 0
    return data


def _norm_text(s):
    """Normaliza texto para comparar respuestas: sin acentos, minusculas, sin espacios extra."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return s.lower().strip()


def _get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def _lessons_done_today(user):
    return LessonProgress.objects.filter(
        user=user, completed=True, completed_at__date=timezone.localdate()).count()


def _user_certificates(user):
    """Unidades totalmente completadas por el usuario (con su fecha)."""
    done = set(LessonProgress.objects.filter(user=user, completed=True)
               .values_list('lesson_id', flat=True))
    certs = []
    for unit in Category.objects.filter(is_active=True).order_by('order'):
        lessons = list(unit.lessons.filter(is_active=True))
        if lessons and all(l.id in done for l in lessons):
            last = (LessonProgress.objects.filter(user=user, lesson__in=lessons, completed=True)
                    .order_by('-completed_at').first())
            certs.append({'unit': unit, 'date': last.completed_at if last else None})
    return certs


def _award_achievements(user):
    """Evalua los logros del usuario y desbloquea los nuevos. Devuelve los recien ganados."""
    profile = _get_profile(user)
    stats = {
        'lessons_completed': LessonProgress.objects.filter(
            user=user, completed=True, lesson__is_active=True).count(),
        'streak': max(profile.streak, profile.best_streak),
        'xp': profile.xp,
        'perfect_quizzes': profile.perfect_quizzes,
    }
    earned_keys = set(
        UserAchievement.objects.filter(user=user).values_list('achievement__key', flat=True))
    newly = []
    for ach in Achievement.objects.filter(is_active=True):
        if ach.key in earned_keys:
            continue
        if stats.get(ach.condition_type, 0) >= ach.threshold:
            UserAchievement.objects.get_or_create(user=user, achievement=ach)
            newly.append(ach)
    return newly


# ---------- Publico ----------

def home(request):
    categories = Category.objects.filter(is_active=True)
    featured = categories.first()
    featured_cards = featured.cards.filter(is_active=True) if featured else []
    return render(request, 'astro/home.html', {
        'categories': categories,
        'featured': featured,
        'featured_cards': featured_cards,
    })


# ---------- Autenticacion ----------

def register(request):
    if request.user.is_authenticated:
        return redirect('astro:ruta')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('astro:onboarding')  # a la bienvenida
    else:
        form = RegisterForm()
    return render(request, 'astro/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('astro:ruta')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next') or request.GET.get('next') or 'astro:ruta')
    else:
        form = LoginForm(request)
    return render(request, 'astro/auth/login.html', {'form': form, 'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    return redirect('astro:home')


# ---------- Logica de desbloqueo secuencial ----------

def _ordered_lessons():
    return list(
        Lesson.objects.filter(is_active=True, category__is_active=True)
        .select_related('category')
        .order_by('category__order', 'order')
    )


def _lesson_status(user, lessons=None):
    """Devuelve (status_por_id, completed_ids). status: completed / current / locked."""
    if lessons is None:
        lessons = _ordered_lessons()
    completed = set(
        LessonProgress.objects.filter(user=user, completed=True)
        .values_list('lesson_id', flat=True)
    )
    status = {}
    prev_completed = True  # la primera leccion siempre esta desbloqueada
    for lesson in lessons:
        is_done = lesson.id in completed
        if is_done:
            status[lesson.id] = 'completed'
        elif prev_completed:
            status[lesson.id] = 'current'
        else:
            status[lesson.id] = 'locked'
        prev_completed = is_done
    return status, completed


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
        if lesson.status == 'current' and current_lesson is None:
            current_lesson = lesson
        if current_unit is None or current_unit['unit'].id != lesson.category_id:
            current_unit = {'unit': lesson.category, 'lessons': [], 'done': 0, 'total': 0}
            units.append(current_unit)
        current_unit['lessons'].append(lesson)
        current_unit['total'] += 1
        if lesson.status == 'completed':
            current_unit['done'] += 1

    for u in units:
        u['complete'] = u['total'] > 0 and u['done'] == u['total']

    total = len(lessons)
    done = len(completed)
    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=['hearts', 'hearts_updated'])
    daily_done = _lessons_done_today(request.user)
    return render(request, 'astro/app/ruta.html', {
        'units': units,
        'current_lesson': current_lesson,
        'all_done': total > 0 and done == total,
        'total': total,
        'done': done,
        'pct': round(done / total * 100) if total else 0,
        'xp': profile.xp,
        'streak': profile.streak,
        'coins': profile.coins,
        'hearts': profile.hearts,
        'hearts_max': HEARTS_MAX,
        'next_heart': _next_heart_minutes(profile),
        'daily_done': min(daily_done, DAILY_GOAL),
        'daily_goal': DAILY_GOAL,
        'daily_met': daily_done >= DAILY_GOAL,
        'active_nav': 'ruta',
    })


@login_required(login_url=LOGIN_URL)
def certificate(request, slug):
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    lessons = list(unit.lessons.filter(is_active=True))
    done = set(LessonProgress.objects.filter(user=request.user, lesson__in=lessons, completed=True)
               .values_list('lesson_id', flat=True))
    if not lessons or not all(l.id in done for l in lessons):
        return redirect('astro:ruta')
    last = (LessonProgress.objects.filter(user=request.user, lesson__in=lessons, completed=True)
            .order_by('-completed_at').first())
    return render(request, 'astro/app/certificate.html', {
        'unit': unit,
        'date': last.completed_at if last else None,
        'n_lessons': len(lessons),
        'n_cards': unit.card_count,
    })


@login_required(login_url=LOGIN_URL)
def onboarding(request):
    profile = _get_profile(request.user)
    if request.method == 'POST':
        profile.onboarded = True
        profile.save(update_fields=['onboarded'])
        return redirect('astro:ruta')
    if profile.onboarded:
        return redirect('astro:ruta')
    return render(request, 'astro/app/onboarding.html', {})


@login_required(login_url=LOGIN_URL)
def profile(request):
    p = _get_profile(request.user)
    total_lessons = Lesson.objects.filter(is_active=True, category__is_active=True).count()
    done = LessonProgress.objects.filter(
        user=request.user, completed=True, lesson__is_active=True).count()

    level = p.xp // 100 + 1
    xp_in_level = p.xp % 100

    earned_ids = set(UserAchievement.objects.filter(user=request.user)
                     .values_list('achievement_id', flat=True))
    achievements = [{'a': a, 'earned': a.id in earned_ids}
                    for a in Achievement.objects.filter(is_active=True)]
    return render(request, 'astro/app/profile.html', {
        'profile': p,
        'total_lessons': total_lessons,
        'done_lessons': done,
        'pct': round(done / total_lessons * 100) if total_lessons else 0,
        'level': level,
        'xp_in_level': xp_in_level,
        'xp_to_next': 100 - xp_in_level,
        'rank': get_rank(p.xp),
        'achievements': achievements,
        'earned_count': len(earned_ids),
        'certificates': _user_certificates(request.user),
        'active_nav': 'profile',
    })


@login_required(login_url=LOGIN_URL)
def lesson(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == 'locked':
        return redirect('astro:ruta')

    cards = lesson_obj.cards.filter(is_active=True)
    is_completed = status.get(lesson_obj.id) == 'completed'
    return render(request, 'astro/app/lesson.html', {
        'lesson': lesson_obj,
        'cards': cards,
        'is_completed': is_completed,
        'has_quiz': lesson_obj.has_quiz,
    })


@login_required(login_url=LOGIN_URL)
def quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == 'locked':
        return redirect('astro:ruta')

    questions = list(
        lesson_obj.questions.filter(is_active=True).prefetch_related('options')
    )
    if not questions:
        return redirect('astro:lesson', slug=lesson_obj.slug)

    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=['hearts', 'hearts_updated'])
    if profile.hearts < 1:
        return render(request, 'astro/app/no_hearts.html', {
            'lesson': lesson_obj,
            'next_heart': _next_heart_minutes(profile),
            'coins': profile.coins,
        })

    return render(request, 'astro/app/quiz.html', {
        'lesson': lesson_obj,
        'questions': questions,
        'hearts': profile.hearts,
        'hearts_max': HEARTS_MAX,
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_quiz(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == 'locked':
        return JsonResponse({'error': 'locked'}, status=403)

    try:
        answers = json.loads(request.body or '{}').get('answers', {})
    except (ValueError, AttributeError):
        answers = {}

    questions = list(lesson_obj.questions.filter(is_active=True).prefetch_related('options'))
    total = len(questions)
    correct = 0
    for q in questions:
        val = answers.get(str(q.id), '')
        if q.qtype == 'text':
            typed = _norm_text(str(val))
            accepted = [_norm_text(o.text) for o in q.options.all() if o.is_correct]
            if typed and typed in accepted:
                correct += 1
        else:
            chosen = str(val)
            if any(o.is_correct and str(o.id) == chosen for o in q.options.all()):
                correct += 1

    passed = total > 0 and correct >= math.ceil(0.6 * total)
    perfect = total > 0 and correct == total

    already_completed = LessonProgress.objects.filter(
        user=request.user, lesson=lesson_obj, completed=True).exists()

    profile = _get_profile(request.user)
    _refill_hearts(profile)
    hearts_lost = min(total - correct, profile.hearts)
    profile.hearts -= hearts_lost

    xp_earned = 0
    coins_earned = 0
    doubled = False
    newly = []
    if passed:
        if perfect:
            profile.perfect_quizzes += 1
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
        profile.save()

        prog, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson_obj)
        if not prog.completed:
            prog.completed = True
            prog.completed_at = timezone.now()
            prog.save()

        newly = _award_achievements(request.user)

    # Meta diaria: si cumpliste la meta de hoy y no la habias cobrado, bono de Cosmos
    daily_bonus = 0
    today = timezone.localdate()
    done_today = _lessons_done_today(request.user)
    if passed and done_today >= DAILY_GOAL and profile.daily_claimed != today:
        profile.daily_claimed = today
        profile.add_coins(DAILY_BONUS)
        daily_bonus = DAILY_BONUS

    profile.save()  # persiste vidas, meta diaria y demas

    return JsonResponse({
        'correct': correct,
        'total': total,
        'passed': passed,
        'perfect': perfect,
        'xp_earned': xp_earned,
        'doubled': doubled,
        'coins_earned': coins_earned,
        'daily_bonus': daily_bonus,
        'hearts': profile.hearts,
        'hearts_lost': hearts_lost,
        'hearts_max': HEARTS_MAX,
        'total_xp': profile.xp,
        'total_coins': profile.coins,
        'streak': profile.streak,
        'newly_achievements': [{'name': a.name, 'icon': a.icon} for a in newly],
    })


@login_required(login_url=LOGIN_URL)
def league(request):
    wk = timezone.localdate().strftime('%G-%V')
    profile = _get_profile(request.user)
    top = list(
        Profile.objects.filter(week_key=wk, weekly_xp__gt=0)
        .select_related('user').order_by('-weekly_xp', 'user__username')[:50]
    )
    for p in top:
        p.rank = get_rank(p.xp)  # rango (por XP total) para mostrar junto al nombre
    my_weekly = profile.weekly_xp if profile.week_key == wk else 0
    my_rank = None
    for i, p in enumerate(top, start=1):
        if p.user_id == request.user.id:
            my_rank = i
            break
    return render(request, 'astro/app/league.html', {
        'top': top,
        'my_rank': my_rank,
        'my_weekly': my_weekly,
        'active_nav': 'league',
    })


@login_required(login_url=LOGIN_URL)
def settings_view(request):
    profile = _get_profile(request.user)
    pw_form = StyledPasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            email = request.POST.get('email', '').strip()
            avatar = request.POST.get('avatar', '').strip()
            valid = True
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    messages.error(request, 'El correo no es valido.')
                    valid = False
            if valid:
                request.user.email = email
                request.user.save(update_fields=['email'])
                profile.avatar = avatar if avatar in AVATAR_ICONS else ''
                profile.save(update_fields=['avatar'])
                messages.success(request, 'Perfil actualizado.')
                return redirect('astro:settings')
        elif 'change_password' in request.POST:
            pw_form = StyledPasswordChangeForm(request.user, request.POST)
            if pw_form.is_valid():
                user = pw_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contrasena cambiada correctamente.')
                return redirect('astro:settings')

    return render(request, 'astro/app/settings.html', {
        'profile': profile,
        'pw_form': pw_form,
        'avatar_icons': AVATAR_ICONS,
        'active_nav': 'profile',
    })


@login_required(login_url=LOGIN_URL)
def store(request):
    profile = _get_profile(request.user)
    _refill_hearts(profile)
    profile.save(update_fields=['hearts', 'hearts_updated'])
    items = ShopItem.objects.filter(is_active=True)
    owned = set(Purchase.objects.filter(user=request.user).values_list('item__key', flat=True))
    return render(request, 'astro/app/store.html', {
        'powerups': [i for i in items if i.effect != 'frame'],
        'frames': [i for i in items if i.effect == 'frame'],
        'owned': owned,
        'profile': profile,
        'hearts_max': HEARTS_MAX,
        'active_nav': 'store',
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def buy_item(request, key):
    item = get_object_or_404(ShopItem, key=key, is_active=True)
    profile = _get_profile(request.user)

    if item.effect == 'frame':
        if Purchase.objects.filter(user=request.user, item=item).exists():
            messages.info(request, f'Ya tienes "{item.name}".')
            return redirect('astro:store')

    if profile.coins < item.price:
        messages.error(request, f'Te faltan Cosmos para comprar "{item.name}".')
        return redirect('astro:store')

    if item.effect == 'refill_hearts' and profile.hearts >= HEARTS_MAX:
        messages.info(request, 'Ya tienes todas tus vidas.')
        return redirect('astro:store')

    profile.coins -= item.price
    if item.effect == 'streak_freeze':
        profile.streak_freezes += 1
    elif item.effect == 'double_xp':
        profile.double_xp_pending = True
    elif item.effect == 'refill_hearts':
        profile.hearts = HEARTS_MAX
        profile.hearts_updated = timezone.now()
    elif item.effect == 'frame':
        Purchase.objects.create(user=request.user, item=item)
        profile.frame = item.key  # lo equipa al comprarlo
    profile.save()
    messages.success(request, f'Compraste "{item.name}". Te quedan {profile.coins} Cosmos.')
    return redirect('astro:store')


@login_required(login_url=LOGIN_URL)
@require_POST
def equip_frame(request, key):
    profile = _get_profile(request.user)
    if key == 'none':
        profile.frame = ''
        profile.save()
        messages.success(request, 'Marco quitado.')
        return redirect('astro:store')
    item = get_object_or_404(ShopItem, key=key, effect='frame', is_active=True)
    if not Purchase.objects.filter(user=request.user, item=item).exists():
        messages.error(request, 'No tienes ese marco.')
        return redirect('astro:store')
    profile.frame = item.key
    profile.save()
    messages.success(request, f'Marco "{item.name}" equipado.')
    return redirect('astro:store')


@login_required(login_url=LOGIN_URL)
@require_POST
def complete_lesson(request, slug):
    lesson_obj = get_object_or_404(Lesson, slug=slug, is_active=True)
    status, _ = _lesson_status(request.user)
    if status.get(lesson_obj.id) == 'locked':
        return redirect('astro:ruta')

    prog, _created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson_obj)
    if not prog.completed:
        prog.completed = True
        prog.completed_at = timezone.now()
        prog.save()
        profile = _get_profile(request.user)
        profile.register_activity()
        profile.save()
        _award_achievements(request.user)
    return redirect('astro:ruta')
