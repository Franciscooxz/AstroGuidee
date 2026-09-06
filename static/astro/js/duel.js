// AstroGuide — duelo 1v1 (mismo set de preguntas, sin vidas)
(function () {
  const stage = document.getElementById('quizStage');
  if (!stage) return;
  const blocks = Array.from(stage.querySelectorAll('.q-block'));
  const bar = document.getElementById('quizBar');
  const total = blocks.length;
  const answers = {};
  let idx = 0;

  function csrf() { const m = document.querySelector('meta[name="csrf-token"]'); return m ? m.getAttribute('content') : ''; }
  function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function norm(s) { s = (s || '').normalize('NFD'); let o = ''; for (let k = 0; k < s.length; k++) if (s.charCodeAt(k) < 128) o += s[k]; return o.toLowerCase().trim(); }
  function showExplain(b) { const e = b.querySelector('.q-explain'); if (e) e.hidden = false; }

  blocks.forEach(function (b) { const w = b.querySelector('.q-options'); if (w) shuffle(Array.from(w.children)).forEach(function (el) { w.appendChild(el); }); });
  function setBar() { bar.style.width = (idx / total * 100) + '%'; }
  setBar();

  stage.addEventListener('click', function (e) {
    const opt = e.target.closest('.q-opt'); if (opt) return onAnswer(opt);
    const check = e.target.closest('.q-check'); if (check) return onCheckText(check.closest('.q-block'));
    const next = e.target.closest('.q-next'); if (next) return onNext();
  });
  stage.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    const b = e.target.closest('.q-block');
    if (b && b.dataset.qtype === 'text' && !b.classList.contains('answered')) { e.preventDefault(); onCheckText(b); }
  });

  function onCheckText(block) {
    if (block.classList.contains('answered')) return;
    const input = block.querySelector('.q-text-input'); const val = input.value.trim(); if (!val) return;
    block.classList.add('answered'); answers[block.dataset.qid] = val;
    const accepted = Array.from(block.querySelectorAll('.q-answers span')).map(function (s) { return norm(s.dataset.text); });
    const ok = accepted.indexOf(norm(val)) !== -1;
    input.classList.add(ok ? 'correct' : 'wrong'); input.disabled = true; block.querySelector('.q-check').disabled = true;
    if (!ok) { const first = block.querySelector('.q-answers span'); const sol = document.createElement('div'); sol.className = 'q-solution'; sol.textContent = 'Respuesta correcta: ' + (first ? first.dataset.text : ''); block.insertBefore(sol, block.querySelector('.q-next')); }
    showExplain(block); block.querySelector('.q-next').disabled = false;
  }
  function onAnswer(opt) {
    const block = opt.closest('.q-block'); if (block.classList.contains('answered')) return;
    block.classList.add('answered'); answers[block.dataset.qid] = opt.dataset.oid;
    const correct = opt.dataset.correct === '1'; opt.classList.add(correct ? 'correct' : 'wrong');
    if (!correct) { const r = block.querySelector('.q-opt[data-correct="1"]'); if (r) r.classList.add('correct'); }
    block.querySelectorAll('.q-opt').forEach(function (o) { o.classList.add('locked'); });
    showExplain(block); block.querySelector('.q-next').disabled = false;
  }
  function onNext() { blocks[idx].hidden = true; idx++; setBar(); if (idx < total) blocks[idx].hidden = false; else finish(); }

  async function finish() {
    let data = null;
    try {
      const res = await fetch(stage.dataset.finish, { method: 'POST', headers: { 'X-CSRFToken': csrf(), 'Content-Type': 'application/json' }, body: JSON.stringify({ answers: answers }) });
      data = await res.json();
    } catch (e) { console.error('No se pudo registrar el duelo:', e); }
    showResult(data);
  }

  function confetti() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var c = document.createElement('canvas'); c.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999'; c.width = innerWidth; c.height = innerHeight; document.body.appendChild(c);
    var x = c.getContext('2d'); var cols = ['#4f7cff', '#8b5cff', '#b18bff', '#ffce4d', '#ff6b81', '#3ddc84']; var ps = [];
    for (var i = 0; i < 90; i++) ps.push({ x: Math.random() * c.width, y: -20 - Math.random() * c.height * 0.4, w: 6 + Math.random() * 6, h: 8 + Math.random() * 8, cc: cols[i % cols.length], vy: 2 + Math.random() * 3.5, vx: -1.5 + Math.random() * 3, r: Math.random() * 6, vr: -0.2 + Math.random() * 0.4 });
    var s = Date.now(); (function f() { x.clearRect(0, 0, c.width, c.height); ps.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.r += p.vr; x.save(); x.translate(p.x, p.y); x.rotate(p.r); x.fillStyle = p.cc; x.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); x.restore(); }); if (Date.now() - s < 2600) requestAnimationFrame(f); else c.remove(); })();
  }

  function showResult(data) {
    stage.hidden = true; bar.style.width = '100%';
    const box = document.getElementById('quizResult'); const back = stage.dataset.duels;
    if (!data) { box.innerHTML = '<div class="result-card"><h2>Ups</h2><p>No se pudo guardar el duelo.</p><a href="' + back + '" class="btn btn-primary">Volver</a></div>'; box.hidden = false; return; }
    let title, badge, icon, sub;
    if (!data.both_done) {
      title = 'Reto enviado'; badge = 'ok'; icon = 'flame';
      sub = 'Acertaste <b>' + data.my_score + '/' + data.total + '</b>. Esperando a tu rival...';
    } else if (data.outcome === 'win') {
      title = 'Ganaste!'; badge = 'perfect'; icon = 'trophy'; try { confetti(); } catch (e) {}
      sub = 'Tu <b>' + data.my_score + '</b> · rival <b>' + data.rival_score + '</b>';
    } else if (data.outcome === 'lose') {
      title = 'Perdiste'; badge = 'fail'; icon = 'x';
      sub = 'Tu <b>' + data.my_score + '</b> · rival <b>' + data.rival_score + '</b>';
    } else {
      title = 'Empate'; badge = 'ok'; icon = 'flame';
      sub = 'Ambos <b>' + data.my_score + '/' + data.total + '</b>';
    }
    box.innerHTML =
      '<div class="result-card">' +
      '<div class="res-badge ' + badge + '"><svg class="ico" width="44" height="44" viewBox="0 0 64 64"><use href="#i-' + icon + '"></use></svg></div>' +
      '<h2>' + title + '</h2><p class="res-score">' + sub + '</p>' +
      '<div class="res-actions"><a href="' + back + '" class="btn btn-primary">Ver mis duelos →</a></div></div>';
    box.hidden = false;
  }
})();
