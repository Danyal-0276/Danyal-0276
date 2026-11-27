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
    "dark": ("#101a17", "#31443c", "#eff7ee", "#afc6bc", "#a5efb3"),
    "light": ("#f1f7f0", "#c5d7ca", "#152720", "#455e52", "#235e43"),
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
    portrait = "\n".join(
        f'<text x="587" y="{46 + index * 6.68:.2f}" textLength="299" lengthAdjust="spacingAndGlyphs">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 400" role="img" aria-labelledby="title description">
<title id="title">Danyal Tanveer</title>
<desc id="description">Full-stack engineer working on web, mobile, and applied AI, based in Lahore, Pakistan. A green ASCII portrait appears on the right.</desc>
<rect x="1" y="1" width="918" height="398" rx="20" fill="{background}" stroke="{border}" stroke-width="2"/>
<path d="M47 55h42m-42 282h474" stroke="{border}" stroke-width="2"/>
<path d="M47 55h14" stroke="{accent}" stroke-width="2"/>
<g font-family="system-ui, Segoe UI, sans-serif" fill="{ink}" font-weight="700" letter-spacing="-3">
  <text x="43" y="145" font-size="74">Danyal</text>
  <text x="43" y="219" font-size="74">Tanveer</text>
</g>
<text x="47" y="275" fill="{accent}" font-family="system-ui, Segoe UI, sans-serif" font-size="26" font-weight="600">Full-stack engineer</text>
<text x="47" y="311" fill="{muted}" font-family="system-ui, Segoe UI, sans-serif" font-size="21">Web, mobile, and applied AI</text>
<text x="47" y="365" fill="{muted}" font-family="Consolas, Menlo, monospace" font-size="15">Lahore, Pakistan</text>
<rect x="574.5" y="20.5" width="324" height="359" rx="12" fill="#0b1813" stroke="{border}"/>
<g aria-hidden="true" font-family="Consolas, Menlo, monospace" font-size="6.8" fill="#97e5aa" xml:space="preserve">
{portrait}
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
