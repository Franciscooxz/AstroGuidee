from django.shortcuts import render
from .models import ResourceCategory, Resource


def resources_index(request):
    categories = ResourceCategory.objects.prefetch_related('items')
    return render(request, 'recursos/index.html', {
        'categories': categories,
        'active_nav': 'recursos',
    })
