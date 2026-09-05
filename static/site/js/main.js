/* Artistic Mold — Public Site JS */
document.addEventListener('DOMContentLoaded', function () {

  // ── FAQ ACCORDION ──────────────────────────────────────
  document.querySelectorAll('.am-accordion-header').forEach(function (header) {
    header.addEventListener('click', function () {
      var item = this.closest('.am-accordion-item');
      var body = item.querySelector('.am-accordion-body');
      var isOpen = item.classList.contains('open');

      document.querySelectorAll('.am-accordion-item.open').forEach(function (openItem) {
        openItem.classList.remove('open');
        openItem.querySelector('.am-accordion-body').classList.remove('open');
      });

      if (!isOpen) {
        item.classList.add('open');
        body.classList.add('open');
      }
    });
  });

  // ── LIGHTBOX ───────────────────────────────────────────
  var overlay = document.getElementById('lightboxOverlay');
  var lightboxImg = document.getElementById('lightboxImg');
  var photos = [];
  var currentIdx = 0;

  if (overlay) {
    document.querySelectorAll('.photo-item img').forEach(function (img, i) {
      photos.push(img.src);
      img.parentElement.addEventListener('click', function () {
        currentIdx = i;
        openLightbox(img.src);
      });
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeLightbox();
    });

    document.addEventListener('keydown', function (e) {
      if (!overlay.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') lightboxNext();
      if (e.key === 'ArrowLeft') lightboxPrev();
    });
  }

  window.openLightbox = function (src) {
    if (!overlay) return;
    lightboxImg.src = src;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  window.closeLightbox = function () {
    if (!overlay) return;
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  };

  window.lightboxNext = function () {
    currentIdx = (currentIdx + 1) % photos.length;
    lightboxImg.src = photos[currentIdx];
  };

  window.lightboxPrev = function () {
    currentIdx = (currentIdx - 1 + photos.length) % photos.length;
    lightboxImg.src = photos[currentIdx];
  };

  // ── SMOOTH NAVBAR SCROLL ───────────────────────────────
  var navbar = document.querySelector('.am-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 60) {
        navbar.style.boxShadow = '0 4px 24px rgba(0,0,0,0.5)';
      } else {
        navbar.style.boxShadow = 'none';
      }
    });
  }

  // ── DISCIPLINE / BLOG FILTER ───────────────────────────
  document.querySelectorAll('.filter-tab[data-cat]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cat = this.getAttribute('data-cat');
      document.querySelectorAll('.filter-tab').forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');

      document.querySelectorAll('[data-category]').forEach(function (card) {
        if (cat === 'all' || card.getAttribute('data-category') === cat) {
          card.closest('.col').style.display = '';
        } else {
          card.closest('.col').style.display = 'none';
        }
      });
    });
  });

  // ── AUTO-DISMISS MESSAGES ──────────────────────────────
  document.querySelectorAll('.am-alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
  });

});
