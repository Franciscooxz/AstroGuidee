// AstroGuide — interaccion de tarjetas y progreso

function getCsrf() {
  const m = document.querySelector('meta[name="csrf-token"]');
  return m ? m.getAttribute('content') : '';
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

// Click: el boton de "dominar" tiene prioridad; el resto de la tarjeta la gira
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.know-btn');
  if (btn) {
    e.stopPropagation();
    toggleKnown(btn);
    return;
  }
  const flip = e.target.closest('.flip');
  if (flip) flip.classList.toggle('is-flipped');
});

// Accesibilidad: girar con Enter / Espacio
document.addEventListener('keydown', function (e) {
  if ((e.key === 'Enter' || e.key === ' ') && document.activeElement.classList.contains('flip')) {
    e.preventDefault();
    document.activeElement.classList.toggle('is-flipped');
  }
});
