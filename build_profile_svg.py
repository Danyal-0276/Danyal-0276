"""Build dark.svg / light.svg with Danyal's ASCII portrait + resume info."""
from __future__ import annotations

from html import escape
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent
IMG = Path(
    r"C:\Users\DONI BUTT\.cursor\projects\c-Users-DONI-BUTT-Documents-github\assets"
    r"\c__Users_DONI_BUTT_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"1096c2425fd3baacb2f7ca9fa598d3ff_images_WhatsApp_Image_2026-07-30_at_"
    r"9.41.08_AM-45fab759-4f4e-4b62-9b7e-78bf1a3e74a6.png"
)

COLS = 95
ROWS = 53
CHARS = " .:-;=+*#%@"


def make_ascii(path: Path) -> list[str]:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # Focus on face / upper torso
    img = img.crop((int(w * 0.10), int(h * 0.00), int(w * 0.90), int(h * 0.70)))
    img = ImageOps.grayscale(img)
    img = ImageEnhance.Contrast(img).enhance(1.65)
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.resize((COLS, ROWS), Image.Resampling.LANCZOS)

    lines: list[str] = []
    pixels = list(img.getdata())
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            val = pixels[y * COLS + x]
            t = 1.0 - (val / 255.0)
            idx = int(t * (len(CHARS) - 1))
            row.append(CHARS[idx])
        lines.append("".join(row).ljust(COLS)[:COLS])
    return lines


def dots(label: str, value: str, width: int = 48) -> str:
    """Pad with dots between label and value like the original layout."""
    # Approximate visual width used by original: label + ': ' + dots + ' ' + value
    base = f"{label}: "
    space_for_dots = max(3, width - len(base) - len(value))
    return f"{base}{'.' * space_for_dots} {value}"


def ascii_tspans(lines: list[str]) -> str:
    start_y = 79.98
    step = 7.55
    out = []
    for i, line in enumerate(lines):
        y = start_y + i * step
        out.append(
            f'<tspan x="30" y="{y:.2f}" xml:space="preserve">{escape(line)}</tspan>'
        )
    return "\n".join(out)


def info_rows() -> list[tuple[str, str]]:
    """Return (kind, html-inner) rows for the SYSTEM.INFO panel.
    kind is 'head'|'row'|'blank'|'accent'|'footer'
    """
    rows: list[tuple[str, str]] = []
    rows.append(
        (
            "head",
            '<tspan x="520" y="42" class="head">danyal@devos</tspan>'
            '<tspan class="cc"> ————————————————————————————————————————-—-</tspan>',
        )
    )

    def row(y: float, key_html: str, pad: str, value: str) -> tuple[str, str]:
        return (
            "row",
            f'<tspan x="520" y="{y}" class="cc">. </tspan>{key_html}'
            f'<tspan class="cc">{escape(pad)}</tspan>'
            f'<tspan class="value">{escape(value)}</tspan>',
        )

    # Manual padding to keep values aligned similar to original
    rows.append(row(66, '<tspan class="key">Subject</tspan>', ": .......................... ", "Danyal Tanveer"))
    rows.append(row(88, '<tspan class="key">Role</tspan>', ": ..................... ", "Jr Software Eng · MERN / AI"))
    rows.append(row(110, '<tspan class="key">Origin</tspan>', ": ................. ", "Lahore, Punjab, Pakistan"))
    rows.append(row(132, '<tspan class="key">Education</tspan>', ": ............... ", "BS CS, UCP · CGPA 3.60"))
    rows.append(row(154, '<tspan class="key">Status</tspan>', ": ............ ", "Building • Learning • Shipping"))
    rows.append(row(176, '<tspan class="key">ToolChain</tspan>', ": ................. ", "VS Code, Git, Docker, Postman"))
    rows.append(("blank", '<tspan x="520" y="198" class="cc">. </tspan>'))
    rows.append(
        row(
            220,
            '<tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Lang</tspan>',
            ": ........ ",
            "JS, TS, Python, Java, C++",
        )
    )
    rows.append(
        row(
            242,
            '<tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Frontend</tspan>',
            ": ...... ",
            "React, Next.js, React Native",
        )
    )
    rows.append(
        row(
            264,
            '<tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Backend</tspan>',
            ": ....... ",
            "Node, Express, Django/DRF",
        )
    )
    rows.append(
        row(
            286,
            '<tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">Database</tspan>',
            ": ...... ",
            "MongoDB, MySQL, Firebase",
        )
    )
    rows.append(
        row(
            308,
            '<tspan class="key">Core</tspan><tspan class="cc">.</tspan><tspan class="key">AI</tspan>',
            ": ............ ",
            "PyTorch, HuggingFace, NLP",
        )
    )
    rows.append(("blank", '<tspan x="520" y="330" class="cc">. </tspan>'))
    rows.append(
        (
            "accent",
            '<tspan x="520" y="352" class="accent">- Contact</tspan>'
            '<tspan class="cc"> ————————————————————————————————————————-—-</tspan>',
        )
    )
    rows.append(
        row(
            374,
            '<tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Mail</tspan>',
            ": ....................... ",
            "donibutt2112@gmail.com",
        )
    )
    rows.append(
        row(
            396,
            '<tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Focus</tspan>',
            ": ...................... ",
            "TRAK · POS · BERT Research",
        )
    )
    rows.append(
        row(
            418,
            '<tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">LinkedIn</tspan>',
            ": ................... ",
            "danyal-tanveer-30b887320",
        )
    )
    rows.append(
        row(
            440,
            '<tspan class="key">Grid</tspan><tspan class="cc">.</tspan><tspan class="key">Github</tspan>',
            ": ..................... ",
            "Danyal-0276",
        )
    )
    rows.append(("blank", '<tspan x="520" y="462" class="cc">. </tspan>'))
    rows.append(
        (
            "accent",
            '<tspan x="520" y="484" class="accent">- Live Stats</tspan>'
            '<tspan class="cc"> ————————————————————————————————————————-—-</tspan>',
        )
    )
    rows.append(
        (
            "footer",
            '<tspan x="520" y="506" class="cc">. </tspan>'
            '<tspan class="value">Jet heatmap below · 900+ contributions ↓</tspan>',
        )
    )
    return rows


def clip_paths() -> str:
    parts = []
    ys = [
        26.00, 50.00, 72.00, 94.00, 116.00, 138.00, 160.00, 182.00, 204.00,
        226.00, 248.00, 270.00, 292.00, 314.00, 336.00, 358.00, 380.00, 402.00,
        424.00, 446.00, 468.00, 490.00,
    ]
    for i, y in enumerate(ys):
        begin = 0.75 + i * 0.115
        parts.append(
            f'<clipPath id="lc{i}"><rect x="500" y="{y:.2f}" width="0" height="24">'
            f'<animate attributeName="width" from="0" to="690" dur="0.38s" '
            f'begin="{begin:.2f}s" fill="freeze"/></rect></clipPath>'
        )
    return "".join(parts)


def info_panel(fill: str) -> str:
    rows = info_rows()
    blocks = []
    for i, (_kind, inner) in enumerate(rows):
        blocks.append(
            f'<g clip-path="url(#lc{i})"><text x="520" y="0" fill="{fill}">{inner}</text></g>'
        )
    return "".join(blocks)


DARK_DEFS_STYLE = """
    .ascii  { font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }
    .key    { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #22D3EE; font-weight: bold; }
    .value  { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #E5E7EB; }
    .cc     { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #475569; }
    .head   { font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: #7C3AED; font-weight: bold; }
    .accent { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #10B981; font-weight: bold; }
    text, tspan { white-space: pre; }
    .term-label { font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #64748B; letter-spacing: 0.5px; }
    .scan-label { font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #F87171; letter-spacing: 1px; }
    .panel-title { font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: #38BDF8; letter-spacing: 2px; opacity: 0.7; }
    .cursor-blink { fill: #22D3EE; }
"""

LIGHT_DEFS_STYLE = """
    .ascii  { font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }
    .key    { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #0EA5E9; font-weight: bold; }
    .value  { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #0F172A; }
    .cc     { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #94A3B8; }
    .head   { font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: #7C3AED; font-weight: bold; }
    .accent { font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: #059669; font-weight: bold; }
    text, tspan { white-space: pre; }
    .term-label { font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: #64748B; letter-spacing: 0.5px; }
    .scan-label { font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: #DC2626; letter-spacing: 1px; }
    .panel-title { font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: #0284C7; letter-spacing: 2px; opacity: 0.75; }
    .cursor-blink { fill: #0EA5E9; }
"""


def build_dark(ascii_block: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#22D3EE">
      <animate attributeName="stop-color" values="#22D3EE;#7C3AED;#38BDF8;#22D3EE" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#7C3AED">
      <animate attributeName="stop-color" values="#7C3AED;#38BDF8;#22D3EE;#7C3AED" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#7C3AED"/>
    <stop offset="50%" stop-color="#22D3EE"/>
    <stop offset="100%" stop-color="#10B981"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="#0B1120"/>
    <stop offset="100%" stop-color="#050816"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
  <stop offset="45%" stop-color="#22D3EE" stop-opacity="0.05"/>
  <stop offset="50%" stop-color="#A5F3FC" stop-opacity="0.65"/>
  <stop offset="55%" stop-color="#22D3EE" stop-opacity="0.05"/>
  <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
</linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#7DD3FC" opacity="0.05"/>
</pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="4" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
  <rect x="0" y="0" width="1180" height="0" fill="#fff">
    <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
  </rect>
</mask>
  {clip_paths()}
  <style>{DARK_DEFS_STYLE}
  </style>
</defs>

<rect width="1180" height="610" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="610" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="#0B1120" fill-opacity="0.85"/>
  <circle cx="24" cy="20" r="5" fill="#EF4444"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="#10B981"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">danyal@devos ~ % ./profile.sh --live</text>
  <circle cx="1122" cy="20" r="4" fill="#F87171">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/>
  </circle>
  <text x="1132" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="#0B1120" fill-opacity="0.35" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="#0B1120" fill-opacity="0.35" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
  <text x="30" y="0" class="ascii">
{ascii_block}
  </text>
  </g>

  {info_panel("#dbeafe")}

  <rect x="522" y="491.0" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="3.66s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.7" style="mix-blend-mode:screen">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.8">
  <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>
'''


def build_light(ascii_block: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#4F46E5">
      <animate attributeName="stop-color" values="#4F46E5;#7C3AED;#0EA5E9;#4F46E5" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#7C3AED">
      <animate attributeName="stop-color" values="#7C3AED;#0EA5E9;#4F46E5;#7C3AED" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#7C3AED"/>
    <stop offset="50%" stop-color="#0EA5E9"/>
    <stop offset="100%" stop-color="#059669"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="#F8FAFC"/>
    <stop offset="100%" stop-color="#E2E8F0"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#0EA5E9" stop-opacity="0"/>
  <stop offset="45%" stop-color="#0EA5E9" stop-opacity="0.06"/>
  <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.55"/>
  <stop offset="55%" stop-color="#0EA5E9" stop-opacity="0.06"/>
  <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
</linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="1" fill="#334155" opacity="0.035"/>
</pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="4" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
  <rect x="0" y="0" width="1180" height="0" fill="#fff">
    <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
  </rect>
</mask>
  {clip_paths()}
  <style>{LIGHT_DEFS_STYLE}
  </style>
</defs>

<rect width="1180" height="610" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="610" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="#FFFFFF" fill-opacity="0.9"/>
  <circle cx="24" cy="20" r="5" fill="#F87171"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="#FBBF24"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="#34D399"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">danyal@devos ~ % ./profile.sh --live</text>
  <circle cx="1122" cy="20" r="4" fill="#EF4444">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/>
  </circle>
  <text x="1132" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="#FFFFFF" fill-opacity="0.55" stroke="url(#borderGrad)" stroke-width="1" opacity="0.4"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="#FFFFFF" fill-opacity="0.55" stroke="url(#borderGrad)" stroke-width="1" opacity="0.4"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
  <text x="30" y="0" class="ascii">
{ascii_block}
  </text>
  </g>

  {info_panel("#1E293B")}

  <rect x="522" y="491.0" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="3.66s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.8" style="mix-blend-mode:multiply">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.75">
  <animate attributeName="opacity" values="0.45;0.9;0.45" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>
'''


def main() -> None:
    if not IMG.exists():
        raise SystemExit(f"Image not found: {IMG}")

    lines = make_ascii(IMG)
    (ROOT / "portrait_ascii.txt").write_text("\n".join(lines), encoding="utf-8")
    ascii_block = ascii_tspans(lines)

    dark = build_dark(ascii_block)
    light = build_light(ascii_block)
    (ROOT / "dark.svg").write_text(dark, encoding="utf-8")
    (ROOT / "light.svg").write_text(light, encoding="utf-8")
    print(f"Wrote dark.svg ({len(dark)} bytes) and light.svg ({len(light)} bytes)")
    print("--- ASCII preview (every 5th line) ---")
    for ln in lines[::5]:
        print(ln)


if __name__ == "__main__":
    main()
