# Basqah website — the ONE approved palm, and every asset derived from it.
#   assets/palm.svg       side-view date palm (master)
#   assets/palm-wire.svg  the same palm as a digital-twin wireframe
#   assets/crown.svg      the same palm seen from above (matches the app's AerialHero crown)
#   assets/favicon.svg    crown on a brand tile
#   tools/art/trunk.svg   problem section: the master palm with a scan band revealing the inside (inline)
#   tools/art/twin.svg    idea section: master palm ⇄ wireframe twin with data flow (inline)
# Usage: python3 tools/art.py  (from the site root)
import math, os, random
os.makedirs('tools/art', exist_ok=True)

H = 250                       # trunk height of the master palm (crown sits at y = -H)
TRUNK_W0, TRUNK_W1 = 15, 9    # half-width at base / at crown

def trunk_path(dx=0):
    """slightly curved, tapered trunk; base centre at (dx, 0)."""
    a, b = TRUNK_W0, TRUNK_W1
    return (f'M{dx-a} 0C{dx-a+1} {-H*.35} {dx-b-3} {-H*.75} {dx-b} {-H}'
            f'L{dx+b} {-H}C{dx+b+3} {-H*.75} {dx+a-1} {-H*.35} {dx+a} 0Z')

# fronds: (angle°, length, droop) — back/low fronds first so the crown overlaps naturally
FRONDS = [(-205, 112, 58), (25, 112, 58), (-192, 118, 40), (12, 118, 40), (-176, 120, 24), (-4, 120, 24),
          (-158, 116, 10), (-22, 116, 10), (-140, 104, 4), (-40, 104, 4), (-122, 90, 2), (-58, 90, 2),
          (-106, 76, 0), (-74, 76, 0), (-90, 64, 0)]
TONES = ['#1f4a2b', '#1f4a2b', '#24533a', '#24533a', '#2a5c36', '#2a5c36', '#2f6b3d', '#2f6b3d',
         '#356f45', '#356f45', '#3c7c4d', '#3c7c4d', '#457f52', '#457f52', '#4e8a5b']

def rachis(ang, L, droop):
    """quadratic rachis from the crown heart: returns (start, control, tip)."""
    a = math.radians(ang)
    sx, sy = 0, -H
    tx, ty = sx + math.cos(a) * L, sy + math.sin(a) * L + droop
    cx, cy = sx + math.cos(a) * L * .55, sy + math.sin(a) * L * .55 - droop * .25
    return (sx, sy), (cx, cy), (tx, ty)

def qpt(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    m = math.hypot(dx, dy) or 1
    return x, y, dx / m, dy / m

def frond_paths(ang, L, droop, n=18):
    n = n if abs(math.cos(math.radians(ang))) > .5 else 12
    """one pinnate frond: rachis + leaflets on both sides (as one stroked path)."""
    p0, p1, p2 = rachis(ang, L, droop)
    d = [f'M{p0[0]:.1f} {p0[1]:.1f}Q{p1[0]:.1f} {p1[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}']
    tips = []
    for k in range(n):
        t = .14 + .84 * k / (n - 1)
        x, y, ux, uy = qpt(p0, p1, p2, t)
        upright = abs(math.cos(math.radians(ang)))          # 0 for the vertical young fronds
        ll = (L * .3 * (1 - .62 * t) + 4) * (.5 + .5 * min(1, upright * 1.3))   # leaflets shorten toward the tip; young fronds stay slim
        for side in (-1, 1):
            # leaflets sweep forward along the rachis and fall a little with gravity
            vx = ux * .62 + (-uy) * side * .78
            vy = uy * .62 + (ux) * side * .78 + .25
            m = math.hypot(vx, vy)
            ex, ey = x + vx / m * ll, y + vy / m * ll
            d.append(f'M{x:.1f} {y:.1f}L{ex:.1f} {ey:.1f}')
    return ''.join(d), p2

def palm_svg_body(dates=True, ids='p'):
    """master palm geometry, solid. Coordinates: base at (0,0), crown at (0,-H)."""
    g = []
    g.append(f'<path d="{trunk_path()}" fill="url(#{ids}bark)"/>')
    g.append(f'<path d="{trunk_path()}" fill="url(#{ids}shade)"/>')
    for (ang, L, dr), col in zip(FRONDS, TONES):
        d, _ = frond_paths(ang, L, dr)
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>')
    g.append(f'<ellipse cx="0" cy="{-H+2}" rx="11" ry="7" fill="#1a3d24"/>')
    if dates:
        for sx in (-1, 1):
            g.append(f'<path d="M{sx*4} {-H+4}Q{sx*14} {-H+6} {sx*16} {-H+16}" fill="none" stroke="#C9962F" stroke-width="2.4" stroke-linecap="round"/>')
            for dx, dy in ((12, 16), (18, 20), (14, 23), (20, 27), (16, 30), (13, 34), (19, 35)):
                g.append(f'<ellipse cx="{sx*dx}" cy="{-H+dy+6}" rx="3.4" ry="4.6" fill="{"#D99114" if (dx+dy)%2 else "#C8741C"}"/>')
    return ''.join(g)

def palm_defs(ids='p'):
    return (f'<pattern id="{ids}bark" width="26" height="18" patternUnits="userSpaceOnUse" x="-13">'
            '<rect width="26" height="18" fill="#93622F"/>'
            '<path d="M0 13L13 4L26 13" fill="none" stroke="#6E4520" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="M-13 22L0 13L13 22L26 13L39 22" fill="none" stroke="#7C5027" stroke-width="2"/></pattern>'
            f'<linearGradient id="{ids}shade" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".22"/>'
            '<stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>')

def palm_wire_body(col='#BCD8C3', sw=1.6, nodes_cls='node'):
    g = [f'<path d="{trunk_path()}" fill="none" stroke="{col}" stroke-width="{sw}"/>']
    for k in range(1, int(H / 18)):
        y = -k * 18; f = k * 18 / H; w = TRUNK_W0 + (TRUNK_W1 - TRUNK_W0) * f
        g.append(f'<path d="M{-w:.1f} {y+6:.1f}L0 {y:.1f}L{w:.1f} {y+6:.1f}" fill="none" stroke="{col}" stroke-width="{sw*.7}" opacity=".65"/>')
    g.append(f'<path d="M0 0V{-H}" stroke="{col}" stroke-width="{sw*.6}" stroke-dasharray="3 5" opacity=".55"/>')
    tips = []
    for ang, L, dr in FRONDS:
        p0, p1, p2 = rachis(ang, L, dr)
        g.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f}Q{p1[0]:.1f} {p1[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        # sparse leaflet ticks to read as a frond
        for k in range(6):
            t = .25 + .65 * k / 5
            x, y, ux, uy = qpt(p0, p1, p2, t); ll = L * .2 * (1 - .6 * t) + 3
            for side in (-1, 1):
                vx = ux * .6 + (-uy) * side * .8; vy = uy * .6 + ux * side * .8 + .2; m = math.hypot(vx, vy)
                g.append(f'<path d="M{x:.1f} {y:.1f}l{vx/m*ll:.1f} {vy/m*ll:.1f}" stroke="{col}" stroke-width="{sw*.6}" opacity=".7"/>')
        tips.append(p2)
    for i, (x, y) in enumerate(tips):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="#183A2B" stroke="{col}" stroke-width="{sw}" class="{nodes_cls}" style="--i:{i}"/>')
    g.append(f'<circle cx="0" cy="{-H}" r="5" fill="{col}"/><circle cx="0" cy="0" r="4" fill="#183A2B" stroke="{col}" stroke-width="{sw}"/>')
    return ''.join(g)

# viewBox that fits the master palm (fronds reach ~±128 and ~-H-90)
VB = (-150, -H - 100, 300, H + 112)
vb = ' '.join(str(v) for v in VB)

open('assets/palm.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><defs>{palm_defs("p")}</defs>{palm_svg_body()}</svg>')
open('assets/palm-wire.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{palm_wire_body()}</svg>')

# crown from above — same fronds, radial (the app's AerialHero sprite, in the lit palette)
def crown(cx, cy, r, rot=0.0, base='#2f6b3d', tip='#7fb08a', heart='#1f4a2b', gid='cg'):
    g = [f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{base}"/><stop offset="1" stop-color="{tip}"/></linearGradient></defs>',
         f'<ellipse cx="{cx+r*.16:.1f}" cy="{cy+r*.2:.1f}" rx="{r*.95:.1f}" ry="{r*.9:.1f}" fill="#000" opacity=".28"/>']
    n = 15
    for i in range(n):
        L = r * (0.78 + (((i) * 37) % 11) / 40)
        a = math.degrees(rot + i / n * 2 * math.pi)
        g.append(f'<g transform="translate({cx} {cy}) rotate({a:.1f})"><path d="M0 0Q{L*.45:.1f} {-r*.11:.1f} {L:.1f} {r*.02:.1f}Q{L*.45:.1f} {r*.11:.1f} 0 0Z" fill="url(#{gid})"/>'
                 f'<path d="M{r*.12:.1f} 0L{L*.95:.1f} {r*.015:.1f}" stroke="#000" stroke-opacity=".18" stroke-width="{r*.03:.2f}"/></g>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r*.16:.1f}" fill="{heart}"/>')
    return ''.join(g)

open('assets/crown.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{crown(32, 30, 20)}</svg>')
open('assets/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#183A2B"/>'
                                      + crown(32, 32, 22, base='#3c7c4d', tip='#bcd8c3', heart='#24643a') + '</svg>')

# ---------------- problem: master palm, scan band reveals the damage inside ----------------
def trunk_reveal():
    s = 1.18; ox, oy = 180, 455           # base position in the 360×480 canvas
    o = ['<svg viewBox="0 0 360 480" class="reveal-art" aria-hidden="true"><defs>' + palm_defs('r') +
         f'<clipPath id="rTrunk"><path d="{trunk_path()}" transform="translate({ox} {oy}) scale({s})"/></clipPath>'
         '<clipPath id="rBand"><rect x="0" y="175" width="360" height="92">'
         '<animate attributeName="y" values="175;350;175" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></rect></clipPath></defs>']
    o.append(f'<path d="M40 {oy}H320" stroke="#2C5A43" stroke-width="2"/><ellipse cx="{ox}" cy="{oy+2}" rx="70" ry="7" fill="#0b2216" opacity=".5"/>')
    o.append(f'<g transform="translate({ox} {oy}) scale({s})">{palm_svg_body(ids="r")}</g>')
    # the inside: cut flesh, fibres, weevil tunnels and larvae (no "heat" — we don't show what we read)
    top, bot = oy - H * s, oy
    inner = [f'<rect x="120" y="{top:.0f}" width="120" height="{bot-top:.0f}" fill="#3A2416"/>']
    for x in range(150, 214, 7):
        inner.append(f'<path d="M{x} {top:.0f}V{bot}" stroke="#4E3220" stroke-width="2"/>')
    tunnels = ['M172 200C186 214 168 232 182 250S176 284 190 300', 'M190 236C178 252 196 268 184 286S194 318 180 336',
               'M168 300C180 312 166 330 178 346S170 380 184 396', 'M196 330C186 344 200 360 190 376', 'M176 380C188 392 172 410 184 430']
    for t in tunnels:
        inner.append(f'<path d="{t}" fill="none" stroke="#170C05" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="{t}" fill="none" stroke="#5C3A22" stroke-width="1.4" stroke-linecap="round" opacity=".7"/>')
    for x, y, r in ((182, 251, -20), (186, 286, 30), (178, 347, -10), (189, 300, 15), (183, 410, 25)):
        inner.append(f'<g transform="translate({x} {y}) rotate({r})"><ellipse rx="7" ry="4.2" fill="#EFE2C6"/>'
                     '<path d="M-3 -4V4M0 -4.2V4.2M3 -4V4" stroke="#C9B48E" stroke-width=".9"/><circle cx="6" cy="0" r="2" fill="#8A4A2A"/></g>')
    o.append('<g clip-path="url(#rTrunk)"><g clip-path="url(#rBand)">' + ''.join(inner) + '</g></g>')
    ride = '<animateTransform attributeName="transform" type="translate" values="0 0;0 175;0 0" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
    o.append('<g>' + ride + '<path d="M120 175H240" stroke="#EEF5EF" stroke-width="2"/><path d="M120 267H240" stroke="#EEF5EF" stroke-width="2" opacity=".6"/>'
             '<rect x="120" y="175" width="120" height="92" fill="#BCD8C3" opacity=".06"/>'
             '<path d="M120 189V175H134M226 175H240V189M240 253V267H226M134 267H120V253" fill="none" stroke="#BCD8C3" stroke-width="3" stroke-linecap="round"/></g>')
    o.append('</svg>')
    return ''.join(o)

# ---------------- idea: master palm ⇄ its wireframe twin ----------------
def twin_art():
    s = 1.05
    o = ['<svg viewBox="0 0 600 420" class="twin-art" aria-hidden="true"><defs>' + palm_defs('t') +
         '<pattern id="tgrid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#BCD8C3" stroke-width=".6" opacity=".18"/></pattern>'
         '<radialGradient id="tfade"><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
         '<mask id="tmask"><rect width="600" height="420" fill="url(#tfade)"/></mask></defs>']
    o.append('<rect x="320" y="0" width="280" height="420" fill="url(#tgrid)" mask="url(#tmask)"/>')
    o.append('<path d="M40 395H270" stroke="#2C5A43" stroke-width="2"/><path d="M330 395H560" stroke="#BCD8C3" stroke-width="1.4" stroke-dasharray="4 6" opacity=".6"/>')
    o.append('<ellipse cx="150" cy="397" rx="56" ry="6" fill="#0b2216" opacity=".45"/>')
    o.append(f'<g transform="translate(150 395) scale({s})">{palm_svg_body(ids="t")}</g>')
    o.append(f'<g transform="translate(450 395) scale({s})" class="wire">{palm_wire_body()}</g>')
    o.append('<path class="flow-a" d="M236 150C280 118 320 118 364 150" fill="none" stroke="#BCD8C3" stroke-width="2.2" stroke-dasharray="2 10" stroke-linecap="round"/>'
             '<path class="flow-b" d="M364 262C320 294 280 294 236 262" fill="none" stroke="#D99114" stroke-width="2.2" stroke-dasharray="2 10" stroke-linecap="round"/>'
             '<path d="M356 141l10 9-12 4" fill="none" stroke="#BCD8C3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M244 271l-10-9 12-4" fill="none" stroke="#D99114" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append('</svg>')
    return ''.join(o)

open('tools/art/trunk.svg', 'w').write(trunk_reveal())
open('tools/art/twin.svg', 'w').write(twin_art())
print('assets written')
