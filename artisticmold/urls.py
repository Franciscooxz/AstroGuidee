from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.defaults import page_not_found, server_error

from apps.core.sitemaps import sitemaps


def robots_txt(request):
    domain = request.build_absolute_uri("/")[:-1]
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /panel/\n"
        "Disallow: /django-admin/\n"
        "\n"
        "Sitemap: {}/sitemap.xml\n".format(domain)
    )
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"
    ),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("apps.astro.urls")),
    path("gestion/", include("apps.astro.panel_urls")),
    path("arte/", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path("artes/", include("apps.disciplines.urls")),
    path("galeria/", include("apps.gallery.urls")),
    path("servicios/", include("apps.services.urls")),
    path("recursos/", include("apps.resources.urls")),
    path("panel/", include("apps.core.panel_urls")),
    path("test-404/", lambda request: page_not_found(request, Exception())),
    path("test-500/", lambda request: server_error(request)),
]

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
