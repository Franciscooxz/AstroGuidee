from django.shortcuts import render
from django.http import Http404
from .models import HomeSection, AboutPage, PolicyPage, Founder
from apps.slider.models import Slide
from apps.faq.models import FAQ
from apps.disciplines.models import Discipline
from apps.blog.models import Post
from apps.testimonials.models import Testimonial


def home(request):
    slides = Slide.objects.filter(is_active=True).order_by('order')
    home_section = HomeSection.get()
    faqs = FAQ.objects.filter(is_active=True)
    featured_disciplines = Discipline.objects.filter(is_featured=True, is_active=True)[:6]
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_at')[:3]
    featured_testimonials = Testimonial.objects.filter(is_featured=True, is_active=True)[:3]
    return render(request, 'home/index.html', {
        'slides': slides,
        'home_section': home_section,
        'faqs': faqs,
        'featured_disciplines': featured_disciplines,
        'recent_posts': recent_posts,
        'featured_testimonials': featured_testimonials,
        'active_nav': 'home',
    })


def nosotros(request):
    about = AboutPage.get()
    founders = Founder.objects.filter(is_active=True)
    return render(request, 'nosotros/index.html', {
        'about': about,
        'founders': founders,
        'active_nav': 'nosotros',
    })


def contacto(request):
    from django.contrib import messages
    from django.core.mail import send_mail
    from django.conf import settings as django_settings
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        servicio = request.POST.get('servicio', '').strip()
        asunto_raw = request.POST.get('asunto', '').strip()
        asunto = asunto_raw or ('Consulta sobre: ' + servicio if servicio else 'Mensaje desde el sitio web')
        mensaje = request.POST.get('mensaje', '').strip()
        if nombre and email and mensaje:
            body = 'Nombre: ' + nombre + '\nEmail: ' + email + ('\nServicio: ' + servicio if servicio else '') + '\n\n' + mensaje
            try:
                send_mail(
                    subject=f"[Artistic Mold] {asunto}",
                    message=body,
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[django_settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Tu mensaje fue enviado. Nos contactaremos pronto.')
            except Exception:
                messages.error(request, 'Hubo un problema al enviar el mensaje. Por favor intenta de nuevo.')
        else:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
    return render(request, 'contacto/index.html', {'active_nav': 'contacto'})


def politica(request):
    policy = PolicyPage.get()
    if not policy.is_active:
        raise Http404
    return render(request, 'politica/index.html', {'policy': policy})
