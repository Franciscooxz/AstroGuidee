from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.files.storage import default_storage
import uuid, os


def _int(value, default=0):
    """Convierte a int de forma segura — evita crash 500 con input no numérico."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _unique_slug(model_class, base_slug, exclude_pk=None):
    """Genera un slug único añadiendo sufijo numérico si ya existe."""
    from django.utils.text import slugify
    slug = base_slug
    qs = model_class.objects.filter(slug=slug)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    counter = 1
    while qs.exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
        qs = model_class.objects.filter(slug=slug)
        if exclude_pk:
            qs = qs.exclude(pk=exclude_pk)
    return slug

from .models import SiteConfig, HomeSection, AboutPage, Founder
from apps.slider.models import Slide
from apps.blog.models import Post, BlogCategory
from apps.disciplines.models import Discipline, DisciplineCategory
from apps.faq.models import FAQ
from apps.testimonials.models import Testimonial
from apps.gallery.models import Album, Photo
from apps.services.models import Service, ServicePDF
from apps.resources.models import ResourceCategory, Resource


def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('panel:dashboard')
        messages.error(request, 'Credenciales incorrectas o sin permisos de staff.')
    return render(request, 'panel/login.html')


@require_POST
def panel_logout(request):
    logout(request)
    return redirect('panel:login')


@login_required(login_url='/panel/login/')
def dashboard(request):
    context = {
        'total_slides': Slide.objects.count(),
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(is_published=True).count(),
        'total_disciplines': Discipline.objects.count(),
        'total_faqs': FAQ.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_albums': Album.objects.count(),
        'total_services': Service.objects.count(),
        'recent_posts': Post.objects.order_by('-created_at')[:5],
    }
    return render(request, 'panel/dashboard.html', context)


# ── SLIDER ──────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def slider_list(request):
    slides = Slide.objects.all()
    return render(request, 'panel/slider/list.html', {'slides': slides})


@login_required(login_url='/panel/login/')
def slide_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        subtitle = request.POST.get('subtitle', '')
        link_url = request.POST.get('link_url', '')
        link_text = request.POST.get('link_text', 'Ver mas')
        order = _int(request.POST.get('order'), 0)
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if image:
            Slide.objects.create(title=title, subtitle=subtitle, link_url=link_url,
                                 link_text=link_text, order=order, is_active=is_active, image=image)
            messages.success(request, 'Slide creado correctamente.')
            return redirect('panel:slider_list')
        messages.error(request, 'Debes seleccionar una imagen.')
    return render(request, 'panel/slider/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def slide_edit(request, pk):
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        slide.title = request.POST.get('title', slide.title)
        slide.subtitle = request.POST.get('subtitle', slide.subtitle)
        slide.link_url = request.POST.get('link_url', slide.link_url)
        slide.link_text = request.POST.get('link_text', slide.link_text) or 'Ver mas'
        slide.order = _int(request.POST.get('order'), slide.order)
        slide.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            slide.image = request.FILES['image']
        slide.save()
        messages.success(request, 'Slide actualizado.')
        return redirect('panel:slider_list')
    return render(request, 'panel/slider/form.html', {'obj': slide})


@login_required(login_url='/panel/login/')
def slide_delete(request, pk):
    slide = get_object_or_404(Slide, pk=pk)
    if request.method == 'POST':
        slide.delete()
        messages.success(request, 'Slide eliminado.')
    return redirect('panel:slider_list')


# ── BLOG ────────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def blog_list(request):
    posts = Post.objects.select_related('category', 'author').all()
    return render(request, 'panel/blog/list.html', {'posts': posts})


@login_required(login_url='/panel/login/')
def post_create(request):
    categories = BlogCategory.objects.all()
    if request.method == 'POST':
        from django.utils.text import slugify
        title = request.POST.get('title', '')
        if title:
            post = Post(
                title=title,
                slug=_unique_slug(Post, slugify(title)),
                category_id=request.POST.get('category') or None,
                excerpt=request.POST.get('excerpt', ''),
                content=request.POST.get('content', ''),
                author=request.user,
                is_published='is_published' in request.POST,
                is_featured='is_featured' in request.POST,
            )
            if post.is_published:
                post.published_at = timezone.now()
            if request.FILES.get('cover'):
                post.cover = request.FILES['cover']
            post.save()
            messages.success(request, 'Post creado.')
            return redirect('panel:blog_list')
        messages.error(request, 'El titulo es obligatorio.')
    return render(request, 'panel/blog/form.html', {'obj': None, 'categories': categories})


@login_required(login_url='/panel/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = BlogCategory.objects.all()
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.category_id = request.POST.get('category') or None
        post.excerpt = request.POST.get('excerpt', post.excerpt)
        post.content = request.POST.get('content', post.content)
        was_published = post.is_published
        post.is_published = 'is_published' in request.POST
        post.is_featured = 'is_featured' in request.POST
        if post.is_published and not was_published:
            post.published_at = timezone.now()
        if request.FILES.get('cover'):
            post.cover = request.FILES['cover']
        post.save()
        messages.success(request, 'Post actualizado.')
        return redirect('panel:blog_list')
    return render(request, 'panel/blog/form.html', {'obj': post, 'categories': categories})


@login_required(login_url='/panel/login/')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado.')
    return redirect('panel:blog_list')


# ── DISCIPLINES ─────────────────────────────────────────
@login_required(login_url='/panel/login/')
def disciplines_list(request):
    cats = DisciplineCategory.objects.prefetch_related('disciplines').all()
    disciplines = Discipline.objects.select_related('category').all()
    return render(request, 'panel/disciplines/list.html', {'disciplines': disciplines, 'cats': cats})


@login_required(login_url='/panel/login/')
def discipline_create(request):
    categories = DisciplineCategory.objects.all()
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', '')
        if name:
            d = Discipline(
                name=name,
                slug=_unique_slug(Discipline, slugify(name)),
                category_id=request.POST.get('category'),
                description=request.POST.get('description', ''),
                is_featured='is_featured' in request.POST,
                is_active='is_active' in request.POST,
                order=_int(request.POST.get('order'), 0),
            )
            if request.FILES.get('image'):
                d.image = request.FILES['image']
            d.save()
            messages.success(request, 'Disciplina creada.')
            return redirect('panel:disciplines_list')
        messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'panel/disciplines/form.html', {'obj': None, 'categories': categories})


@login_required(login_url='/panel/login/')
def discipline_edit(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    categories = DisciplineCategory.objects.all()
    if request.method == 'POST':
        discipline.name = request.POST.get('name', discipline.name)
        discipline.category_id = request.POST.get('category')
        discipline.description = request.POST.get('description', discipline.description)
        discipline.is_featured = 'is_featured' in request.POST
        discipline.is_active = 'is_active' in request.POST
        discipline.order = _int(request.POST.get('order'), discipline.order)
        if request.FILES.get('image'):
            discipline.image = request.FILES['image']
        discipline.save()
        messages.success(request, 'Disciplina actualizada.')
        return redirect('panel:disciplines_list')
    return render(request, 'panel/disciplines/form.html', {'obj': discipline, 'categories': categories})


@login_required(login_url='/panel/login/')
def discipline_delete(request, pk):
    d = get_object_or_404(Discipline, pk=pk)
    if request.method == 'POST':
        d.delete()
        messages.success(request, 'Disciplina eliminada.')
    return redirect('panel:disciplines_list')


# ── DISCIPLINE CATEGORIES ────────────────────────────────
@login_required(login_url='/panel/login/')
def discipline_categories_list(request):
    cats = DisciplineCategory.objects.annotate_discipline_count() if hasattr(DisciplineCategory, 'annotate_discipline_count') else DisciplineCategory.objects.all()
    from django.db.models import Count
    cats = DisciplineCategory.objects.annotate(n=Count('disciplines')).order_by('order', 'name')
    return render(request, 'panel/disciplines/categories.html', {'cats': cats})


@login_required(login_url='/panel/login/')
def discipline_category_create(request):
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', '').strip()
        if name:
            slug = _unique_slug(DisciplineCategory, slugify(name))
            DisciplineCategory.objects.create(
                name=name,
                slug=slug,
                icon=request.POST.get('icon', 'fa-star').strip() or 'fa-star',
                color=request.POST.get('color', '#F5C518').strip() or '#F5C518',
                order=_int(request.POST.get('order'), 0),
            )
            messages.success(request, 'Categoría creada.')
            return redirect('panel:discipline_categories_list')
        messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'panel/disciplines/category_form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def discipline_category_edit(request, pk):
    cat = get_object_or_404(DisciplineCategory, pk=pk)
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', cat.name).strip()
        cat.name = name
        cat.slug = _unique_slug(DisciplineCategory, slugify(name), exclude_pk=pk)
        cat.icon = request.POST.get('icon', cat.icon).strip() or 'fa-star'
        cat.color = request.POST.get('color', cat.color).strip() or '#F5C518'
        cat.order = _int(request.POST.get('order'), cat.order)
        cat.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('panel:discipline_categories_list')
    return render(request, 'panel/disciplines/category_form.html', {'obj': cat})


@login_required(login_url='/panel/login/')
def discipline_category_delete(request, pk):
    cat = get_object_or_404(DisciplineCategory, pk=pk)
    if request.method == 'POST':
        if cat.disciplines.exists():
            messages.error(request, 'No se puede eliminar: tiene disciplinas asociadas.')
        else:
            cat.delete()
            messages.success(request, 'Categoría eliminada.')
    return redirect('panel:discipline_categories_list')


# ── FAQ ──────────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'panel/faq/list.html', {'faqs': faqs})


@login_required(login_url='/panel/login/')
def faq_create(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        if question and answer:
            FAQ.objects.create(question=question, answer=answer,
                               order=_int(request.POST.get('order'), 0),
                               is_active='is_active' in request.POST)
            messages.success(request, 'Pregunta creada.')
            return redirect('panel:faq_list')
    return render(request, 'panel/faq/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.question = request.POST.get('question', faq.question)
        faq.answer = request.POST.get('answer', faq.answer)
        faq.order = _int(request.POST.get('order'), faq.order)
        faq.is_active = 'is_active' in request.POST
        faq.save()
        messages.success(request, 'Pregunta actualizada.')
        return redirect('panel:faq_list')
    return render(request, 'panel/faq/form.html', {'obj': faq})


@login_required(login_url='/panel/login/')
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'Pregunta eliminada.')
    return redirect('panel:faq_list')


# ── TESTIMONIALS ─────────────────────────────────────────
@login_required(login_url='/panel/login/')
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'panel/testimonials/list.html', {'testimonials': testimonials})


@login_required(login_url='/panel/login/')
def testimonial_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        if name:
            t = Testimonial(
                name=name,
                role=request.POST.get('role', ''),
                quote=request.POST.get('quote', ''),
                event=request.POST.get('event', ''),
                is_featured='is_featured' in request.POST,
                is_active='is_active' in request.POST,
                order=_int(request.POST.get('order'), 0),
            )
            if request.FILES.get('photo'):
                t.photo = request.FILES['photo']
            t.save()
            messages.success(request, 'Testimonio creado.')
            return redirect('panel:testimonials_list')
    return render(request, 'panel/testimonials/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def testimonial_edit(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        t.name = request.POST.get('name', t.name)
        t.role = request.POST.get('role', t.role)
        t.quote = request.POST.get('quote', t.quote)
        t.event = request.POST.get('event', t.event)
        t.is_featured = 'is_featured' in request.POST
        t.is_active = 'is_active' in request.POST
        t.order = _int(request.POST.get('order'), t.order)
        if request.FILES.get('photo'):
            t.photo = request.FILES['photo']
        t.save()
        messages.success(request, 'Testimonio actualizado.')
        return redirect('panel:testimonials_list')
    return render(request, 'panel/testimonials/form.html', {'obj': t})


@login_required(login_url='/panel/login/')
def testimonial_delete(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        t.delete()
        messages.success(request, 'Testimonio eliminado.')
    return redirect('panel:testimonials_list')


# ── GALLERY ──────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def gallery_list(request):
    albums = Album.objects.prefetch_related('photos').all()
    return render(request, 'panel/gallery/list.html', {'albums': albums})


@login_required(login_url='/panel/login/')
def album_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        year = request.POST.get('year', '')
        if title:
            year_raw = (year or '').strip()
            year_val = _int(year_raw, None) if year_raw.lstrip('-').isdigit() else None
            album = Album(
                title=title, year=year_val,
                description=request.POST.get('description', ''),
                order=_int(request.POST.get('order'), 0),
                is_active='is_active' in request.POST,
            )
            if request.FILES.get('cover'):
                album.cover = request.FILES['cover']
            album.save()
            photos = request.FILES.getlist('photos')
            for i, photo_file in enumerate(photos):
                Photo.objects.create(album=album, image=photo_file, order=i)
            messages.success(request, 'Album creado con {} fotos.'.format(len(photos)))
            return redirect('panel:gallery_list')
    return render(request, 'panel/gallery/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def album_edit(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.title = request.POST.get('title', album.title)
        year_raw = request.POST.get('year', '').strip()
        album.year = _int(year_raw, None) if year_raw.lstrip('-').isdigit() else album.year
        album.description = request.POST.get('description', album.description)
        album.order = _int(request.POST.get('order'), album.order)
        album.is_active = 'is_active' in request.POST
        if request.FILES.get('cover'):
            album.cover = request.FILES['cover']
        album.save()
        photos = request.FILES.getlist('photos')
        last_order = album.photos.count()
        for i, photo_file in enumerate(photos):
            Photo.objects.create(album=album, image=photo_file, order=last_order + i)
        messages.success(request, 'Album actualizado.')
        return redirect('panel:gallery_list')
    return render(request, 'panel/gallery/form.html', {'obj': album})


@login_required(login_url='/panel/login/')
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Album eliminado.')
    return redirect('panel:gallery_list')


@login_required(login_url='/panel/login/')
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    album_pk = photo.album.pk
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Foto eliminada.')
    return redirect('panel:album_edit', pk=album_pk)


# ── SERVICES ─────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def services_list(request):
    services = Service.objects.all()
    pdfs = ServicePDF.objects.all()
    return render(request, 'panel/services/list.html', {'services': services, 'pdfs': pdfs})


@login_required(login_url='/panel/login/')
def service_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title:
            s = Service(
                title=title,
                description=request.POST.get('description', ''),
                icon=request.POST.get('icon', 'fa-star'),
                order=_int(request.POST.get('order'), 0),
                is_active='is_active' in request.POST,
            )
            if request.FILES.get('image'):
                s.image = request.FILES['image']
            s.save()
            messages.success(request, 'Servicio creado.')
            return redirect('panel:services_list')
    return render(request, 'panel/services/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.title = request.POST.get('title', service.title)
        service.description = request.POST.get('description', service.description)
        service.icon = request.POST.get('icon', 'fa-star')
        service.order = _int(request.POST.get('order'), service.order)
        service.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            service.image = request.FILES['image']
        service.save()
        messages.success(request, 'Servicio actualizado.')
        return redirect('panel:services_list')
    return render(request, 'panel/services/form.html', {'obj': service})


@login_required(login_url='/panel/login/')
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Servicio eliminado.')
    return redirect('panel:services_list')


# ── BLOG CATEGORIES ──────────────────────────────────────
@login_required(login_url='/panel/login/')
def blog_categories_list(request):
    from django.db.models import Count
    cats = BlogCategory.objects.annotate(n=Count('posts')).order_by('order', 'name')
    return render(request, 'panel/blog/categories.html', {'cats': cats})


@login_required(login_url='/panel/login/')
def blog_category_create(request):
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', '').strip()
        if name:
            BlogCategory.objects.create(
                name=name,
                slug=_unique_slug(BlogCategory, slugify(name)),
                order=_int(request.POST.get('order'), 0),
            )
            messages.success(request, 'Categoría creada.')
            return redirect('panel:blog_categories_list')
        messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'panel/blog/category_form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def blog_category_edit(request, pk):
    cat = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', cat.name).strip()
        cat.name = name
        cat.slug = _unique_slug(BlogCategory, slugify(name), exclude_pk=pk)
        cat.order = _int(request.POST.get('order'), cat.order)
        cat.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('panel:blog_categories_list')
    return render(request, 'panel/blog/category_form.html', {'obj': cat})


@login_required(login_url='/panel/login/')
def blog_category_delete(request, pk):
    cat = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Categoría eliminada. Los posts que la usaban quedaron sin categoría.')
    return redirect('panel:blog_categories_list')


# ── RESOURCES ────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def resources_list(request):
    categories = ResourceCategory.objects.prefetch_related('items').all()
    return render(request, 'panel/resources/list.html', {'categories': categories})


@login_required(login_url='/panel/login/')
def resource_create(request):
    categories = ResourceCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category_id = request.POST.get('category')
        if title and category_id:
            r = Resource(
                title=title,
                category_id=category_id,
                content=request.POST.get('content', ''),
                order=_int(request.POST.get('order'), 0),
                is_active='is_active' in request.POST,
            )
            if request.FILES.get('image'):
                r.image = request.FILES['image']
            if request.FILES.get('file'):
                r.file = request.FILES['file']
            r.save()
            messages.success(request, 'Recurso creado.')
            return redirect('panel:resources_list')
        messages.error(request, 'El título y la categoría son obligatorios.')
    return render(request, 'panel/resources/form.html', {'obj': None, 'categories': categories})


@login_required(login_url='/panel/login/')
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    categories = ResourceCategory.objects.all()
    if request.method == 'POST':
        resource.title = request.POST.get('title', resource.title)
        resource.category_id = request.POST.get('category') or resource.category_id
        resource.content = request.POST.get('content', resource.content)
        resource.order = _int(request.POST.get('order'), resource.order)
        resource.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            resource.image = request.FILES['image']
        if request.FILES.get('file'):
            resource.file = request.FILES['file']
        resource.save()
        messages.success(request, 'Recurso actualizado.')
        return redirect('panel:resources_list')
    return render(request, 'panel/resources/form.html', {'obj': resource, 'categories': categories})


@login_required(login_url='/panel/login/')
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Recurso eliminado.')
    return redirect('panel:resources_list')


@login_required(login_url='/panel/login/')
def resource_category_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            ResourceCategory.objects.create(
                title=title,
                intro=request.POST.get('intro', ''),
                icon=request.POST.get('icon', 'fa-book').strip() or 'fa-book',
                order=_int(request.POST.get('order'), 0),
            )
            messages.success(request, 'Categoría de recursos creada.')
            return redirect('panel:resources_list')
        messages.error(request, 'El título es obligatorio.')
    return render(request, 'panel/resources/category_form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def resource_category_edit(request, pk):
    cat = get_object_or_404(ResourceCategory, pk=pk)
    if request.method == 'POST':
        cat.title = request.POST.get('title', cat.title).strip() or cat.title
        cat.intro = request.POST.get('intro', cat.intro)
        cat.icon = request.POST.get('icon', cat.icon).strip() or 'fa-book'
        cat.order = _int(request.POST.get('order'), cat.order)
        cat.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('panel:resources_list')
    return render(request, 'panel/resources/category_form.html', {'obj': cat})


@login_required(login_url='/panel/login/')
def resource_category_delete(request, pk):
    cat = get_object_or_404(ResourceCategory, pk=pk)
    if request.method == 'POST':
        if cat.items.exists():
            messages.error(request, 'No se puede eliminar: tiene recursos asociados.')
        else:
            cat.delete()
            messages.success(request, 'Categoría eliminada.')
    return redirect('panel:resources_list')


# ── FOUNDERS ─────────────────────────────────────────────
@login_required(login_url='/panel/login/')
def founders_list(request):
    founders = Founder.objects.all()
    return render(request, 'panel/founders/list.html', {'founders': founders})


@login_required(login_url='/panel/login/')
def founder_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            f = Founder(
                name=name,
                role=request.POST.get('role', ''),
                bio=request.POST.get('bio', ''),
                order=_int(request.POST.get('order'), 0),
                is_active='is_active' in request.POST,
            )
            if request.FILES.get('photo'):
                f.photo = request.FILES['photo']
            f.save()
            messages.success(request, 'Fundador creado.')
            return redirect('panel:founders_list')
        messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'panel/founders/form.html', {'obj': None})


@login_required(login_url='/panel/login/')
def founder_edit(request, pk):
    f = get_object_or_404(Founder, pk=pk)
    if request.method == 'POST':
        f.name = request.POST.get('name', f.name)
        f.role = request.POST.get('role', f.role)
        f.bio = request.POST.get('bio', f.bio)
        f.order = _int(request.POST.get('order'), f.order)
        f.is_active = 'is_active' in request.POST
        if request.FILES.get('photo'):
            f.photo = request.FILES['photo']
        f.save()
        messages.success(request, 'Fundador actualizado.')
        return redirect('panel:founders_list')
    return render(request, 'panel/founders/form.html', {'obj': f})


@login_required(login_url='/panel/login/')
def founder_delete(request, pk):
    f = get_object_or_404(Founder, pk=pk)
    if request.method == 'POST':
        f.delete()
        messages.success(request, 'Fundador eliminado.')
    return redirect('panel:founders_list')


# ── POLICY PAGE ──────────────────────────────────────────
@login_required(login_url='/panel/login/')
def policy_edit(request):
    from .models import PolicyPage
    obj = PolicyPage.get()
    if request.method == 'POST':
        obj.content = request.POST.get('content', obj.content)
        obj.is_active = 'is_active' in request.POST
        obj.save()
        messages.success(request, 'Política de privacidad actualizada.')
        return redirect('panel:policy_edit')
    return render(request, 'panel/politica/form.html', {'obj': obj, 'active_panel': 'policy'})


# ── SITE CONFIG ──────────────────────────────────────────
@login_required(login_url='/panel/login/')
def site_config_edit(request):
    from .models import SiteConfig, HomeSection, AboutPage
    config = SiteConfig.get()
    home = HomeSection.get()
    about = AboutPage.get()
    if request.method == 'POST':
        section = request.POST.get('section', 'config')
        if section == 'config':
            config.site_name = request.POST.get('site_name', config.site_name)
            config.tagline = request.POST.get('tagline', config.tagline)
            config.phone = request.POST.get('phone', config.phone)
            config.whatsapp = request.POST.get('whatsapp', config.whatsapp)
            config.email = request.POST.get('email', config.email)
            config.instagram = request.POST.get('instagram', config.instagram)
            config.instagram_url = request.POST.get('instagram_url', '')
            config.facebook = request.POST.get('facebook', config.facebook)
            config.facebook_url = request.POST.get('facebook_url', '')
            config.blog_section_name = request.POST.get('blog_section_name', 'Blog')
            config.address = request.POST.get('address', '')
            config.convenio = request.POST.get('convenio', '')
            if request.FILES.get('logo'):
                config.logo = request.FILES['logo']
            if request.FILES.get('favicon'):
                config.favicon = request.FILES['favicon']
            config.save()
        elif section == 'home':
            home.title = request.POST.get('title', home.title)
            home.description = request.POST.get('description', home.description)
            home.cta_text = request.POST.get('cta_text', '')
            home.cta_url = request.POST.get('cta_url', '')
            home.stat_1_number = request.POST.get('stat_1_number', '')
            home.stat_1_label = request.POST.get('stat_1_label', '')
            home.stat_2_number = request.POST.get('stat_2_number', '')
            home.stat_2_label = request.POST.get('stat_2_label', '')
            home.stat_3_number = request.POST.get('stat_3_number', '')
            home.stat_3_label = request.POST.get('stat_3_label', '')
            if request.FILES.get('image_1'):
                home.image_1 = request.FILES['image_1']
            if request.FILES.get('image_2'):
                home.image_2 = request.FILES['image_2']
            home.save()
        elif section == 'about':
            about.historia = request.POST.get('historia', '')
            about.mision = request.POST.get('mision', '')
            about.vision = request.POST.get('vision', '')
            about.preceptos = request.POST.get('preceptos', '')
            about.simbolos = request.POST.get('simbolos', '')
            about.frase_emblema = request.POST.get('frase_emblema', '')
            if request.FILES.get('imagen_hero'):
                about.imagen_hero = request.FILES['imagen_hero']
            about.save()
        messages.success(request, 'Configuracion guardada correctamente.')
        return redirect('panel:site_config')
    return render(request, 'panel/config.html', {
        'config': config,
        'home': home,
        'about': about,
    })


# ── EDITOR MEDIA UPLOAD ───────────────────────────────────
@login_required(login_url='/panel/login/')
def editor_upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        ext = os.path.splitext(img.name)[1].lower()
        filename = 'editor/' + uuid.uuid4().hex + ext
        saved = default_storage.save(filename, img)
        from django.conf import settings
        url = settings.MEDIA_URL + saved
        return JsonResponse({'url': url})
    return JsonResponse({'error': 'No image'}, status=400)
