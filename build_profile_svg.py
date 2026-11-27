"""Build both GitHub profile banners from the committed ASCII portrait."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTRAIT = ROOT / "portrait_ascii.txt"
COLS = 80
ROWS = 50
GLYPHS = ".,:;irsXA253hMHGS#9B&@"

THEMES = {
    "dark": ("#0d1117", "#30363d", "#f0f6fc", "#a6b3c2", "#79b8ff"),
    "light": ("#f6f8fa", "#d0d7de", "#1f2328", "#57606a", "#0969da"),
}


def make_ascii(photo: Path, crop: tuple[int, int, int, int] | None) -> list[str]:
    from PIL import Image, ImageFilter, ImageOps

    with Image.open(photo) as source:
        image = ImageOps.exif_transpose(source).convert("L")
    if crop:
        left, top, right, bottom = crop
        if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
            raise ValueError("Crop must be inside the photo after EXIF orientation.")
        image = image.crop(crop)

    image = ImageOps.fit(image, (COLS * 5, ROWS * 7), Image.Resampling.LANCZOS)
    image = ImageOps.autocontrast(image, cutoff=2).filter(ImageFilter.UnsharpMask())
    image = image.resize((COLS, ROWS), Image.Resampling.LANCZOS)

    return [
        "".join(GLYPHS[image.getpixel((x, y)) * (len(GLYPHS) - 1) // 255] for x in range(COLS))
        for y in range(ROWS)
    ]


def build_banner(lines: list[str], colors: tuple[str, str, str, str, str]) -> str:
    background, border, ink, muted, accent = colors
    portrait_bands = []
    for start in range(0, ROWS, 10):
        rows = "\n".join(
            f'<text x="587" y="{46 + index * 6.68:.2f}" textLength="299" lengthAdjust="spacingAndGlyphs">{escape(line)}</text>'
            for index, line in enumerate(lines[start:start + 10], start)
        )
        delay = 0.15 + start * 0.019
        portrait_bands.append(f'<g class="portrait-band" style="--delay: {delay:.2f}s">\n{rows}\n</g>')
    portrait = "\n".join(portrait_bands)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" role="img" aria-labelledby="title description">
<title id="title">Danyal Tanveer</title>
<desc id="description">Full-stack engineer working on web, mobile, and applied AI, based in Lahore, Pakistan. A blue ASCII portrait appears on the right.</desc>
<style>
  @media (prefers-reduced-motion: no-preference) {{
    .reveal {{ animation: reveal .55s ease-out var(--delay, 0s) both; }}
    .portrait-band {{ animation: resolve .36s steps(4, end) var(--delay) both; }}
    .scan {{ animation: sweep 1.3s ease-out .12s both; }}
    .cursor {{ animation: flicker .48s steps(1, end) .65s 2; }}
  }}
  @keyframes reveal {{
    from {{ opacity: .2; transform: translateX(-7px); }}
    to {{ opacity: 1; transform: translateX(0); }}
  }}
  @keyframes resolve {{
    from {{ opacity: .18; }}
    to {{ opacity: 1; }}
  }}
  @keyframes sweep {{
    0% {{ opacity: 0; transform: translateY(0); }}
    18% {{ opacity: .52; }}
    82% {{ opacity: .35; }}
    100% {{ opacity: 0; transform: translateY(339px); }}
  }}
  @keyframes flicker {{
    50% {{ opacity: .15; }}
  }}
</style>
<rect x="1" y="1" width="918" height="398" rx="20" fill="{background}" stroke="{border}" stroke-width="2"/>
<g aria-hidden="true" font-family="Consolas, Menlo, monospace" font-size="15">
  <path d="m49 51 5 4-5 4" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="66" y="60" fill="{muted}">~/danyal-0276</text>
  <path d="M49 335h471" stroke="{border}"/>
</g>
<g font-family="system-ui, Segoe UI, sans-serif">
  <text class="reveal" x="45" y="146" fill="{ink}" font-size="64" font-weight="630" letter-spacing="-2.5">Danyal</text>
  <text class="reveal" style="--delay: .14s" x="43" y="228" fill="{accent}" font-size="88" font-weight="790" letter-spacing="-4">Tanveer<tspan class="cursor" dx="14" font-size="42" letter-spacing="0" aria-hidden="true">_</tspan></text>
  <g class="reveal" style="--delay: .32s">
    <text x="49" y="281" fill="{ink}" font-size="26" font-weight="600">Full-stack engineer</text>
    <text x="49" y="311" fill="{muted}" font-size="20">Web, mobile, and applied AI</text>
  </g>
</g>
<text x="49" y="362" fill="{muted}" font-family="Consolas, Menlo, monospace" font-size="15">Lahore, Pakistan</text>
<rect x="574.5" y="20.5" width="324" height="359" rx="12" fill="#101a29" stroke="{border}"/>
<g aria-hidden="true" font-family="Consolas, Menlo, monospace" font-size="6.8" fill="#9ec6ef" xml:space="preserve">
{portrait}
</g>
<g aria-hidden="true" fill="none" stroke="#8bbdff">
  <path d="M582 45v-13h14m282 0h13v13m0 309v13h-13m-282 0h-14v-13" opacity=".55"/>
  <path class="scan" d="M584 31h305" opacity="0"/>
</g>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photo", type=Path, help="replace the ASCII portrait using a local image")
    parser.add_argument("--crop", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    args = parser.parse_args()

    if args.crop and not args.photo:
        parser.error("--crop requires --photo")
    if args.photo:
        lines = make_ascii(args.photo, tuple(args.crop) if args.crop else None)
        PORTRAIT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        lines = PORTRAIT.read_text(encoding="utf-8").splitlines()

    if len(lines) != ROWS or any(len(line) != COLS for line in lines):
        parser.error(f"{PORTRAIT.name} must contain {ROWS} lines of {COLS} characters.")

    for theme, colors in THEMES.items():
        (ROOT / f"{theme}.svg").write_text(build_banner(lines, colors), encoding="utf-8")


if __name__ == "__main__":
    main()
