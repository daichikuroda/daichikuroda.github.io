"""Generate Figures 1 and 3 of the hierarchical clustering research page.

Usage (from the repository root):  python3 _scripts/research_figures.py assets/img/research
Writes flat-clusterings.svg (Figure 1) and backbone.svg (Figure 3). Figure 1 uses the same
points as hierarchy-example.svg (Figure 2): same sub-cluster centers and random seed.
"""
import math, random, sys

OUT = sys.argv[1]
TEAL, TEAL2, AMBER, RED, BLUE, PURPLE = "#0d6470", "#4a9aa6", "#b26b12", "#b8433a", "#3b6fb6", "#7b5ea7"
INK, MUTED, LINE = "#1b2329", "#6b757d", "#e3e0d8"
FONT = 'font-family="Inter, Helvetica, Arial, sans-serif"'


def blobs(centers, seed, n=5, rmin=5, rmax=12):
    random.seed(seed)
    pts = {}
    for k, (cx, cy) in centers.items():
        pts[k] = []
        for i in range(n):
            a = 2 * math.pi * i / n + random.uniform(-0.4, 0.4)
            r = random.uniform(rmin, rmax)
            pts[k].append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def head(w, h, title, desc):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" {FONT} role="img" aria-labelledby="t d">',
        f'<title id="t">{title}</title>',
        f'<desc id="d">{desc}</desc>',
        f'<rect width="{w}" height="{h}" rx="12" fill="#ffffff"/>',
    ]


def text(x, y, s, size=12, fill=INK, weight="400", anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


# ---------------------------------------------------------------- Figure 1
# Same data as hierarchy-example.svg (same centers and seed).
SUBS = {"A1": (85, 92), "A2": (148, 150), "B1": (222, 212), "B2": (290, 212), "B3": (256, 153)}
P = blobs(SUBS, 7)


def panel_points(ox, oy, s, colors, outlines):
    """Draw the 25 points scaled by s with offset; colors: dict sub->color."""
    out = []
    tx = lambda x: ox + (x - 55) * s
    ty = lambda y: oy + (y - 60) * s
    for kind, spec in outlines:
        if kind == "ellipse":
            cx, cy, rx, ry, rot, col = spec
            out.append(f'<ellipse cx="{tx(cx):.1f}" cy="{ty(cy):.1f}" rx="{rx*s:.1f}" ry="{ry*s:.1f}" transform="rotate({rot} {tx(cx):.1f} {ty(cy):.1f})" fill="{col}" fill-opacity=".06" stroke="{col}" stroke-opacity=".7" stroke-dasharray="5 4" stroke-width="1.4"/>')
        if kind == "circle":
            cx, cy, r, col = spec
            out.append(f'<circle cx="{tx(cx):.1f}" cy="{ty(cy):.1f}" r="{r*s:.1f}" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-opacity=".75" stroke-width="1.3"/>')
    for k, pts in P.items():
        for x, y in pts:
            out.append(f'<circle cx="{tx(x):.1f}" cy="{ty(y):.1f}" r="3.4" fill="{colors.get(k, "#7d868d")}"/>')
    return out


W, H = 720, 262
svg = head(W, H, "The same data clustered at two resolutions",
           "Three panels. Left: 25 unlabeled points. Middle: the points split into two clusters. Right: the same points split into five smaller clusters.")
s = 0.8
panels = [
    ("(a) Data", {}, []),
    ("(b) Two clusters", {k: (TEAL if k[0] == "A" else AMBER) for k in SUBS},
     [("ellipse", (116, 121, 80, 58, 42, TEAL)), ("ellipse", (256, 192, 72, 70, 0, AMBER))]),
    ("(c) Five clusters", {"A1": TEAL, "A2": BLUE, "B1": AMBER, "B2": RED, "B3": PURPLE},
     [("circle", (cx, cy, 21, c)) for (k, (cx, cy)), c in zip(SUBS.items(), [TEAL, BLUE, AMBER, RED, PURPLE])]),
]
for i, (label, cols, outl) in enumerate(panels):
    ox = 22 + i * 240
    svg += panel_points(ox, 22, s, cols, outl)
    svg.append(text(ox + 102, 246, label, 13, INK, "600", "middle"))
    if i:
        svg.append(f'<line x1="{ox-14}" y1="24" x2="{ox-14}" y2="224" stroke="{LINE}"/>')
svg.append("</svg>")
open(f"{OUT}/flat-clusterings.svg", "w").write("\n".join(svg) + "\n")

# ---------------------------------------------------------------- Figure 3
SUBS3 = {"A1": (70, 78), "A2": (128, 132), "B1": (196, 214), "B2": (250, 204), "B3": (306, 214)}
P3 = blobs(SUBS3, 11, n=5, rmin=4, rmax=10)
W, H = 720, 590
svg = head(W, H, "Different admissible methods share a common backbone",
           "Four panels. (a) Points forming two well-separated groups A and B; A has two clearly separated sub-groups, while in B the middle sub-group B2 is about as close to B1 as to B3. (b) The shared backbone: A, A1, A2 and B, with B1, B2 and B3 merging at once. (c) One method groups B1 with B2. (d) Another groups B2 with B3.")
# panel frames
svg.append(f'<line x1="360" y1="24" x2="360" y2="566" stroke="{LINE}"/>')
svg.append(f'<line x1="24" y1="296" x2="696" y2="296" stroke="{LINE}"/>')
# (a) data
ox, oy = 10, 10
def t3(x, y):
    return ox + x, oy + y
for (cx, cy, rx, ry, rot, col) in [(99, 105, 64, 46, 43, TEAL), (251, 208, 92, 54, 0, AMBER)]:
    X, Y = t3(cx, cy)
    svg.append(f'<ellipse cx="{X}" cy="{Y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {X} {Y})" fill="{col}" fill-opacity=".05" stroke="{col}" stroke-opacity=".7" stroke-dasharray="5 4" stroke-width="1.4"/>')
for k, (cx, cy) in SUBS3.items():
    col = TEAL if k[0] == "A" else AMBER
    X, Y = t3(cx, cy)
    if k[0] == "A":
        svg.append(f'<circle cx="{X}" cy="{Y}" r="17" fill="none" stroke="{col}" stroke-opacity=".75" stroke-width="1.3"/>')
    for x, y in P3[k]:
        X2, Y2 = t3(x, y)
        svg.append(f'<circle cx="{X2:.1f}" cy="{Y2:.1f}" r="3.4" fill="{col}"/>')
    if k[0] == "A":
        svg.append(text(X - 24, Y + 4, k, 12, col, "600", "end"))
    else:
        svg.append(text(X, Y + 26, k, 12, col, "600", "middle"))
# distance hints between B sub-groups: two equal measurement bars meeting at B2
yb = 186
for (x1, x2) in [(SUBS3["B1"][0], SUBS3["B2"][0]), (SUBS3["B2"][0], SUBS3["B3"][0])]:
    X1, Y1 = t3(x1, yb)
    X2, _ = t3(x2, yb)
    svg.append(f'<path d="M{X1+3} {Y1}H{X2-3}M{X1+3} {Y1-4}V{Y1+4}M{X2-3} {Y1-4}V{Y1+4}" stroke="{MUTED}" stroke-width="1"/>')
X, Y = t3(SUBS3["B2"][0], yb - 12)
svg.append(text(X, Y, "≈ equal gaps", 11, MUTED, "400", "middle"))
svg.append(text(24, 280, "(a) Data", 13, INK, "600"))


def tree(ox, oy, variant, label):
    lx = {"A1": 50, "A2": 105, "B1": 185, "B2": 245, "B3": 305}
    base, hA, hPair, hB, hRoot = 228, 150, 178, 128, 64
    g = []
    L = lambda d, col, dash=False, w=2.2: g.append(f'<path d="{d}" transform="translate({ox} {oy})" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{" stroke-dasharray=\"5 4\"" if dash else ""}/>')
    # A part
    L(f"M{lx['A1']} {base}V{hA}H{lx['A2']}V{base}", TEAL)
    a_mid = (lx["A1"] + lx["A2"]) / 2
    if variant == "m1":
        p_mid = (lx["B1"] + lx["B2"]) / 2
        L(f"M{lx['B1']} {base}V{hPair}H{lx['B2']}V{base}", PURPLE)
        L(f"M{p_mid} {hPair}V{hB}H{lx['B3']}V{base}", AMBER)
        b_mid = (p_mid + lx["B3"]) / 2
    elif variant == "m2":
        p_mid = (lx["B2"] + lx["B3"]) / 2
        L(f"M{lx['B2']} {base}V{hPair}H{lx['B3']}V{base}", PURPLE)
        L(f"M{lx['B1']} {base}V{hB}H{p_mid}V{hPair}", AMBER)
        b_mid = (lx["B1"] + p_mid) / 2
    else:
        L(f"M{lx['B1']} {base}V{hB}H{lx['B3']}V{base}M{lx['B2']} {base}V{hB}", AMBER)
        b_mid = lx["B2"]
    L(f"M{a_mid} {hA}V{hRoot}H{b_mid}V{hB}M{(a_mid+b_mid)/2} {hRoot}V{hRoot-20}", INK)
    for k, x in lx.items():
        col = TEAL if k[0] == "A" else AMBER
        g.append(f'<circle cx="{ox+x}" cy="{oy+base}" r="5" fill="{col}"/>')
        g.append(text(ox + x, oy + base + 22, k, 12, col, "600", "middle"))
    if variant in ("m1", "m2"):
        px = ((lx["B1"] + lx["B2"]) / 2) if variant == "m1" else ((lx["B2"] + lx["B3"]) / 2)
        g.append(text(ox + px, oy + hPair + 20, "{B1, B2}" if variant == "m1" else "{B2, B3}", 11, PURPLE, "600", "middle"))
    else:
        g.append(text(ox + lx["B2"] + 8, oy + hB - 8, "3-way merge", 11, MUTED, "400", "start"))
    g.append(text(ox + 14, oy + 270, label, 13, INK, "600"))
    return g


svg += tree(370, 10, "back", "(b) Shared backbone")
svg += tree(10, 290, "m1", "(c) Admissible method 1")
svg += tree(370, 290, "m2", "(d) Admissible method 2")
svg.append("</svg>")
open(f"{OUT}/backbone.svg", "w").write("\n".join(svg) + "\n")
print("ok")
