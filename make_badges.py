"""Regenerates badges/*.svg and points README.md at them. Run: python make_badges.py
Needs Pillow and Verdana Bold (Windows font) only to measure text; the SVGs carry
textLength so they keep their size on systems without Verdana."""
import io, os, re
from xml.sax.saxutils import escape
from PIL import ImageFont

GREEN, GREY = "#287a54", "#555"
FONT = "Verdana,Geneva,DejaVu Sans,sans-serif"
bold = lambda size: ImageFont.truetype("C:/Windows/Fonts/verdanab.ttf", size * 10)
width = lambda text, size: bold(size).getlength(text) / 10
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().replace("+", "p")).strip("-")

def small(text):
    tw = width(text, 11); w = round(tw + 14)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{escape(text)}">'
            f'<rect width="{w}" height="20" fill="{GREEN}"/>'
            f'<text x="{w/2}" y="14" fill="#fff" font-family="{FONT}" font-size="11" font-weight="bold" '
            f'text-anchor="middle" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{escape(text)}</text></svg>')

BUTTONS = [("Portfolio", "francke.tech", "https://francke.tech"),
           ("LinkedIn", "Connect", "https://www.linkedin.com/in/g-francke")]
spaced = lambda t: width(t, 10) + 1.25 * (len(t) - 1)
# every half of every button shares the widest text's width: the colour split sits
# at the centre and both buttons are the same size
HALF = round(max(spaced(t.upper()) for l, m, _ in BUTTONS for t in (l, m)) + 26)

def button(label, message):
    label, message = label.upper(), message.upper()
    half = HALF
    t = lambda x, s: (f'<text x="{x}" y="17.5" fill="#fff" font-family="{FONT}" font-size="10" font-weight="bold" '
                      f'text-anchor="middle" textLength="{spaced(s):.1f}" lengthAdjust="spacing">{escape(s)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{2*half}" height="28" role="img" aria-label="{escape(label)}: {escape(message)}">'
            f'<rect width="{half}" height="28" fill="{GREY}"/><rect x="{half}" width="{half}" height="28" fill="{GREEN}"/>'
            f'{t(half/2, label)}{t(half*1.5, message)}</svg>')

os.makedirs("badges", exist_ok=True)
def save(name, svg):
    io.open(f"badges/{name}.svg", "w", encoding="utf-8", newline="\n").write(svg)
    return f"badges/{name}.svg"

s = io.open("README.md", encoding="utf-8").read()
# skill and tech badges: shields URL or an already generated local file
s = re.sub(r'<img src="[^"]+" alt="([^"]+)"(?: height="20")?>',
           lambda m: f'<img src="{save(slug(m[1]), small(m[1]))}" alt="{m[1]}" height="20">', s)
for label, message, href in BUTTONS:
    path = save(slug(label), button(label, message))
    s = re.sub(rf'\[!\[{label}[^\]]*\]\([^)]*\)\]\([^)]*\)', f'[![{label}: {message}]({path})]({href})', s)
io.open("README.md", "w", encoding="utf-8", newline="\n").write(s)
