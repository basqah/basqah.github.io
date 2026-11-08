// Basqah site: language, nav state, scroll story, team flip cards, reveal on scroll.
(function () {
  var root = document.documentElement;
  var hasJS = root.classList.contains('js');

  document.getElementById('langBtn').addEventListener('click', function () {
    var lang = root.lang === 'ar' ? 'en' : 'ar';
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    try { localStorage.setItem('basqah-lang', lang); } catch (e) {}
  });

  // nav: transparent over the hero, solid light bar after it
  var nav = document.getElementById('nav');
  var hero = document.querySelector('.hero');
  function onScroll() { nav.classList.toggle('solid', window.scrollY > hero.offsetHeight - 80); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // "From the sky to the palm"
  //   wide screens: the sticky stage follows whichever step is in the middle of the screen
  //   phones: the stage sits on top and the steps play by themselves while the section is on screen
  var stage = document.getElementById('stage');
  var steps = document.querySelectorAll('.step');
  var narrow = window.matchMedia('(max-width: 880px)');
  var current = 1, timer = null, pauseUntil = 0;
  function setStep(n) {
    current = +n;
    stage.dataset.step = current;
    steps.forEach(function (s) { s.classList.toggle('active', s.dataset.step === String(current)); });
  }
  function startAuto() {
    if (timer) return;
    timer = setInterval(function () { if (Date.now() > pauseUntil) setStep(current % 3 + 1); }, 3400);
  }
  function stopAuto() { clearInterval(timer); timer = null; }
  if ('IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (entries) {
      if (narrow.matches) return;
      entries.forEach(function (e) { if (e.isIntersecting) setStep(e.target.dataset.step); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    steps.forEach(function (s) { so.observe(s); });
    new IntersectionObserver(function (entries) {
      var on = entries[0].isIntersecting && narrow.matches && hasJS;
      if (on) startAuto(); else stopAuto();
    }, { threshold: .35 }).observe(document.getElementById('system'));
  }
  steps.forEach(function (s) {
    s.addEventListener('click', function () { setStep(s.dataset.step); pauseUntil = Date.now() + 6000; });
  });

  // team: tap a founder to flip to their contacts, tap the back to flip again.
  // A 2-D flip (squash → swap faces → open) — smooth on every device and nothing bleeds through.
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.member').forEach(function (m) {
    var front = m.querySelector('.front'), back = m.querySelector('.back'), busy = false;
    function toggle(open) {
      if (busy) return;
      var swap = function () {
        m.classList.toggle('open', open);
        front.setAttribute('aria-expanded', String(open));
        (open ? back : front).focus({ preventScroll: true });
      };
      if (reduceMotion) { swap(); return; }
      busy = true;
      m.classList.add('squash');
      setTimeout(function () { swap(); m.classList.remove('squash'); setTimeout(function () { busy = false; }, 280); }, 270);
    }
    front.addEventListener('click', function () { toggle(true); });
    back.addEventListener('click', function (e) { if (!e.target.closest('a')) toggle(false); });
    back.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('a')) { e.preventDefault(); toggle(false); }
    });
  });

  // reveal on scroll (staggered within each group); founders get "scanned" once on touch screens
  var touch = window.matchMedia('(hover: none)').matches;
  var items = document.querySelectorAll('.reveal');
  if (!hasJS || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.classList.contains('reveal'); });
      var delay = Math.min(sibs.indexOf(el), 5) * 90;
      el.style.transitionDelay = delay + 'ms';
      el.classList.add('in');
      if (touch && el.classList.contains('member')) setTimeout(function () { el.classList.add('scanned'); }, delay + 700);
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();
