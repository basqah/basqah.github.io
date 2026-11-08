// The hero orchard — a vanilla port of the app's welcome screen (basqah-web/src/components/AerialHero.tsx):
// an illustrated aerial palm orchard with a scan line and a drone sweeping across it. Palms light up as the
// line passes and a few raise an alert colour. Each crown is drawn once into a sprite; frames only stamp sprites.
(function () {
  var canvas = document.getElementById('orchard');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var SWEEP_MS = 3800, HOLD_MS = 1800, FADE_MS = 800, CYCLE = SWEEP_MS + HOLD_MS + FADE_MS;
  var GROUND_TOP = '#0f2e1a', GROUND_BOTTOM = '#1b4f2d';
  var DIM = { base: '#1f4a2b', tip: '#2d5c37', heart: '#163a21' };
  var LIT = { base: '#3c7c4d', tip: '#bcd8c3', heart: '#24643a' };
  var URGENT = '#d94c45', WATCH = '#d99114', TONES = 3;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).has('static');

  function random(seed) { var v = seed; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }

  function layout(w, h) {
    var next = random(7), spacing = Math.max(56, Math.min(74, w / 18)), palms = [], row = 0;
    for (var y = spacing * 0.2; y < h + spacing; y += spacing * 0.86, row++) {
      for (var x = (row % 2 ? spacing / 2 : 0) - spacing * 0.3; x < w + spacing; x += spacing) {
        palms.push({ x: x + (next() - 0.5) * spacing * 0.18, y: y + (next() - 0.5) * spacing * 0.18,
          size: spacing * (0.44 + next() * 0.1), rotation: next() * Math.PI * 2, tone: Math.floor(next() * TONES), flag: '' });
      }
    }
    // a few alerts, away from the headline (which sits on the reading side)
    var rtl = document.documentElement.dir === 'rtl';
    var cand = palms.filter(function (p) {
      var side = rtl ? p.x < w * 0.42 : p.x > w * 0.58;
      return side && p.y > h * 0.22 && p.y < h * 0.8 && p.x > w * 0.06 && p.x < w * 0.94;
    });
    [0.12, 0.5, 0.86].forEach(function (at, i) { var p = cand[Math.floor(at * (cand.length - 1))]; if (p) p.flag = i === 1 ? 'watch' : 'urgent'; });
    return palms;
  }

  function crownSprite(radius, ratio, colors, tone) {
    var size = Math.ceil(radius * 2.6), s = document.createElement('canvas');
    s.width = Math.ceil(size * ratio); s.height = Math.ceil(size * ratio);
    var c = s.getContext('2d'); c.scale(ratio, ratio); c.translate(size / 2, size / 2);
    c.fillStyle = 'rgba(0,0,0,0.25)'; c.beginPath(); c.ellipse(radius * 0.16, radius * 0.2, radius * 0.95, radius * 0.9, 0, 0, Math.PI * 2); c.fill();
    var fronds = 15;
    for (var i = 0; i < fronds; i++) {
      var len = radius * (0.78 + (((i + tone * 5) * 37) % 11) / 40);
      c.save(); c.rotate((i / fronds) * Math.PI * 2 + ((((i + tone) * 53) % 7) - 3) * 0.03);
      var g = c.createLinearGradient(0, 0, len, 0); g.addColorStop(0, colors.base); g.addColorStop(1, colors.tip);
      c.fillStyle = g; c.beginPath(); c.moveTo(0, 0);
      c.quadraticCurveTo(len * 0.45, -radius * 0.11, len, radius * 0.02); c.quadraticCurveTo(len * 0.45, radius * 0.11, 0, 0); c.fill();
      c.strokeStyle = 'rgba(0,0,0,0.18)'; c.lineWidth = 0.8; c.beginPath(); c.moveTo(radius * 0.12, 0); c.lineTo(len * 0.95, radius * 0.015); c.stroke();
      c.restore();
    }
    c.fillStyle = colors.heart; c.beginPath(); c.arc(0, 0, radius * 0.16, 0, Math.PI * 2); c.fill();
    return s;
  }

  function drawDrone(x, y, now) {
    var arm = 17, d = [[-1, -1], [1, -1], [-1, 1], [1, 1]];
    ctx.save(); ctx.translate(x, y);
    ctx.fillStyle = 'rgba(0,0,0,0.28)'; ctx.beginPath(); ctx.ellipse(10, 14, 22, 18, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#163a21'; ctx.lineWidth = 3.5; ctx.lineCap = 'round';
    d.forEach(function (v) { ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(v[0] * arm, v[1] * arm); ctx.stroke(); });
    d.forEach(function (v) {
      ctx.fillStyle = 'rgba(238,245,239,0.45)'; ctx.beginPath(); ctx.arc(v[0] * arm, v[1] * arm, 9.5, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.translate(v[0] * arm, v[1] * arm); ctx.rotate(now / 40 + v[0]);
      ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(-9, 0); ctx.lineTo(9, 0); ctx.stroke(); ctx.restore();
    });
    ctx.fillStyle = '#36633e'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
    ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(-8, -10, 16, 20, 6); else ctx.rect(-8, -10, 16, 20); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#bcd8c3'; ctx.beginPath(); ctx.arc(0, -4, 2.4, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  var palms = [], width = 0, height = 0, start = 0, bgCanvas = null, sprites = null, visible = true, frame = 0;

  function resize() {
    var ratio = Math.min(2, window.devicePixelRatio || 1);
    width = canvas.clientWidth; height = canvas.clientHeight;
    if (!width || !height) return;
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    palms = layout(width, height);
    bgCanvas = document.createElement('canvas'); bgCanvas.width = canvas.width; bgCanvas.height = canvas.height;
    var bg = bgCanvas.getContext('2d'); bg.scale(ratio, ratio);
    var gr = bg.createLinearGradient(0, 0, 0, height); gr.addColorStop(0, GROUND_TOP); gr.addColorStop(1, GROUND_BOTTOM);
    bg.fillStyle = gr; bg.fillRect(0, 0, width, height);
    bg.strokeStyle = 'rgba(188,216,195,0.06)';
    for (var y = 0; y < height; y += Math.max(30, width / 24)) { bg.beginPath(); bg.moveTo(0, y); bg.lineTo(width, y); bg.stroke(); }
    var radius = Math.max.apply(null, palms.map(function (p) { return p.size; }));
    sprites = { radius: radius, dim: [], lit: [] };
    for (var t = 0; t < TONES; t++) { sprites.dim.push(crownSprite(radius, ratio, DIM, t)); sprites.lit.push(crownSprite(radius, ratio, LIT, t)); }
    if (reduced) requestAnimationFrame(draw);   // resizing clears the canvas: repaint the still frame
  }

  function stamp(sprite, p, radius) {
    var size = radius * 2.6 * (p.size / radius);
    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rotation); ctx.drawImage(sprite, -size / 2, -size / 2, size, size); ctx.restore();
  }

  function draw(now) {
    if (!start) start = now;
    if (bgCanvas && sprites) {
      var rtl = document.documentElement.dir === 'rtl';
      var t = reduced ? SWEEP_MS + 1 : (now - start) % CYCLE;
      var sweep = Math.min(1, t / SWEEP_MS), eased = 1 - Math.pow(1 - sweep, 2);
      var lineX = rtl ? width + 40 - (width + 80) * eased : -40 + (width + 80) * eased;
      var fade = t > SWEEP_MS + HOLD_MS ? 1 - (t - SWEEP_MS - HOLD_MS) / FADE_MS : 1;
      ctx.drawImage(bgCanvas, 0, 0, width, height);
      for (var i = 0; i < palms.length; i++) {
        var p = palms[i];
        var lit = Math.max(0, Math.min(1, (rtl ? p.x - lineX : lineX - p.x) / 40)) * fade;
        if (lit < 1) stamp(sprites.dim[p.tone], p, sprites.radius);
        if (lit > 0) { ctx.globalAlpha = lit; stamp(sprites.lit[p.tone], p, sprites.radius); ctx.globalAlpha = 1; }
        if (p.flag && lit > 0) {
          var color = p.flag === 'urgent' ? URGENT : WATCH, pulse = 0.5 + 0.5 * Math.sin(now / 320);
          ctx.globalAlpha = lit * (0.18 + 0.14 * pulse); ctx.fillStyle = color;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size * (1.12 + 0.12 * pulse), 0, Math.PI * 2); ctx.fill();
          ctx.globalAlpha = lit; ctx.strokeStyle = color; ctx.lineWidth = 2.5;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size * 1.02, 0, Math.PI * 2); ctx.stroke(); ctx.globalAlpha = 1;
        }
      }
      if (sweep < 1) {
        var gx = rtl ? lineX : lineX - 90;
        var glow = ctx.createLinearGradient(rtl ? lineX : lineX, 0, rtl ? lineX + 90 : lineX - 90, 0);
        glow.addColorStop(0, 'rgba(188,216,195,0.28)'); glow.addColorStop(1, 'rgba(188,216,195,0)');
        ctx.fillStyle = glow; ctx.fillRect(gx, 0, 90, height);
        ctx.fillStyle = 'rgba(238,245,239,0.95)'; ctx.fillRect(lineX - 1, 0, 2, height);
        drawDrone(lineX, height * (0.5 + 0.18 * Math.sin(now / 700)), now);
      }
    }
    if (!reduced && visible) frame = requestAnimationFrame(draw);
  }

  resize();
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas); else window.addEventListener('resize', resize);
  // pause when the hero is off screen
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) {
      var was = visible; visible = e[0].isIntersecting;
      if (visible && !was && !reduced) frame = requestAnimationFrame(draw);
    }).observe(canvas);
  }
  // re-place the alert palms when the language (reading side) changes
  new MutationObserver(resize).observe(document.documentElement, { attributes: true, attributeFilter: ['dir'] });
  frame = requestAnimationFrame(draw);
})();
