# Generates the inline SVG illustrations used by index.html (palms, trunk cut-away, twin wireframe).
# Usage: python3 tools/art.py   → writes tools/art/*.svg snippets that index.html includes verbatim.
import math, os, random
os.makedirs('tools/art', exist_ok=True)

def frond(x, y, ang, L, w, droop, fill='', stroke='', sw=1.2, extra=''):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); px, py = -dy, dx
    tx, ty = x + dx * L, y + dy * L + droop
    mx, my = x + dx * L * .55, y + dy * L * .55 - abs(droop) * .15
    d = f'M{x:.1f} {y:.1f}Q{mx+px*w:.1f} {my+py*w:.1f} {tx:.1f} {ty:.1f}Q{mx-px*w:.1f} {my-py*w:.1f} {x:.1f} {y:.1f}Z'
    if stroke:
        return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>', (tx, ty)
    return f'<path d="{d}" fill="{fill}" {extra}/>', (tx, ty)

CROWN = [(-200, 70, 34), (20, 70, 34), (-186, 74, 22), (6, 74, 22), (-166, 76, 10), (-14, 76, 10),
         (-146, 72, 2), (-34, 72, 2), (-124, 66, 0), (-56, 66, 0), (-104, 58, 0), (-76, 58, 0), (-90, 50, 0)]

def palm_side(cx, base, h, s=1.0, trunk='#8A5A2B', ring='#6E4520', leaf=('#2f6b3d', '#3c7c4d', '#6fa57e'), dates=True, w=1.0):
    """Side-view date palm, solid. Returns svg string."""
    g = [f'<g transform="translate({cx} {base}) scale({s})">']
    tw = 13 * w
    g.append(f'<path d="M{-tw} 0C{-tw*.95} {-h*.4} {-tw*.6} {-h*.8} {-tw*.55} {-h}L{tw*.55} {-h}C{tw*.6} {-h*.8} {tw*.95} {-h*.4} {tw} 0Z" fill="{trunk}"/>')
    for k in range(1, int(h / 16)):
        yy = -k * 16; ww = tw * (1 - .45 * k * 16 / h)
        g.append(f'<path d="M{-ww:.1f} {yy+5:.1f}L0 {yy:.1f}L{ww:.1f} {yy+5:.1f}" fill="none" stroke="{ring}" stroke-width="2.4" stroke-linecap="round"/>')
    for i, (ang, L, dr) in enumerate(CROWN):
        col = leaf[0] if i < 4 else (leaf[1] if i < 9 else leaf[2])
        p, _ = frond(0, -h, ang, L, 9, dr, fill=col); g.append(p)
    if dates:
        for sx in (-1, 1):
            for dx, dy in ((8, 10), (13, 15), (9, 18), (14, 22), (10, 25)):
                g.append(f'<ellipse cx="{sx*dx}" cy="{-h+dy}" rx="3.2" ry="4.4" fill="#D99114"/>')
    g.append('</g>')
    return ''.join(g)

def palm_wire(cx, base, h, s=1.0, col='#BCD8C3', sw=1.6):
    """Same palm as a digital-twin wireframe: outlines, rings and data nodes."""
    g = [f'<g transform="translate({cx} {base}) scale({s})" class="wire">']
    tw = 13
    g.append(f'<path d="M{-tw} 0C{-tw*.95} {-h*.4} {-tw*.6} {-h*.8} {-tw*.55} {-h}L{tw*.55} {-h}C{tw*.6} {-h*.8} {tw*.95} {-h*.4} {tw} 0Z" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    nodes = []
    for k in range(1, int(h / 16)):
        yy = -k * 16; ww = tw * (1 - .45 * k * 16 / h)
        g.append(f'<path d="M{-ww:.1f} {yy+5:.1f}L0 {yy:.1f}L{ww:.1f} {yy+5:.1f}" fill="none" stroke="{col}" stroke-width="{sw*.7}" opacity=".7"/>')
    g.append(f'<path d="M0 0V{-h}" stroke="{col}" stroke-width="{sw*.6}" stroke-dasharray="3 5" opacity=".6"/>')
    for ang, L, dr in CROWN:
        p, tip = frond(0, -h, ang, L, 9, dr, stroke=col, sw=sw); g.append(p); nodes.append(tip)
        a = math.radians(ang)
        g.append(f'<path d="M0 {-h}L{tip[0]:.1f} {tip[1]:.1f}" stroke="{col}" stroke-width="{sw*.5}" opacity=".55"/>')
    for i, (x, y) in enumerate(nodes):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#183A2B" stroke="{col}" stroke-width="{sw}" class="node" style="--i:{i}"/>')
    g.append(f'<circle cx="0" cy="{-h}" r="4.5" fill="{col}"/>')
    g.append(f'<circle cx="0" cy="0" r="3.5" fill="#183A2B" stroke="{col}" stroke-width="{sw}"/>')
    g.append('</g>')
    return ''.join(g)

# ---------- problem: trunk cut-away revealed by a scan band ----------
def trunk_reveal():
    W, H = 360, 470
    trunk = 'M146 440C150 340 158 240 165 168L195 168C202 240 210 340 214 440Z'
    random.seed(3)
    o = [f'<svg viewBox="0 0 {W} {H}" class="reveal-art" aria-hidden="true">']
    o.append('<defs>'
             '<pattern id="bark" width="24" height="18" patternUnits="userSpaceOnUse"><rect width="24" height="18" fill="#93622F"/>'
             '<path d="M0 12L12 4L24 12" fill="none" stroke="#6E4520" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M-12 21L0 13L12 21M12 21L24 13L36 21" fill="none" stroke="#7C5027" stroke-width="2"/></pattern>'
             '<radialGradient id="heat"><stop offset="0" stop-color="#FF6A4D" stop-opacity=".95"/><stop offset=".45" stop-color="#D94C45" stop-opacity=".55"/><stop offset="1" stop-color="#D94C45" stop-opacity="0"/></radialGradient>'
             '<radialGradient id="heat2"><stop offset="0" stop-color="#F2B35A" stop-opacity=".9"/><stop offset="1" stop-color="#D99114" stop-opacity="0"/></radialGradient>'
             f'<clipPath id="trunkClip"><path d="{trunk}"/></clipPath>'
             '<clipPath id="band"><rect x="0" y="170" width="360" height="92">'
             '<animate attributeName="y" values="170;342;170" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></rect></clipPath>'
             '</defs>')
    o.append('<path d="M40 440H320" stroke="#2C5A43" stroke-width="2"/>')
    o.append('<ellipse cx="180" cy="442" rx="70" ry="7" fill="#0b2216" opacity=".5"/>')
    # outside: a healthy-looking palm
    o.append(f'<path d="{trunk}" fill="url(#bark)"/>')
    o.append(f'<path d="{trunk}" fill="none" stroke="#5A3A1C" stroke-width="1.5"/>')
    crown = palm_side(180, 168 + 0.1, 0.1, 1.15, dates=False, leaf=('#2f6b3d', '#3c7c4d', '#6fa57e'))
    o.append(crown)
    for sx in (-1, 1):
        for dx, dy in ((9, 12), (15, 18), (10, 22), (16, 27), (11, 30)):
            o.append(f'<ellipse cx="{180+sx*dx}" cy="{168+dy}" rx="3.6" ry="5" fill="#D99114"/>')
    # inside, only within the scan band
    inner = [f'<path d="{trunk}" fill="#3A2416"/>']
    for x in range(150, 214, 7):
        inner.append(f'<path d="M{x} 170V440" stroke="#4E3220" stroke-width="2"/>')
    tunnels = ['M172 200C186 214 168 232 182 250S176 284 190 300', 'M190 236C178 252 196 268 184 286S194 318 180 336',
               'M168 300C180 312 166 330 178 346S170 380 184 396', 'M196 330C186 344 200 360 190 376']
    for t in tunnels:
        inner.append(f'<path d="{t}" fill="none" stroke="#170C05" stroke-width="7" stroke-linecap="round"/>')
        inner.append(f'<path d="{t}" fill="none" stroke="#5C3A22" stroke-width="1.4" stroke-linecap="round" opacity=".7"/>')
    inner.append('<circle cx="183" cy="282" r="38" fill="url(#heat)"/><circle cx="176" cy="372" r="26" fill="url(#heat2)"/>')
    for x, y, r in ((182, 251, -20), (186, 286, 30), (178, 347, -10), (189, 300, 15)):
        inner.append(f'<g transform="translate({x} {y}) rotate({r})"><ellipse rx="7" ry="4.2" fill="#EFE2C6"/>'
                     '<path d="M-3 -4V4M0 -4.2V4.2M3 -4V4" stroke="#C9B48E" stroke-width=".9"/><circle cx="6" cy="0" r="2" fill="#8A4A2A"/></g>')
    o.append('<g clip-path="url(#trunkClip)"><g clip-path="url(#band)">' + ''.join(inner) + '</g></g>')
    # the scanner: lens brackets + edge lines riding the band
    def ride(el):
        return el.replace('@', '<animateTransform attributeName="transform" type="translate" values="0 0;0 172;0 0" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>')
    o.append(ride('<g>@<path d="M118 170H242" stroke="#EEF5EF" stroke-width="2"/><path d="M118 262H242" stroke="#EEF5EF" stroke-width="2" opacity=".6"/>'
                  '<rect x="118" y="170" width="124" height="92" fill="#BCD8C3" opacity=".06"/>'
                  '<path d="M118 184V170H132M228 170H242V184M242 248V262H228M132 262H118V248" fill="none" stroke="#BCD8C3" stroke-width="3" stroke-linecap="round"/></g>'))
    # finding chip, visible while the band passes the hot spot
    o.append('<g class="find"><path d="M214 282H250" stroke="#D94C45" stroke-width="1.6" stroke-dasharray="3 3"/>'
             '<circle cx="214" cy="282" r="4" fill="#D94C45"/>'
             '<animate attributeName="opacity" values="0;0;1;1;0;0;1;1;0;0" keyTimes="0;.12;.15;.36;.4;.6;.64;.86;.9;1" dur="7s" repeatCount="indefinite"/></g>')
    o.append('</svg>')
    return ''.join(o)

# ---------- idea: real palm  ⇄  digital twin ----------
def twin_art():
    o = ['<svg viewBox="0 0 560 420" class="twin-art" aria-hidden="true">']
    o.append('<defs><pattern id="tgrid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#BCD8C3" stroke-width=".6" opacity=".18"/></pattern>'
             '<linearGradient id="tfade" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff"/><stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             '<mask id="tmask"><rect width="560" height="420" fill="url(#tfade)"/></mask></defs>')
    o.append('<rect x="300" y="20" width="250" height="390" rx="22" fill="url(#tgrid)" mask="url(#tmask)"/>')
    o.append('<path d="M30 380H250" stroke="#2C5A43" stroke-width="2"/><path d="M310 380H530" stroke="#BCD8C3" stroke-width="1.4" stroke-dasharray="4 6" opacity=".6"/>')
    o.append('<ellipse cx="140" cy="382" rx="56" ry="6" fill="#0b2216" opacity=".45"/>')
    o.append(palm_side(140, 380, 230, 1.18, leaf=('#2f6b3d', '#3c7c4d', '#6fa57e')))
    o.append(palm_wire(420, 380, 230, 1.18))
    # data flowing both ways
    o.append('<path class="flow-a" d="M212 150C260 120 300 120 348 150" fill="none" stroke="#BCD8C3" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>')
    o.append('<path class="flow-b" d="M348 250C300 280 260 280 212 250" fill="none" stroke="#D99114" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>')
    o.append('<path d="M340 142l10 8-12 4" fill="none" stroke="#BCD8C3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append('<path d="M220 258l-10-8 12-4" fill="none" stroke="#D99114" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append('</svg>')
    return ''.join(o)

open('tools/art/trunk.svg', 'w').write(trunk_reveal())
open('tools/art/twin.svg', 'w').write(twin_art())
print('ok')
