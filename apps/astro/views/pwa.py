"""Vistas: pwa."""

from .common import *  # noqa: F401,F403

# ---------- PWA (manifest + service worker) ----------


def manifest(request):
    from django.templatetags.static import static

    data = {
        "name": "AstroGuide",
        "short_name": "AstroGuide",
        "description": "Aprende astronomia con tarjetas y quizzes.",
        "start_url": "/app/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#05060f",
        "theme_color": "#0a0b1e",
        "lang": "es",
        "icons": [
            {"src": static("astro/img/icon-192.png"), "sizes": "192x192", "type": "image/png"},
            {"src": static("astro/img/icon-512.png"), "sizes": "512x512", "type": "image/png"},
            {
                "src": static("astro/img/icon-maskable-512.png"),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable",
            },
        ],
    }
    return JsonResponse(data, content_type="application/manifest+json")


def service_worker(request):
    resp = render(request, "astro/sw.js", content_type="application/javascript")
    resp["Service-Worker-Allowed"] = "/"
    resp["Cache-Control"] = "no-cache"
    return resp
