// Basqah site: language toggle, solid nav on scroll, reveal-on-scroll.
(function () {
  var root = document.documentElement;

  // language (initial value is set in <head> before paint)
  document.getElementById('langBtn').addEventListener('click', function () {
    var lang = root.lang === 'ar' ? 'en' : 'ar';
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    try { localStorage.setItem('basqah-lang', lang); } catch (e) {}
  });

  // nav gets a solid background once the page scrolls
  var nav = document.getElementById('nav');
  function onScroll() { nav.classList.toggle('solid', window.scrollY > 24); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // reveal sections as they enter the viewport
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach(function (el, i) {
    el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + 'ms';
    io.observe(el);
  });
})();
