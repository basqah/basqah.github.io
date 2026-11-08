# Generates assets/farm.svg: a top-down date-palm farm (satellite feel) sized for the phone screen in the hero.
# Usage: python3 tools/farm.py  (run from the site root). Prints the % positions of the flagged palms.
import math, random
random.seed(7)
W, H = 300, 640
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">']
out.append('<defs>'
           '<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#3B2E1C" stop-opacity=".45"/><stop offset="1" stop-color="#3B2E1C" stop-opacity="0"/></radialGradient>'
           '<linearGradient id="lf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2C5636"/><stop offset="1" stop-color="#5E9466"/></linearGradient>'
           '<linearGradient id="lf2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#244A2E"/><stop offset="1" stop-color="#4C7F55"/></linearGradient>'
           '</defs>')
# ground: warm sand with irrigation rows and a farm track
out.append(f'<rect width="{W}" height="{H}" fill="#CBB284"/>')
for y in range(0, H, 6):
    out.append(f'<path d="M0 {y}H{W}" stroke="#C2A877" stroke-width="2" opacity="{random.uniform(.3,.8):.2f}"/>')
out.append(f'<path d="M0 318H{W}" stroke="#D9C49C" stroke-width="16"/><path d="M0 310H{W}M0 326H{W}" stroke="#B89C6C" stroke-width="1"/>')

def leaf(cx, cy, a, L, w, fill):
    tx, ty = cx + math.cos(a) * L, cy + math.sin(a) * L
    px, py = -math.sin(a) * w, math.cos(a) * w
    mx, my = cx + math.cos(a) * L * .45, cy + math.sin(a) * L * .45
    return f'<path d="M{cx:.1f} {cy:.1f}Q{mx+px:.1f} {my+py:.1f} {tx:.1f} {ty:.1f}Q{mx-px:.1f} {my-py:.1f} {cx:.1f} {cy:.1f}Z" fill="{fill}"/>'

def crown(cx, cy, r, rot, grad):
    g = [f'<ellipse cx="{cx+3:.1f}" cy="{cy+4:.1f}" rx="{r*1.15:.1f}" ry="{r*1.05:.1f}" fill="url(#sh)"/>']
    for k in range(16):                                   # outer, older fronds: long and darker
        a = rot + k * 2 * math.pi / 16
        g.append(leaf(cx, cy, a, r * (0.92 + 0.08 * (k % 2)), r * .3, 'url(#lf2)'))
    for k in range(10):                                   # inner, young fronds: shorter and lighter
        a = rot + .2 + k * 2 * math.pi / 10
        g.append(leaf(cx, cy, a, r * .62, r * .24, 'url(#lf)'))
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*.16:.1f}" fill="#8A7A45"/>')
    return ''.join(g)

palms = []
sp = 36
for row, y in enumerate(range(26, H, sp)):
    if abs(y - 318) < 22:
        continue
    off = (sp / 2) if row % 2 else 0
    for x in range(int(14 + off), W + 10, sp):
        jx, jy = random.uniform(-2.5, 2.5), random.uniform(-2.5, 2.5)
        palms.append((x + jx, y + jy, random.uniform(12, 14.5), random.uniform(0, 6.28), 'lf' if random.random() > .35 else 'lf2'))
for p in palms:
    out.append(crown(*p))
out.append('</svg>')
open('assets/farm.svg', 'w').write(''.join(out))

# palms used for the overlays (closest to these targets)
def pick(tx, ty):
    p = min(palms, key=lambda q: (q[0]-tx)**2 + (q[1]-ty)**2)
    return round(p[0]/W*100, 2), round(p[1]/H*100, 2)
print('watch', pick(110, 170), 'urgent', pick(200, 250))
