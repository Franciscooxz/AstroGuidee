// AstroGuide — motor unico de quiz (una pregunta a la vez).
// El modo (quiz | review | exam | duel) se lee de #quizStage[data-mode]
// y decide solo la pantalla de resultado. El resto de la interaccion es comun.
(function () {
  const stage = document.getElementById("quizStage");
  if (!stage) return;

  const mode = stage.dataset.mode || "quiz";
  const blocks = Array.from(stage.querySelectorAll(".q-block"));
  const bar = document.getElementById("quizBar");
  const total = blocks.length;
  const answers = {};
  let idx = 0;

  // Vidas (solo en modo quiz; en el resto no existe #quizHearts y es no-op)
  const heartsBox = document.getElementById("quizHearts");
  const heartsMax = heartsBox ? parseInt(heartsBox.dataset.max, 10) || 0 : 0;
  let heartsLeft = heartsBox ? parseInt(heartsBox.dataset.hearts, 10) || 0 : 0;
  function heartSvg(full) {
    return (
      '<svg class="ico" width="22" height="22" viewBox="0 0 64 64"><use href="#i-heart' +
      (full ? "" : "-empty") +
      '"></use></svg>'
    );
  }
  function renderHearts() {
    if (!heartsBox) return;
    let out = "";
    for (let k = 0; k < heartsMax; k++) out += heartSvg(k < heartsLeft);
    heartsBox.innerHTML = out;
  }
  function loseHeart() {
    if (heartsLeft > 0) {
      heartsLeft--;
      renderHearts();
    }
  }
  renderHearts();

  // ---- Utilidades ----
  function csrf() {
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute("content") : "";
  }
  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
  function norm(s) {
    s = (s || "").normalize("NFD");
    let out = "";
    for (let k = 0; k < s.length; k++) {
      if (s.charCodeAt(k) < 128) out += s[k];
    }
    return out.toLowerCase().trim();
  }
  function showExplain(block) {
    const ex = block.querySelector(".q-explain");
    if (ex) ex.hidden = false;
  }

  // Barajar las opciones (solo en preguntas con opciones)
  blocks.forEach(function (b) {
    const wrap = b.querySelector(".q-options");
    if (wrap)
      shuffle(Array.from(wrap.children)).forEach(function (el) {
        wrap.appendChild(el);
      });
  });

  function setBar() {
    bar.style.width = (idx / total) * 100 + "%";
  }
  setBar();

  // ---- Interaccion ----
  stage.addEventListener("click", function (e) {
    const opt = e.target.closest(".q-opt");
    if (opt) return onAnswer(opt);
    const check = e.target.closest(".q-check");
    if (check) return onCheckText(check.closest(".q-block"));
    const next = e.target.closest(".q-next");
    if (next) return onNext();
  });
  stage.addEventListener("keydown", function (e) {
    if (e.key !== "Enter") return;
    const block = e.target.closest(".q-block");
    if (block && block.dataset.qtype === "text" && !block.classList.contains("answered")) {
      e.preventDefault();
      onCheckText(block);
    }
  });

  function onCheckText(block) {
    if (block.classList.contains("answered")) return;
    const input = block.querySelector(".q-text-input");
    const val = input.value.trim();
    if (!val) return;
    block.classList.add("answered");
    answers[block.dataset.qid] = val;

    const accepted = Array.from(block.querySelectorAll(".q-answers span")).map(function (s) {
      return norm(s.dataset.text);
    });
    const ok = accepted.indexOf(norm(val)) !== -1;
    input.classList.add(ok ? "correct" : "wrong");
    input.disabled = true;
    block.querySelector(".q-check").disabled = true;
    if (!ok) {
      loseHeart();
      const first = block.querySelector(".q-answers span");
      const sol = document.createElement("div");
      sol.className = "q-solution";
      sol.textContent = "Respuesta correcta: " + (first ? first.dataset.text : "");
      block.insertBefore(sol, block.querySelector(".q-next"));
    }
    showExplain(block);
    block.querySelector(".q-next").disabled = false;
  }

  function onAnswer(opt) {
    const block = opt.closest(".q-block");
    if (block.classList.contains("answered")) return;
    block.classList.add("answered");

    answers[block.dataset.qid] = opt.dataset.oid;
    const correct = opt.dataset.correct === "1";
    opt.classList.add(correct ? "correct" : "wrong");
    if (!correct) {
      loseHeart();
      const right = block.querySelector('.q-opt[data-correct="1"]');
      if (right) right.classList.add("correct");
    }
    block.querySelectorAll(".q-opt").forEach(function (o) {
      o.classList.add("locked");
    });
    showExplain(block);
    block.querySelector(".q-next").disabled = false;
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
        method: "POST",
        headers: { "X-CSRFToken": csrf(), "Content-Type": "application/json" },
        body: JSON.stringify({ answers: answers }),
      });
      data = await res.json();
    } catch (e) {
      console.error("No se pudo registrar el resultado:", e);
    }
    renderResult(data);
  }

  function confetti() {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var canvas = document.createElement("canvas");
    canvas.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:9999";
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    document.body.appendChild(canvas);
    var ctx = canvas.getContext("2d");
    var colors = ["#4f7cff", "#8b5cff", "#b18bff", "#ffce4d", "#ff6b81", "#3ddc84"];
    var parts = [];
    for (var i = 0; i < 90; i++) {
      parts.push({
        x: Math.random() * canvas.width,
        y: -20 - Math.random() * canvas.height * 0.4,
        w: 6 + Math.random() * 6,
        h: 8 + Math.random() * 8,
        c: colors[i % colors.length],
        vy: 2 + Math.random() * 3.5,
        vx: -1.5 + Math.random() * 3,
        rot: Math.random() * 6,
        vr: -0.2 + Math.random() * 0.4,
      });
    }
    var start = Date.now();
    (function frame() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      parts.forEach(function (p) {
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.c;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      });
      if (Date.now() - start < 2600) requestAnimationFrame(frame);
      else canvas.remove();
    })();
  }

  function badge(cls, icon) {
    return (
      '<div class="res-badge ' +
      cls +
      '"><svg class="ico" width="44" height="44" viewBox="0 0 64 64"><use href="#i-' +
      icon +
      '"></use></svg></div>'
    );
  }
  function plural(n) {
    return n === 1 ? "" : "s";
  }

  // ---- Pantallas de resultado por modo ----
  function achievementsHtml(list) {
    if (!list || !list.length) return "";
    let out = '<div class="res-achs">';
    list.forEach(function (a) {
      out +=
        '<div class="res-ach"><svg class="ico" width="26" height="26" viewBox="0 0 64 64"><use href="#i-' +
        (a.icon || "star") +
        '"></use></svg><span>Logro: <b>' +
        a.name +
        "</b></span></div>";
    });
    return out + "</div>";
  }

  function resultQuiz(data) {
    const ruta = stage.dataset.ruta;
    const passed = data.passed;
    let rewards = "";
    if (data.xp_earned > 0) {
      rewards =
        '<div class="res-rewards"><span class="res-xp">+' +
        data.xp_earned +
        " XP" +
        (data.doubled ? " x2" : "") +
        "</span>";
      if (data.coins_earned > 0)
        rewards += '<span class="res-coins">+' + data.coins_earned + " Cosmos</span>";
      rewards += "</div>";
    } else if (passed) {
      rewards = '<div class="res-xp muted">Ya habías ganado las recompensas de esta lección</div>';
    }
    if (data.daily_bonus > 0) {
      rewards +=
        '<div class="res-daily"><svg class="ico inline" width="18" height="18" viewBox="0 0 64 64" aria-hidden="true"><use href="#i-target"></use></svg> ¡Meta diaria cumplida! +' +
        data.daily_bonus +
        " Cosmos</div>";
    }
    if (data.hearts_lost > 0) {
      rewards +=
        '<div class="res-hearts">Perdiste ' +
        data.hearts_lost +
        " vida" +
        plural(data.hearts_lost) +
        " · te quedan " +
        data.hearts +
        "/" +
        data.hearts_max +
        "</div>";
    }
    if (passed) {
      try {
        confetti();
      } catch (e) {}
    }
    const badgeClass = passed ? (data.perfect ? "perfect" : "ok") : "fail";
    return (
      '<div class="result-card ' +
      (passed ? "ok" : "fail") +
      '">' +
      badge(badgeClass, passed ? "check" : "x") +
      "<h2>" +
      (passed ? (data.perfect ? "¡Perfecto!" : "¡Lección completada!") : "Casi lo tienes") +
      "</h2>" +
      '<p class="res-score">Acertaste <b>' +
      data.correct +
      "</b> de <b>" +
      data.total +
      "</b></p>" +
      (!passed && data.needed
        ? '<p class="res-needed">Necesitabas <b>' + data.needed + "</b> para aprobar este nivel</p>"
        : "") +
      rewards +
      '<div class="res-stats"><span>Racha: <b>' +
      data.streak +
      "</b> día" +
      plural(data.streak) +
      "</span>" +
      "<span>Total: <b>" +
      data.total_xp +
      " XP</b></span>" +
      "<span><b>" +
      data.total_coins +
      "</b> Cosmos</span></div>" +
      achievementsHtml(data.newly_achievements) +
      '<div class="res-actions">' +
      (passed ? "" : '<a href="" onclick="location.reload();return false;" class="btn">Reintentar</a>') +
      '<a href="' +
      ruta +
      '" class="btn btn-primary">Volver a la ruta →</a>' +
      "</div></div>"
    );
  }

  function resultReview(data) {
    const ruta = stage.dataset.ruta;
    const perfect = data.correct === data.total && data.total > 0;
    if (perfect) {
      try {
        confetti();
      } catch (e) {}
    }
    let rewards = "";
    if (data.xp_earned > 0) {
      rewards = '<div class="res-rewards"><span class="res-xp">+' + data.xp_earned + " XP</span></div>";
    }
    return (
      '<div class="result-card ok">' +
      badge(perfect ? "perfect" : "ok", "progress") +
      "<h2>" +
      (perfect ? "¡Repaso perfecto!" : "¡Repaso hecho!") +
      "</h2>" +
      '<p class="res-score">Recordaste <b>' +
      data.correct +
      "</b> de <b>" +
      data.total +
      "</b></p>" +
      rewards +
      '<div class="res-stats"><span>Racha: <b>' +
      data.streak +
      "</b> día" +
      plural(data.streak) +
      "</span>" +
      "<span>Total: <b>" +
      data.total_xp +
      " XP</b></span></div>" +
      '<p class="res-srs">Las que fallaste volverán pronto; las que acertaste, más adelante.</p>' +
      '<div class="res-actions">' +
      '<a href="' +
      window.location.pathname +
      '" class="btn">Repasar más</a>' +
      '<a href="' +
      ruta +
      '" class="btn btn-primary">Volver a la ruta →</a>' +
      "</div></div>"
    );
  }

  function resultExam(data) {
    const cert = stage.dataset.cert;
    const passed = data.passed;
    if (passed) {
      try {
        confetti();
      } catch (e) {}
    }
    let rewards = "";
    if (data.bonus > 0)
      rewards = '<div class="res-rewards"><span class="res-coins">+' + data.bonus + " Cosmos</span></div>";
    const title = passed
      ? data.honors
        ? "¡Aprobado con honores!"
        : "¡Examen superado!"
      : "No alcanzaste el 80%";
    return (
      '<div class="result-card ' +
      (passed ? "ok" : "fail") +
      '">' +
      badge(passed ? (data.honors ? "perfect" : "ok") : "fail", passed ? "trophy" : "x") +
      "<h2>" +
      title +
      "</h2>" +
      '<p class="res-score">Nota: <b>' +
      data.pct +
      "%</b> · " +
      data.correct +
      "/" +
      data.total +
      "</p>" +
      rewards +
      '<div class="res-stats"><span>Mejor nota: <b>' +
      data.best_score +
      "%</b></span></div>" +
      '<div class="res-actions">' +
      (passed ? "" : '<a href="" onclick="location.reload();return false;" class="btn">Reintentar</a>') +
      '<a href="' +
      cert +
      '" class="btn btn-primary">Ver certificado →</a>' +
      "</div></div>"
    );
  }

  function resultDuel(data) {
    const back = stage.dataset.duels;
    let title, cls, icon, sub;
    if (!data.both_done) {
      title = "Reto enviado";
      cls = "ok";
      icon = "flame";
      sub = "Acertaste <b>" + data.my_score + "/" + data.total + "</b>. Esperando a tu rival...";
    } else if (data.outcome === "win") {
      title = "Ganaste!";
      cls = "perfect";
      icon = "trophy";
      try {
        confetti();
      } catch (e) {}
      sub = "Tu <b>" + data.my_score + "</b> · rival <b>" + data.rival_score + "</b>";
    } else if (data.outcome === "lose") {
      title = "Perdiste";
      cls = "fail";
      icon = "x";
      sub = "Tu <b>" + data.my_score + "</b> · rival <b>" + data.rival_score + "</b>";
    } else {
      title = "Empate";
      cls = "ok";
      icon = "flame";
      sub = "Ambos <b>" + data.my_score + "/" + data.total + "</b>";
    }
    return (
      '<div class="result-card">' +
      badge(cls, icon) +
      "<h2>" +
      title +
      '</h2><p class="res-score">' +
      sub +
      "</p>" +
      '<div class="res-actions"><a href="' +
      back +
      '" class="btn btn-primary">Ver mis duelos →</a></div></div>'
    );
  }

  function errorCard() {
    const back = stage.dataset.ruta || stage.dataset.cert || stage.dataset.duels || "/app/";
    return (
      '<div class="result-card"><h2>Ups</h2><p>No pudimos guardar tu resultado. Revisa tu conexión.</p>' +
      '<a href="' +
      back +
      '" class="btn btn-primary">Volver</a></div>'
    );
  }

  function renderResult(data) {
    stage.hidden = true;
    bar.style.width = "100%";
    const box = document.getElementById("quizResult");
    if (!data) {
      box.innerHTML = errorCard();
      box.hidden = false;
      return;
    }
    let html;
    if (mode === "review") html = resultReview(data);
    else if (mode === "exam") html = resultExam(data);
    else if (mode === "duel") html = resultDuel(data);
    else html = resultQuiz(data);
    box.innerHTML = html;
    box.hidden = false;
  }
})();
