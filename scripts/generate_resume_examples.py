#!/usr/bin/env python3
"""Generate static resume sample assets for example pages.

Outputs for each role:
  - assets/examples/<slug>/sample.pdf
  - assets/examples/<slug>/preview.png
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "assets" / "examples"

PALETTE = {
    "green": (22, 163, 74),
    "red": (220, 38, 38),
    "blue": (37, 99, 235),
    "purple": (124, 58, 237),
}
TEMPLATE_ORDER = ("A", "B", "C")


@dataclass(frozen=True)
class RoleProfile:
    slug: str
    role_title: str
    person_name: str
    location: str
    email: str
    template: str
    summary: str
    skills: list[str]
    experience: list[str]
    achievements: list[str]


PROFILES: list[RoleProfile] = [
    RoleProfile(
        slug="software-engineer",
        role_title="Software Engineer",
        person_name="Alex Carter",
        location="Berlin, DE",
        email="alex.carter@example.com",
        template="A",
        summary="Backend engineer focused on reliable APIs and performance optimization.",
        skills=["Python", "Go", "AWS", "PostgreSQL", "Docker", "CI/CD"],
        experience=[
            "Senior Software Engineer — NimbleCore (2023-Now)",
            "Software Engineer — PixelScale (2020-2023)",
        ],
        achievements=[
            "Reduced API p95 latency by 41% through query and cache tuning.",
            "Migrated monolith jobs to event workers and cut failed runs by 63%.",
            "Built release health checks that lowered rollback incidents by 28%.",
        ],
    ),
    RoleProfile(
        slug="product-manager",
        role_title="Product Manager",
        person_name="Taylor Morgan",
        location="Amsterdam, NL",
        email="taylor.morgan@example.com",
        template="B",
        summary="Product manager translating user research into roadmap decisions and measurable outcomes.",
        skills=["Roadmapping", "A/B Testing", "SQL", "Figma", "Jira", "Stakeholder Mgmt"],
        experience=[
            "Product Manager — OrbitFlow (2022-Now)",
            "Associate PM — SignalDesk (2019-2022)",
        ],
        achievements=[
            "Launched onboarding revamp that improved activation rate by 19%.",
            "Prioritized retention backlog and reduced 90-day churn by 11%.",
            "Introduced KPI dashboard cadence across product and growth teams.",
        ],
    ),
    RoleProfile(
        slug="marketing-manager",
        role_title="Marketing Manager",
        person_name="Jordan Lee",
        location="Warsaw, PL",
        email="jordan.lee@example.com",
        template="C",
        summary="Marketing manager driving demand generation with clear funnel accountability.",
        skills=["Campaign Strategy", "GA4", "HubSpot", "Content Ops", "SEO", "Budgeting"],
        experience=[
            "Marketing Manager — BrightMint (2021-Now)",
            "Growth Specialist — NovaRetail (2018-2021)",
        ],
        achievements=[
            "Increased MQL volume by 34% with segmented campaign structure.",
            "Improved paid media ROAS from 2.1x to 3.3x in two quarters.",
            "Built monthly reporting framework aligned to pipeline metrics.",
        ],
    ),
    RoleProfile(
        slug="digital-marketing",
        role_title="Digital Marketing Manager",
        person_name="Sam Rivera",
        location="Lisbon, PT",
        email="sam.rivera@example.com",
        template="A",
        summary="Digital marketer combining paid, SEO, and CRO to accelerate qualified growth.",
        skills=["Google Ads", "Meta Ads", "SEO", "Looker Studio", "CRO", "Automation"],
        experience=[
            "Digital Marketing Manager — WavePilot (2022-Now)",
            "Performance Marketer — OpenNest (2019-2022)",
        ],
        achievements=[
            "Cut CAC by 22% while scaling lead volume by 31%.",
            "Improved landing page conversion by 17% via test roadmap.",
            "Built attribution dashboard adopted by sales and marketing leaders.",
        ],
    ),
    RoleProfile(
        slug="content-writer",
        role_title="Content Writer",
        person_name="Casey Brooks",
        location="Prague, CZ",
        email="casey.brooks@example.com",
        template="B",
        summary="Content writer creating SEO-focused articles and conversion-friendly product narratives.",
        skills=["SEO Writing", "Briefing", "On-page SEO", "CMS", "Editing", "Research"],
        experience=[
            "Senior Content Writer — LedgerPath (2023-Now)",
            "Content Specialist — StoryGrid (2020-2023)",
        ],
        achievements=[
            "Published 90+ articles with avg time-on-page above 4 minutes.",
            "Grew organic traffic by 48% on priority non-brand topics.",
            "Raised article-to-trial conversion through intent-based briefs.",
        ],
    ),
    RoleProfile(
        slug="event-planner",
        role_title="Event Planner",
        person_name="Riley Kim",
        location="Barcelona, ES",
        email="riley.kim@example.com",
        template="C",
        summary="Event planner delivering high-attendance events with vendor and budget control.",
        skills=["Vendor Mgmt", "Run of Show", "Budgeting", "Client Relations", "CRM", "Logistics"],
        experience=[
            "Event Planner — SummitHouse (2021-Now)",
            "Event Coordinator — KeyMoment (2018-2021)",
        ],
        achievements=[
            "Delivered 40+ B2B events with 96% attendee satisfaction.",
            "Negotiated vendor contracts and reduced spend by 14% YoY.",
            "Standardized checklists that lowered day-of incidents by 37%.",
        ],
    ),
    RoleProfile(
        slug="data-scientist",
        role_title="Data Scientist",
        person_name="Morgan Patel",
        location="Dublin, IE",
        email="morgan.patel@example.com",
        template="A",
        summary="Data scientist building predictive models and analytics products for business teams.",
        skills=["Python", "scikit-learn", "SQL", "Experimentation", "Feature Eng", "ML Ops"],
        experience=[
            "Data Scientist — QuantLeaf (2022-Now)",
            "Data Analyst — Horizon Labs (2019-2022)",
        ],
        achievements=[
            "Improved demand forecast MAPE from 18% to 11%.",
            "Shipped churn prediction model used in weekly retention workflows.",
            "Reduced notebook-to-production handoff time by 45%.",
        ],
    ),
    RoleProfile(
        slug="sales-manager",
        role_title="Sales Manager",
        person_name="Drew Collins",
        location="London, UK",
        email="drew.collins@example.com",
        template="B",
        summary="Sales leader developing quota-carrying teams and predictable pipeline execution.",
        skills=["Pipeline Mgmt", "Forecasting", "Coaching", "CRM", "Negotiation", "Outbound"],
        experience=[
            "Sales Manager — LeadSprout (2021-Now)",
            "Account Executive — GrowthLane (2017-2021)",
        ],
        achievements=[
            "Exceeded annual team quota at 118% across two consecutive years.",
            "Raised win-rate by 9 points via discovery and objection playbooks.",
            "Introduced forecast hygiene process improving accuracy to +/- 6%.",
        ],
    ),
]


def seed_from_slug(slug: str) -> int:
    return int(hashlib.sha256(slug.encode("utf-8")).hexdigest()[:8], 16)


def color_mix(slug: str) -> dict[str, tuple[int, int, int]]:
    rng = random.Random(seed_from_slug(slug))
    colors = list(PALETTE.values())
    rng.shuffle(colors)
    return {
        "primary": colors[0],
        "secondary": colors[1],
        "tertiary": colors[2],
        "quaternary": colors[3],
    }


def to_pdf_color(rgb: tuple[int, int, int]) -> Color:
    return Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)


def wrap_words(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    current_len = 0
    for word in words:
        add = len(word) + (1 if current else 0)
        if current_len + add > max_chars:
            lines.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += add
    if current:
        lines.append(" ".join(current))
    return lines


def draw_pdf_header(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], page_w: float, page_h: float) -> float:
    c.setFillColor(to_pdf_color(mix["primary"]))
    c.rect(36, page_h - 76, page_w - 72, 6, fill=1, stroke=0)
    c.setFillColor(Color(0, 0, 0))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(36, page_h - 52, profile.person_name.upper())
    c.setFont("Helvetica", 11)
    c.drawString(36, page_h - 68, f"{profile.role_title}  |  {profile.location}  |  {profile.email}")
    return page_h - 92


def draw_pdf_template_a(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float, page_h: float) -> None:
    sidebar_x = 36
    sidebar_w = 145
    content_x = sidebar_x + sidebar_w + 20
    bottom = 42
    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(1.2)
    c.line(sidebar_x + sidebar_w, bottom, sidebar_x + sidebar_w, start_y)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(sidebar_x, start_y - 6, "SKILLS")
    y = start_y - 22
    c.setFont("Helvetica", 9)
    for i, skill in enumerate(profile.skills):
        color_key = ("primary", "secondary", "tertiary", "quaternary")[i % 4]
        c.setFillColor(to_pdf_color(mix[color_key]))
        c.circle(sidebar_x + 3.5, y + 2.5, 2.2, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.drawString(sidebar_x + 10, y, skill)
        y -= 14

    c.setFont("Helvetica-Bold", 11)
    c.drawString(content_x, start_y - 6, "SUMMARY")
    c.setFont("Helvetica", 10)
    y = start_y - 22
    for line in wrap_words(profile.summary, 76):
        c.drawString(content_x, y, line)
        y -= 13

    y -= 6
    c.setStrokeColor(to_pdf_color(mix["primary"]))
    c.line(content_x, y, 560, y)
    y -= 14
    c.setFont("Helvetica-Bold", 11)
    c.drawString(content_x, y, "EXPERIENCE")
    y -= 14
    c.setFont("Helvetica", 10)
    for exp in profile.experience:
        c.drawString(content_x, y, exp)
        y -= 12
    y -= 4
    c.setFont("Helvetica-Bold", 11)
    c.drawString(content_x, y, "KEY RESULTS")
    y -= 14
    c.setFont("Helvetica", 10)
    for i, point in enumerate(profile.achievements):
        color_key = ("primary", "secondary", "tertiary", "quaternary")[i % 4]
        c.setFillColor(to_pdf_color(mix[color_key]))
        c.circle(content_x + 3, y + 2.5, 2.1, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        for line in wrap_words(point, 68):
            c.drawString(content_x + 10, y, line)
            y -= 12
        y -= 1


def draw_pdf_template_b(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float) -> None:
    x0 = 36
    x1 = 560
    y = start_y - 2

    sections = [
        ("SUMMARY", [profile.summary]),
        ("CORE SKILLS", [", ".join(profile.skills)]),
        ("EXPERIENCE", profile.experience),
        ("ACHIEVEMENTS", profile.achievements),
    ]

    for idx, (title, rows) in enumerate(sections):
        color_key = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        c.setStrokeColor(to_pdf_color(mix[color_key]))
        c.setLineWidth(1.4)
        c.line(x0, y, x1, y)
        y -= 14
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x0, y, title)
        y -= 14
        c.setFont("Helvetica", 10)
        for item in rows:
            lines = wrap_words(item, 92)
            if title in {"EXPERIENCE", "ACHIEVEMENTS"}:
                c.setFillColor(to_pdf_color(mix[color_key]))
                c.circle(x0 + 3.2, y + 2.5, 2.1, stroke=0, fill=1)
                c.setFillColor(Color(0, 0, 0))
                text_x = x0 + 10
            else:
                text_x = x0
            for line in lines:
                c.drawString(text_x, y, line)
                y -= 12
            y -= 1
        y -= 5


def draw_pdf_template_c(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float) -> None:
    left_x = 68
    line_top = start_y - 8
    line_bottom = 120
    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(1.6)
    c.line(left_x, line_bottom, left_x, line_top)

    y = start_y - 18
    entries = [
        ("PROFILE", [profile.summary]),
        ("SKILLS", [", ".join(profile.skills)]),
        ("EXPERIENCE", profile.experience + profile.achievements[:1]),
        ("RESULTS", profile.achievements[1:]),
    ]
    for idx, (title, rows) in enumerate(entries):
        color_key = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        dot_color = to_pdf_color(mix[color_key])
        c.setFillColor(dot_color)
        c.circle(left_x, y + 3, 4, fill=1, stroke=0)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_x + 18, y, title)
        y -= 14
        c.setFont("Helvetica", 10)
        for row in rows:
            for line in wrap_words(row, 82):
                c.drawString(left_x + 18, y, line)
                y -= 12
            y -= 1
        y -= 8


def generate_pdf(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "sample.pdf"
    page_w, page_h = A4
    mix = color_mix(profile.slug)

    c = canvas.Canvas(str(out_file), pagesize=A4)
    c.setTitle(f"{profile.role_title} Resume Example")
    start_y = draw_pdf_header(c, profile, mix, page_w, page_h)

    if profile.template == "A":
        draw_pdf_template_a(c, profile, mix, start_y, page_h)
    elif profile.template == "B":
        draw_pdf_template_b(c, profile, mix, start_y)
    else:
        draw_pdf_template_c(c, profile, mix, start_y)

    c.showPage()
    c.save()
    return out_file


def font_for(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: Iterable[str] = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def png_header(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int) -> int:
    draw.rectangle((54, 56, width - 54, 68), fill=mix["primary"])
    draw.text((54, 84), profile.person_name.upper(), fill=(0, 0, 0), font=font_for(40, bold=True))
    draw.text(
        (54, 132),
        f"{profile.role_title}  |  {profile.location}  |  {profile.email}",
        fill=(0, 0, 0),
        font=font_for(20),
    )
    return 176


def draw_png_template_a(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, height: int, start_y: int) -> None:
    sidebar_x = 54
    sidebar_w = 280
    body_x = sidebar_x + sidebar_w + 32
    draw.line((sidebar_x + sidebar_w, start_y, sidebar_x + sidebar_w, height - 72), fill=mix["secondary"], width=3)
    draw.text((sidebar_x, start_y + 10), "SKILLS", fill=(0, 0, 0), font=font_for(22, bold=True))

    y = start_y + 46
    for i, skill in enumerate(profile.skills):
        color = mix[("primary", "secondary", "tertiary", "quaternary")[i % 4]]
        draw.ellipse((sidebar_x, y + 8, sidebar_x + 10, y + 18), fill=color)
        draw.text((sidebar_x + 18, y), skill, fill=(0, 0, 0), font=font_for(18))
        y += 34

    y2 = start_y + 10
    draw.text((body_x, y2), "SUMMARY", fill=(0, 0, 0), font=font_for(24, bold=True))
    y2 += 34
    for line in wrap_words(profile.summary, 55):
        draw.text((body_x, y2), line, fill=(0, 0, 0), font=font_for(18))
        y2 += 29

    y2 += 8
    draw.line((body_x, y2, width - 60, y2), fill=mix["primary"], width=3)
    y2 += 16
    draw.text((body_x, y2), "EXPERIENCE", fill=(0, 0, 0), font=font_for(24, bold=True))
    y2 += 36
    for exp in profile.experience:
        draw.text((body_x, y2), exp, fill=(0, 0, 0), font=font_for(18))
        y2 += 30

    y2 += 10
    draw.text((body_x, y2), "KEY RESULTS", fill=(0, 0, 0), font=font_for(24, bold=True))
    y2 += 34
    for i, item in enumerate(profile.achievements):
        color = mix[("primary", "secondary", "tertiary", "quaternary")[i % 4]]
        draw.ellipse((body_x, y2 + 7, body_x + 10, y2 + 17), fill=color)
        for line in wrap_words(item, 53):
            draw.text((body_x + 18, y2), line, fill=(0, 0, 0), font=font_for(18))
            y2 += 28
        y2 += 3


def draw_png_template_b(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, start_y: int) -> None:
    x0 = 54
    x1 = width - 54
    y = start_y + 8
    sections = [
        ("SUMMARY", [profile.summary]),
        ("CORE SKILLS", [", ".join(profile.skills)]),
        ("EXPERIENCE", profile.experience),
        ("ACHIEVEMENTS", profile.achievements),
    ]
    for idx, (title, rows) in enumerate(sections):
        color = mix[("primary", "secondary", "tertiary", "quaternary")[idx % 4]]
        draw.line((x0, y, x1, y), fill=color, width=3)
        y += 14
        draw.text((x0, y), title, fill=(0, 0, 0), font=font_for(24, bold=True))
        y += 36
        for row in rows:
            lines = wrap_words(row, 88)
            if title in {"EXPERIENCE", "ACHIEVEMENTS"}:
                draw.ellipse((x0, y + 7, x0 + 10, y + 17), fill=color)
                tx = x0 + 18
            else:
                tx = x0
            for line in lines:
                draw.text((tx, y), line, fill=(0, 0, 0), font=font_for(18))
                y += 28
            y += 4
        y += 8


def draw_png_template_c(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], height: int, start_y: int) -> None:
    timeline_x = 96
    draw.line((timeline_x, start_y + 10, timeline_x, height - 90), fill=mix["secondary"], width=4)
    y = start_y + 24
    entries = [
        ("PROFILE", [profile.summary]),
        ("SKILLS", [", ".join(profile.skills)]),
        ("EXPERIENCE", profile.experience + profile.achievements[:1]),
        ("RESULTS", profile.achievements[1:]),
    ]
    for idx, (title, rows) in enumerate(entries):
        color = mix[("primary", "secondary", "tertiary", "quaternary")[idx % 4]]
        draw.ellipse((timeline_x - 8, y + 4, timeline_x + 8, y + 20), fill=color)
        draw.text((timeline_x + 22, y), title, fill=(0, 0, 0), font=font_for(24, bold=True))
        y += 36
        for row in rows:
            for line in wrap_words(row, 78):
                draw.text((timeline_x + 22, y), line, fill=(0, 0, 0), font=font_for(18))
                y += 28
            y += 5
        y += 10


def generate_png(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "preview.png"
    mix = color_mix(profile.slug)

    width = 1240
    height = 1754
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    start_y = png_header(draw, profile, mix, width)

    if profile.template == "A":
        draw_png_template_a(draw, profile, mix, width, height, start_y)
    elif profile.template == "B":
        draw_png_template_b(draw, profile, mix, width, start_y)
    else:
        draw_png_template_c(draw, profile, mix, height, start_y)

    image.save(out_file, format="PNG", optimize=True)
    return out_file


def generate_manifest() -> Path:
    manifest_path = OUTPUT_ROOT / "manifest.json"
    data = {
        profile.slug: {
            "role_title": profile.role_title,
            "template": profile.template,
            "pdf": f"/assets/examples/{profile.slug}/sample.pdf",
            "preview": f"/assets/examples/{profile.slug}/preview.png",
            "colors": color_mix(profile.slug),
        }
        for profile in PROFILES
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return manifest_path


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        generate_pdf(profile)
        generate_png(profile)
    generate_manifest()
    print(f"Generated assets for {len(PROFILES)} roles in {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
