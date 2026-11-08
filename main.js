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

  // "From the sky to the palm": the sticky stage follows whichever step is in the middle of the screen
  var stage = document.getElementById('stage');
  var steps = document.querySelectorAll('.step');
  function setStep(n) {
    stage.dataset.step = n;
    steps.forEach(function (s) { s.classList.toggle('active', s.dataset.step === String(n)); });
  }
  if ('IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) setStep(e.target.dataset.step); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    steps.forEach(function (s) { so.observe(s); });
  }
  steps.forEach(function (s) { s.addEventListener('click', function () { setStep(s.dataset.step); }); });

  // team: tap a founder to flip the card to their contacts
  document.querySelectorAll('.member').forEach(function (m) {
    var front = m.querySelector('.front');
    function toggle(open) {
      m.classList.toggle('open', open);
      front.setAttribute('aria-expanded', String(open));
    }
    front.addEventListener('click', function () { toggle(true); });
    m.querySelector('.b-close').addEventListener('click', function () { toggle(false); front.focus(); });
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
