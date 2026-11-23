"""Generate the figures of the hierarchical clustering research page.

Usage (from the repository root):  python3 _scripts/research_figures.py assets/img/research
Writes clustering-at-work.svg (the opening figure), flat-clusterings.svg (Figure 1),
backbone.svg (Figure 3), ultrametric.svg (Figure 4) and refinement-order.svg (Figure 5). Figure 1 uses the same
points as hierarchy-example.svg (Figure 2): same sub-cluster centers and random seed.
"""
import math, random, sys

OUT = sys.argv[1]
TEAL, TEAL2, AMBER, RED, BLUE, PURPLE = "#0d6470", "#4a9aa6", "#b26b12", "#b8433a", "#3b6fb6", "#7b5ea7"
INK, MUTED, LINE, LINE_STRONG = "#1b2329", "#6b757d", "#e3e0d8", "#cfcac0"
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

# ---------------------------------------------------------------- Figure 5
# The refinement order on the dissimilarity of Example 2 in the paper: each arrow points to a
# finer method, which adds clusters. Global separation is refined both by non-binary single
# linkage and by Bryant-Berry stable clusters. These two cannot be combined: {1,2,3,5} and
# {1,2,3,4} overlap.
D = [[0, 1, 2, 4, 3], [1, 0, 4, 5, 6], [2, 4, 0, 5, 6], [4, 5, 5, 0, 7], [3, 6, 6, 7, 0]]
W, H = 720, 380
RED = "#b8433a"
svg = head(W, H, "Admissible methods ordered by refinement",
           "Left: a 5 by 5 dissimilarity matrix. Right: three hierarchies of the same five points, arranged from coarse (bottom) to fine (top). "
           "Global separation finds {1,2}; single linkage adds {1,2,3} and {1,2,3,5}; stable clusters add {1,2,3} and {1,2,3,4} instead. "
           "The two top hierarchies cannot be combined because {1,2,3,5} and {1,2,3,4} overlap without being nested.")
CLUSTER_COL = {frozenset({1, 2}): TEAL, frozenset({1, 2, 3}): TEAL, frozenset({1, 2, 3, 5}): AMBER, frozenset({1, 2, 3, 4}): PURPLE}

# (a) the dissimilarity matrix
cell, mx, my = 26, 40, 140
svg.append(text(mx + 65, my - 34, "(a) Dissimilarity d", 13, INK, "600", "middle"))
for i in range(5):
    svg.append(text(mx - 10, my + i * cell + 17, str(i + 1), 11, MUTED, "600", "middle"))
    svg.append(text(mx + i * cell + 13, my - 8, str(i + 1), 11, MUTED, "600", "middle"))
    for j in range(5):
        v = D[i][j]
        shade = 0.04 + 0.5 * (1 - v / 7) if i != j else 0
        svg.append(f'<rect x="{mx + j*cell}" y="{my + i*cell}" width="{cell}" height="{cell}" fill="{TEAL}" fill-opacity="{shade:.2f}" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(text(mx + j * cell + 13, my + i * cell + 17, str(v), 11, INK if i != j else MUTED, "400", "middle"))
svg.append(f'<line x1="196" y1="24" x2="196" y2="360" stroke="{LINE}"/>')


def hierarchy_tree(ox, oy, clusters, order, label):
    """Draw the hierarchy (root, leaves and the given clusters) as a layered tree in a 200x110 box."""
    leaves = [frozenset({k}) for k in order]
    nodes = [frozenset(order)] + sorted((frozenset(c) for c in clusters), key=len, reverse=True)
    def children(n):
        inner = [m for m in nodes if m < n and not any(m < k < n for k in nodes)]
        covered = set().union(*inner) if inner else set()
        return inner + [l for l in leaves if not (l & covered) and l <= n]
    def depth(n):
        return sum(1 for m in nodes if n < m)
    x = {l: ox + 20 + 40 * i for i, l in enumerate(leaves)}
    y_leaf = oy + 96
    levels = max(depth(n) for n in nodes) + 1
    def ypos(n):
        return oy + 10 + depth(n) * (70 / max(levels, 1))
    def xpos(n):
        if n in x:
            return x[n]
        ch = children(n)
        x[n] = sum(xpos(c) for c in ch) / len(ch)
        return x[n]
    g = []
    for n in sorted(nodes, key=len):
        ch = children(n)
        col = CLUSTER_COL.get(n, INK)
        yn = ypos(n)
        xs = [xpos(c) for c in ch]
        g.append(f'<path d="M{min(xs):.1f} {yn:.1f}H{max(xs):.1f}" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
        for c in ch:
            yc = y_leaf if c in leaves else ypos(c)
            g.append(f'<path d="M{xpos(c):.1f} {yn:.1f}V{yc:.1f}" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
    root = nodes[0]
    g.append(f'<path d="M{xpos(root):.1f} {ypos(root):.1f}v-10" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    for l in leaves:
        g.append(f'<circle cx="{x[l]}" cy="{y_leaf}" r="4" fill="{INK}"/>')
        g.append(text(x[l], y_leaf + 17, str(next(iter(l))), 11, INK, "600", "middle"))
    for n in nodes[1:]:
        col = CLUSTER_COL.get(n, INK)
        lab = "{" + ",".join(str(k) for k in sorted(n)) + "}"
        g.append(text(xpos(n) - 5, ypos(n) - 5, lab, 10, col, "600", "end"))
    g.append(text(ox + 100, oy + 132, label, 12, INK, "600", "middle"))
    return g


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr4)"/>'


svg.insert(4, f'<defs><marker id="arr4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker></defs>')
svg.append(text(458, 22, "(b) Hierarchies of d, from fine (top) to coarse (bottom)", 13, INK, "600", "middle"))
svg += hierarchy_tree(232, 44, [{1, 2}, {1, 2, 3}, {1, 2, 3, 5}], [1, 2, 3, 5, 4], "Single linkage")
svg += hierarchy_tree(486, 44, [{1, 2}, {1, 2, 3}, {1, 2, 3, 4}], [1, 2, 3, 4, 5], "Stable clusters")
svg += hierarchy_tree(359, 214, [{1, 2}], [1, 2, 3, 4, 5], "Global separation")
svg.append(arrow(432, 214, 376, 190))
svg.append(arrow(486, 214, 542, 190))
svg.append(text(366, 212, "adds {1,2,3}", 10, TEAL, "600", "end"))
svg.append(text(366, 225, "and {1,2,3,5}", 10, AMBER, "600", "end"))
svg.append(text(552, 212, "adds {1,2,3}", 10, TEAL, "600", "start"))
svg.append(text(552, 225, "and {1,2,3,4}", 10, PURPLE, "600", "start"))
svg.append(f'<path d="M440 110H478" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 3"/>')
svg.append(f'<path d="M453 104l12 12M465 104l-12 12" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>')
svg.append(text(459, 136, "cannot be", 10, RED, "600", "middle"))
svg.append(text(459, 148, "combined", 10, RED, "600", "middle"))
svg.append("</svg>")
open(f"{OUT}/refinement-order.svg", "w").write("\n".join(svg) + "\n")

# ---------------------------------------------------------------- Figure 4: ultrametric and its natural hierarchy
# A 6-point ultrametric: {a,b} merge at 1, {c,d,e} at 2 (a three-way merge), {a,...,e} at 3, all at 4.
# Each matrix entry equals the height at which the two points first meet in the tree.
LAB = ["a", "b", "c", "d", "e", "f"]
U = [[0, 1, 3, 3, 3, 4], [1, 0, 3, 3, 3, 4], [3, 3, 0, 2, 2, 4], [3, 3, 2, 0, 2, 4], [3, 3, 2, 2, 0, 4], [4, 4, 4, 4, 4, 0]]
LEVEL_COL = {1: TEAL, 2: AMBER, 3: PURPLE, 4: INK}
W, H = 720, 300
svg = head(W, H, "An ultrametric and its natural hierarchy",
           "Left: a 6 by 6 dissimilarity matrix on points a to f, with values 1, 2, 3 and 4 coloured by value. Right: the corresponding tree. "
           "Points a and b merge at height 1, points c, d and e merge together at height 2, these five points merge at height 3, and all six at height 4. "
           "Each matrix entry equals the height at which the two points meet in the tree.")
cell, mx, my = 30, 50, 62
svg.append(text(mx + 90, 34, "(a) Ultrametric dissimilarity", 13, INK, "600", "middle"))
for i in range(6):
    svg.append(text(mx - 12, my + i * cell + 20, LAB[i], 12, MUTED, "600", "middle"))
    svg.append(text(mx + i * cell + 15, my - 9, LAB[i], 12, MUTED, "600", "middle"))
    for j in range(6):
        v = U[i][j]
        if i == j:
            svg.append(f'<rect x="{mx + j*cell}" y="{my + i*cell}" width="{cell}" height="{cell}" fill="#f5f8f8" stroke="#ffffff" stroke-width="1.5"/>')
            svg.append(text(mx + j * cell + 15, my + i * cell + 20, "0", 12, MUTED, "400", "middle"))
        else:
            col = LEVEL_COL[v]
            svg.append(f'<rect x="{mx + j*cell}" y="{my + i*cell}" width="{cell}" height="{cell}" fill="{col}" fill-opacity="{0.32 if v < 4 else 0.12}" stroke="#ffffff" stroke-width="1.5"/>')
            svg.append(text(mx + j * cell + 15, my + i * cell + 20, str(v), 12, INK, "600", "middle"))
svg.append(f'<line x1="292" y1="24" x2="292" y2="276" stroke="{LINE}"/>')
# (b) the tree with a height axis
ox, base, unit = 360, 246, 46
xs = {k: ox + 40 + 52 * i for i, k in enumerate(LAB)}
svg.append(text(ox + 170, 34, "(b) Its natural hierarchy", 13, INK, "600", "middle"))
svg.append(f'<path d="M{ox} {base}V{base - 4.4 * unit}" stroke="{LINE_STRONG}" stroke-width="1"/>')
for h in range(0, 5):
    yy = base - h * unit
    svg.append(f'<path d="M{ox - 4} {yy}H{ox}" stroke="{LINE_STRONG}" stroke-width="1"/>')
    svg.append(text(ox - 8, yy + 4, str(h), 11, MUTED, "400", "end"))
    if h:
        svg.append(f'<path d="M{ox} {yy}H{ox + 330}" stroke="{LEVEL_COL[h]}" stroke-opacity=".25" stroke-dasharray="3 4"/>')
svg.append(text(ox - 26, base - 2.2 * unit, "height", 11, MUTED, "400", "middle", f'transform="rotate(-90 {ox - 26} {base - 2.2 * unit})"'))
def ybar(h):
    return base - h * unit
ab = (xs["a"] + xs["b"]) / 2
cde = xs["d"]
top5 = (ab + cde) / 2
root = (top5 + xs["f"]) / 2
paths = [
    (f'M{xs["a"]} {base}V{ybar(1)}H{xs["b"]}V{base}', TEAL),
    (f'M{xs["c"]} {base}V{ybar(2)}H{xs["e"]}V{base}M{xs["d"]} {base}V{ybar(2)}', AMBER),
    (f'M{ab} {ybar(1)}V{ybar(3)}H{cde}V{ybar(2)}', PURPLE),
    (f'M{top5} {ybar(3)}V{ybar(4)}H{xs["f"]}V{base}M{root} {ybar(4)}V{ybar(4) - 12}', INK),
]
for d_, col in paths:
    svg.append(f'<path d="{d_}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
for k, x in xs.items():
    svg.append(f'<circle cx="{x}" cy="{base}" r="5" fill="{INK}"/>')
    svg.append(text(x, base + 22, k, 12, INK, "600", "middle"))
svg.append(text(ab - 6, ybar(1) - 7, "{a, b}", 11, TEAL, "600", "end"))
svg.append(text(xs["e"] + 8, ybar(2) + 4, "{c, d, e}", 11, AMBER, "600", "start"))
svg.append(text(ab - 8, ybar(3) - 7, "{a, b, c, d, e}", 11, PURPLE, "600", "start"))
svg.append("</svg>")
open(f"{OUT}/ultrametric.svg", "w").write("\n".join(svg) + "\n")

# ---------------------------------------------------------------- Clustering at work (unnumbered)
# Top row: clustering on its own (phylogenies, cell types, network communities).
# Bottom row: clustering inside ML systems (nearest-neighbor search, self-supervised
# learning, retrieval for language models).
W, H = 720, 440
TW, TH = 224, 150
TILE_BG = "#f5f8f8"
svg = head(W, H, "Clustering at work",
           "Six small illustrations. Top row, clustering on its own: a phylogenetic tree with colored clades, cells grouped into cell types, "
           "and a network split into communities. Bottom row, clustering inside machine-learning systems: nearest-neighbor search that "
           "visits only the clusters closest to a query, self-supervised learning with cluster assignments as pseudo-labels, and documents "
           "organized into a tree of clusters and summaries for retrieval.")


def tile(ix, row_y, label, body):
    ox, oy = 12 + ix * (TW + 12), row_y
    g = [f'<g transform="translate({ox} {oy})">', f'<rect width="{TW}" height="{TH}" rx="12" fill="{TILE_BG}"/>']
    g += body
    g.append(text(TW / 2, TH + 22, label, 13, INK, "600", "middle"))
    g.append("</g>")
    return g


def line(x1, y1, x2, y2, col, w=1.2, op=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def doc(x, y, col, w=26, h=32):
    g = [f'<path d="M{x} {y}h{w - 8}l8 8v{h - 8}h-{w}z" fill="#ffffff" stroke="{col}" stroke-width="1.3" stroke-linejoin="round"/>']
    for j in range(3):
        g.append(line(x + 5, y + 12 + j * 6, x + w - (5 if j % 2 == 0 else 10), y + 12 + j * 6, col, 1.6, 0.5))
    return g


ROW1, ROW2 = 30, 236
svg.append(text(14, 20, "On its own", 12, MUTED, "600"))
svg.append(text(14, ROW2 - 10, "Inside machine-learning systems", 12, MUTED, "600"))

# 1. phylogeny (rectangular cladogram, clades colored)
b = []
leaves = [24, 40, 56, 76, 92, 112, 128]
cols = [TEAL, TEAL, TEAL, AMBER, AMBER, PURPLE, PURPLE]
XL = 186
def br(d, col):
    b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
yA1 = (leaves[0] + leaves[1]) / 2
br(f"M{XL} {leaves[0]}H150V{leaves[1]}H{XL}", TEAL)
br(f"M150 {yA1}H118V{leaves[2]}H{XL}", TEAL)
br(f"M{XL} {leaves[3]}H140V{leaves[4]}H{XL}", AMBER)
br(f"M{XL} {leaves[5]}H160V{leaves[6]}H{XL}", PURPLE)
yA = (yA1 + leaves[2]) / 2
yB = (leaves[3] + leaves[4]) / 2
yC = (leaves[5] + leaves[6]) / 2
br(f"M140 {yB}H84V{yC}H160", INK)
br(f"M118 {yA}H46V{(yB + yC) / 2}H84", INK)
br(f"M28 {(yA + (yB + yC) / 2) / 2}H46", INK)
for y, c in zip(leaves, cols):
    b.append(f'<circle cx="{XL + 7}" cy="{y}" r="4.5" fill="{c}"/>')
svg += tile(0, ROW1, "Phylogenies", b)

# 2. cell types (embedding-like blobs of cells)
random.seed(3)
b = []
for (cx, cy, sx, sy, col, n) in [(64, 52, 26, 14, TEAL, 16), (156, 44, 18, 16, AMBER, 13), (154, 110, 28, 12, PURPLE, 15), (72, 112, 14, 12, BLUE, 9)]:
    for _ in range(n):
        x, y = random.gauss(cx, sx / 1.6), random.gauss(cy, sy / 1.6)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.2" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1"/>')
        b.append(f'<circle cx="{x + 0.8:.1f}" cy="{y - 0.6:.1f}" r="1.8" fill="{col}"/>')
svg += tile(1, ROW1, "Cell types", b)

# 3. network communities
random.seed(5)
b = []
nodes = []
for ci, ((cx, cy), col) in enumerate([((60, 58), TEAL), ((164, 54), AMBER), ((112, 112), PURPLE)]):
    for k in range(6):
        a = 2 * math.pi * k / 6 + random.uniform(-0.3, 0.3)
        r = random.uniform(14, 26)
        nodes.append((cx + r * math.cos(a), cy + r * 0.8 * math.sin(a), ci, col))
edges = [(i, j) for i in range(len(nodes)) for j in range(i + 1, len(nodes)) if nodes[i][2] == nodes[j][2] and random.random() < 0.55]
bridges = [(2, 9), (8, 15), (4, 13)]
for i, j in edges:
    b.append(line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1], nodes[i][3], 1.2, 0.55))
for i, j in bridges:
    b.append(line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1], MUTED, 1.2, 0.5, "3 3"))
for x, y, _, col in nodes:
    b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="{TILE_BG}" stroke-width="1.5"/>')
svg += tile(2, ROW1, "Network communities", b)

# 4. nearest-neighbor search: the query only visits its two closest clusters
random.seed(9)
b = []
cents = [(46, 40), (112, 30), (184, 44), (40, 112), (110, 92), (180, 116)]
q = (132, 70)
order = sorted(range(len(cents)), key=lambda k: (cents[k][0] - q[0]) ** 2 + (cents[k][1] - q[1]) ** 2)
visited = set(order[:2])
for _ in range(90):
    x, y = random.uniform(14, TW - 14), random.uniform(12, TH - 12)
    k = min(range(len(cents)), key=lambda k: (cents[k][0] - x) ** 2 + (cents[k][1] - y) ** 2)
    if k in visited:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{TEAL}"/>')
    else:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#b9c2c7"/>')
for k, (cx, cy) in enumerate(cents):
    col = TEAL if k in visited else "#9aa4aa"
    b.append(f'<path d="M{cx - 5} {cy}h10M{cx} {cy - 5}v10" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>')
for k in visited:
    b.append(line(q[0], q[1], cents[k][0], cents[k][1], AMBER, 1.5, 0.9, "4 3"))
star = " ".join(f"{q[0] + (9 if i % 2 == 0 else 4) * math.sin(i * math.pi / 5):.1f},{q[1] - (9 if i % 2 == 0 else 4) * math.cos(i * math.pi / 5):.1f}" for i in range(10))
b.append(f'<polygon points="{star}" fill="{AMBER}" stroke="#ffffff" stroke-width="1.2" stroke-linejoin="round"/>')
svg += tile(0, ROW2, "Nearest-neighbor search", b)

# 5. self-supervised learning: cluster assignments become pseudo-labels for images
b = []
thumbs = [(18, 20, TEAL, "sun"), (18, 62, AMBER, "hill"), (18, 104, PURPLE, "box"), (62, 20, AMBER, "hill"), (62, 62, PURPLE, "box"), (62, 104, TEAL, "sun")]
for (x, y, col, kind) in thumbs:
    b.append(f'<rect x="{x}" y="{y}" width="34" height="28" rx="5" fill="#ffffff" stroke="#c9d1d5"/>')
    if kind == "sun":
        b.append(f'<circle cx="{x + 17}" cy="{y + 14}" r="7" fill="#9aa4aa"/>')
    elif kind == "hill":
        b.append(f'<path d="M{x + 5} {y + 23}L{x + 15} {y + 9}L{x + 22} {y + 17}L{x + 26} {y + 12}L{x + 31} {y + 23}Z" fill="#9aa4aa"/>')
    else:
        b.append(f'<rect x="{x + 10}" y="{y + 7}" width="14" height="14" rx="2" fill="#9aa4aa"/>')
    b.append(f'<circle cx="{x + 33}" cy="{y + 2}" r="5" fill="{col}" stroke="#ffffff" stroke-width="1.5"/>')
random.seed(4)
for (cx, cy, col) in [(170, 42, TEAL), (196, 92, AMBER), (152, 104, PURPLE)]:
    for _ in range(8):
        b.append(f'<circle cx="{random.gauss(cx, 7):.1f}" cy="{random.gauss(cy, 7):.1f}" r="3" fill="{col}"/>')
b.append(f'<path d="M104 70C120 70 124 70 136 70" fill="none" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr)"/>')
b.append(f'<path d="M182 122C172 146 104 148 88 137" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr)"/>')
b.append(text(134, 132, "pseudo-labels", 10, MUTED, "400", "middle"))
svg += tile(1, ROW2, "Self-supervised learning", b)

# 6. retrieval for language models: documents organized into a tree of clusters and summaries
b = []
xs = [14, 48, 82, 116, 150, 184]
colsd = [TEAL, TEAL, AMBER, AMBER, PURPLE, PURPLE]
for x, c in zip(xs, colsd):
    b += doc(x, 104, c)
sumx = [(31, TEAL), (99, AMBER), (167, PURPLE)]
for (x, c), (i1, i2) in zip(sumx, [(0, 1), (2, 3), (4, 5)]):
    b.append(line(xs[i1] + 13, 104, x + 13, 84, c, 1.4, 0.7))
    b.append(line(xs[i2] + 13, 104, x + 13, 84, c, 1.4, 0.7))
    b.append(f'<rect x="{x}" y="58" width="26" height="26" rx="6" fill="{c}" fill-opacity=".16" stroke="{c}" stroke-width="1.3"/>')
    b.append(line(x + 6, 67, x + 20, 67, c, 1.6, 0.8))
    b.append(line(x + 6, 74, x + 16, 74, c, 1.6, 0.8))
    b.append(line(x + 13, 58, 112, 40, INK, 1.4, 0.6))
b.append(f'<rect x="96" y="14" width="32" height="26" rx="6" fill="#ffffff" stroke="{INK}" stroke-width="1.3"/>')
b.append(line(103, 23, 121, 23, INK, 1.6, 0.7))
b.append(line(103, 30, 116, 30, INK, 1.6, 0.7))
svg += tile(2, ROW2, "Retrieval for language models", b)

svg.insert(4, f'<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker></defs>')
svg.append("</svg>")
open(f"{OUT}/clustering-at-work.svg", "w").write("\n".join(svg) + "\n")
print("ok")
