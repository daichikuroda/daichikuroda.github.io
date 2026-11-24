"""Generate the figures of the hierarchical clustering research page.

Usage (from the repository root):  python3 _scripts/research_figures.py assets/img/research
Writes clustering-at-work.svg (the opening figure), flat-clusterings.svg (Figure 1),
backbone.svg (Figure 3), kleinberg-axioms.svg (Figure 4), flat-consistency.svg (Figure 5),
hierarchy.svg (Figure 6), axioms.svg (Figure 7), ultrametric.svg (Figure 8), refinement-order.svg (Figure 9)
and well-separated.svg (Figure 10). Figure 1 uses the same
points as hierarchy-example.svg (Figure 2): same sub-cluster centers and random seed.
"""
import itertools, math, random, sys

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

# ---------------------------------------------------------------- Figure 9: the refinement order
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

# ---------------------------------------------------------------- Figure 8: ultrametric and its natural hierarchy
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

# ---------------------------------------------------------------- Figure 10: well-separated (globally separated) sets
# (a) a set whose largest internal distance is smaller than its smallest distance to the rest;
# (b) a set where this fails; (c) the well-separated sets of a small data set, which are nested.
# Distances are Euclidean distances in the picture; every claim is checked below.
W, H = 720, 330
GREEN, RED = "#2f7d4f", "#b8433a"
svg = head(W, H, "Well-separated sets",
           "Three panels. (a) A set of points whose largest internal distance is smaller than its smallest distance to the other points: it is well separated. "
           "(b) A stretched-out set whose largest internal distance is larger than its distance to a nearby point: it is not well separated. "
           "(c) A small data set with all its well-separated sets outlined; they are nested and form a hierarchy.")


def far_pair(C):
    return max(((a, b) for a in C for b in C), key=lambda ab: math.dist(*ab))


def gap_pair(C, O):
    return min(((a, z) for a in C for z in O), key=lambda az: math.dist(*az))


def well_separated(C, O):
    return math.dist(*far_pair(C)) < math.dist(*gap_pair(C, O))


def seg(a, b, col, dash=None, w=2):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{ds}/>'


def hull_circle(C, col, pad=9, dash="4 4", op=0.08):
    cx = sum(p[0] for p in C) / len(C); cy = sum(p[1] for p in C) / len(C)
    r = max(math.dist((cx, cy), p) for p in C) + pad
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-opacity=".7" stroke-width="1.3" stroke-dasharray="{dash}"/>'


def dots(pts, col):
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}"/>' for (x, y) in pts]


# legend
svg.append(seg((150, 26), (176, 26), TEAL))
svg.append(text(182, 30, "largest distance inside the set", 11, INK, "400"))
svg.append(seg((390, 26), (416, 26), AMBER, "4 3"))
svg.append(text(422, 30, "smallest distance to the other points", 11, INK, "400"))

# (a) well separated
ox, oy = 12, 46
C = [(ox + 80 + dx, oy + 120 + dy) for dx, dy in [(-14, -6), (-4, -16), (10, -8), (6, 10), (-10, 12)]]
O = [(ox + x, oy + y) for x, y in [(180, 60), (196, 116), (176, 196), (60, 226), (26, 40), (150, 24)]]
assert well_separated(C, O)
svg.append(f'<rect x="{ox}" y="{oy}" width="220" height="244" rx="12" fill="#f5f8f8"/>')
svg.append(hull_circle(C, TEAL))
a, b = far_pair(C); g1, g2 = gap_pair(C, O)
svg.append(seg(g1, g2, AMBER, "4 3"))
svg += dots(O, "#9aa4aa") + dots(C, TEAL)
svg.append(seg(a, b, TEAL, None, 2.4))
svg.append(text(ox + 110, oy + 270, "(a) Well separated", 13, INK, "600", "middle"))
svg.append(f'<path d="M{ox + 172} {oy + 228}l6 6l12 -14" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')

# (b) not well separated
ox = 250
C = [(ox + 40 + 26 * k, oy + 140 + (6 if k % 2 else -6)) for k in range(6)]
O = [(ox + x, oy + y) for x, y in [(196, 112), (40, 50), (120, 40), (70, 222), (180, 214)]]
assert not well_separated(C, O)
svg.append(f'<rect x="{ox}" y="{oy}" width="220" height="244" rx="12" fill="#f5f8f8"/>')
cx = sum(p[0] for p in C) / len(C); cy = sum(p[1] for p in C) / len(C)
svg.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="80" ry="20" fill="{TEAL}" fill-opacity=".08" stroke="{TEAL}" stroke-opacity=".7" stroke-width="1.3" stroke-dasharray="4 4"/>')
a, b = far_pair(C); g1, g2 = gap_pair(C, O)
svg.append(seg(g1, g2, AMBER, "4 3"))
svg += dots(O, "#9aa4aa") + dots(C, TEAL)
svg.append(seg((a[0], a[1] + 30), (b[0], b[1] + 30), TEAL, None, 2.4))
svg.append(seg((a[0], a[1] + 24), (a[0], a[1] + 36), TEAL, None, 2))
svg.append(seg((b[0], b[1] + 24), (b[0], b[1] + 36), TEAL, None, 2))
svg.append(text(ox + 110, oy + 270, "(b) Not well separated", 13, INK, "600", "middle"))
svg.append(f'<path d="M{ox + 178} {oy + 220}l12 12M{ox + 190} {oy + 220}l-12 12" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>')

# (c) nested well-separated sets
ox = 488
s3 = 12 * math.sqrt(3) / 2
pair = [(ox + 34, oy + 76), (ox + 44, oy + 82)]
Lset = pair + [(ox + 54, oy + 104)]
Rset = [(ox + 104, oy + 80), (ox + 122, oy + 80), (ox + 113, oy + 94)]
Bset = [(ox + 140, oy + 200), (ox + 160, oy + 200), (ox + 150, oy + 216)]
allp = Lset + Rset + Bset
groups = [("pair", pair), ("L", Lset), ("R", Rset), ("B", Bset), ("LR", Lset + Rset)]
for name, G in groups:
    assert well_separated(G, [p for p in allp if p not in G]), name
# brute force: the outlined sets are exactly the nontrivial well-separated sets
found = {frozenset(c) for k in range(2, len(allp)) for c in itertools.combinations(allp, k)
         if well_separated(list(c), [q for q in allp if q not in c])}
assert found == {frozenset(G) for _, G in groups}, found
svg.append(f'<rect x="{ox}" y="{oy}" width="220" height="244" rx="12" fill="#f5f8f8"/>')
LR = Lset + Rset
xs_, ys_ = [q[0] for q in LR], [q[1] for q in LR]
svg.append(f'<ellipse cx="{(min(xs_) + max(xs_)) / 2:.1f}" cy="{(min(ys_) + max(ys_)) / 2:.1f}" rx="{(max(xs_) - min(xs_)) / 2 + 26:.1f}" ry="{(max(ys_) - min(ys_)) / 2 + 28:.1f}" fill="{PURPLE}" fill-opacity=".05" stroke="{PURPLE}" stroke-opacity=".7" stroke-width="1.3" stroke-dasharray="4 4"/>')
svg.append(hull_circle(Lset, TEAL, pad=8))
svg.append(hull_circle(pair, TEAL, pad=6, dash="2 3", op=0.06))
svg.append(hull_circle(Rset, AMBER, pad=8))
svg.append(hull_circle(Bset, BLUE, pad=9))
svg += dots(Lset, TEAL) + dots(Rset, AMBER) + dots(Bset, BLUE)
svg.append(text(ox + 110, oy + 270, "(c) Nested well-separated sets", 13, INK, "600", "middle"))
svg.append("</svg>")
open(f"{OUT}/well-separated.svg", "w").write("\n".join(svg) + "\n")

# ---------------------------------------------------------------- Shared helpers for the definition figures
def outline(pts, col, pad=10, dash="4 4", op=0.08, sw=1.3):
    xs_, ys_ = [q[0] for q in pts], [q[1] for q in pts]
    cx, cy = (min(xs_) + max(xs_)) / 2, (min(ys_) + max(ys_)) / 2
    rx, ry = (max(xs_) - min(xs_)) / 2 + pad, (max(ys_) - min(ys_)) / 2 + pad
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}" fill-opacity="{op}" '
            f'stroke="{col}" stroke-opacity=".75" stroke-width="{sw}" stroke-dasharray="{dash}"/>')


def box(pts, col, pad=12, dash="4 4", op=0.03):
    xs_, ys_ = [q[0] for q in pts], [q[1] for q in pts]
    return (f'<rect x="{min(xs_) - pad:.1f}" y="{min(ys_) - pad:.1f}" width="{max(xs_) - min(xs_) + 2 * pad:.1f}" height="{max(ys_) - min(ys_) + 2 * pad:.1f}" rx="{pad + 6:.1f}" '
            f'fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-opacity=".75" stroke-width="1.3" stroke-dasharray="{dash}"/>')


def pt(x, y, col, label=None, hollow=False, r=4.2, dy=-8):
    g = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{"#ffffff" if hollow else col}" stroke="{col}" stroke-width="{1.6 if hollow else 0}"/>']
    if label is not None:
        g.append(text(x, y + dy, label, 10, INK, "600", "middle"))
    return g


def big_arrow(x1, x2, y, label):
    return [f'<path d="M{x1} {y}H{x2}" stroke="{MUTED}" stroke-width="1.6" marker-end="url(#arrA)"/>',
            text((x1 + x2) / 2, y - 8, label, 10, MUTED, "400", "middle")]


ARROW_DEF = (f'<defs><marker id="arrA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
             f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUTED}"/></marker></defs>')


# ---------------------------------------------------------------- Figure 4: Kleinberg's axioms (flat clustering)
# Same panel layout as the admissibility figure (Figure 7).
W, H = 720, 470
PW, PH = 348, 206
svg = head(W, H, "Strengthening and Kleinberg's three axioms",
           "Four panels, each showing data before and after a change. Strengthening: distances inside each cluster shrink and distances between clusters grow. "
           "Scale invariance: enlarging all distances keeps the same clusters. "
           "Richness: for any chosen grouping of the points, some data make this grouping the output. "
           "Consistency: after pulling the points of each cluster together and pushing clusters apart, the output stays the same.")
svg.insert(4, ARROW_DEF)


def kpanel(ix, iy, title):
    ox, oy = 12 + ix * (PW + 12), 12 + iy * (PH + 28)
    svg.append(f'<rect x="{ox}" y="{oy}" width="{PW}" height="{PH}" rx="12" fill="#f5f8f8"/>')
    svg.append(text(ox + 14, oy + 22, title, 13, INK, "600"))
    return ox, oy


def seg2(a, b, col, dash=None, w=1.8):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="{col}" stroke-width="{w}"{da} stroke-linecap="round"/>'


# 1. strengthening of the partition {A, B}: one distance inside A (solid) shrinks, one distance
#    between A and B (dashed) grows; every pairwise distance is checked below.
ox, oy = kpanel(0, 0, "Strengthening")
shapeA = [(-20, -12), (6, -20), (18, 8), (-8, 18)]
shapeB = [(0, -12), (11, 7), (-11, 7)]
def place2(c, shape, s):
    return [(c[0] + s * x, c[1] + s * y) for x, y in shape]
A0, B0 = place2((ox + 46, oy + 94), shapeA, 1.0), place2((ox + 110, oy + 94), shapeB, 1.0)
A1, B1 = place2((ox + 216, oy + 94), shapeA, 0.55), place2((ox + 310, oy + 94), shapeB, 0.7)
for i in range(len(shapeA)):
    for j in range(len(shapeA)):
        assert math.dist(A1[i], A1[j]) <= math.dist(A0[i], A0[j]) + 1e-9
    for k in range(len(shapeB)):
        assert math.dist(A1[i], B1[k]) >= math.dist(A0[i], B0[k]) - 1e-9
for i in range(len(shapeB)):
    for j in range(len(shapeB)):
        assert math.dist(B1[i], B1[j]) <= math.dist(B0[i], B0[j]) + 1e-9
for (A_, B_, pad, lab_dy) in [(A0, B0, 11, 0), (A1, B1, 9, 0)]:
    svg.append(outline(A_, TEAL, pad=pad))
    svg.append(outline(B_, AMBER, pad=pad))
    svg.append(seg2(A_[0], A_[2], TEAL))          # x - y, inside A
    svg.append(seg2(A_[2], B_[2], MUTED, "3 3"))   # y - z, between A and B
    for q in A_:
        svg += pt(*q, TEAL, r=3.8)
    for q in B_:
        svg += pt(*q, AMBER, r=3.8)
    for q, lab, dx, dy in [(A_[0], "x", -9, -4), (A_[2], "y", 4, 15), (B_[2], "z", -4, 15)]:
        svg.append(text(q[0] + dx, q[1] + dy, lab, 10, INK, "600", "middle", 'font-style="italic"'))
svg.append(text(ox + 46, oy + 140, "A", 11, TEAL, "600", "middle"))
svg.append(text(ox + 110, oy + 140, "B", 11, AMBER, "600", "middle"))
svg.append(text(ox + 216, oy + 140, "A", 11, TEAL, "600", "middle"))
svg.append(text(ox + 310, oy + 140, "B", 11, AMBER, "600", "middle"))
svg += big_arrow(ox + 146, ox + 186, oy + 98, "strengthen")
svg.append(seg2((ox + 62, oy + PH - 34), (ox + 84, oy + PH - 34), TEAL))
svg.append(text(ox + 90, oy + PH - 30, "same cluster: distances shrink", 11, INK))
svg.append(seg2((ox + 62, oy + PH - 16), (ox + 84, oy + PH - 16), MUTED, "3 3"))
svg.append(text(ox + 90, oy + PH - 12, "different clusters: distances grow", 11, INK))

# 2. scale invariance: as in the admissibility figure, but the output is just the partition
ox, oy = kpanel(1, 0, "Scale invariance")
for (cx, cy, k) in [(ox + 40, oy + 96, 0.8), (ox + 222, oy + 84, 1.6)]:
    q = place2((cx, cy), [(0, 0), (12, 8), (-6, 14), (44, 4), (52, 16)], k)
    svg.append(outline(q[:3], TEAL, pad=7 * k))
    svg.append(outline(q[3:], AMBER, pad=7 * k))
    for (x, y) in q:
        svg += pt(x, y, TEAL if (x, y) in q[:3] else AMBER)
svg += big_arrow(ox + 104, ox + 186, oy + 104, "all distances × 2")
svg.append(text(ox + PW / 2, oy + PH - 16, "Same clusters at any scale.", 11, INK, "400", "middle"))

# 3. richness
ox, oy = kpanel(0, 1, "Richness")
cols = {1: TEAL, 2: AMBER, 3: AMBER, 4: TEAL, 5: AMBER, 6: PURPLE}
ring = {i: (ox + 70 + 38 * math.cos(2 * math.pi * (i - 1) / 6 - math.pi / 2), oy + 104 + 38 * math.sin(2 * math.pi * (i - 1) / 6 - math.pi / 2)) for i in range(1, 7)}
for i, (x, y) in ring.items():
    svg += pt(x, y, cols[i], str(i), dy=-9)
svg.append(text(ox + 70, oy + 172, "any grouping", 10, MUTED, "400", "middle"))
svg += big_arrow(ox + 128, ox + 186, oy + 104, "some data")
pos = {1: (220, 76), 4: (236, 90), 2: (290, 70), 3: (306, 84), 5: (292, 98), 6: (252, 150)}
pp = {i: (ox + x, oy + y) for i, (x, y) in pos.items()}
svg.append(outline([pp[1], pp[4]], TEAL, pad=10))
svg.append(outline([pp[2], pp[3], pp[5]], AMBER, pad=10))
svg.append(outline([pp[6]], PURPLE, pad=9))
for i, (x, y) in pp.items():
    svg += pt(x, y, cols[i], str(i), dy=-9)
svg.append(text(ox + PW / 2, oy + PH - 16, "Every grouping is the output for some data.", 11, INK, "400", "middle"))

# 4. consistency: both clusters are made tighter and pushed apart (a strengthening of the output);
#    the output must be the same partition {A, B}.
ox, oy = kpanel(1, 1, "Consistency")
ringA = [(ox + 56 + 30 * math.cos(2 * math.pi * k / 6), oy + 100 + 30 * math.sin(2 * math.pi * k / 6)) for k in range(6)]
B_before = [(ox + 120, oy + 92), (ox + 128, oy + 110), (ox + 112, oy + 112)]
A_after = [(ox + 217 + 0.4 * (x - ox - 56), oy + 100 + 0.4 * (y - oy - 100)) for (x, y) in ringA]
cB = (ox + 120, oy + 104.67)
B_after = [(ox + 316 + 0.7 * (x - cB[0]), oy + 100 + 0.7 * (y - cB[1])) for (x, y) in B_before]
for i in range(6):
    for j in range(6):
        assert math.dist(A_after[i], A_after[j]) <= math.dist(ringA[i], ringA[j]) + 1e-9
    for k in range(3):
        assert math.dist(A_after[i], B_after[k]) >= math.dist(ringA[i], B_before[k]) - 1e-9
for i in range(3):
    for j in range(3):
        assert math.dist(B_after[i], B_after[j]) <= math.dist(B_before[i], B_before[j]) + 1e-9
svg.append(outline(ringA, TEAL, pad=10))
svg.append(outline(B_before, AMBER, pad=9))
for q in ringA:
    svg += pt(*q, TEAL)
for q in B_before:
    svg += pt(*q, AMBER)
svg += big_arrow(ox + 144, ox + 184, oy + 104, "strengthen")
svg.append(outline(A_after, TEAL, pad=8))
svg.append(outline(B_after, AMBER, pad=8))
for q in A_after:
    svg += pt(*q, TEAL, r=3.6)
for q in B_after:
    svg += pt(*q, AMBER, r=3.6)
svg.append(text(ox + 56, oy + 152, "A", 11, TEAL, "600", "middle"))
svg.append(text(ox + 120, oy + 136, "B", 11, AMBER, "600", "middle"))
svg.append(text(ox + 217, oy + 136, "A", 11, TEAL, "600", "middle"))
svg.append(text(ox + 316, oy + 136, "B", 11, AMBER, "600", "middle"))
svg.append(text(ox + PW / 2, oy + PH - 30, "Clusters made tighter and further apart", 11, INK, "400", "middle"))
svg.append(text(ox + PW / 2, oy + PH - 16, "are found again: the output stays A and B.", 11, INK, "400", "middle"))
svg.append("</svg>")
open(f"{OUT}/kleinberg-axioms.svg", "w").write("\n".join(svg) + "\n")


# ---------------------------------------------------------------- Figure 5: the problem with consistency for flat clustering
# A strengthening of the partition {C1 u C2, C3} that turns C1 and C2 into groups of their own.
# A consistent flat method must still return exactly {C1 u C2, C3}; a hierarchy can add C1 and C2.
W, H = 720, 262
svg = head(W, H, "Why consistency is a problem for flat clustering",
           "Three panels. (a) Data with two clusters: a loose ring of six points, three filled and three hollow, and a small group of three points. "
           "(b) After a strengthening, the filled and hollow points form two tight groups next to each other and the small group is further away; "
           "a consistent flat method must still return the same two clusters. "
           "(c) On the same data, a hierarchy keeps the big cluster and adds the two tight groups inside it.")


def cname(i, extra=None, idx2=None):
    """Italic C with subscript i, optionally followed by ' u C_idx2'."""
    s = f'<tspan font-style="italic">C</tspan><tspan font-size="8" dy="3">{i}</tspan>'
    if idx2 is not None:
        s += f'<tspan dy="-3"> ∪ </tspan><tspan font-style="italic">C</tspan><tspan font-size="8" dy="3">{idx2}</tspan>'
    return s


def ring_pts(cx, cy, R):
    pts_ = [(cx + R * math.cos(math.pi / 6 + math.pi * k / 3), cy + R * math.sin(math.pi / 6 + math.pi * k / 3)) for k in range(6)]
    return pts_[0::2], pts_[1::2]


def tri(cx, cy, r, up=True):
    s_ = -1 if up else 1
    return [(cx + r * math.cos(math.pi / 2 + 2 * math.pi * k / 3) * (1 if up else -1), cy + s_ * r * math.sin(math.pi / 2 + 2 * math.pi * k / 3)) for k in range(3)]


# relative coordinates inside a panel
C1_0, C2_0 = ring_pts(70, 98, 40)
C3_0 = tri(156, 98, 11)
C1_1, C2_1 = tri(36, 100, 5, up=True), tri(62, 100, 5, up=False)
C3_1 = tri(200, 100, 7)
A0, A1_ = C1_0 + C2_0, C1_1 + C2_1
for i in range(6):
    for j in range(6):
        assert math.dist(A1_[i], A1_[j]) <= math.dist(A0[i], A0[j]) + 1e-9
    for k in range(3):
        assert math.dist(A1_[i], C3_1[k]) >= math.dist(A0[i], C3_0[k]) - 1e-9
for i in range(3):
    for j in range(3):
        assert math.dist(C3_1[i], C3_1[j]) <= math.dist(C3_0[i], C3_0[j]) + 1e-9
# after the strengthening, C1 and C2 are groups of their own: each is tighter than its distance to the rest
for G, O in [(C1_1, C2_1 + C3_1), (C2_1, C1_1 + C3_1)]:
    assert max(math.dist(p, q) for p in G for q in G) < min(math.dist(p, q) for p in G for q in O)


def draw(ox, oy, c1, c2, c3, r=4.2):
    g = []
    for q in c1:
        g += pt(ox + q[0], oy + q[1], TEAL, r=r)
    for q in c2:
        g += pt(ox + q[0], oy + q[1], TEAL, hollow=True, r=r)
    for q in c3:
        g += pt(ox + q[0], oy + q[1], AMBER, r=r)
    return g


def sh(ox, oy, P_):
    return [(ox + x, oy + y) for x, y in P_]


oy = 12
PW3, PH3 = 226, 210
for ix, label in enumerate(["(a) Before", "(b) After: flat clustering", "(c) After: hierarchy"]):
    ox = 12 + ix * (PW3 + 12)
    svg.append(f'<rect x="{ox}" y="{oy}" width="{PW3}" height="{PH3}" rx="12" fill="#f5f8f8"/>')
    svg.append(text(ox + PW3 / 2, oy + PH3 + 26, label, 13, INK, "600", "middle"))

# (a)
ox = 12
svg.append(outline(sh(ox, oy, A0), TEAL, pad=12))
svg.append(outline(sh(ox, oy, C3_0), AMBER, pad=9))
svg += draw(ox, oy, C1_0, C2_0, C3_0)
svg.append(text(ox + 70, oy + 168, cname(1, idx2=2), 12, TEAL, "600", "middle"))
svg.append(text(ox + 156, oy + 134, cname(3), 12, AMBER, "600", "middle"))

# (b) a consistent flat method returns the same partition
ox = 12 + PW3 + 12
svg.append(outline(sh(ox, oy, A1_), TEAL, pad=10))
svg.append(outline(sh(ox, oy, C3_1), AMBER, pad=8))
svg += draw(ox, oy, C1_1, C2_1, C3_1, r=3.8)
svg.append(text(ox + 49, oy + 134, cname(1, idx2=2), 12, TEAL, "600", "middle"))
svg.append(text(ox + 200, oy + 132, cname(3), 12, AMBER, "600", "middle"))
svg.append(text(ox + PW3 / 2, oy + 170, "A consistent flat method must return", 11, INK, "400", "middle"))
svg.append(text(ox + PW3 / 2, oy + 186, "the same two clusters.", 11, INK, "400", "middle"))

# (c) a hierarchy keeps C1 u C2 and adds C1 and C2
ox = 12 + 2 * (PW3 + 12)
svg.append(outline(sh(ox, oy, A1_), TEAL, pad=13))
svg.append(outline(sh(ox, oy, C1_1), TEAL, pad=5, dash="2 3", op=0.14))
svg.append(outline(sh(ox, oy, C2_1), TEAL, pad=5, dash="2 3", op=0.14))
svg.append(outline(sh(ox, oy, C3_1), AMBER, pad=8))
svg += draw(ox, oy, C1_1, C2_1, C3_1, r=3.8)
svg.append(text(ox + 34, oy + 74, cname(1), 12, TEAL, "600", "middle"))
svg.append(text(ox + 64, oy + 74, cname(2), 12, TEAL, "600", "middle"))
svg.append(text(ox + 49, oy + 137, cname(1, idx2=2), 12, TEAL, "600", "middle"))
svg.append(text(ox + 200, oy + 132, cname(3), 12, AMBER, "600", "middle"))
svg.append(text(ox + PW3 / 2, oy + 170, "A hierarchy keeps both clusters", 11, INK, "400", "middle"))
svg.append(text(ox + PW3 / 2, oy + 186, "and adds the two new groups.", 11, INK, "400", "middle"))
svg.append("</svg>")
open(f"{OUT}/flat-consistency.svg", "w").write("\n".join(svg) + "\n")


# ---------------------------------------------------------------- Figure 6: what a hierarchy is
W, H = 720, 290
svg = head(W, H, "A hierarchy as nested clusters and as a tree",
           "Three panels. (a) Seven points a to g with nested clusters: {a,b} inside {a,b,c}, {f,g} inside {d,e,f,g}, all inside the whole set. "
           "(b) The same hierarchy drawn as a tree, with the whole set at the root and single points as leaves. "
           "(c) Two clusters {a,b,c} and {c,d} that overlap without one containing the other: they cannot both belong to a hierarchy.")
svg.insert(4, ARROW_DEF)
P7 = {"a": (40, 90), "b": (58, 104), "c": (84, 84), "d": (140, 118), "e": (166, 98), "f": (176, 140), "g": (196, 128)}
ox, oy = 12, 34
svg.append(f'<rect x="{ox}" y="{oy}" width="226" height="216" rx="12" fill="#f5f8f8"/>')
g = []
pts = {k: (ox + x, oy + y) for k, (x, y) in P7.items()}
g.append(box(list(pts.values()), "#8a949b", pad=26))
g.append(outline([pts["a"], pts["b"], pts["c"]], TEAL, pad=12))
g.append(outline([pts["a"], pts["b"]], TEAL, pad=7, op=0.1))
g.append(outline([pts[k] for k in "defg"], AMBER, pad=12))
g.append(outline([pts["f"], pts["g"]], AMBER, pad=7, op=0.1))
for k, (x, y) in pts.items():
    g += pt(x, y, INK, k, dy=17)
svg += g
svg.append(text(ox + 113, oy + 240, "(a) Nested clusters", 13, INK, "600", "middle"))

# (b) the same hierarchy as a tree
ox = 250
svg.append(f'<rect x="{ox}" y="{oy}" width="226" height="216" rx="12" fill="#f5f8f8"/>')
lx = {k: ox + 24 + 30 * i for i, k in enumerate("abcdefg")}
yl, y1, y2, yr = oy + 176, oy + 134, oy + 96, oy + 54
def br(d_, col):
    svg.append(f'<path d="{d_}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
ab = (lx["a"] + lx["b"]) / 2
fg = (lx["f"] + lx["g"]) / 2
abc = (ab + lx["c"]) / 2
defg = (lx["d"] + lx["e"] + fg) / 3
br(f'M{lx["a"]} {yl}V{y1}H{lx["b"]}V{yl}', TEAL)
br(f'M{ab} {y1}V{y2}H{lx["c"]}V{yl}', TEAL)
br(f'M{lx["f"]} {yl}V{y1}H{lx["g"]}V{yl}', AMBER)
br(f'M{lx["d"]} {yl}V{y2}H{fg}V{y1}M{lx["e"]} {yl}V{y2}', AMBER)
br(f'M{abc} {y2}V{yr}H{defg}V{y2}M{(abc + defg) / 2} {yr}V{yr - 14}', INK)
for k, x in lx.items():
    svg += pt(x, yl, INK, k, dy=18)
svg.append(text((abc + defg) / 2 + 8, yr - 6, "root: all points", 10, MUTED, "400", "start"))
svg.append(text(ox + 113, yl + 34, "leaves: single points", 10, MUTED, "400", "middle"))
svg.append(text(ox + 113, oy + 240, "(b) The same hierarchy as a tree", 13, INK, "600", "middle"))

# (c) not a hierarchy
ox = 488
svg.append(f'<rect x="{ox}" y="{oy}" width="220" height="216" rx="12" fill="#f5f8f8"/>')
Q = {"a": (40, 110), "b": (64, 124), "c": (96, 104), "d": (150, 112)}
qp = {k: (ox + x, oy + y) for k, (x, y) in Q.items()}
svg.append(outline([qp["a"], qp["b"], qp["c"]], TEAL, pad=14))
svg.append(outline([qp["c"], qp["d"]], PURPLE, pad=14))
for k, (x, y) in qp.items():
    svg += pt(x, y, INK, k, dy=20)
svg.append(f'<path d="M{ox + 176} {oy + 176}l14 14M{ox + 190} {oy + 176}l-14 14" stroke="#b8433a" stroke-width="2.6" stroke-linecap="round"/>')
svg.append(text(ox + 110, oy + 58, "{a, b, c} and {c, d} overlap", 10, MUTED, "400", "middle"))
svg.append(text(ox + 110, oy + 72, "without one containing the other", 10, MUTED, "400", "middle"))
svg.append(text(ox + 110, oy + 240, "(c) Not a hierarchy", 13, INK, "600", "middle"))
svg.append("</svg>")
open(f"{OUT}/hierarchy.svg", "w").write("\n".join(svg) + "\n")


# ---------------------------------------------------------------- Figure 7: the four axioms
W, H = 720, 470
PW, PH = 348, 206
svg = head(W, H, "The four axioms of admissibility",
           "Four panels, each showing data before and after a change. Scale invariance: enlarging all distances keeps the same clusters. "
           "Partition richness: for any chosen grouping of the points, some data make these groups clusters. "
           "Partition consistency: pulling the points of each cluster together and pushing clusters apart keeps these clusters, while new smaller clusters may appear. "
           "Permutation invariance: renaming the points renames the clusters in the same way.")
svg.insert(4, ARROW_DEF)


def panel(ix, iy, title):
    ox, oy = 12 + ix * (PW + 12), 12 + iy * (PH + 28)
    svg.append(f'<rect x="{ox}" y="{oy}" width="{PW}" height="{PH}" rx="12" fill="#f5f8f8"/>')
    svg.append(text(ox + 14, oy + 22, title, 13, INK, "600"))
    return ox, oy


# 1. scale invariance
ox, oy = panel(0, 0, "Scale invariance")
base = [(0, 0), (12, 8), (-6, 14), (44, 4), (52, 16)]
def place(cx, cy, k):
    return [(cx + k * x, cy + k * y) for x, y in base]
for (cx, cy, k) in [(ox + 40, oy + 96, 0.8), (ox + 222, oy + 84, 1.6)]:
    q = place(cx, cy, k)
    svg.append(box(q, "#8a949b", pad=12 * k))
    svg.append(outline(q[:3], TEAL, pad=7 * k))
    svg.append(outline(q[3:], AMBER, pad=7 * k))
    for (x, y) in q:
        svg += pt(x, y, TEAL if (x, y) in q[:3] else AMBER)
svg += big_arrow(ox + 104, ox + 186, oy + 104, "all distances × 2")
svg.append(text(ox + PW / 2, oy + PH - 16, "Same clusters at any scale.", 11, INK, "400", "middle"))

# 2. partition richness
ox, oy = panel(1, 0, "Partition richness")
cols = {1: TEAL, 2: AMBER, 3: AMBER, 4: TEAL, 5: AMBER, 6: PURPLE}
ring = {i: (ox + 70 + 38 * math.cos(2 * math.pi * (i - 1) / 6 - math.pi / 2), oy + 104 + 38 * math.sin(2 * math.pi * (i - 1) / 6 - math.pi / 2)) for i in range(1, 7)}
for i, (x, y) in ring.items():
    svg += pt(x, y, cols[i], str(i), dy=-9)
svg.append(text(ox + 70, oy + 172, "any grouping", 10, MUTED, "400", "middle"))
svg += big_arrow(ox + 128, ox + 186, oy + 104, "some data")
pos = {1: (220, 76), 4: (236, 90), 2: (290, 70), 3: (306, 84), 5: (292, 98), 6: (252, 150)}
pp = {i: (ox + x, oy + y) for i, (x, y) in pos.items()}
svg.append(outline([pp[1], pp[4]], TEAL, pad=10))
svg.append(outline([pp[2], pp[3], pp[5]], AMBER, pad=10))
svg.append(outline([pp[6]], PURPLE, pad=9))
for i, (x, y) in pp.items():
    svg += pt(x, y, cols[i], str(i), dy=-9)
svg.append(text(ox + PW / 2, oy + PH - 16, "Every grouping appears in the hierarchy for some data.", 11, INK, "400", "middle"))

# 3. partition consistency: A is a loose ring mixing two hidden subgroups; after strengthening,
#    A's points move closer (all distances inside A shrink), B moves away, and A splits into A1, A2.
ox, oy = panel(0, 1, "Partition consistency")
ringA = [(ox + 56 + 30 * math.cos(2 * math.pi * k / 6), oy + 100 + 30 * math.sin(2 * math.pi * k / 6)) for k in range(6)]
A1_before, A2_before = ringA[0::2], ringA[1::2]
B_before = [(ox + 120, oy + 92), (ox + 128, oy + 110), (ox + 112, oy + 112)]
A1_after = [(ox + 206 + dx, oy + 100 + dy) for dx, dy in [(0, -5), (-4.5, 3), (4.5, 3)]]
A2_after = [(ox + 228 + dx, oy + 100 + dy) for dx, dy in [(0, 5), (-4.5, -3), (4.5, -3)]]
B_after = [(x + 206, y) for (x, y) in B_before]
before_A, after_A = A1_before + A2_before, A1_after + A2_after
for i in range(6):
    for j in range(6):
        assert math.dist(after_A[i], after_A[j]) <= math.dist(before_A[i], before_A[j]) + 1e-9
    for k in range(3):
        assert math.dist(after_A[i], B_after[k]) >= math.dist(before_A[i], B_before[k]) - 1e-9
svg.append(outline(before_A, TEAL, pad=10))
svg.append(outline(B_before, AMBER, pad=9))
for q in A1_before:
    svg += pt(*q, TEAL)
for q in A2_before:
    svg += pt(*q, TEAL, hollow=True)
for q in B_before:
    svg += pt(*q, AMBER)
svg += big_arrow(ox + 144, ox + 184, oy + 104, "strengthen")
svg.append(outline(after_A, TEAL, pad=10))
svg.append(outline(A1_after, TEAL, pad=5, dash="2 3", op=0.12))
svg.append(outline(A2_after, TEAL, pad=5, dash="2 3", op=0.12))
svg.append(outline(B_after, AMBER, pad=9))
for q in A1_after:
    svg += pt(*q, TEAL, r=3.4)
for q in A2_after:
    svg += pt(*q, TEAL, hollow=True, r=3.4)
for q in B_after:
    svg += pt(*q, AMBER)
svg.append(text(ox + 217, oy + 136, "new clusters", 10, TEAL, "600", "middle"))
svg.append(text(ox + PW / 2, oy + PH - 30, "Clusters made tighter and further apart are kept;", 11, INK, "400", "middle"))
svg.append(text(ox + PW / 2, oy + PH - 16, "new, smaller clusters may appear inside them.", 11, INK, "400", "middle"))

# 4. permutation invariance
ox, oy = panel(1, 1, "Permutation invariance")
geo = [(40, 90), (58, 104), (96, 82), (112, 98), (104, 118)]
ren = {1: 3, 2: 5, 3: 1, 4: 2, 5: 4}
for (sx, labels) in [(0, [1, 2, 3, 4, 5]), (186, [ren[i] for i in [1, 2, 3, 4, 5]])]:
    q = [(ox + 20 + sx + x, oy + y) for x, y in geo]
    svg.append(outline(q[:2], TEAL, pad=10))
    svg.append(outline(q[2:], AMBER, pad=10))
    for (x, y), lab in zip(q, labels):
        svg += pt(x, y, TEAL if (x, y) in q[:2] else AMBER, str(lab), dy=-9)
svg += big_arrow(ox + 146, ox + 196, oy + 104, "rename")
svg.append(text(ox + PW / 2, oy + PH - 16, "Renaming the points renames the clusters.", 11, INK, "400", "middle"))
svg.append("</svg>")
open(f"{OUT}/axioms.svg", "w").write("\n".join(svg) + "\n")

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
