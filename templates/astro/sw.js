{% load static %}// AstroGuide — service worker (PWA: instalable + offline basico)
const CACHE = 'astroguide-{{ ASSET_VERSION }}';
const ASSETS = [
  '{% static "astro/css/astro.css" %}',
  '{% static "astro/js/astro.js" %}',
  '{% static "astro/img/icon-192.png" %}',
  '{% static "astro/img/icon-512.png" %}',
];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;  // no interceptar terceros (NASA, fuentes)

  // Estaticos: cache primero, actualiza en segundo plano
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    e.respondWith(caches.match(req).then(function (hit) {
      const net = fetch(req).then(function (res) {
        if (res && res.ok) caches.open(CACHE).then(function (c) { c.put(req, res.clone()); });
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    }));
    return;
  }

  // Navegaciones: red primero, con aviso offline si falla
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).catch(function () {
      return new Response(
        '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
        '<title>Sin conexion</title>' +
        '<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#05060f;color:#eef2ff;font-family:system-ui,sans-serif;text-align:center">' +
        '<div style="padding:24px"><h1 style="margin:0 0 8px">Sin conexion</h1>' +
        '<p style="color:#8f98c0">No hay internet ahora mismo. Vuelve a intentarlo cuando te reconectes.</p>' +
        '<button onclick="location.reload()" style="margin-top:14px;padding:10px 20px;border:none;border-radius:100px;cursor:pointer;font-weight:700;color:#fff;background:linear-gradient(150deg,#4f7cff,#8b5cff)">Reintentar</button>' +
        '</div></body>',
        { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
    }));
  }
});
