// AstroGuide — carrusel de tarjetas de una leccion
(function () {
  const track = document.getElementById('lessonCards');
  if (!track) return;

  const cards = Array.from(track.querySelectorAll('.flip'));
  const prev = document.getElementById('carPrev');
  const next = document.getElementById('carNext');
  const dotsWrap = document.getElementById('carDots');
  const posEl = document.getElementById('carPos');
  let i = 0;

  cards.forEach(function (_, idx) {
    const d = document.createElement('button');
    d.type = 'button';
    d.className = 'car-dot';
    d.setAttribute('aria-label', 'Tarjeta ' + (idx + 1));
    d.addEventListener('click', function () { go(idx); });
    dotsWrap.appendChild(d);
  });

  function render() {
    cards.forEach(function (c, idx) {
      c.hidden = idx !== i;
      if (idx !== i) c.classList.remove('is-flipped');
    });
    Array.from(dotsWrap.children).forEach(function (d, idx) {
      d.classList.toggle('on', idx === i);
    });
    posEl.textContent = i + 1;
    prev.disabled = i === 0;
    next.disabled = i === cards.length - 1;
  }

  function go(n) {
    i = Math.max(0, Math.min(cards.length - 1, n));
    render();
  }

  prev.addEventListener('click', function () { go(i - 1); });
  next.addEventListener('click', function () { go(i + 1); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') go(i - 1);
    else if (e.key === 'ArrowRight') go(i + 1);
  });

  render();
})();
