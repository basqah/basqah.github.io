# Basqah website — the ONE approved palm (the original "twin" palm), and every asset derived from it.
#   assets/palm.svg       side-view date palm (master)
#   assets/palm-wire.svg  the same palm as a digital-twin wireframe
#   assets/crown.svg      a palm crown seen from above (the app's AerialHero crown)
#   assets/favicon.svg    crown on a brand tile
#   tools/art/trunk.svg   problem section: master palm, a scan band reveals the damage inside (inline)
#   tools/art/twin.svg    idea section: master palm ⇄ its wireframe twin, data flowing between (inline)
# Usage: python3 tools/art.py  (from the site root)
import math, os
os.makedirs('tools/art', exist_ok=True)

H = 230          # trunk height of the master palm
TW = 13          # trunk half-width at the base
CROWN = [(-200, 70, 34), (20, 70, 34), (-186, 74, 22), (6, 74, 22), (-166, 76, 10), (-14, 76, 10),
         (-146, 72, 2), (-34, 72, 2), (-124, 66, 0), (-56, 66, 0), (-104, 58, 0), (-76, 58, 0), (-90, 50, 0)]
LEAF = ('#2f6b3d', '#3c7c4d', '#6fa57e')

def trunk_d():
    return f'M{-TW} 0C{-TW*.95} {-H*.4} {-TW*.6} {-H*.8} {-TW*.55} {-H}L{TW*.55} {-H}C{TW*.6} {-H*.8} {TW*.95} {-H*.4} {TW} 0Z'

def frond(x, y, ang, L, w, droop):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); px, py = -dy, dx
    tx, ty = x + dx * L, y + dy * L + droop
    mx, my = x + dx * L * .55, y + dy * L * .55 - abs(droop) * .15
    return f'M{x:.1f} {y:.1f}Q{mx+px*w:.1f} {my+py*w:.1f} {tx:.1f} {ty:.1f}Q{mx-px*w:.1f} {my-py*w:.1f} {x:.1f} {y:.1f}Z', (tx, ty)

def palm(dates=True):
    """master palm: base at (0,0), crown at (0,-H)."""
    g = [f'<path d="{trunk_d()}" fill="#8A5A2B"/>']
    for k in range(1, int(H / 16)):
        yy = -k * 16; ww = TW * (1 - .45 * k * 16 / H)
        g.append(f'<path d="M{-ww:.1f} {yy+5:.1f}L0 {yy:.1f}L{ww:.1f} {yy+5:.1f}" fill="none" stroke="#6E4520" stroke-width="2.4" stroke-linecap="round"/>')
    for i, (ang, L, dr) in enumerate(CROWN):
        d, _ = frond(0, -H, ang, L, 9, dr)
        g.append(f'<path d="{d}" fill="{LEAF[0] if i < 4 else (LEAF[1] if i < 9 else LEAF[2])}"/>')
    if dates:
        for sx in (-1, 1):
            for dx, dy in ((8, 10), (13, 15), (9, 18), (14, 22), (10, 25)):
                g.append(f'<ellipse cx="{sx*dx}" cy="{-H+dy}" rx="3.2" ry="4.4" fill="#D99114"/>')
    return ''.join(g)

def palm_wire(col='#BCD8C3', sw=1.6):
    g = [f'<path d="{trunk_d()}" fill="none" stroke="{col}" stroke-width="{sw}"/>']
    for k in range(1, int(H / 16)):
        yy = -k * 16; ww = TW * (1 - .45 * k * 16 / H)
        g.append(f'<path d="M{-ww:.1f} {yy+5:.1f}L0 {yy:.1f}L{ww:.1f} {yy+5:.1f}" fill="none" stroke="{col}" stroke-width="{sw*.7}" opacity=".7"/>')
    g.append(f'<path d="M0 0V{-H}" stroke="{col}" stroke-width="{sw*.6}" stroke-dasharray="3 5" opacity=".6"/>')
    tips = []
    for ang, L, dr in CROWN:
        d, tip = frond(0, -H, ang, L, 9, dr)
        g.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>')
        g.append(f'<path d="M0 {-H}L{tip[0]:.1f} {tip[1]:.1f}" stroke="{col}" stroke-width="{sw*.5}" opacity=".55"/>')
        tips.append(tip)
    for i, (x, y) in enumerate(tips):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#183A2B" stroke="{col}" stroke-width="{sw}" class="node" style="--i:{i}"/>')
    g.append(f'<circle cx="0" cy="{-H}" r="4.5" fill="{col}"/><circle cx="0" cy="0" r="3.5" fill="#183A2B" stroke="{col}" stroke-width="{sw}"/>')
    return ''.join(g)

VB = '-100 -300 200 306'
open('assets/palm.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}">{palm()}</svg>')
open('assets/palm-wire.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}">{palm_wire()}</svg>')

def crown(cx, cy, r, rot=0.0, base='#2f6b3d', tip='#7fb08a', heart='#1f4a2b', gid='cg'):
    g = [f'<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{base}"/><stop offset="1" stop-color="{tip}"/></linearGradient></defs>',
         f'<ellipse cx="{cx+r*.16:.1f}" cy="{cy+r*.2:.1f}" rx="{r*.95:.1f}" ry="{r*.9:.1f}" fill="#000" opacity=".28"/>']
    n = 15
    for i in range(n):
        L = r * (0.78 + ((i * 37) % 11) / 40)
        a = math.degrees(rot + i / n * 2 * math.pi)
        g.append(f'<g transform="translate({cx} {cy}) rotate({a:.1f})"><path d="M0 0Q{L*.45:.1f} {-r*.11:.1f} {L:.1f} {r*.02:.1f}Q{L*.45:.1f} {r*.11:.1f} 0 0Z" fill="url(#{gid})"/>'
                 f'<path d="M{r*.12:.1f} 0L{L*.95:.1f} {r*.015:.1f}" stroke="#000" stroke-opacity=".18" stroke-width="{r*.03:.2f}"/></g>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r*.16:.1f}" fill="{heart}"/>')
    return ''.join(g)

open('assets/crown.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{crown(32, 30, 20)}</svg>')
open('assets/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#183A2B"/>'
                                      + crown(32, 32, 22, base='#3c7c4d', tip='#bcd8c3', heart='#24643a') + '</svg>')

# ---------------- problem: master palm; a scan band reveals the damage inside ----------------
def trunk_reveal():
    s, ox, oy = 1.42, 180, 462
    tr = f'translate({ox} {oy}) scale({s})'
    top = oy - H * s
    band_y0, band_y1, bh = round(top + 20), round(oy - 110), 92
    anim = f'values="{band_y0};{band_y1};{band_y0}" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
    o = ['<svg viewBox="0 0 360 480" class="reveal-art" aria-hidden="true"><defs>'
         f'<clipPath id="rTrunk"><path d="{trunk_d()}" transform="{tr}"/></clipPath>'
         f'<clipPath id="rBand"><rect x="0" y="{band_y0}" width="360" height="{bh}"><animate attributeName="y" {anim}/></rect></clipPath></defs>']
    o.append(f'<path d="M40 {oy}H320" stroke="#2C5A43" stroke-width="2"/><ellipse cx="{ox}" cy="{oy+2}" rx="64" ry="7" fill="#0b2216" opacity=".5"/>')
    o.append(f'<g transform="{tr}">{palm()}</g>')
    inner = [f'<rect x="140" y="{top:.0f}" width="80" height="{oy-top:.0f}" fill="#3A2416"/>']
    for x in range(158, 204, 6):
        inner.append(f'<path d="M{x} {top:.0f}V{oy}" stroke="#4E3220" stroke-width="2"/>')
    y0 = top + 30
    for x, dy in ((174, 0), (186, 50), (172, 105), (188, 150), (176, 200), (184, 240)):
        y = y0 + dy
        t = f'M{x} {y:.0f}C{x+10} {y+12:.0f} {x-6} {y+28:.0f} {x+4} {y+44:.0f}S{x-2} {y+70:.0f} {x+8} {y+84:.0f}'
        inner.append(f'<path d="{t}" fill="none" stroke="#170C05" stroke-width="6.5" stroke-linecap="round"/>'
                     f'<path d="{t}" fill="none" stroke="#5C3A22" stroke-width="1.3" stroke-linecap="round" opacity=".7"/>')
    for x, dy, r in ((180, 46, -20), (184, 96, 30), (176, 156, -10), (186, 206, 15), (180, 262, 25)):
        inner.append(f'<g transform="translate({x} {y0+dy:.0f}) rotate({r})"><ellipse rx="6.5" ry="4" fill="#EFE2C6"/>'
                     '<path d="M-3 -3.8V3.8M0 -4V4M3 -3.8V3.8" stroke="#C9B48E" stroke-width=".9"/><circle cx="5.6" cy="0" r="1.9" fill="#8A4A2A"/></g>')
    o.append('<g clip-path="url(#rTrunk)"><g clip-path="url(#rBand)">' + ''.join(inner) + '</g></g>')
    ride = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {band_y1-band_y0};0 0" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
    x0, x1 = 128, 232
    o.append(f'<g>{ride}<path d="M{x0} {band_y0}H{x1}" stroke="#EEF5EF" stroke-width="2"/><path d="M{x0} {band_y0+bh}H{x1}" stroke="#EEF5EF" stroke-width="2" opacity=".6"/>'
             f'<rect x="{x0}" y="{band_y0}" width="{x1-x0}" height="{bh}" fill="#BCD8C3" opacity=".06"/>'
             f'<path d="M{x0} {band_y0+14}V{band_y0}H{x0+14}M{x1-14} {band_y0}H{x1}V{band_y0+14}M{x1} {band_y0+bh-14}V{band_y0+bh}H{x1-14}M{x0+14} {band_y0+bh}H{x0}V{band_y0+bh-14}" fill="none" stroke="#BCD8C3" stroke-width="3" stroke-linecap="round"/></g>')
    o.append('</svg>')
    return ''.join(o)

# ---------------- idea: master palm ⇄ wireframe twin ----------------
def twin_art():
    s = 1.18
    o = ['<svg viewBox="0 0 560 420" class="twin-art" aria-hidden="true"><defs>'
         '<pattern id="tgrid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#BCD8C3" stroke-width=".6" opacity=".18"/></pattern>'
         '<radialGradient id="tfade"><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
         '<mask id="tmask"><rect width="560" height="420" fill="url(#tfade)"/></mask></defs>']
    o.append('<rect x="300" y="0" width="260" height="420" fill="url(#tgrid)" mask="url(#tmask)"/>')
    o.append('<path d="M30 380H250" stroke="#2C5A43" stroke-width="2"/><path d="M310 380H530" stroke="#BCD8C3" stroke-width="1.4" stroke-dasharray="4 6" opacity=".6"/>')
    o.append('<ellipse cx="140" cy="382" rx="56" ry="6" fill="#0b2216" opacity=".45"/>')
    o.append(f'<g transform="translate(140 380) scale({s})">{palm()}</g>')
    o.append(f'<g transform="translate(420 380) scale({s})" class="wire">{palm_wire()}</g>')
    # both paths are drawn in the direction their data travels; arrowheads are markers that follow each path's end tangent
    o.insert(1, '<defs><marker id="ahM" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto">'
                '<path d="M2 2L10 6L2 10" fill="none" stroke="#BCD8C3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="ahA" viewBox="0 0 12 12" refX="9" refY="6" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto">'
                '<path d="M2 2L10 6L2 10" fill="none" stroke="#D99114" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    o.append('<path class="flow" d="M214 156C262 124 302 124 344 152" fill="none" stroke="#BCD8C3" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round" marker-end="url(#ahM)"/>'
             '<path class="flow" d="M346 246C298 276 258 276 216 248" fill="none" stroke="#D99114" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round" marker-end="url(#ahA)"/>')
    o.append('</svg>')
    return ''.join(o)

open('tools/art/trunk.svg', 'w').write(trunk_reveal())
open('tools/art/twin.svg', 'w').write(twin_art())
print('assets written')
