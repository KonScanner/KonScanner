#!/usr/bin/env python3
"""Generate the career path diagram as light and dark SVGs.

Colours are muted derivations of each organisation's own brand colour,
sampled from their live sites. Run: python3 assets/make_path.py
"""
from pathlib import Path

CARDS = [
    ("2016 to 2020",     "University",      ["Physics BSc", "Data Science MSc"], "#34576E"),
    ("2020 to 2021",     "TX Connected",    ["Junior Data Scientist", "Vehicle telematics"], "#93353D"),
    ("2021 to 2022",     "LeasePlan",       ["Data Scientist", "Credit risk scoring"], "#B06A3A"),
    ("2022",             "Flipside Crypto", ["Bounty hunter", "part time"], "#4F4F4F"),
    ("2022 to 2023",     "Polygon Labs",    ["Data Lead", "Analytics Engineer"], "#6B4A96"),
    ("2023 to 2025",     "ZettaBlock",      ["Senior Data Engineer", "Data Scientist"], "#43479B"),
    ("2025 to May 2026", "Share.xyz",       ["Social crypto app", "end to end"], "#292929"),
]

W, MARGIN, GAP = 960, 20, 10
HEAD_H, BODY_H = 26, 68
CARD_H = HEAD_H + BODY_H
TICK, AXIS_GAP = 12, 0
CARD_W = (W - 2 * MARGIN - GAP * (len(CARDS) - 1)) // len(CARDS)
AXIS_Y = CARD_H + TICK + 14
H = AXIS_Y + 26

THEMES = {
    "light": dict(axis="#57606A", label="#1F2328", faint="#8C959F"),
    "dark":  dict(axis="#8B949E", label="#E6EDF3", faint="#7D8590"),
}
FONT = ("ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',"
        "Helvetica,Arial,sans-serif")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" '
         f'aria-label="Career path from physics to blockchain data">']
    o.append(f'<defs><marker id="ah" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
             f'orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="{t["axis"]}"/></marker></defs>')

    for i, (period, title, lines, colour) in enumerate(CARDS):
        x = MARGIN + i * (CARD_W + GAP)
        cx = x + CARD_W / 2
        o.append(f'<g>')
        # card body, then a darker header strip on top
        o.append(f'<rect x="{x}" y="0" width="{CARD_W}" height="{CARD_H}" rx="5" fill="{colour}"/>')
        o.append(f'<path d="M{x} 5 a5 5 0 0 1 5 -5 h{CARD_W-10} a5 5 0 0 1 5 5 v{HEAD_H-5} h-{CARD_W} z" '
                 f'fill="#000" fill-opacity="0.26"/>')
        o.append(f'<text x="{cx:.0f}" y="17.5" text-anchor="middle" font-size="12" '
                 f'font-weight="700" fill="#FFFFFF">{esc(period)}</text>')
        o.append(f'<text x="{cx:.0f}" y="{HEAD_H+21}" text-anchor="middle" font-size="13.5" '
                 f'font-weight="700" fill="#FFFFFF">{esc(title)}</text>')
        for j, ln in enumerate(lines):
            o.append(f'<text x="{cx:.0f}" y="{HEAD_H+38+j*15}" text-anchor="middle" '
                     f'font-size="11.5" font-weight="600" fill="#FFFFFF" '
                     f'fill-opacity="0.90">{esc(ln)}</text>')
        # tick down to the axis
        o.append(f'<line x1="{cx:.0f}" y1="{CARD_H}" x2="{cx:.0f}" y2="{AXIS_Y}" '
                 f'stroke="{t["faint"]}" stroke-width="1.5"/>')
        o.append('</g>')

    o.append(f'<line x1="{MARGIN}" y1="{AXIS_Y}" x2="{W-MARGIN-46}" y2="{AXIS_Y}" '
             f'stroke="{t["axis"]}" stroke-width="2" marker-end="url(#ah)"/>')
    o.append(f'<text x="{W-MARGIN-34}" y="{AXIS_Y+4.5}" font-size="12.5" font-weight="700" '
             f'fill="{t["label"]}">time</text>')
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = Path(__file__).parent
    for name in THEMES:
        (here / f"path-{name}.svg").write_text(build(name) + "\n")
        print(f"wrote assets/path-{name}.svg")
