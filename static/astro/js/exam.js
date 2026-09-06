// AstroGuide — examen final de unidad (todas las preguntas, sin vidas)
(function () {
  const stage = document.getElementById('quizStage');
  if (!stage) return;

  const blocks = Array.from(stage.querySelectorAll('.q-block'));
  const bar = document.getElementById('quizBar');
  const total = blocks.length;
  const answers = {};
  let idx = 0;

  function csrf() {
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute('content') : '';
  }
  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
  function norm(s) {
    s = (s || '').normalize('NFD');
    let out = '';
    for (let k = 0; k < s.length; k++) if (s.charCodeAt(k) < 128) out += s[k];
    return out.toLowerCase().trim();
  }
  function showExplain(block) {
    const ex = block.querySelector('.q-explain');
    if (ex) ex.hidden = false;
  }

  blocks.forEach(function (b) {
    const wrap = b.querySelector('.q-options');
    if (wrap) shuffle(Array.from(wrap.children)).forEach(function (el) { wrap.appendChild(el); });
  });

  function setBar() { bar.style.width = (idx / total * 100) + '%'; }
  setBar();

  stage.addEventListener('click', function (e) {
    const opt = e.target.closest('.q-opt');
    if (opt) return onAnswer(opt);
    const check = e.target.closest('.q-check');
    if (check) return onCheckText(check.closest('.q-block'));
    const next = e.target.closest('.q-next');
    if (next) return onNext();
  });
  stage.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    const block = e.target.closest('.q-block');
    if (block && block.dataset.qtype === 'text' && !block.classList.contains('answered')) {
      e.preventDefault();
      onCheckText(block);
    }
  });

  function onCheckText(block) {
    if (block.classList.contains('answered')) return;
    const input = block.querySelector('.q-text-input');
    const val = input.value.trim();
    if (!val) return;
    block.classList.add('answered');
    answers[block.dataset.qid] = val;
    const accepted = Array.from(block.querySelectorAll('.q-answers span'))
      .map(function (s) { return norm(s.dataset.text); });
    const ok = accepted.indexOf(norm(val)) !== -1;
    input.classList.add(ok ? 'correct' : 'wrong');
    input.disabled = true;
    block.querySelector('.q-check').disabled = true;
    if (!ok) {
      const first = block.querySelector('.q-answers span');
      const sol = document.createElement('div');
      sol.className = 'q-solution';
      sol.textContent = 'Respuesta correcta: ' + (first ? first.dataset.text : '');
      block.insertBefore(sol, block.querySelector('.q-next'));
    }
    showExplain(block);
    block.querySelector('.q-next').disabled = false;
  }

  function onAnswer(opt) {
    const block = opt.closest('.q-block');
    if (block.classList.contains('answered')) return;
    block.classList.add('answered');
    answers[block.dataset.qid] = opt.dataset.oid;
    const correct = opt.dataset.correct === '1';
    opt.classList.add(correct ? 'correct' : 'wrong');
    if (!correct) {
      const right = block.querySelector('.q-opt[data-correct="1"]');
      if (right) right.classList.add('correct');
    }
    block.querySelectorAll('.q-opt').forEach(function (o) { o.classList.add('locked'); });
    showExplain(block);
    block.querySelector('.q-next').disabled = false;
  }

  function onNext() {
    blocks[idx].hidden = true;
    idx++;
    setBar();
    if (idx < total) blocks[idx].hidden = false;
    else finish();
  }

  async function finish() {
    let data = null;
    try {
      const res = await fetch(stage.dataset.finish, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: answers }),
      });
      data = await res.json();
    } catch (e) { console.error('No se pudo registrar el examen:', e); }
    showResult(data);
  }

  function confetti() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999';
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    var colors = ['#4f7cff', '#8b5cff', '#b18bff', '#ffce4d', '#ff6b81', '#3ddc84'];
    var parts = [];
    for (var i = 0; i < 90; i++) parts.push({
      x: Math.random() * canvas.width, y: -20 - Math.random() * canvas.height * 0.4,
      w: 6 + Math.random() * 6, h: 8 + Math.random() * 8, c: colors[i % colors.length],
      vy: 2 + Math.random() * 3.5, vx: -1.5 + Math.random() * 3, rot: Math.random() * 6, vr: -0.2 + Math.random() * 0.4,
    });
    var start = Date.now();
    (function frame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      parts.forEach(function (p) {
        p.x += p.vx; p.y += p.vy; p.rot += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
        ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); ctx.restore();
      });
      if (Date.now() - start < 2800) requestAnimationFrame(frame); else canvas.remove();
    })();
  }

  function showResult(data) {
    stage.hidden = true;
    bar.style.width = '100%';
    const box = document.getElementById('quizResult');
    const cert = stage.dataset.cert;
    if (!data) {
      box.innerHTML = '<div class="result-card"><h2>Ups</h2><p>No pudimos guardar tu examen. Revisa tu conexion.</p>' +
        '<a href="' + cert + '" class="btn btn-primary">Volver</a></div>';
      box.hidden = false; return;
    }
    const passed = data.passed;
    if (passed) { try { confetti(); } catch (e) {} }
    let rewards = '';
    if (data.bonus > 0) rewards = '<div class="res-rewards"><span class="res-coins">+' + data.bonus + ' Cosmos</span></div>';
    const title = passed ? (data.honors ? '¡Aprobado con honores!' : '¡Examen superado!') : 'No alcanzaste el 80%';
    const icon = passed ? 'trophy' : 'x';
    box.innerHTML =
      '<div class="result-card ' + (passed ? 'ok' : 'fail') + '">' +
      '<div class="res-badge ' + (passed ? (data.honors ? 'perfect' : 'ok') : 'fail') + '">' +
      '<svg class="ico" width="44" height="44" viewBox="0 0 64 64"><use href="#i-' + icon + '"></use></svg></div>' +
      '<h2>' + title + '</h2>' +
      '<p class="res-score">Nota: <b>' + data.pct + '%</b> · ' + data.correct + '/' + data.total + '</p>' +
      rewards +
      '<div class="res-stats"><span>Mejor nota: <b>' + data.best_score + '%</b></span></div>' +
      '<div class="res-actions">' +
      (passed ? '' : '<a href="" onclick="location.reload();return false;" class="btn">Reintentar</a>') +
      '<a href="' + cert + '" class="btn btn-primary">Ver certificado →</a>' +
      '</div></div>';
    box.hidden = false;
  }
})();
