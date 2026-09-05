from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (Achievement, Card, Category, Lesson, LessonProgress,
                     Profile, Question, ShopItem, UserAchievement)
from .panel_forms import (AchievementForm, CardForm, LessonForm, OptionFormSet,
                          QuestionForm, ShopItemForm, UnitForm)

LOGIN = 'astro:login'
User = get_user_model()


# ---------- Inicio ----------

@staff_member_required(login_url=LOGIN)
def dashboard(request):
    return render(request, 'astro/panel/dashboard.html', {
        'n_units': Category.objects.count(),
        'n_lessons': Lesson.objects.count(),
        'n_cards': Card.objects.count(),
        'n_questions': Question.objects.count(),
        'n_users': User.objects.count(),
        'active': 'inicio',
    })


# ---------- Estadisticas ----------

@staff_member_required(login_url=LOGIN)
def stats(request):
    User = get_user_model()
    week_ago = timezone.localdate() - timedelta(days=7)

    lessons = list(
        Lesson.objects.filter(is_active=True)
        .annotate(completions=Count('progress', filter=Q(progress__completed=True)))
        .select_related('category')
    )
    top_lessons = sorted(lessons, key=lambda l: l.completions, reverse=True)[:6]
    hardest = sorted(lessons, key=lambda l: l.completions)[:6]

    return render(request, 'astro/panel/stats.html', {
        'n_users': User.objects.count(),
        'active_week': Profile.objects.filter(last_active__gte=week_ago).count(),
        'total_completions': LessonProgress.objects.filter(completed=True).count(),
        'total_xp': Profile.objects.aggregate(s=Sum('xp'))['s'] or 0,
        'total_achievements': UserAchievement.objects.count(),
        'perfect_quizzes': Profile.objects.aggregate(s=Sum('perfect_quizzes'))['s'] or 0,
        'top_lessons': top_lessons,
        'hardest': hardest,
        'active': 'stats',
    })


# ---------- Unidades ----------

@staff_member_required(login_url=LOGIN)
def units(request):
    return render(request, 'astro/panel/units_list.html', {
        'units': Category.objects.all(), 'active': 'unidades',
    })


@staff_member_required(login_url=LOGIN)
def unit_edit(request, pk=None):
    obj = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion:units')
    else:
        form = UnitForm(instance=obj)
    return render(request, 'astro/panel/form.html', {
        'form': form, 'title': 'Editar unidad' if obj else 'Nueva unidad',
        'back': 'gestion:units', 'active': 'unidades',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def unit_delete(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect('gestion:units')


# ---------- Lecciones ----------

@staff_member_required(login_url=LOGIN)
def lessons(request):
    return render(request, 'astro/panel/lessons_list.html', {
        'lessons': Lesson.objects.select_related('category').all(), 'active': 'lecciones',
    })


@staff_member_required(login_url=LOGIN)
def lesson_edit(request, pk=None):
    obj = get_object_or_404(Lesson, pk=pk) if pk else None
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion:lessons')
    else:
        form = LessonForm(instance=obj)
    return render(request, 'astro/panel/form.html', {
        'form': form, 'title': 'Editar leccion' if obj else 'Nueva leccion',
        'back': 'gestion:lessons', 'active': 'lecciones',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def lesson_delete(request, pk):
    get_object_or_404(Lesson, pk=pk).delete()
    return redirect('gestion:lessons')


# ---------- Tarjetas ----------

@staff_member_required(login_url=LOGIN)
def cards(request):
    qs = Card.objects.select_related('lesson', 'category').all()
    lesson_id = request.GET.get('lesson')
    if lesson_id:
        qs = qs.filter(lesson_id=lesson_id)
    return render(request, 'astro/panel/cards_list.html', {
        'cards': qs, 'all_lessons': Lesson.objects.select_related('category').all(),
        'lesson_filter': lesson_id, 'active': 'tarjetas',
    })


@staff_member_required(login_url=LOGIN)
def card_edit(request, pk=None):
    obj = get_object_or_404(Card, pk=pk) if pk else None
    if request.method == 'POST':
        form = CardForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion:cards')
    else:
        form = CardForm(instance=obj)
    return render(request, 'astro/panel/form.html', {
        'form': form, 'title': 'Editar tarjeta' if obj else 'Nueva tarjeta',
        'back': 'gestion:cards', 'active': 'tarjetas',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def card_delete(request, pk):
    get_object_or_404(Card, pk=pk).delete()
    return redirect('gestion:cards')


# ---------- Quizzes (preguntas) ----------

@staff_member_required(login_url=LOGIN)
def questions(request):
    qs = Question.objects.select_related('lesson', 'lesson__category').all()
    return render(request, 'astro/panel/questions_list.html', {
        'questions': qs, 'active': 'quizzes',
    })


@staff_member_required(login_url=LOGIN)
def question_edit(request, pk=None):
    obj = get_object_or_404(Question, pk=pk) if pk else None
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=obj)
        formset = OptionFormSet(request.POST, instance=obj)
        if form.is_valid() and formset.is_valid():
            question = form.save()
            formset.instance = question
            formset.save()
            return redirect('gestion:questions')
    else:
        form = QuestionForm(instance=obj)
        formset = OptionFormSet(instance=obj)
    return render(request, 'astro/panel/question_form.html', {
        'form': form, 'formset': formset,
        'title': 'Editar pregunta' if obj else 'Nueva pregunta',
        'active': 'quizzes',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def question_delete(request, pk):
    get_object_or_404(Question, pk=pk).delete()
    return redirect('gestion:questions')


# ---------- Tienda ----------

@staff_member_required(login_url=LOGIN)
def shop(request):
    return render(request, 'astro/panel/shop_list.html', {
        'items': ShopItem.objects.all(), 'active': 'tienda',
    })


@staff_member_required(login_url=LOGIN)
def shop_edit(request, pk=None):
    obj = get_object_or_404(ShopItem, pk=pk) if pk else None
    if request.method == 'POST':
        form = ShopItemForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion:shop')
    else:
        form = ShopItemForm(instance=obj)
    return render(request, 'astro/panel/form.html', {
        'form': form, 'title': 'Editar articulo' if obj else 'Nuevo articulo',
        'back': 'gestion:shop', 'active': 'tienda',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def shop_delete(request, pk):
    get_object_or_404(ShopItem, pk=pk).delete()
    return redirect('gestion:shop')


# ---------- Logros ----------

@staff_member_required(login_url=LOGIN)
def achievements(request):
    return render(request, 'astro/panel/achievements_list.html', {
        'items': Achievement.objects.all(), 'active': 'logros',
    })


@staff_member_required(login_url=LOGIN)
def achievement_edit(request, pk=None):
    obj = get_object_or_404(Achievement, pk=pk) if pk else None
    if request.method == 'POST':
        form = AchievementForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('gestion:achievements')
    else:
        form = AchievementForm(instance=obj)
    return render(request, 'astro/panel/form.html', {
        'form': form, 'title': 'Editar logro' if obj else 'Nuevo logro',
        'back': 'gestion:achievements', 'active': 'logros',
    })


@staff_member_required(login_url=LOGIN)
@require_POST
def achievement_delete(request, pk):
    get_object_or_404(Achievement, pk=pk).delete()
    return redirect('gestion:achievements')
