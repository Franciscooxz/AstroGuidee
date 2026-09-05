from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Post
from apps.disciplines.models import Discipline
from apps.gallery.models import Album
from apps.services.models import Service


class StaticSitemap(Sitemap):
    pages = [
        ('home', 1.0, 'weekly'),
        ('nosotros', 0.7, 'monthly'),
        ('contacto', 0.6, 'monthly'),
        ('politica', 0.3, 'yearly'),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class SectionSitemap(Sitemap):
    """Páginas de sección (listas)."""
    changefreq = 'weekly'
    priority = 0.8

    sections = [
        '/artes/',
        '/servicios/',
        '/blog/',
        '/galeria/',
        '/recursos/',
    ]

    def items(self):
        return self.sections

    def location(self, item):
        return item


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(is_published=True).order_by('-published_at')

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return '/blog/{}/'.format(obj.slug)


class DisciplineSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Discipline.objects.filter(is_active=True).order_by('order')

    def location(self, obj):
        return '/artes/{}/'.format(obj.slug)


class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Album.objects.filter(is_active=True).order_by('order')

    def location(self, obj):
        return '/galeria/{}/'.format(obj.pk)


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Service.objects.filter(is_active=True).exclude(slug=None).order_by('order')

    def location(self, obj):
        return '/servicios/{}/'.format(obj.slug)


sitemaps = {
    'static': StaticSitemap,
    'sections': SectionSitemap,
    'posts': PostSitemap,
    'disciplines': DisciplineSitemap,
    'albums': AlbumSitemap,
    'services': ServiceSitemap,
}
