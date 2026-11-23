from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        # Zonas privadas o de accion (sin valor para buscadores): no rastrear.
        "Disallow: /app/\n"
        "Disallow: /gestion/\n"
        "Disallow: /django-admin/\n"
        "Disallow: /registro/\n"
        "Disallow: /entrar/\n"
        "Disallow: /salir/\n"
        "Disallow: /recuperar/\n"
        "Crawl-delay: 5\n"
    )
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("apps.astro.urls")),
    path("gestion/", include("apps.astro.panel_urls")),
]

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
