from django.shortcuts import render, get_object_or_404
from .models import Service, ServicePDF


def services_index(request):
    services = Service.objects.filter(is_active=True)
    pdf = ServicePDF.objects.first()
    return render(request, 'servicios/index.html', {
        'services': services,
        'pdf': pdf,
        'active_nav': 'servicios',
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]
    return render(request, 'servicios/detail.html', {
        'service': service,
        'related': related,
        'active_nav': 'servicios',
    })
