#!/usr/bin/env python3
"""
Apply repeated GEO trust/editorial upgrades across static HTML pages.

This script updates:
- article/career/example pages that currently use Organization as the author
- publisher blocks with richer organization metadata
- speakable selectors on article pages
- visible editorial note blocks in repeated page templates
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/workspace")

AUTHOR_REPLACEMENT = (
    '"author": {"@type": "Person", "name": "Serhii Maryshchak", '
    '"jobTitle": "Founder and editorial lead, Pitch My CV", '
    '"url": "https://pitchcv.app/about#editorial-standards", '
    '"worksFor": {"@type": "Organization", "name": "MARYSCHAKGROUP LTD", '
    '"url": "https://pitchcv.app/"}, '
    '"knowsAbout": ["ATS resume optimization", "resume strategy", "job search communication"]}'
)

PUBLISHER_REPLACEMENT = (
    '"publisher": {"@type": "Organization", "name": "Pitch My CV", '
    '"legalName": "MARYSCHAKGROUP LTD", "url": "https://pitchcv.app/", '
    '"logo": {"@type": "ImageObject", "url": "https://pitchcv.app/favicon.svg"}, '
    '"publishingPrinciples": "https://pitchcv.app/about#editorial-standards"}'
)

EDITORIAL_NOTE_HTML = {
    "career": (
        '\n      <div class="editorial-note career-editorial-note">\n'
        '        <p><strong>Editorial note:</strong> This guide is reviewed by '
        '<a href="/about#editorial-standards">Serhii Maryshchak, founder and editorial lead at Pitch My CV</a>. '
        'We update it against current ATS parsing constraints, recruiter review habits, and role-specific resume expectations.</p>\n'
        '      </div>'
    ),
    "example": (
        '\n      <div class="editorial-note example-editorial-note">\n'
        '        <p><strong>Editorial note:</strong> This example page is reviewed by '
        '<a href="/about#editorial-standards">Serhii Maryshchak, founder and editorial lead at Pitch My CV</a>. '
        'It is designed to stay ATS-safe, recruiter-readable, and aligned with the role-specific guidance published across the site.</p>\n'
        '      </div>'
    ),
    "guide": (
        '\n    <div class="editorial-note guide-editorial-note">\n'
        '      <p><strong>Editorial note:</strong> This resource is reviewed by '
        '<a href="/about#editorial-standards">Serhii Maryshchak, founder and editorial lead at Pitch My CV</a>. '
        'We maintain these guides to reflect current ATS behavior, recruiter screening patterns, and practical resume optimization workflows.</p>\n'
        '    </div>\n'
    ),
}


def replace_author_and_publisher(text: str) -> str:
    text = re.sub(
        r'"author"\s*:\s*\{\s*"@type"\s*:\s*"Organization"\s*,\s*"name"\s*:\s*"Pitch My CV"\s*\}',
        AUTHOR_REPLACEMENT,
        text,
        count=1,
    )
    text = re.sub(
        r'"publisher"\s*:\s*\{\s*"@type"\s*:\s*"Organization"\s*,\s*"name"\s*:\s*"Pitch My CV"\s*\}',
        PUBLISHER_REPLACEMENT,
        text,
        count=1,
    )
    return text


def add_speakable(text: str, selectors: list[str]) -> str:
    if '"speakable"' in text:
        return text
    selectors_json = ", ".join(f'"{selector}"' for selector in selectors)
    return re.sub(
        r'("mainEntityOfPage"\s*:\s*"[^"]+")',
        (
            r'\1, "speakable": {"@type": "SpeakableSpecification", '
            f'"cssSelector": [{selectors_json}]}}'
        ),
        text,
        count=1,
    )


def insert_after_first(pattern: str, insertion: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return text
    end = match.end()
    return text[:end] + insertion + text[end:]


def update_career_page(path: Path) -> None:
    text = path.read_text()
    original = text
    text = replace_author_and_publisher(text)
    text = add_speakable(text, [".career-hero p", ".career-article h2", ".career-article p"])
    if 'career-editorial-note' not in text:
        text = insert_after_first(r'<p class="career-keyline">.*?</p>', EDITORIAL_NOTE_HTML["career"], text)
    if text != original:
        path.write_text(text)


def update_example_page(path: Path) -> None:
    text = path.read_text()
    original = text
    text = replace_author_and_publisher(text)
    text = add_speakable(text, [".example-hero p", ".example-article h2", ".example-article p"])
    if 'example-editorial-note' not in text:
        text = insert_after_first(r'<p class="example-keyline">.*?</p>', EDITORIAL_NOTE_HTML["example"], text)
    if text != original:
        path.write_text(text)


def update_guide_page(path: Path) -> None:
    text = path.read_text()
    original = text
    text = replace_author_and_publisher(text)
    text = add_speakable(text, [".seo-header p", ".guide-wrap h2", ".guide-wrap p"])
    if 'guide-editorial-note' not in text:
        text = text.replace('<main class="guide-wrap">\n', '<main class="guide-wrap">\n' + EDITORIAL_NOTE_HTML["guide"], 1)
    if text != original:
        path.write_text(text)


def main() -> None:
    career_pages = sorted((ROOT / "careers").glob("*-resume/index.html"))
    example_pages = sorted((ROOT / "examples").glob("*/index.html"))
    guide_pages = [
        ROOT / "ats-resume-checklist/index.html",
        ROOT / "ats-resume-mistakes/index.html",
        ROOT / "resume-keyword-optimization/index.html",
        ROOT / "resume-pelmeni-case/index.html",
    ]

    for path in career_pages:
        update_career_page(path)

    for path in example_pages:
        update_example_page(path)

    for path in guide_pages:
        update_guide_page(path)


if __name__ == "__main__":
    main()
