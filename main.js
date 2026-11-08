// Basqah site: language, nav state, reveal on scroll, before/after switch, team accordion.
(function () {
  var root = document.documentElement;

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

  // team: each card opens to show contact links
  document.querySelectorAll('.m-head').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      btn.closest('.member').classList.toggle('open', !open);
    });
  });

  // reveal on scroll (staggered within each group)
  var items = document.querySelectorAll('.reveal');
  if (!root.classList.contains('js') || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var sibs = Array.prototype.filter.call(e.target.parentElement.children, function (c) { return c.classList.contains('reveal'); });
      e.target.style.transitionDelay = Math.min(sibs.indexOf(e.target), 5) * 80 + 'ms';
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();
