import json
import math
import unicodedata
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, StyledPasswordChangeForm
from .models import (Achievement, Card, Category, Follow, Lesson,
                     LessonProgress, MissionClaim, Notification, Profile,
                     Purchase, Question, QuestionReport, QuestionStat,
                     ReviewItem, ShopItem, UnitExam, UserAchievement)

LOGIN_URL = 'astro:login'
AVATAR_ICONS = ['orbit', 'sun', 'earth', 'saturn', 'galaxy', 'blackhole',
                'star', 'rocket', 'atom', 'planet', 'coin', 'flame']
XP_PER_CORRECT = 10
XP_PERFECT_BONUS = 20
COINS_PER_LESSON = 5
COINS_PERFECT_BONUS = 5
DAILY_GOAL = 1          # meta diaria por defecto (lecciones)
DAILY_GOALS = [         # opciones configurables: (lecciones, etiqueta)
    (1, 'Casual'), (2, 'Constante'), (3, 'En serio'), (5, 'Intenso'),
]
DAILY_BONUS = 15        # Cosmos de recompensa al cumplirla
HEARTS_MAX = 5          # vidas maximas
HEART_REFILL_MIN = 30   # minutos para recuperar 1 vida
XP_PER_REVIEW = 3       # XP por cada repaso acertado
REVIEW_BATCH = 15       # preguntas maximas por sesion de repaso

# Umbral de aprobado por nivel de dificultad de la unidad (1 facil -> 5 dificil).
PASS_RATIO = {1: 0.60, 2: 0.67, 3: 0.75, 4: 0.85, 5: 0.90}


def _pass_ratio(difficulty):
    return PASS_RATIO.get(difficulty, 0.60)


def _record_answer(user, question, correct):
    """Acumula la estadistica del usuario sobre una pregunta (precision / temas flojos)."""
    stat, _ = QuestionStat.objects.get_or_create(user=user, question=question)
    stat.seen += 1
    if correct:
        stat.correct += 1
    stat.last_seen = timezone.now()
    stat.save(update_fields=['seen', 'correct', 'last_seen'])


def _needed_correct(total, difficulty):
    """Aciertos minimos para aprobar segun el nivel."""
    return math.ceil(_pass_ratio(difficulty) * total) if total else 0


def _seed_reviews(user, lesson):
    """Crea items de repaso para las preguntas de una leccion recien completada."""
    qs = lesson.questions.filter(is_active=True)
    existing = set(ReviewItem.objects.filter(user=user, question__in=qs)
                   .values_list('question_id', flat=True))
    nuevos = [ReviewItem(user=user, question=q, due=timezone.localdate() + timedelta(days=1))
              for q in qs if q.id not in existing]
    if nuevos:
        ReviewItem.objects.bulk_create(nuevos)


def _due_reviews(user):
    """Items de repaso vencidos (hoy o antes) del usuario, con la pregunta y opciones."""
    return (ReviewItem.objects.filter(user=user, due__lte=timezone.localdate(),
                                      question__is_active=True)
            .select_related('question', 'question__lesson')
            .prefetch_related('question__options'))


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
        if profile.hearts >= HEARTS_MAX:
            Notification.push(profile.user, 'Tus vidas se recargaron al maximo. A seguir aprendiendo!',
                              icon='heart', url=reverse('astro:ruta'))
    return profile


def _next_heart_minutes(profile):
    """Minutos aproximados hasta recuperar la proxima vida (0 si estan al maximo)."""
    if profile.hearts >= HEARTS_MAX or not profile.hearts_updated:
        return 0
    nxt = profile.hearts_updated + timedelta(minutes=HEART_REFILL_MIN)
    return max(0, int(round((nxt - timezone.now()).total_seconds() / 60)))

# Divisiones de liga (ascendentes): (key, nombre, color, icono). Distintas de RANKS.
DIVISIONS = [
    ('cometa', 'Cometa', '#8ea2ff', 'rocket'),
    ('luna', 'Luna', '#c0c8d8', 'planet'),
    ('estrella', 'Estrella', '#f5b301', 'star'),
    ('nebulosa', 'Nebulosa', '#b18bff', 'orbit'),
    ('galaxia', 'Galaxia', '#4f7cff', 'galaxy'),
    ('cosmos', 'Cosmos', '#6ee7ff', 'sun'),
]
# Misiones semanales: metric in {xp, lessons, streak, perfect}. reward = Cosmos.
MISSIONS = [
    {'key': 'xp150', 'name': 'Coleccionista de XP', 'desc': 'Gana 150 XP esta semana',
     'icon': 'star', 'metric': 'xp', 'target': 150, 'reward': 20},
    {'key': 'lessons5', 'name': 'Maraton de lecciones', 'desc': 'Completa 5 lecciones esta semana',
     'icon': 'cards', 'metric': 'lessons', 'target': 5, 'reward': 25},
    {'key': 'perfect3', 'name': 'Sin fallos', 'desc': 'Consigue 3 quizzes perfectos esta semana',
     'icon': 'check', 'metric': 'perfect', 'target': 3, 'reward': 30},
    {'key': 'streak5', 'name': 'Constancia', 'desc': 'Manten una racha de 5 dias',
     'icon': 'flame', 'metric': 'streak', 'target': 5, 'reward': 15},
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
        Notification.push(profile.user, 'Cofre de racha desbloqueado! Abrelo en tu ruta.',
                          icon='trophy', url=reverse('astro:ruta'))
    return changed


LEAGUE_PROMOTE = 7   # top N ascienden de division
LEAGUE_RELEGATE = 7  # ultimos N descienden de division
LEAGUE_SHOW = 30     # cuantos mostrar en la tabla


def get_division(index):
    """Devuelve datos de una division por su indice (0 = mas baja)."""
    i = max(0, min(index, len(DIVISIONS) - 1))
    key, name, color, icon = DIVISIONS[i]
    return {
        'index': i, 'key': key, 'name': name, 'color': color, 'icon': icon,
        'is_top': i == len(DIVISIONS) - 1,
        'is_bottom': i == 0,
        'next_name': DIVISIONS[i + 1][1] if i + 1 < len(DIVISIONS) else None,
        'prev_name': DIVISIONS[i - 1][1] if i > 0 else None,
    }


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
            _, created = UserAchievement.objects.get_or_create(user=user, achievement=ach)
            if created:
                Notification.push(user, f'Logro desbloqueado: {ach.name}',
                                  icon=ach.icon or 'trophy', url=reverse('astro:profile'))
                newly.append(ach)
    return newly


# ---------- PWA (manifest + service worker) ----------

def manifest(request):
    from django.templatetags.static import static
    data = {
        'name': 'AstroGuide',
        'short_name': 'AstroGuide',
        'description': 'Aprende astronomia con tarjetas y quizzes.',
        'start_url': '/app/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#05060f',
        'theme_color': '#0a0b1e',
        'lang': 'es',
        'icons': [
            {'src': static('astro/img/icon-192.png'), 'sizes': '192x192', 'type': 'image/png'},
            {'src': static('astro/img/icon-512.png'), 'sizes': '512x512', 'type': 'image/png'},
            {'src': static('astro/img/icon-maskable-512.png'), 'sizes': '512x512',
             'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    return JsonResponse(data, content_type='application/manifest+json')


def service_worker(request):
    resp = render(request, 'astro/sw.js', content_type='application/javascript')
    resp['Service-Worker-Allowed'] = '/'
    resp['Cache-Control'] = 'no-cache'
    return resp


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
    reviews_due = _due_reviews(request.user).count()
    mission_items, _ = _build_missions(request.user)
    missions_claimable = sum(1 for m in mission_items if m['claimable'])
    return render(request, 'astro/app/ruta.html', {
        'units': units,
        'current_lesson': current_lesson,
        'reviews_due': reviews_due,
        'missions_claimable': missions_claimable,
        'pending_chest': profile.pending_chest,
        'chest_reward': dict(STREAK_REWARDS).get(profile.pending_chest, 0),
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
        'daily_done': min(daily_done, profile.daily_goal),
        'daily_goal': profile.daily_goal,
        'daily_met': daily_done >= profile.daily_goal,
        'active_nav': 'ruta',
    })


def _unit_complete(user, unit):
    """True si el usuario completo todas las lecciones activas de la unidad."""
    lessons = list(unit.lessons.filter(is_active=True))
    if not lessons:
        return False, []
    done = set(LessonProgress.objects.filter(user=user, lesson__in=lessons, completed=True)
               .values_list('lesson_id', flat=True))
    return all(l.id in done for l in lessons), lessons


@login_required(login_url=LOGIN_URL)
def certificate(request, slug):
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return redirect('astro:ruta')
    last = (LessonProgress.objects.filter(user=request.user, lesson__in=lessons, completed=True)
            .order_by('-completed_at').first())
    exam = UnitExam.objects.filter(user=request.user, category=unit).first()
    return render(request, 'astro/app/certificate.html', {
        'unit': unit,
        'date': last.completed_at if last else None,
        'n_lessons': len(lessons),
        'n_cards': unit.card_count,
        'exam': exam,
    })


EXAM_PASS = 0.8    # % para aprobar el examen final
EXAM_HONORS = 100  # % para "con honores"
EXAM_BONUS = 50    # Cosmos la primera vez que se aprueba


@login_required(login_url=LOGIN_URL)
def exam(request, slug):
    """Examen final de una unidad: todas sus preguntas, disponible al completarla."""
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return redirect('astro:ruta')
    questions = list(Question.objects.filter(
        lesson__in=lessons, is_active=True).prefetch_related('options'))
    if not questions:
        return redirect('astro:certificate', slug=unit.slug)
    return render(request, 'astro/app/exam.html', {
        'unit': unit,
        'questions': questions,
        'needed': math.ceil(EXAM_PASS * len(questions)),
        'active_nav': 'ruta',
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_exam(request, slug):
    unit = get_object_or_404(Category, slug=slug, is_active=True)
    complete, lessons = _unit_complete(request.user, unit)
    if not complete:
        return JsonResponse({'error': 'locked'}, status=403)

    try:
        answers = json.loads(request.body or '{}').get('answers', {})
    except (ValueError, AttributeError):
        answers = {}

    questions = list(Question.objects.filter(
        lesson__in=lessons, is_active=True).prefetch_related('options'))
    total = len(questions)
    correct = 0
    for q in questions:
        val = answers.get(str(q.id), '')
        if q.qtype == 'text':
            typed = _norm_text(str(val))
            accepted = [_norm_text(o.text) for o in q.options.all() if o.is_correct]
            ok = bool(typed) and typed in accepted
        else:
            ok = any(o.is_correct and str(o.id) == str(val) for o in q.options.all())
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
        profile.save(update_fields=['coins'])
        Notification.push(request.user, f'Examen final de {unit.name} superado! +{bonus} Cosmos.',
                          icon='trophy', url=reverse('astro:certificate', args=[unit.slug]))

    return JsonResponse({
        'correct': correct, 'total': total, 'pct': pct,
        'passed': passed, 'honors': honors, 'bonus': bonus,
        'best_score': ex.best_score,
        'cert_url': reverse('astro:certificate', args=[unit.slug]),
    })


def _get_apod():
    """Imagen astronomica del dia (NASA APOD), cacheada 6h. None si falla."""
    import json
    import os
    import urllib.request
    from django.core.cache import cache

    cached = cache.get('apod')
    if cached is not None:
        return cached or None  # '' guardado = fallo reciente, no reintentar
    api_key = os.environ.get('NASA_API_KEY', 'DEMO_KEY')
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            d = json.load(r)
        apod = {
            'title': d.get('title', ''),
            'explanation': d.get('explanation', ''),
            'date': d.get('date', ''),
            'media_type': d.get('media_type', 'image'),
            'url': d.get('url', ''),
            'hdurl': d.get('hdurl', ''),
            'copyright': d.get('copyright', ''),
        }
        cache.set('apod', apod, 60 * 60 * 6)
        return apod
    except Exception:
        cache.set('apod', '', 60 * 30)  # evita reintentar cada carga durante 30 min
        return None


@login_required(login_url=LOGIN_URL)
def glossary(request):
    """Explorar/buscar todas las tarjetas del contenido (glosario libre)."""
    q = request.GET.get('q', '').strip()
    cards = Card.objects.filter(is_active=True, category__is_active=True).select_related('category', 'lesson')
    if q:
        cards = cards.filter(
            Q(title__icontains=q) | Q(subtitle__icontains=q) |
            Q(summary__icontains=q) | Q(content__icontains=q) | Q(fun_fact__icontains=q))
    cards = list(cards.order_by('category__order', 'lesson__order', 'order')[:120])
    return render(request, 'astro/app/glossary.html', {
        'cards': cards,
        'q': q,
        'total': len(cards),
        'apod': _get_apod() if not q else None,  # hero solo sin busqueda
        'active_nav': 'glossary',
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
def stats(request):
    """Estadisticas personales del usuario: precision, temas flojos, actividad, racha."""
    from django.db.models import Sum
    user = request.user
    p = _get_profile(user)

    # Precision por unidad (a partir de QuestionStat)
    agg = {row['question__lesson__category']: row for row in
           QuestionStat.objects.filter(user=user)
           .values('question__lesson__category')
           .annotate(seen=Sum('seen'), correct=Sum('correct'))}

    # Progreso (lecciones completadas) por unidad
    done_ids = set(LessonProgress.objects.filter(user=user, completed=True)
                   .values_list('lesson_id', flat=True))

    units = []
    total_seen = total_correct = 0
    for unit in Category.objects.filter(is_active=True).order_by('order'):
        lessons = list(unit.lessons.filter(is_active=True))
        row = agg.get(unit.id)
        seen = row['seen'] if row else 0
        corr = row['correct'] if row else 0
        total_seen += seen
        total_correct += corr
        done = sum(1 for l in lessons if l.id in done_ids)
        units.append({
            'unit': unit,
            'seen': seen,
            'accuracy': round(corr / seen * 100) if seen else None,
            'done': done,
            'total': len(lessons),
            'progress': round(done / len(lessons) * 100) if lessons else 0,
        })

    global_acc = round(total_correct / total_seen * 100) if total_seen else None
    # Temas mas flojos: unidades con precision mas baja (con datos suficientes)
    weak = sorted([u for u in units if u['seen'] >= 3 and u['accuracy'] is not None],
                  key=lambda u: u['accuracy'])[:3]

    # Actividad: lecciones completadas por dia en los ultimos 14 dias
    today = timezone.localdate()
    start = today - timedelta(days=13)
    per_day = {}
    for d in (LessonProgress.objects.filter(user=user, completed=True,
                                            completed_at__date__gte=start)
              .values_list('completed_at', flat=True)):
        key = timezone.localtime(d).date() if timezone.is_aware(d) else d.date()
        per_day[key] = per_day.get(key, 0) + 1
    activity = [{'date': start + timedelta(days=i),
                 'count': per_day.get(start + timedelta(days=i), 0)} for i in range(14)]
    act_max = max((a['count'] for a in activity), default=0)

    level = p.xp // 100 + 1
    return render(request, 'astro/app/stats.html', {
        'profile': p,
        'level': level,
        'rank': get_rank(p.xp),
        'global_acc': global_acc,
        'total_seen': total_seen,
        'units': units,
        'weak': weak,
        'activity': activity,
        'act_max': act_max,
        'active_nav': 'stats',
    })


def _user_public_stats(user):
    """Datos publicos de un usuario para su perfil/tarjeta social."""
    p = _get_profile(user)
    done = LessonProgress.objects.filter(user=user, completed=True, lesson__is_active=True).count()
    achievements = UserAchievement.objects.filter(user=user).count()
    return {
        'user': user, 'profile': p, 'level': p.xp // 100 + 1, 'rank': get_rank(p.xp),
        'division': get_division(p.division), 'done_lessons': done,
        'achievements': achievements, 'certificates': len(_user_certificates(user)),
    }


@login_required(login_url=LOGIN_URL)
def pub_profile(request, username):
    """Perfil publico de otro usuario, con boton de seguir."""
    User = get_user_model()
    target = get_object_or_404(User, username=username, is_active=True)
    if target == request.user:
        return redirect('astro:profile')
    stats = _user_public_stats(target)
    stats['is_following'] = Follow.objects.filter(follower=request.user, following=target).exists()
    stats['followers'] = Follow.objects.filter(following=target).count()
    stats['following'] = Follow.objects.filter(follower=target).count()
    stats['active_nav'] = 'friends'
    return render(request, 'astro/app/pub_profile.html', stats)


@login_required(login_url=LOGIN_URL)
@require_POST
def follow_toggle(request, username):
    User = get_user_model()
    target = get_object_or_404(User, username=username, is_active=True)
    if target != request.user:
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if created:
            Notification.push(target, f'{request.user.username} te empezo a seguir.',
                              icon='user', url=reverse('astro:pub_profile', args=[request.user.username]))
        else:
            obj.delete()
    return redirect('astro:pub_profile', username=username)


@login_required(login_url=LOGIN_URL)
def friends(request):
    """Amigos: a quienes sigues + clasificacion semanal entre amigos."""
    wk = timezone.localdate().strftime('%G-%V')
    following_ids = list(Follow.objects.filter(follower=request.user)
                         .values_list('following_id', flat=True))
    following = [_user_public_stats(p.user) for p in
                 Profile.objects.filter(user_id__in=following_ids).select_related('user')]
    following.sort(key=lambda s: -s['profile'].xp)

    # Clasificacion semanal: amigos + tu, por XP de la semana
    board_profiles = list(Profile.objects.filter(user_id__in=following_ids + [request.user.id])
                          .select_related('user'))
    for p in board_profiles:
        p.eff = _weekly_of(p, wk)
    board_profiles.sort(key=lambda p: (-p.eff, p.user.username.lower()))
    board = [{'pos': i, 'p': p, 'me': p.user_id == request.user.id,
              'rank': get_rank(p.xp)} for i, p in enumerate(board_profiles, start=1)]

    return render(request, 'astro/app/friends.html', {
        'following': following,
        'board': board,
        'n_following': len(following_ids),
        'n_followers': Follow.objects.filter(following=request.user).count(),
        'active_nav': 'friends',
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

    difficulty = lesson_obj.category.difficulty
    return render(request, 'astro/app/quiz.html', {
        'lesson': lesson_obj,
        'questions': questions,
        'hearts': profile.hearts,
        'hearts_max': HEARTS_MAX,
        'difficulty': difficulty,
        'difficulty_name': lesson_obj.category.difficulty_name,
        'needed': _needed_correct(len(questions), difficulty),
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
        user=request.user, lesson=lesson_obj, completed=True).exists()

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
            Notification.push(request.user, f'Subiste al nivel {level_after}! Sigue asi.',
                              icon='star', url=reverse('astro:profile'))

        newly = _award_achievements(request.user)

    # Meta diaria: si cumpliste la meta de hoy y no la habias cobrado, bono de Cosmos
    daily_bonus = 0
    today = timezone.localdate()
    done_today = _lessons_done_today(request.user)
    if passed and done_today >= profile.daily_goal and profile.daily_claimed != today:
        profile.daily_claimed = today
        profile.add_coins(DAILY_BONUS)
        daily_bonus = DAILY_BONUS
        Notification.push(request.user, f'Meta diaria cumplida! +{DAILY_BONUS} Cosmos.',
                          icon='coin', url=reverse('astro:store'))

    profile.save()  # persiste vidas, meta diaria y demas

    return JsonResponse({
        'correct': correct,
        'total': total,
        'needed': needed,
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


def _weekly_of(profile, wk):
    """XP de la semana actual del perfil (0 si su week_key no es la actual)."""
    return profile.weekly_xp if profile.week_key == wk else 0


def _week_monday():
    today = timezone.localdate()
    return today - timedelta(days=today.isoweekday() - 1)


def _lessons_this_week(user):
    return LessonProgress.objects.filter(
        user=user, completed=True, completed_at__date__gte=_week_monday()).count()


def _mission_metric(profile, metric, wk, week_lessons):
    if metric == 'xp':
        return _weekly_of(profile, wk)
    if metric == 'lessons':
        return week_lessons
    if metric == 'perfect':
        return profile.week_perfect if profile.week_key == wk else 0
    if metric == 'streak':
        return profile.streak
    return 0


def _build_missions(user):
    """Devuelve las misiones semanales con su progreso y estado de reclamo."""
    profile = _get_profile(user)
    wk = timezone.localdate().strftime('%G-%V')
    week_lessons = _lessons_this_week(user)
    claimed = set(MissionClaim.objects.filter(user=user, week_key=wk)
                  .values_list('mission_key', flat=True))
    out = []
    for m in MISSIONS:
        value = _mission_metric(profile, m['metric'], wk, week_lessons)
        done = value >= m['target']
        out.append({**m, 'value': min(value, m['target']), 'raw': value, 'done': done,
                    'pct': min(100, round(value / m['target'] * 100)) if m['target'] else 0,
                    'claimed': m['key'] in claimed,
                    'claimable': done and m['key'] not in claimed})
    return out, wk


@login_required(login_url=LOGIN_URL)
def missions(request):
    items, _ = _build_missions(request.user)
    return render(request, 'astro/app/missions.html', {
        'missions': items,
        'active_nav': 'missions',
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def open_chest(request):
    """Abre el cofre de racha pendiente y otorga su recompensa."""
    profile = _get_profile(request.user)
    if profile.pending_chest <= 0:
        messages.info(request, 'No tienes cofres por abrir.')
        return redirect('astro:ruta')
    day = profile.pending_chest
    reward = dict(STREAK_REWARDS).get(day, 15)
    profile.add_coins(reward)
    freeze = 1 if day >= 7 else 0
    profile.streak_freezes += freeze
    profile.pending_chest = 0
    profile.save()
    extra = ' y 1 congelador de racha' if freeze else ''
    messages.success(request, f'Cofre de {day} dias abierto: +{reward} Cosmos{extra}!')
    return redirect('astro:ruta')


@login_required(login_url=LOGIN_URL)
@require_POST
def claim_mission(request, key):
    items, wk = _build_missions(request.user)
    mission = next((m for m in items if m['key'] == key), None)
    if not mission:
        messages.error(request, 'Mision no encontrada.')
    elif mission['claimed']:
        messages.info(request, 'Ya reclamaste esa mision.')
    elif not mission['done']:
        messages.error(request, 'Aun no completaste esa mision.')
    else:
        MissionClaim.objects.get_or_create(
            user=request.user, mission_key=key, week_key=wk)
        profile = _get_profile(request.user)
        profile.add_coins(mission['reward'])
        profile.save(update_fields=['coins'])
        messages.success(request, f'Mision completada: +{mission["reward"]} Cosmos.')
    return redirect('astro:missions')


@login_required(login_url=LOGIN_URL)
def league(request):
    wk = timezone.localdate().strftime('%G-%V')
    profile = _get_profile(request.user)
    div = get_division(profile.division)

    # Cohorte = todos los de tu division, ordenados por XP de esta semana
    cohort = list(Profile.objects.filter(division=profile.division).select_related('user'))
    for p in cohort:
        p.eff = _weekly_of(p, wk)
    cohort.sort(key=lambda p: (-p.eff, p.user.username.lower()))

    total = len(cohort)
    promote_n = 0 if div['is_top'] else LEAGUE_PROMOTE
    relegate_n = 0 if div['is_bottom'] else LEAGUE_RELEGATE
    # Solo tiene sentido zona de descenso si la cohorte es mayor que las dos zonas
    relegate_cut = (total - relegate_n) if total > promote_n + relegate_n else total

    rows, my_rank = [], None
    for i, p in enumerate(cohort, start=1):
        zone = 'up' if i <= promote_n else ('down' if i > relegate_cut else '')
        if p.user_id == request.user.id:
            my_rank = i
        if i <= LEAGUE_SHOW or p.user_id == request.user.id:
            rows.append({'pos': i, 'p': p, 'eff': p.eff, 'zone': zone,
                         'me': p.user_id == request.user.id,
                         'rank': get_rank(p.xp)})

    relegate_start = relegate_cut + 1 if relegate_n and total > promote_n + relegate_n else None
    return render(request, 'astro/app/league.html', {
        'division': div,
        'rows': rows,
        'my_rank': my_rank,
        'my_weekly': _weekly_of(profile, wk),
        'total': total,
        'promote_n': promote_n,
        'relegate_n': relegate_n,
        'relegate_start': relegate_start,
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
        elif 'save_goal' in request.POST:
            try:
                goal = int(request.POST.get('daily_goal', 1))
            except (TypeError, ValueError):
                goal = 1
            if goal in [g for g, _ in DAILY_GOALS]:
                profile.daily_goal = goal
                profile.save(update_fields=['daily_goal'])
                messages.success(request, 'Meta diaria actualizada.')
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
        'daily_goals': DAILY_GOALS,
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
def notifications(request):
    """Centro de notificaciones: lista el historial y marca todo como leido."""
    qs = Notification.objects.filter(user=request.user)
    items = list(qs[:100])
    qs.filter(is_read=False).update(is_read=True)
    return render(request, 'astro/app/notifications.html', {
        'items': items,
        'active_nav': 'notifications',
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def report_question(request, qid):
    """Registra un reporte del usuario sobre una pregunta (posible error)."""
    question = get_object_or_404(Question, id=qid)
    try:
        reason = json.loads(request.body or '{}').get('reason', 'otro')
    except (ValueError, AttributeError):
        reason = 'otro'
    valid = {k for k, _ in QuestionReport.REASONS}
    if reason not in valid:
        reason = 'otro'
    QuestionReport.objects.update_or_create(
        user=request.user, question=question,
        defaults={'reason': reason, 'resolved': False})
    return JsonResponse({'ok': True})


@login_required(login_url=LOGIN_URL)
@require_POST
def clear_notifications(request):
    """Borra todo el historial de notificaciones del usuario."""
    Notification.objects.filter(user=request.user).delete()
    messages.success(request, 'Notificaciones borradas.')
    return redirect('astro:notifications')


@login_required(login_url=LOGIN_URL)
def review(request):
    """Repaso inteligente: presenta las preguntas vencidas (repeticion espaciada)."""
    due = list(_due_reviews(request.user)[:REVIEW_BATCH])
    total_due = _due_reviews(request.user).count()
    next_item = (ReviewItem.objects.filter(user=request.user, due__gt=timezone.localdate())
                 .order_by('due').first())
    total_items = ReviewItem.objects.filter(user=request.user).count()
    weak_available = QuestionStat.objects.filter(
        user=request.user, seen__gt=0, correct__lt=F('seen')).exists()
    return render(request, 'astro/app/review.html', {
        'items': due,
        'questions': [it.question for it in due],
        'total_due': total_due,
        'next_due': next_item.due if next_item else None,
        'total_items': total_items,
        'weak_available': weak_available,
        'active_nav': 'review',
    })


def _weak_questions(user):
    """Preguntas donde el usuario mas falla (menor precision), peor primero."""
    stats = list(
        QuestionStat.objects.filter(user=user, seen__gt=0, correct__lt=F('seen'))
        .select_related('question', 'question__lesson')
        .prefetch_related('question__options')
    )
    stats.sort(key=lambda s: (s.correct / s.seen, -s.seen))
    return [s.question for s in stats[:REVIEW_BATCH]]


@login_required(login_url=LOGIN_URL)
def review_weak(request):
    """Practica dirigida: prioriza las preguntas donde mas fallas."""
    questions = _weak_questions(request.user)
    return render(request, 'astro/app/review.html', {
        'items': questions,
        'questions': questions,
        'weak': True,
        'active_nav': 'review',
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def finish_review(request):
    """Corrige una sesion de repaso: reprograma (SM-2) y acumula estadisticas.

    Califica las preguntas realmente enviadas, asi sirve tanto al repaso por
    vencimiento como al modo 'practicar temas flojos'.
    """
    try:
        answers = json.loads(request.body or '{}').get('answers', {})
    except (ValueError, AttributeError):
        answers = {}

    qids = [k for k in answers.keys()][:REVIEW_BATCH]
    questions = (Question.objects.filter(id__in=qids, is_active=True)
                 .prefetch_related('options'))
    correct = 0
    total = 0
    for q in questions:
        val = answers.get(str(q.id), '')
        if q.qtype == 'text':
            typed = _norm_text(str(val))
            accepted = [_norm_text(o.text) for o in q.options.all() if o.is_correct]
            ok = bool(typed) and typed in accepted
        else:
            ok = any(o.is_correct and str(o.id) == str(val) for o in q.options.all())
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

    return JsonResponse({
        'correct': correct,
        'total': total,
        'xp_earned': xp_earned,
        'total_xp': profile.xp,
        'streak': profile.streak,
    })


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
        _check_streak_chest(profile)
        profile.save()
        _seed_reviews(request.user, lesson_obj)
        _award_achievements(request.user)
    return redirect('astro:ruta')
