#!/usr/bin/env python3
"""Generate the profile hero banner and dock icon SVGs for github.com/Esl1h/Esl1h.

Run once locally to (re)produce assets/hero-{dark,light}.svg and assets/dock/*.svg.
Deterministic: same output every run, no external dependencies.
"""
import math
import os

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
HERO_DIR = os.path.join(REPO_ROOT, "assets")
DOCK_DIR = os.path.join(REPO_ROOT, "assets", "dock")
os.makedirs(HERO_DIR, exist_ok=True)
os.makedirs(DOCK_DIR, exist_ok=True)

MONO = ("ui-monospace, SFMono-Regular, 'DejaVu Sans Mono', "
        "'Liberation Mono', Menlo, monospace")

# ---------------------------------------------------------------------------
# Hero banner: a card with a latency/spectrum bar chart, DNSbench/easy1090
# vocabulary. Two static files (dark, light), selected via <picture>.
# ---------------------------------------------------------------------------

HERO_THEMES = {
    "dark": dict(
        bg="#0E1620", border="#1E2C3A", grid="#182534",
        name="#D8E1E8", dim="#6E8090", amber="#E8A33D",
        grad_from="#57A6B8", grad_to="#E8A33D",
    ),
    "light": dict(
        bg="#F4F6F8", border="#DCE3E9", grid="#E6EBEF",
        name="#16202A", dim="#5C6C79", amber="#B5771A",
        grad_from="#2F7C90", grad_to="#B5771A",
    ),
}

STACK_TAGS = ["shell", "v", "python", "terraform", "dns", "privacy", "aws"]


def hero_svg(theme: str) -> str:
    c = HERO_THEMES[theme]
    W, H = 1200, 300
    chart_x0, chart_x1 = 686, 1144
    baseline, max_h = 196, 108.6

    bars = []
    n = 46
    step = (chart_x1 - chart_x0) / n
    bar_w = 6
    for i in range(n):
        t = i / (n - 1)
        # calm floor, one bell-shaped peak two-thirds across, in the
        # vocabulary of a DNSbench latency histogram
        v = math.exp(-((t - 0.68) ** 2) / 0.028)
        v = max(0.18, v)
        h = round(v * max_h, 1)
        y = round(baseline - h, 1)
        op = round(0.35 + 0.55 * (h / max_h), 2)
        x = round(chart_x0 + i * step, 1)
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" rx="1.5" '
                     f'fill="url(#sig-{theme})" opacity="{op}"/>')

    grid = "".join(
        f'<line x1="{chart_x0}" y1="{y}" x2="{chart_x1}" y2="{y}"/>'
        for y in (74, 114, 155, 196)
    )

    tags = []
    x = 58
    for i, tag in enumerate(STACK_TAGS):
        tags.append(f'<text x="{x}" y="248" font-family="{MONO}" font-size="15" '
                     f'fill="{c["dim"]}">{tag}</text>')
        x += len(tag) * 8.6 + 13
        if i < len(STACK_TAGS) - 1:
            tags.append(f'<circle cx="{x}" cy="243" r="2" fill="{c["amber"]}"/>')
            x += 13

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Esli Silva: SRE, Network and GNU/Linux">
  <defs>
    <linearGradient id="sig-{theme}" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="{c['grad_from']}"/>
      <stop offset="100%" stop-color="{c['grad_to']}"/>
    </linearGradient>
    <clipPath id="card-{theme}"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#card-{theme})">
    <rect x="0" y="0" width="{W}" height="{H}" fill="{c['bg']}"/>
    <g stroke="{c['grid']}" stroke-width="1">{grid}</g>
    {"".join(bars)}
    <text x="56" y="104" font-family="{MONO}" font-size="46" font-weight="700" letter-spacing="1" fill="{c['name']}">Esli Silva</text>
    <text x="58" y="140" font-family="{MONO}" font-size="17" fill="{c['dim']}">SRE &#183; Network &#183; GNU/Linux</text>
    <text x="58" y="176" font-family="{MONO}" font-size="17" fill="{c['amber']}">esli.blog</text>
    <line x1="56" y1="212" x2="1144" y2="212" stroke="{c['grid']}" stroke-width="1"/>
    {"".join(tags)}
    <text x="1144" y="248" text-anchor="end" font-family="{MONO}" font-size="15" fill="{c['dim']}">RTFM, then automate it</text>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{c['border']}"/>
</svg>
'''

# ---------------------------------------------------------------------------
# Dock: each tile is its own SVG file; the bottom 14px is a full-width shelf
# band. Written with no whitespace between the <a> tags in the README, the
# bands merge into one continuous dock shelf. Colours are theme-agnostic
# (one neutral hue at low opacity, plus an amber accent) so the same files
# work on GitHub's light and dark themes without a <picture> swap.
# ---------------------------------------------------------------------------

DOCK_W, DOCK_H = 76, 92
DOCK_TILE = 64
SHELF_TOP = 78
NEUTRAL = "#7F8D9B"
AMBER = "#D2932C"
DOCK_DISPLAY_H = 68  # <img height> in the README; tiles are natively 92px tall, so this stays supersampled

# label, title (tooltip/href key), href, running-indicator
DOCK_ITEMS = [
    ("blog", "esli.blog", "https://esli.blog", True),
    ("s.o.", "Stack Overflow", "https://stackoverflow.com/users/4122311/esli-silva", True),
    ("s.e.", "Stack Exchange", "https://stackexchange.com/users/4974728/esli-silva", False),
    ("in", "LinkedIn", "https://www.linkedin.com/in/eslih/?locale=en_US", True),
    ("SEP", "", "", False),
    ("x", "X", "https://x.com/esl1h", False),
    ("yt", "YouTube", "https://youtube.com/@eslih", False),
    ("SEP", "", "", False),
    ("matrix", "Matrix", "https://matrix.to/#/@esli:matrix.org", False),
    ("pgp", "PGP public key", "https://keys.openpgp.org/vks/v1/by-fingerprint/6DDA9E4841D4B1F1E43A64775EF74834A3C9651A", False),
    ("mirrors", "GitLab, Codeberg, Radicle", "https://esli.blog/posts/git/", False),
]


def dock_shelf() -> str:
    return (
        f'<rect x="0" y="{SHELF_TOP}" width="{DOCK_W}" height="{DOCK_H - SHELF_TOP}" '
        f'fill="{NEUTRAL}" fill-opacity="0.10"/>'
        f'<rect x="0" y="{SHELF_TOP}" width="{DOCK_W}" height="1" '
        f'fill="{NEUTRAL}" fill-opacity="0.28"/>'
    )


def dock_tile_svg(label: str, running: bool) -> str:
    size = {1: 18, 2: 17, 3: 15, 4: 14, 5: 13, 6: 12, 7: 11}.get(len(label), 11)
    x = (DOCK_W - DOCK_TILE) / 2
    dot = (f'<circle cx="{DOCK_W / 2}" cy="{SHELF_TOP + 7}" r="2.2" fill="{AMBER}"/>'
           if running else "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DOCK_W} {DOCK_H}" width="{DOCK_W}" height="{DOCK_H}" role="img" aria-label="{label}">
  <rect x="{x}" y="4" width="{DOCK_TILE}" height="{DOCK_TILE}" rx="15" fill="{NEUTRAL}" fill-opacity="0.13"/>
  <rect x="{x + 0.5}" y="4.5" width="{DOCK_TILE - 1}" height="{DOCK_TILE - 1}" rx="14.5" fill="none" stroke="{NEUTRAL}" stroke-opacity="0.30"/>
  <text x="{DOCK_W / 2}" y="{4 + DOCK_TILE / 2}" text-anchor="middle" dominant-baseline="central" font-family="{MONO}" font-size="{size}" font-weight="600" fill="{NEUTRAL}">{label}</text>
  {dock_shelf()}
  {dot}
</svg>
'''


def dock_separator_svg() -> str:
    w = 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {DOCK_H}" width="{w}" height="{DOCK_H}" role="presentation">
  <rect x="{w / 2 - 0.5}" y="18" width="1" height="40" fill="{NEUTRAL}" fill-opacity="0.30"/>
  <rect x="0" y="{SHELF_TOP}" width="{w}" height="{DOCK_H - SHELF_TOP}" fill="{NEUTRAL}" fill-opacity="0.10"/>
  <rect x="0" y="{SHELF_TOP}" width="{w}" height="1" fill="{NEUTRAL}" fill-opacity="0.28"/>
</svg>
'''


def main():
    with open(os.path.join(HERO_DIR, "hero-dark.svg"), "w") as f:
        f.write(hero_svg("dark"))
    with open(os.path.join(HERO_DIR, "hero-light.svg"), "w") as f:
        f.write(hero_svg("light"))

    dock_markup, n = [], 0
    for label, title, href, running in DOCK_ITEMS:
        if label == "SEP":
            n += 1
            name = f"{n:02d}-sep.svg"
            with open(os.path.join(DOCK_DIR, name), "w") as f:
                f.write(dock_separator_svg())
            dock_markup.append(f'<img src="./assets/dock/{name}" alt="" height="{DOCK_DISPLAY_H}">')
            continue
        n += 1
        slug = label.replace(".", "").replace(" ", "-")
        name = f"{n:02d}-{slug}.svg"
        with open(os.path.join(DOCK_DIR, name), "w") as f:
            f.write(dock_tile_svg(label, running))
        dock_markup.append(
            f'<a href="{href}" title="{title}">'
            f'<img src="./assets/dock/{name}" alt="{title}" height="{DOCK_DISPLAY_H}"></a>'
        )

    # no whitespace between the tags: that is what keeps the shelf continuous
    with open(os.path.join(REPO_ROOT, "dock-snippet.html"), "w") as f:
        f.write('<p align="center">\n' + "".join(dock_markup) + "\n</p>\n")

    print(f"hero: {HERO_DIR}/hero-{{dark,light}}.svg")
    print(f"dock: {n} files in {DOCK_DIR}/")


if __name__ == "__main__":
    main()
