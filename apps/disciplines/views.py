from django.shortcuts import render, get_object_or_404
from .models import Discipline, DisciplineCategory


def discipline_list(request):
    category_slug = request.GET.get('cat')
    categories = DisciplineCategory.objects.all()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(DisciplineCategory, slug=category_slug)
        disciplines = Discipline.objects.filter(category=active_category, is_active=True)
    else:
        disciplines = Discipline.objects.filter(is_active=True)
    return render(request, 'artes/list.html', {
        'disciplines': disciplines,
        'categories': categories,
        'active_category': active_category,
        'active_nav': 'artes',
    })


def discipline_detail(request, slug):
    discipline = get_object_or_404(Discipline, slug=slug, is_active=True)
    related = Discipline.objects.filter(category=discipline.category, is_active=True).exclude(pk=discipline.pk)[:4]
    return render(request, 'artes/detail.html', {
        'discipline': discipline,
        'related': related,
        'active_nav': 'artes',
    })
