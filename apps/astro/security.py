"""Utilidades de seguridad anti-abuso: rate limiting por IP y honeypot.

No dependen de paquetes externos: usan el cache de Django (LocMemCache por
defecto). Con un solo worker de gunicorn (plan free de Render) el contador es
consistente; para varios workers/instancias conviene un cache compartido
(Redis) — el algoritmo no cambia.
"""

import json
import urllib.parse
import urllib.request
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

# Campo trampa: invisible para humanos, los bots lo rellenan.
HONEYPOT_FIELD = "website"


def client_ip(request):
    """IP real del cliente. Detras del proxy de Render viene en X-Forwarded-For."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or "desconocida"


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest" or "application/json" in (
        request.content_type or ""
    )


def _too_many(request):
    msg = "Demasiados intentos. Espera un momento e intenta de nuevo."
    if _is_ajax(request):
        return JsonResponse({"error": msg}, status=429)
    return HttpResponse(msg, status=429, content_type="text/plain; charset=utf-8")


def rate_limit(scope, limit, window, methods=("POST",)):
    """Limita a `limit` peticiones por IP cada `window` segundos (ventana fija).

    Solo cuenta los `methods` indicados; el resto pasa sin tocar el contador.
    """

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if request.method in methods:
                key = f"rl:{scope}:{client_ip(request)}"
                cache.add(key, 0, window)  # inicia la ventana si no existe (no resetea TTL)
                try:
                    count = cache.incr(key)
                except ValueError:  # expiro entre el add y el incr
                    cache.set(key, 1, window)
                    count = 1
                if count > limit:
                    return _too_many(request)
            return view(request, *args, **kwargs)

        return wrapped

    return decorator


def honeypot_tripped(request):
    """True si el campo trampa viene relleno: es un bot, no un humano."""
    return bool(request.POST.get(HONEYPOT_FIELD, "").strip())


def turnstile_ok(request):
    """Verifica Cloudflare Turnstile (CAPTCHA invisible).

    Si no hay TURNSTILE_SECRET configurado, no bloquea (True) -> queda inactivo
    hasta que pongas tus llaves. Si Cloudflare no responde, tampoco bloquea para
    no dejar fuera a usuarios legitimos.
    """
    secret = getattr(settings, "TURNSTILE_SECRET", "")
    if not secret:
        return True
    token = request.POST.get("cf-turnstile-response", "")
    if not token:
        return False
    try:
        data = urllib.parse.urlencode(
            {"secret": secret, "response": token, "remoteip": client_ip(request)}
        ).encode()
        req = urllib.request.Request(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify", data=data
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return bool(json.load(resp).get("success"))
    except Exception:
        return True
