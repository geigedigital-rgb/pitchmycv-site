#!/usr/bin/env python3
"""Replace inline 24x24 Feather-style SVGs with Phosphor Web icons."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SVG_RE = re.compile(
    r"<svg\s+([^>]*viewBox=\"0\s+0\s+24\s+24\"[^>]*)>(.*?)</svg>",
    re.DOTALL | re.IGNORECASE,
)


def norm_body(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


# inner HTML (normalized) -> (weight_prefix, icon_class_suffix, extra_classes optional)
# weight prefix: always "ph" (Regular / outline)
MAP = {
    '<polyline points="6 9 12 15 18 9"></polyline>': ("ph", "ph-caret-down", ""),
    '<polyline points="20 6 9 17 4 12"></polyline>': ("ph", "ph-check", ""),
    '<path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9z"></path><polyline points="14 2 14 9 21 9"></polyline><path d="M12 18v-6"></path><path d="m9.5 14 2.5-2.5 2.5 2.5"></path>': (
        "ph",
        "ph-file-arrow-up",
        "",
    ),
    '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>': ("ph", "ph-x", ""),
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>': (
        "ph",
        "ph-file-text",
        "",
    ),
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path> <polyline points="14 2 14 8 20 8"></polyline> <line x1="12" y1="18" x2="12" y2="12"></line> <line x1="9" y1="15" x2="12" y2="12"></line> <line x1="15" y1="15" x2="12" y2="12"></line>': (
        "ph",
        "ph-file-arrow-up",
        "",
    ),
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><polyline points="16 11 18 13 22 9"></polyline>': (
        "ph",
        "ph-user-circle-check",
        "",
    ),
    '<path d="M12 20h9"></path><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>': (
        "ph",
        "ph-pencil-simple",
        "",
    ),
    '<path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>': (
        "ph",
        "ph-pencil-simple",
        "",
    ),
    '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>': (
        "ph",
        "ph-check-circle",
        "",
    ),
    '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>': ("ph", "ph-pulse", ""),
    '<path d="M22 2L11 13"></path><path d="M22 2l-7 20-4-9-9-4 20-7z"></path>': ("ph", "ph-paper-plane-tilt", ""),
    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><line x1="9" y1="10" x2="15" y2="10"></line><line x1="12" y1="7" x2="12" y2="13"></line>': (
        "ph",
        "ph-chat-teardrop",
        "",
    ),
    '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>': (
        "ph",
        "ph-x-circle",
        "",
    ),
    '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>': (
        "ph",
        "ph-info",
        "",
    ),
    '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>': (
        "ph",
        "ph-warning-circle",
        "",
    ),
    '<path d="M2 20.6L12 3l10 17.6H2z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>': (
        "ph",
        "ph-warning",
        "",
    ),
    '<path d="M12 6v6l4 2"></path><circle cx="12" cy="12" r="9"></circle>': ("ph", "ph-clock", ""),
    '<path d="M3 12h18"></path><path d="M12 3v18"></path><circle cx="12" cy="12" r="9"></circle>': (
        "ph",
        "ph-crosshair",
        "",
    ),
    '<path d="M3 7h18"></path><path d="M6 3h12v18H6z"></path><path d="M9 12h6"></path>': (
        "ph",
        "ph-notepad",
        "",
    ),
    '<circle cx="12" cy="12" r="9"></circle><path d="M9 10c0-1.1 1-2 3-2s3 .9 3 2-1 2-3 2-3 .9-3 2 1 2 3 2 3-.9 3-2"></path>': (
        "ph",
        "ph-currency-circle-dollar",
        "",
    ),
    '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>': (
        "ph",
        "ph-lock",
        "",
    ),
}


def attrs_to_styles(opening_inner: str) -> tuple[str, str]:
    """Return (class_append, inline_style)."""
    extra_classes = []
    style_parts = []

    m = re.search(r'class="([^"]*)"', opening_inner)
    if m:
        extra_classes.append(m.group(1))

    m = re.search(r'style="([^"]*)"', opening_inner)
    if m:
        style_parts.append(m.group(1).strip().rstrip(";"))

    m = re.search(r'width="(\d+)"', opening_inner)
    w = m.group(1) if m else None
    if w:
        style_parts.append(f"font-size:{w}px")

    m = re.search(r'stroke="([^"]+)"', opening_inner)
    if m and m.group(1) not in ("currentColor",):
        style_parts.append(f"color:{m.group(1)}")

    return (" ".join(extra_classes), ";".join(style_parts))


def replace_svg(match: re.Match) -> str:
    opening = match.group(1)
    body = norm_body(match.group(2))
    if body not in MAP:
        print(f"UNMAPPED: {body[:90]}...", file=sys.stderr)
        return match.group(0)

    weight, icon, _ = MAP[body]
    extra_cls, inline = attrs_to_styles(opening)
    classes = f"{weight} {icon}" + (f" {extra_cls}" if extra_cls else "")
    style_attr = f' style="{inline}"' if inline else ""
    return f'<i class="{classes}"{style_attr} aria-hidden="true"></i>'


def process_file(path: Path) -> bool:
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="latin-1")
    updated, n = SVG_RE.subn(replace_svg, raw)
    if n == 0:
        return False
    path.write_text(updated, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {n} icons")
    return True


def main():
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if process_file(path):
            count += 1
    print(f"Done. Files touched: {count}")


if __name__ == "__main__":
    main()
