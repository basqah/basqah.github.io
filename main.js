// Language toggle (Arabic ⇄ English). The initial language is set in <head> before paint.
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('langBtn');
  btn.addEventListener('click', function () {
    var lang = root.lang === 'ar' ? 'en' : 'ar';
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    try { localStorage.setItem('basqah-lang', lang); } catch (e) {}
  });
})();
