// AstroGuide — interaccion de tarjetas y progreso

// Toasts / notificaciones
(function () {
  function dismiss(toast) {
    toast.classList.add('hide');
    setTimeout(function () { toast.remove(); }, 320);
  }
  document.addEventListener('click', function (e) {
    const x = e.target.closest('.toast-x');
    if (x) dismiss(x.closest('.toast'));
  });
  document.querySelectorAll('.toast').forEach(function (toast, i) {
    setTimeout(function () { if (toast.isConnected) dismiss(toast); }, 4200 + i * 400);
  });
})();

function getCsrf() {
  const m = document.querySelector('meta[name="csrf-token"]');
  return m ? m.getAttribute('content') : '';
}

function flashToast(msg) {
  let box = document.getElementById('toasts');
  if (!box) { box = document.createElement('div'); box.className = 'toasts'; box.id = 'toasts'; document.body.appendChild(box); }
  const t = document.createElement('div');
  t.className = 'toast success';
  t.innerHTML = '<span class="toast-dot"></span><span class="toast-msg"></span><button type="button" class="toast-x" aria-label="Cerrar">&times;</button>';
  t.querySelector('.toast-msg').textContent = msg;
  box.appendChild(t);
  setTimeout(function () {
    t.classList.add('hide');
    setTimeout(function () { t.remove(); }, 320);
  }, 3200);
}

async function shareUrl(btn) {
  const url = location.origin + btn.getAttribute('data-path');
  const title = btn.getAttribute('data-title') || 'AstroGuide';
  if (navigator.share) {
    try { await navigator.share({ title: title, url: url }); return; }
    catch (e) { if (e && e.name === 'AbortError') return; }
  }
  try { await navigator.clipboard.writeText(url); flashToast('Enlace copiado al portapapeles'); }
  catch (e) { window.prompt('Copia el enlace para compartir:', url); }
}

function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  const next = cur === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('astro-theme', next); } catch (e) {}
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute('content', next === 'light' ? '#f7f8fd' : '#0a0b1e');
}

async function toggleKnown(btn) {
  const id = btn.getAttribute('data-card');
  btn.disabled = true;
  try {
    const res = await fetch('/app/tarjeta/' + id + '/dominar/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf(), 'X-Requested-With': 'XMLHttpRequest' },
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    // Estado del boton y la tarjeta
    btn.classList.toggle('on', data.known);
    btn.querySelector('.know-label').textContent = data.known ? 'Dominada' : 'Marcar como dominada';
    const card = btn.closest('.flip');
    if (card) card.classList.toggle('known', data.known);

    // Barra de progreso del tema
    const fill = document.getElementById('deckBarFill');
    if (fill) fill.style.width = data.pct + '%';
    const known = document.getElementById('deckKnown');
    if (known) known.textContent = data.known_count;
    const pct = document.getElementById('deckPct');
    if (pct) pct.textContent = data.pct;
  } catch (e) {
    console.error('No se pudo guardar el progreso:', e);
  } finally {
    btn.disabled = false;
  }
}

function speakCard(btn) {
  if (!('speechSynthesis' in window)) return;
  const speaking = btn.classList.contains('on');
  window.speechSynthesis.cancel();
  document.querySelectorAll('.tts-btn.on').forEach(function (b) { b.classList.remove('on'); });
  if (speaking) return;  // segundo clic: detiene
  const u = new SpeechSynthesisUtterance(btn.getAttribute('data-tts') || '');
  u.lang = 'es-ES';
  u.onend = function () { btn.classList.remove('on'); };
  u.onerror = function () { btn.classList.remove('on'); };
  btn.classList.add('on');
  window.speechSynthesis.speak(u);
}

// Click: botones de tarjeta (escuchar / dominar) tienen prioridad; el resto la gira
document.addEventListener('click', function (e) {
  const tts = e.target.closest('.tts-btn');
  if (tts) {
    e.stopPropagation();
    speakCard(tts);
    return;
  }
  const btn = e.target.closest('.know-btn');
  if (btn) {
    e.stopPropagation();
    toggleKnown(btn);
    return;
  }
  const flip = e.target.closest('.flip');
  if (flip) flip.classList.toggle('is-flipped');
});

if (!('speechSynthesis' in window)) document.documentElement.classList.add('no-tts');

// Accesibilidad: girar con Enter / Espacio
document.addEventListener('keydown', function (e) {
  if ((e.key === 'Enter' || e.key === ' ') && document.activeElement.classList.contains('flip')) {
    e.preventDefault();
    document.activeElement.classList.toggle('is-flipped');
  }
});

// Reportar pregunta (en quiz y repaso)
document.addEventListener('click', function (e) {
  const toggle = e.target.closest('.q-report');
  if (toggle) {
    const current = document.querySelector('.q-block:not([hidden]) .q-report-wrap');
    document.querySelectorAll('.q-report-panel').forEach(function (p) {
      if (!current || p.parentElement !== current) p.hidden = true;
    });
    const panel = current && current.querySelector('.q-report-panel');
    if (panel) panel.hidden = !panel.hidden;
    return;
  }
  const reason = e.target.closest('.q-report-panel [data-reason]');
  if (reason) {
    const wrap = reason.closest('.q-report-wrap');
    sendReport(wrap, reason.getAttribute('data-reason'));
  }
});

async function sendReport(wrap, reason) {
  if (!wrap || wrap.dataset.sent) return;
  wrap.dataset.sent = '1';
  try {
    await fetch(wrap.dataset.url, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: reason }),
    });
  } catch (e) {
    console.error('No se pudo enviar el reporte:', e);
  }
  wrap.innerHTML = '<span class="q-report-done">Gracias, lo revisaremos.</span>';
}

// Ruta: une los planetas con una curva punteada medida sobre su posicion real.
// El tramo que llega a una leccion bloqueada queda mas tenue.
(function () {
  var SVGNS = 'http://www.w3.org/2000/svg';
  function num(v) { return v.toFixed(1); }
  function draw() {
    document.querySelectorAll('.sky-path').forEach(function (box) {
      if (!box.getClientRects().length) return;
      var svg = box.querySelector('[data-path]');
      if (!svg) return;
      var nodes = Array.prototype.slice.call(box.querySelectorAll('.sky-node'));
      svg.innerHTML = '';
      if (nodes.length < 2) return;
      var br = box.getBoundingClientRect();
      svg.setAttribute('viewBox', '0 0 ' + num(br.width) + ' ' + num(br.height));
      for (var i = 0; i < nodes.length - 1; i++) {
        var a = nodes[i].querySelector('[data-planet]');
        var b = nodes[i + 1].querySelector('[data-planet]');
        if (!a || !b) continue;
        var ar = a.getBoundingClientRect();
        var bp = b.getBoundingClientRect();
        var nr = nodes[i].getBoundingClientRect();
        var nr2 = nodes[i + 1].getBoundingClientRect();
        var x1 = (ar.left + ar.right) / 2 - br.left;
        var y1 = ar.bottom - br.top;
        var x2 = (bp.left + bp.right) / 2 - br.left;
        var y2 = bp.top - br.top;
        var gapTop = nr.bottom - br.top + 8;
        var gapBot = nr2.top - br.top - 8;
        var lane = (gapTop + gapBot) / 2;
        if (gapBot < gapTop + 10) lane = (y1 + y2) / 2;
        var mid = (x1 + x2) / 2;
        var d = 'M ' + num(x1) + ' ' + num(y1) +
          ' C ' + num(x1) + ' ' + num(lane) + ', ' + num(mid) + ' ' + num(lane) + ', ' + num(mid) + ' ' + num(lane) +
          ' C ' + num(mid) + ' ' + num(lane) + ', ' + num(x2) + ' ' + num(lane) + ', ' + num(x2) + ' ' + num(y2);
        var path = document.createElementNS(SVGNS, 'path');
        path.setAttribute('class', nodes[i + 1].classList.contains('locked') ? 'sky-ln ahead' : 'sky-ln');
        path.setAttribute('d', d);
        svg.appendChild(path);
      }
    });
  }
  function focusCurrent() {
    var cur = document.getElementById('route-current');
    if (!cur) return;
    var top = cur.getBoundingClientRect().top;
    if (top < window.innerHeight * 0.72) return;
    var y = top + window.pageYOffset - 96;
    window.scrollTo(0, Math.max(0, y));
  }
  function boot() {
    draw();
    focusCurrent();
    document.querySelectorAll('.sky-fold').forEach(function (fold) {
      fold.addEventListener('toggle', draw);
    });
  }
  if (document.querySelector('.sky-path') || document.querySelector('.sky-fold')) {
    if (document.readyState !== 'loading') boot();
    else document.addEventListener('DOMContentLoaded', boot);
    var t;
    window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(draw, 150); });
  }
})();
