#!/usr/bin/env python3
"""Generate rich static resume sample assets for example pages.

Outputs for each role:
  - assets/examples/<slug>/sample.pdf
  - assets/examples/<slug>/preview.png
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "assets" / "examples"

PALETTE = {
    "green": (22, 163, 74),
    "red": (220, 38, 38),
    "blue": (37, 99, 235),
    "purple": (124, 58, 237),
}


@dataclass(frozen=True)
class ExperienceItem:
    period: str
    title: str
    company: str
    location: str
    bullets: list[str]


@dataclass(frozen=True)
class EducationItem:
    period: str
    degree: str
    school: str
    details: str


@dataclass(frozen=True)
class ProjectItem:
    name: str
    details: str


@dataclass(frozen=True)
class SkillRating:
    name: str
    level: int  # 1-5


@dataclass(frozen=True)
class RoleProfile:
    slug: str
    template: str
    person_name: str
    role_title: str
    location: str
    phone: str
    email: str
    website: str
    linkedin: str
    summary: str
    core_skills: list[str]
    tools: list[str]
    experience: list[ExperienceItem]
    education: list[EducationItem]
    projects: list[ProjectItem]
    certifications: list[str]
    languages: list[str]
    interests: list[str]
    skill_ratings: list[SkillRating]


PROFILES: list[RoleProfile] = [
    RoleProfile(
        slug="software-engineer",
        template="A",
        person_name="Alex Carter",
        role_title="Senior Software Engineer",
        location="Berlin, Germany",
        phone="+49 30 8847 2291",
        email="alex.carter@example.com",
        website="alexcarter.dev",
        linkedin="linkedin.com/in/alexcarterdev",
        summary=(
            "Backend-focused software engineer with 7+ years building distributed services for "
            "B2B SaaS. Strong in Python, Go, and cloud operations. Known for reducing latency, "
            "improving reliability, and mentoring engineers through production-scale delivery."
        ),
        core_skills=["System Design", "API Architecture", "Microservices", "Observability", "Incident Response", "Mentoring"],
        tools=["Python", "Go", "PostgreSQL", "Redis", "Kafka", "AWS", "Docker", "Kubernetes", "Terraform", "GitHub Actions"],
        experience=[
            ExperienceItem(
                period="2022 - Present",
                title="Senior Software Engineer",
                company="NimbleCore",
                location="Berlin",
                bullets=[
                    "Led redesign of billing APIs and reduced p95 latency by 41% through query tuning and cache strategy.",
                    "Built event-driven ingestion service in Go; improved data freshness from 15 minutes to under 4 minutes.",
                    "Introduced release quality gates and lowered rollback incidents by 28% across three product teams.",
                ],
            ),
            ExperienceItem(
                period="2019 - 2022",
                title="Software Engineer",
                company="PixelScale",
                location="Remote",
                bullets=[
                    "Implemented multi-tenant permissions model used by 1,200+ enterprise customers.",
                    "Automated CI pipelines and cut average deployment time from 42 to 14 minutes.",
                    "Partnered with product and support teams to eliminate top 10 recurring incident classes.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2014 - 2018",
                degree="BSc Computer Science",
                school="Technical University of Berlin",
                details="Graduated with honors. Focus: distributed systems, databases, and software architecture.",
            ),
            EducationItem(
                period="2017",
                degree="Cloud Engineering Exchange Program",
                school="Aalto University",
                details="Semester exchange with emphasis on scalable cloud-native application design.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Internal Reliability Scorecard",
                details="Created reliability metrics framework adopted by engineering leadership for weekly operational reviews.",
            ),
            ProjectItem(
                name="Developer Platform Toolkit",
                details="Built CLI templates and runbook automation that accelerated onboarding of new backend engineers.",
            ),
        ],
        certifications=["AWS Certified Developer Associate", "CKA (in progress)"],
        languages=["English (Fluent)", "German (Professional)"],
        interests=["Open-source backend tooling", "Running", "Tech mentoring communities"],
        skill_ratings=[
            SkillRating("Python", 5),
            SkillRating("Go", 4),
            SkillRating("System Design", 5),
            SkillRating("Kubernetes", 4),
            SkillRating("Data Modeling", 4),
        ],
    ),
    RoleProfile(
        slug="product-manager",
        template="B",
        person_name="Taylor Morgan",
        role_title="Product Manager",
        location="Amsterdam, Netherlands",
        phone="+31 20 441 7082",
        email="taylor.morgan@example.com",
        website="taylormorgan.pm",
        linkedin="linkedin.com/in/taylormorgan",
        summary=(
            "Product manager with 6+ years experience in SaaS and platform products. Blends user "
            "research, analytics, and delivery leadership to ship features that increase retention "
            "and activation. Comfortable owning discovery through launch and post-release metrics."
        ),
        core_skills=["Roadmapping", "Discovery", "Experimentation", "Stakeholder Alignment", "PRDs", "Metrics Strategy"],
        tools=["Amplitude", "Mixpanel", "SQL", "Jira", "Confluence", "Figma", "Miro", "Notion"],
        experience=[
            ExperienceItem(
                period="2021 - Present",
                title="Product Manager",
                company="OrbitFlow",
                location="Amsterdam",
                bullets=[
                    "Owned onboarding and activation roadmap; increased first-week activation by 19%.",
                    "Prioritized retention initiatives that reduced 90-day churn by 11%.",
                    "Introduced KPI review ritual linking product squads to revenue and expansion goals.",
                ],
            ),
            ExperienceItem(
                period="2018 - 2021",
                title="Associate Product Manager",
                company="SignalDesk",
                location="Rotterdam",
                bullets=[
                    "Managed integrations backlog and launched 12 customer-requested connectors.",
                    "Built experiment framework used by growth and core platform teams.",
                    "Partnered with design to standardize job-to-be-done interview guides.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2013 - 2017",
                degree="BBA Digital Business",
                school="Erasmus University Rotterdam",
                details="Concentration in digital strategy and product economics.",
            ),
            EducationItem(
                period="2020",
                degree="Product Leadership Program",
                school="Reforge",
                details="Applied lifecycle and growth loops methodology to subscription product initiatives.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Customer Feedback Operating System",
                details="Unified NPS, support tickets, and sales notes into one product-priority scoring model.",
            ),
            ProjectItem(
                name="Self-serve Trial Funnel",
                details="Redesigned trial journey from signup to value moment; increased trial-to-paid conversion by 8 points.",
            ),
        ],
        certifications=["PSPO I", "Pragmatic Product Foundations"],
        languages=["English (Fluent)", "Dutch (Professional)"],
        interests=["Behavioral design", "Cycling", "Product writing"],
        skill_ratings=[
            SkillRating("Roadmapping", 5),
            SkillRating("User Research", 4),
            SkillRating("SQL", 4),
            SkillRating("Experimentation", 5),
            SkillRating("Stakeholder Mgmt", 5),
        ],
    ),
    RoleProfile(
        slug="marketing-manager",
        template="C",
        person_name="Jordan Lee",
        role_title="Marketing Manager",
        location="Warsaw, Poland",
        phone="+48 22 884 9931",
        email="jordan.lee@example.com",
        website="jordanleemarketing.com",
        linkedin="linkedin.com/in/jordanleemktg",
        summary=(
            "Marketing manager with broad B2B demand generation experience across content, paid media, "
            "lifecycle programs, and GTM reporting. Builds measurable funnel systems, coaches cross-functional "
            "teams, and aligns marketing execution with sales pipeline and revenue targets quarter over quarter."
        ),
        core_skills=[
            "Demand Generation",
            "Campaign Planning",
            "Funnel Analytics",
            "Content Strategy",
            "Team Leadership",
            "Budget Ownership",
        ],
        tools=["GA4", "HubSpot", "Salesforce", "Google Ads", "Meta Ads", "Looker Studio", "Semrush", "Ahrefs", "Tableau", "VWO"],
        experience=[
            ExperienceItem(
                period="2021 - Present",
                title="Marketing Manager",
                company="BrightMint",
                location="Warsaw",
                bullets=[
                    "Scaled MQL pipeline by 34% through segmented campaigns, offer-specific landing pages, and weekly channel testing.",
                    "Improved paid media ROAS from 2.1x to 3.3x in two quarters while maintaining lead quality thresholds set by sales.",
                    "Built monthly funnel review process shared with GTM leadership, linking spend, SQL quality, and closed-won revenue.",
                ],
            ),
            ExperienceItem(
                period="2017 - 2021",
                title="Growth Specialist",
                company="NovaRetail",
                location="Krakow",
                bullets=[
                    "Increased non-brand organic traffic by 52% across regional content hubs through topic clusters and content refresh sprints.",
                    "Designed lifecycle nurture series that lifted SQL conversion by 14% and shortened average lead response latency.",
                    "Collaborated with sales ops to map campaign influence to closed-won opportunities and improve forecasting confidence.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2012 - 2016",
                degree="BA Marketing and Communication",
                school="University of Warsaw",
                details="Coursework in consumer psychology, market research, and digital media planning.",
            ),
            EducationItem(
                period="2019",
                degree="Advanced Performance Marketing Certificate",
                school="CXL Institute",
                details="Hands-on training in experimentation and conversion optimization frameworks.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Annual Campaign Calendar Framework",
                details="Created cross-team planning model that reduced launch delays by 30%.",
            ),
            ProjectItem(
                name="Marketing Analytics Glossary",
                details="Standardized KPI definitions and reporting formulas across marketing and sales ops.",
            ),
        ],
        certifications=["Google Analytics 4 Certification", "HubSpot Marketing Software"],
        languages=["English (Fluent)", "Polish (Native)"],
        interests=["Brand strategy", "Photography", "Community events"],
        skill_ratings=[
            SkillRating("Demand Gen", 5),
            SkillRating("SEO", 4),
            SkillRating("Paid Media", 4),
            SkillRating("Lifecycle", 5),
            SkillRating("Reporting", 5),
        ],
    ),
    RoleProfile(
        slug="digital-marketing",
        template="A",
        person_name="Sam Rivera",
        role_title="Digital Marketing Manager",
        location="Lisbon, Portugal",
        phone="+351 21 442 1905",
        email="sam.rivera@example.com",
        website="samriveradigital.com",
        linkedin="linkedin.com/in/samriveradigital",
        summary=(
            "Digital marketing professional driving full-funnel growth with paid media, SEO, and "
            "conversion experimentation. Strong at turning channel performance data into repeatable "
            "playbooks that increase qualified leads while lowering acquisition costs."
        ),
        core_skills=["Performance Marketing", "Paid Search", "Paid Social", "CRO", "Attribution", "Landing Page Strategy"],
        tools=["Google Ads", "Meta Ads", "LinkedIn Ads", "GA4", "Looker Studio", "Hotjar", "HubSpot", "Zapier"],
        experience=[
            ExperienceItem(
                period="2022 - Present",
                title="Digital Marketing Manager",
                company="WavePilot",
                location="Lisbon",
                bullets=[
                    "Reduced blended CAC by 22% while increasing lead volume by 31%.",
                    "Built channel attribution dashboard adopted by marketing and sales teams.",
                    "Led CRO roadmap and improved landing page conversion by 17%.",
                ],
            ),
            ExperienceItem(
                period="2018 - 2022",
                title="Performance Marketer",
                company="OpenNest",
                location="Porto",
                bullets=[
                    "Launched new paid social structures that doubled qualified demo requests.",
                    "Created audience segmentation strategy improving SQL quality from paid channels.",
                    "Automated campaign QA checklists, reducing setup errors by 40%.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2012 - 2016",
                degree="BSc Business and Marketing Analytics",
                school="Nova School of Business and Economics",
                details="Studied growth analytics, statistics, and performance media optimization.",
            ),
            EducationItem(
                period="2021",
                degree="Growth Marketing Minidegree",
                school="CXL Institute",
                details="Completed advanced modules on experimentation velocity and paid media structure.",
            ),
        ],
        projects=[
            ProjectItem(
                name="SEO + PPC Topic Clusters",
                details="Aligned content and paid campaigns around high-intent themes to increase SERP coverage.",
            ),
            ProjectItem(
                name="Creative Testing Framework",
                details="Introduced weekly ad creative scorecards and improved CTR consistency across channels.",
            ),
        ],
        certifications=["Google Ads Search Certification", "Meta Certified Digital Marketing Associate"],
        languages=["English (Fluent)", "Portuguese (Native)", "Spanish (Professional)"],
        interests=["Behavioral economics", "Travel photography", "Padel"],
        skill_ratings=[
            SkillRating("Paid Search", 5),
            SkillRating("Paid Social", 4),
            SkillRating("CRO", 4),
            SkillRating("Attribution", 4),
            SkillRating("Automation", 5),
        ],
    ),
    RoleProfile(
        slug="content-writer",
        template="B",
        person_name="Casey Brooks",
        role_title="Senior Content Writer",
        location="Prague, Czech Republic",
        phone="+420 224 772 519",
        email="casey.brooks@example.com",
        website="caseywrites.co",
        linkedin="linkedin.com/in/caseybrooks",
        summary=(
            "Content writer with strong SEO and product storytelling background. Produces high-intent "
            "articles, landing pages, and email sequences that improve organic visibility and conversion. "
            "Experienced in collaborating with product, sales, and demand generation teams."
        ),
        core_skills=["SEO Writing", "Editorial Planning", "Content Strategy", "User Intent Mapping", "On-page Optimization", "Copy Editing"],
        tools=["Google Search Console", "Ahrefs", "Semrush", "Notion", "Webflow", "WordPress", "Grammarly", "SurferSEO"],
        experience=[
            ExperienceItem(
                period="2023 - Present",
                title="Senior Content Writer",
                company="LedgerPath",
                location="Prague",
                bullets=[
                    "Published 90+ long-form pieces with average read time above 4 minutes.",
                    "Grew non-brand organic traffic by 48% on priority cluster topics.",
                    "Partnered with growth team on BOFU pages that lifted trial conversion by 12%.",
                ],
            ),
            ExperienceItem(
                period="2020 - 2023",
                title="Content Specialist",
                company="StoryGrid",
                location="Brno",
                bullets=[
                    "Created messaging style guide used by content, product marketing, and customer success.",
                    "Improved article update cycle from quarterly to monthly for top traffic pages.",
                    "Built SME interview workflow reducing first-draft turnaround by 25%.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2013 - 2017",
                degree="BA Journalism and Media",
                school="Charles University",
                details="Focused on digital publishing, narrative structure, and editorial ethics.",
            ),
            EducationItem(
                period="2022",
                degree="SEO Content Strategy Course",
                school="HubSpot Academy",
                details="Advanced training in search intent mapping and topic cluster design.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Content Refresh Program",
                details="Designed refresh prioritization matrix that improved ranking retention on aging content.",
            ),
            ProjectItem(
                name="Editorial QA Checklist",
                details="Implemented plain-language and SEO QA workflow used by freelance and in-house writers.",
            ),
        ],
        certifications=["HubSpot Content Marketing", "SEMrush SEO Fundamentals"],
        languages=["English (Fluent)", "Czech (Professional)"],
        interests=["Narrative nonfiction", "Coffee roasting", "Travel journals"],
        skill_ratings=[
            SkillRating("SEO Writing", 5),
            SkillRating("Research", 5),
            SkillRating("Editing", 4),
            SkillRating("Content Strategy", 4),
            SkillRating("CMS Publishing", 5),
        ],
    ),
    RoleProfile(
        slug="event-planner",
        template="C",
        person_name="Riley Kim",
        role_title="Event Planner",
        location="Barcelona, Spain",
        phone="+34 93 442 8155",
        email="riley.kim@example.com",
        website="rileykimevents.com",
        linkedin="linkedin.com/in/rileykim-events",
        summary=(
            "Event planner experienced in B2B conferences, partner summits, and executive off-sites. "
            "Delivers high-attendance programs with strict budget control, clear vendor coordination, "
            "and operational playbooks that reduce event-day risks."
        ),
        core_skills=["Event Operations", "Vendor Management", "Run of Show", "Budget Planning", "Stakeholder Comms", "On-site Execution"],
        tools=["Cvent", "Asana", "Google Workspace", "Canva", "HubSpot", "Excel", "Slack", "Zoom Events"],
        experience=[
            ExperienceItem(
                period="2021 - Present",
                title="Event Planner",
                company="SummitHouse",
                location="Barcelona",
                bullets=[
                    "Managed 40+ B2B events with average attendee satisfaction score of 96%.",
                    "Negotiated multi-vendor contracts reducing annual event spend by 14%.",
                    "Built standardized event-day playbook used by five regional event squads.",
                ],
            ),
            ExperienceItem(
                period="2018 - 2021",
                title="Event Coordinator",
                company="KeyMoment",
                location="Madrid",
                bullets=[
                    "Supported 25+ conferences from planning to post-event reporting.",
                    "Introduced registration QA process cutting attendee check-in issues by 37%.",
                    "Coordinated speakers, sponsors, and venue teams for hybrid event formats.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2012 - 2016",
                degree="BA Hospitality and Event Management",
                school="University of Barcelona",
                details="Studied event logistics, operations, and service management principles.",
            ),
            EducationItem(
                period="2020",
                degree="Professional Event Management Certificate",
                school="Event Leadership Institute",
                details="Specialization in sponsorship operations and event ROI reporting.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Speaker Readiness Program",
                details="Created briefing process and rehearsal templates that improved on-stage quality.",
            ),
            ProjectItem(
                name="Sustainable Venue Checklist",
                details="Implemented eco-friendly procurement guidelines across annual flagship events.",
            ),
        ],
        certifications=["CMP (Certified Meeting Professional)", "Google Project Management Certificate"],
        languages=["English (Fluent)", "Spanish (Fluent)", "Korean (Native)"],
        interests=["Community workshops", "Design fairs", "Food culture"],
        skill_ratings=[
            SkillRating("Vendor Negotiation", 5),
            SkillRating("Budgeting", 4),
            SkillRating("Operations", 5),
            SkillRating("Stakeholder Mgmt", 4),
            SkillRating("Crisis Handling", 4),
        ],
    ),
    RoleProfile(
        slug="data-scientist",
        template="A",
        person_name="Morgan Patel",
        role_title="Data Scientist",
        location="Dublin, Ireland",
        phone="+353 1 441 7742",
        email="morgan.patel@example.com",
        website="morganpatel.ai",
        linkedin="linkedin.com/in/morganpatel",
        summary=(
            "Data scientist with experience shipping predictive models and decision-support analytics "
            "for commercial and operations teams. Works across experimentation, feature engineering, "
            "and model deployment with a strong focus on measurable business outcomes."
        ),
        core_skills=["Predictive Modeling", "Experiment Design", "Feature Engineering", "Data Storytelling", "MLOps Collaboration", "Business Analytics"],
        tools=["Python", "SQL", "scikit-learn", "XGBoost", "Pandas", "Airflow", "dbt", "BigQuery", "Power BI", "MLflow"],
        experience=[
            ExperienceItem(
                period="2022 - Present",
                title="Data Scientist",
                company="QuantLeaf",
                location="Dublin",
                bullets=[
                    "Improved demand forecast MAPE from 18% to 11% for core planning models.",
                    "Shipped churn prediction pipeline integrated into retention playbooks.",
                    "Partnered with product managers to operationalize weekly experiment readouts.",
                ],
            ),
            ExperienceItem(
                period="2019 - 2022",
                title="Data Analyst",
                company="Horizon Labs",
                location="Cork",
                bullets=[
                    "Built self-serve dashboards for GTM teams reducing ad-hoc reporting volume by 35%.",
                    "Developed segmentation logic used in lifecycle and pricing experiments.",
                    "Documented data quality checks and reduced dashboard incidents by 29%.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2013 - 2017",
                degree="BSc Statistics and Computer Science",
                school="Trinity College Dublin",
                details="Focus on machine learning, statistical modeling, and data systems.",
            ),
            EducationItem(
                period="2021",
                degree="Applied Machine Learning Program",
                school="Coursera / DeepLearning.AI",
                details="Completed practical modules on model validation and deployment workflows.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Demand Forecast Monitoring",
                details="Built model drift alerts and retraining criteria to maintain forecast quality over time.",
            ),
            ProjectItem(
                name="Experiment Insight Library",
                details="Created reusable notebook templates for cross-functional experiment reporting.",
            ),
        ],
        certifications=["Google Professional Data Analytics", "AWS Machine Learning Specialty (prep)"],
        languages=["English (Fluent)", "Hindi (Native)"],
        interests=["Applied ML communities", "Chess", "Long-distance running"],
        skill_ratings=[
            SkillRating("Python", 5),
            SkillRating("SQL", 5),
            SkillRating("Modeling", 4),
            SkillRating("Experimentation", 4),
            SkillRating("Visualization", 4),
        ],
    ),
    RoleProfile(
        slug="sales-manager",
        template="B",
        person_name="Drew Collins",
        role_title="Sales Manager",
        location="London, United Kingdom",
        phone="+44 20 7946 8821",
        email="drew.collins@example.com",
        website="drewcollinssales.com",
        linkedin="linkedin.com/in/drewcollins",
        summary=(
            "Sales manager with 9+ years in B2B SaaS revenue teams. Builds repeatable pipeline systems, "
            "coaches account executives, and drives consistent forecasting discipline. Strong record of "
            "improving win rates and exceeding quarterly quota targets."
        ),
        core_skills=["Pipeline Management", "Sales Coaching", "Forecasting", "Deal Strategy", "Territory Planning", "Cross-functional Alignment"],
        tools=["Salesforce", "HubSpot", "Gong", "Outreach", "Clari", "Apollo", "LinkedIn Sales Navigator", "Excel"],
        experience=[
            ExperienceItem(
                period="2021 - Present",
                title="Sales Manager",
                company="LeadSprout",
                location="London",
                bullets=[
                    "Led 10-account-executive team to 118% annual quota attainment for two consecutive years.",
                    "Introduced discovery and objection coaching playbooks; win rate improved by 9 points.",
                    "Implemented forecast hygiene framework increasing commit accuracy to within +/-6%.",
                ],
            ),
            ExperienceItem(
                period="2017 - 2021",
                title="Account Executive",
                company="GrowthLane",
                location="Manchester",
                bullets=[
                    "Closed enterprise deals up to 220k ARR across fintech and logistics accounts.",
                    "Ranked top 5% of AE team in expansion revenue and multi-threaded deal execution.",
                    "Partnered with marketing on ICP-based outbound messaging framework.",
                ],
            ),
        ],
        education=[
            EducationItem(
                period="2010 - 2014",
                degree="BA Business Management",
                school="University of Manchester",
                details="Specialized in sales strategy, negotiation, and commercial finance.",
            ),
            EducationItem(
                period="2022",
                degree="Revenue Leadership Certificate",
                school="Winning by Design",
                details="Practical training in pipeline review cadences and forecast governance.",
            ),
        ],
        projects=[
            ProjectItem(
                name="Quarterly Deal Review Framework",
                details="Created account-level review rituals that improved close planning quality.",
            ),
            ProjectItem(
                name="Enablement Content Hub",
                details="Developed objection handling and discovery resources for new-hire onboarding.",
            ),
        ],
        certifications=["MEDDICC Academy", "HubSpot Sales Software Certification"],
        languages=["English (Native)", "French (Conversational)"],
        interests=["Team coaching", "Basketball", "Public speaking"],
        skill_ratings=[
            SkillRating("Forecasting", 5),
            SkillRating("Coaching", 5),
            SkillRating("Negotiation", 4),
            SkillRating("CRM Hygiene", 4),
            SkillRating("Pipeline Build", 5),
        ],
    ),
]


def seed_from_slug(slug: str) -> int:
    return int(hashlib.sha256(slug.encode("utf-8")).hexdigest()[:8], 16)


def color_mix(slug: str) -> dict[str, tuple[int, int, int]]:
    rng = random.Random(seed_from_slug(slug))
    colors = list(PALETTE.values())
    accent = colors[rng.randrange(0, len(colors))]
    return {"text": (17, 17, 17), "accent": accent}


def to_pdf_color(rgb: tuple[int, int, int]) -> Color:
    return Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def fit_pdf_text(text: str, font_name: str, font_size: float, max_width: float) -> str:
    text = normalize_text(text)
    if pdfmetrics.stringWidth(text, font_name, font_size) <= max_width:
        return text
    if max_width <= 8:
        return ""
    suffix = "..."
    candidate = text
    while candidate and pdfmetrics.stringWidth(candidate + suffix, font_name, font_size) > max_width:
        candidate = candidate[:-1]
    return (candidate.rstrip() + suffix) if candidate else suffix


def wrap_pdf_text(text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    words = normalize_text(text).split(" ")
    if not words or words == [""]:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if pdfmetrics.stringWidth(trial, font_name, font_size) <= max_width:
            current = trial
        else:
            lines.append(current)
            if pdfmetrics.stringWidth(word, font_name, font_size) <= max_width:
                current = word
            else:
                current = fit_pdf_text(word, font_name, font_size, max_width)
    lines.append(current)
    return lines


def draw_pdf_wrapped(
    c: canvas.Canvas,
    x: float,
    y: float,
    text: str,
    max_width: float,
    font_name: str = "Helvetica",
    font_size: float = 8.3,
    leading: float = 9.6,
    max_lines: int | None = None,
) -> float:
    lines = wrap_pdf_text(text, font_name, font_size, max_width)
    if max_lines is not None and len(lines) > max_lines:
        tail = " ".join(lines[max_lines - 1 :])
        lines = lines[: max_lines - 1] + [fit_pdf_text(tail, font_name, font_size, max_width)]
    c.setFont(font_name, font_size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_pdf_bullets(
    c: canvas.Canvas,
    x: float,
    y: float,
    bullets: list[str],
    max_width: float,
    accent: tuple[int, int, int],
    max_items: int = 3,
    max_lines_per_item: int = 2,
    font_size: float = 8.1,
    leading: float = 9.2,
) -> float:
    text_x = x + 9
    text_width = max_width - 9
    for bullet in bullets[:max_items]:
        lines = wrap_pdf_text(bullet, "Helvetica", font_size, text_width)
        if len(lines) > max_lines_per_item:
            tail = " ".join(lines[max_lines_per_item - 1 :])
            lines = lines[: max_lines_per_item - 1] + [fit_pdf_text(tail, "Helvetica", font_size, text_width)]
        c.setFillColor(to_pdf_color(accent))
        c.circle(x + 2.4, y + 2.2, 1.5, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica", font_size)
        for idx, line in enumerate(lines):
            c.drawString(text_x, y, line)
            y -= leading
        if lines:
            y -= 1
    return y


def pdf_section_title(c: canvas.Canvas, x: float, y: float, width: float, title: str, accent: tuple[int, int, int]) -> float:
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.0)
    c.line(x, y, x + width, y)
    c.setFillColor(Color(0, 0, 0))
    c.setFont("Helvetica-Bold", 10.0)
    c.drawString(x, y - 12, title.upper())
    return y - 22


def role_intro(profile: RoleProfile) -> str:
    return (
        f"{profile.role_title} with strong hands-on delivery across cross-functional teams. "
        f"{profile.summary}"
    )


def technology_rows(profile: RoleProfile) -> list[tuple[str, str]]:
    return [
        (profile.core_skills[0], f"Execution in {profile.core_skills[0].lower()} and {profile.core_skills[1].lower()}."),
        (profile.core_skills[2], f"Delivered complex initiatives in {profile.role_title.lower()} responsibilities."),
        ("Tools", ", ".join(profile.tools[:6])),
        ("Certifications", ", ".join(profile.certifications[:2])),
    ]


def marketing_skill_descriptions(profile: RoleProfile) -> list[tuple[str, str]]:
    return [
        ("Demand generation", "Owns full-funnel programs from campaign launch to SQL handoff quality."),
        ("Campaign planning", "Builds quarterly channel plans with budget pacing and clear experiment cadence."),
        ("Funnel analytics", "Tracks MQL-to-revenue conversion and improves attribution confidence across GTM."),
        ("Content strategy", "Aligns SEO, lifecycle, and sales enablement messaging with priority ICP segments."),
    ]


def marketing_success_highlights(profile: RoleProfile) -> list[str]:
    return [
        "Grew qualified pipeline while reducing CAC with stronger message-to-landing alignment.",
        "Improved paid and lifecycle efficiency through structured experiment roadmaps.",
        "Standardized KPI reviews to connect campaign investment with revenue outcomes.",
    ]


def draw_pdf_resume(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], page_w: float, page_h: float) -> None:
    accent = mix["accent"]
    text_rgb = mix["text"]
    margin = 34
    content_w = page_w - margin * 2
    bottom_safe = 44

    c.setFillColor(to_pdf_color(text_rgb))

    # Header
    c.setFont("Helvetica-Bold", 25)
    c.drawString(margin, page_h - 40, profile.person_name.upper())

    intro_x = 214
    intro_w = content_w - (intro_x - margin)
    intro_y = page_h - 28
    intro_y = draw_pdf_wrapped(
        c,
        intro_x,
        intro_y,
        role_intro(profile),
        intro_w,
        font_name="Helvetica",
        font_size=9.4,
        leading=11.0,
        max_lines=5,
    )

    contact_line_y = min(page_h - 78, intro_y - 4)
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.0)
    c.line(margin, contact_line_y, page_w - margin, contact_line_y)

    contact_y = contact_line_y - 14
    contact_col_w = content_w / 4
    contact_items = [profile.website, profile.email, profile.linkedin, profile.phone]
    c.setFont("Helvetica", 8.4)
    for idx, item in enumerate(contact_items):
        x = margin + idx * contact_col_w
        text = fit_pdf_text(item, "Helvetica", 8.4, contact_col_w - 10)
        c.drawString(x, contact_y, text)

    y = contact_y - 17

    # Experience
    y = pdf_section_title(c, margin, y, content_w, "Experience", accent)
    year_col = 96
    for exp in profile.experience[:3]:
        if y <= bottom_safe + 200:
            break
        c.setFont("Helvetica-Bold", 8.9)
        c.drawString(margin, y, fit_pdf_text(exp.period.replace(" - ", "–"), "Helvetica-Bold", 8.9, year_col - 8))
        c.drawString(
            margin + year_col,
            y,
            fit_pdf_text(exp.title, "Helvetica-Bold", 8.9, content_w - year_col - 4),
        )
        y -= 10
        c.setFont("Helvetica-Oblique", 8.0)
        c.drawString(
            margin + year_col,
            y,
            fit_pdf_text(f"{exp.company}, {exp.location}", "Helvetica-Oblique", 8.0, content_w - year_col - 4),
        )
        y -= 10
        y = draw_pdf_bullets(
            c,
            margin + year_col,
            y,
            exp.bullets,
            content_w - year_col,
            accent,
            max_items=3,
            max_lines_per_item=2,
            font_size=8.0,
            leading=9.2,
        )
        c.setStrokeColor(Color(0.87, 0.87, 0.87))
        c.setLineWidth(0.5)
        c.line(margin + year_col, y + 2, margin + content_w, y + 2)
        y -= 5

    # Technology
    y = pdf_section_title(c, margin, y, content_w, "Technology", accent)
    label_w = 124
    for label, desc in technology_rows(profile):
        if y <= bottom_safe + 120:
            break
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(margin, y, fit_pdf_text(label, "Helvetica-Bold", 8.6, label_w - 6))
        y = draw_pdf_wrapped(
            c,
            margin + label_w,
            y,
            desc,
            content_w - label_w,
            font_name="Helvetica",
            font_size=8.1,
            leading=9.1,
            max_lines=2,
        )
        y -= 2

    # Two columns
    col_gap = 16
    col_w = (content_w - col_gap) / 2
    left_x = margin
    right_x = margin + col_w + col_gap
    y -= 1

    left_y = pdf_section_title(c, left_x, y, col_w, "Leadership", accent)
    leadership = [
        f"Led initiatives in {profile.core_skills[0].lower()} and {profile.core_skills[3].lower()} for multi-team delivery.",
        f"Mentored peers on {profile.tools[0]}, {profile.tools[1]}, and reusable implementation standards.",
    ]
    left_y = draw_pdf_bullets(
        c,
        left_x,
        left_y,
        leadership,
        col_w,
        accent,
        max_items=2,
        max_lines_per_item=2,
        font_size=8.0,
        leading=9.1,
    )

    right_y = pdf_section_title(c, right_x, y, col_w, "Project highlights", accent)
    for pr in profile.projects[:2]:
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(right_x, right_y, fit_pdf_text(pr.name, "Helvetica-Bold", 8.5, col_w))
        right_y -= 9
        right_y = draw_pdf_wrapped(
            c,
            right_x,
            right_y,
            pr.details,
            col_w,
            font_name="Helvetica",
            font_size=7.9,
            leading=8.8,
            max_lines=2,
        )
        right_y -= 2

    y = max(left_y, right_y) + 2

    # Education + language
    if y > bottom_safe + 40:
        y = pdf_section_title(c, margin, y, content_w, "Education and Language", accent)
        edu_x = margin
        lang_x = margin + content_w * 0.62
        edu_y = y
        for edu in profile.education[:2]:
            c.setFont("Helvetica-Bold", 8.4)
            c.drawString(edu_x, edu_y, fit_pdf_text(edu.period.replace(" - ", "–"), "Helvetica-Bold", 8.4, 54))
            c.drawString(edu_x + 58, edu_y, fit_pdf_text(edu.degree, "Helvetica-Bold", 8.4, 210))
            edu_y -= 9
            c.setFont("Helvetica-Oblique", 7.9)
            c.drawString(edu_x + 58, edu_y, fit_pdf_text(edu.school, "Helvetica-Oblique", 7.9, 210))
            edu_y -= 9

        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(lang_x, y, "Languages")
        lang_y = y - 10
        c.setFont("Helvetica", 8.0)
        for lang in profile.languages[:3]:
            c.drawString(lang_x, lang_y, fit_pdf_text(lang, "Helvetica", 8.0, content_w - (lang_x - margin)))
            lang_y -= 9


def generate_pdf(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "sample.pdf"
    page_w, page_h = A4
    mix = color_mix(profile.slug)

    c = canvas.Canvas(str(out_file), pagesize=A4)
    c.setTitle(f"{profile.role_title} Resume Example")
    draw_pdf_resume(c, profile, mix, page_w, page_h)
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


def pil_text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    if not text:
        return 0.0
    left, _, right, _ = draw.textbbox((0, 0), text, font=font)
    return float(right - left)


def fit_pil_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: float) -> str:
    text = normalize_text(text)
    if pil_text_width(draw, text, font) <= max_width:
        return text
    suffix = "..."
    candidate = text
    while candidate and pil_text_width(draw, candidate + suffix, font) > max_width:
        candidate = candidate[:-1]
    return (candidate.rstrip() + suffix) if candidate else suffix


def wrap_pil_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: float) -> list[str]:
    words = normalize_text(text).split(" ")
    if not words or words == [""]:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if pil_text_width(draw, trial, font) <= max_width:
            current = trial
        else:
            lines.append(current)
            if pil_text_width(draw, word, font) <= max_width:
                current = word
            else:
                current = fit_pil_text(draw, word, font, max_width)
    lines.append(current)
    return lines


def draw_png_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    max_width: int,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    leading: int = 22,
    max_lines: int | None = None,
) -> int:
    lines = wrap_pil_text(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        tail = " ".join(lines[max_lines - 1 :])
        lines = lines[: max_lines - 1] + [fit_pil_text(draw, tail, font, max_width)]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def png_section_title(
    draw: ImageDraw.ImageDraw,
    title: str,
    x: int,
    y: int,
    width: int,
    accent: tuple[int, int, int],
    title_font: ImageFont.ImageFont,
) -> int:
    draw.line((x, y, x + width, y), fill=accent, width=3)
    draw.text((x, y + 8), title.upper(), font=title_font, fill=(0, 0, 0))
    return y + 38


def draw_png_bullets(
    draw: ImageDraw.ImageDraw,
    bullets: list[str],
    x: int,
    y: int,
    max_width: int,
    accent: tuple[int, int, int],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_items: int = 3,
    max_lines_per_item: int = 2,
    leading: int = 22,
) -> int:
    text_x = x + 14
    text_width = max_width - 14
    for bullet in bullets[:max_items]:
        lines = wrap_pil_text(draw, bullet, font, text_width)
        if len(lines) > max_lines_per_item:
            tail = " ".join(lines[max_lines_per_item - 1 :])
            lines = lines[: max_lines_per_item - 1] + [fit_pil_text(draw, tail, font, text_width)]
        draw.ellipse((x, y + 8, x + 8, y + 16), fill=accent)
        for line in lines:
            draw.text((text_x, y), line, font=font, fill=fill)
            y += leading
        y += 2
    return y


def draw_png_resume(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, height: int) -> None:
    accent = mix["accent"]
    text_color = mix["text"]
    margin = 54
    content_w = width - margin * 2
    bottom_safe = height - 54
    body_font = font_for(16)
    section_font = font_for(20, bold=True)

    # Header area
    draw.text((margin, 54), profile.person_name.upper(), fill=text_color, font=font_for(44, bold=True))
    intro_x = 380
    intro_w = width - margin - intro_x
    intro_y = 70
    intro_y = draw_png_wrapped(
        draw,
        role_intro(profile),
        intro_x,
        intro_y,
        intro_w,
        body_font,
        text_color,
        leading=22,
        max_lines=5,
    )
    contact_line_y = max(148, intro_y + 4)
    draw.line((margin, contact_line_y, width - margin, contact_line_y), fill=accent, width=3)

    # Contact row
    contacts = [profile.website, profile.email, profile.linkedin, profile.phone]
    contact_y = contact_line_y + 14
    col_w = content_w // 4
    small_font = font_for(14)
    for idx, item in enumerate(contacts):
        x = margin + idx * col_w
        draw.text((x, contact_y), fit_pil_text(draw, item, small_font, col_w - 12), fill=text_color, font=small_font)

    y = contact_y + 38
    y = png_section_title(draw, "Experience", margin, y, content_w, accent, section_font)
    year_col = 132
    for exp in profile.experience[:3]:
        if y > bottom_safe - 560:
            break
        draw.text((margin, y), fit_pil_text(draw, exp.period.replace(" - ", "–"), font_for(15, bold=True), year_col - 10), fill=text_color, font=font_for(15, bold=True))
        draw.text(
            (margin + year_col, y),
            fit_pil_text(draw, exp.title, font_for(17, bold=True), content_w - year_col - 6),
            fill=text_color,
            font=font_for(17, bold=True),
        )
        y += 24
        draw.text(
            (margin + year_col, y),
            fit_pil_text(draw, f"{exp.company}, {exp.location}", font_for(15), content_w - year_col - 6),
            fill=text_color,
            font=font_for(15),
        )
        y += 22
        y = draw_png_bullets(
            draw,
            exp.bullets,
            margin + year_col,
            y,
            content_w - year_col,
            accent,
            body_font,
            text_color,
            max_items=3,
            max_lines_per_item=2,
            leading=21,
        )
        draw.line((margin + year_col, y + 2, margin + content_w, y + 2), fill=(220, 220, 220), width=1)
        y += 4

    y = png_section_title(draw, "Technology", margin, y, content_w, accent, section_font)
    name_x, desc_x = margin, margin + 236
    for name, desc in technology_rows(profile):
        if y > bottom_safe - 320:
            break
        draw.text((name_x, y), fit_pil_text(draw, name, font_for(15, bold=True), 220), fill=text_color, font=font_for(15, bold=True))
        y = draw_png_wrapped(draw, desc, desc_x, y, content_w - (desc_x - margin), body_font, text_color, leading=21, max_lines=2)
        y += 2

    col_gap = 24
    col_w = (content_w - col_gap) // 2
    left_x = margin
    right_x = left_x + col_w + col_gap

    y_left = png_section_title(draw, "Leadership", left_x, y, col_w, accent, section_font)
    leadership = [
        f"Led initiatives in {profile.core_skills[0].lower()} and {profile.core_skills[3].lower()}.",
        f"Mentored teams on {profile.tools[0]}, {profile.tools[1]}, and delivery standards.",
    ]
    y_left = draw_png_bullets(
        draw,
        leadership,
        left_x,
        y_left,
        col_w,
        accent,
        body_font,
        text_color,
        max_items=2,
        max_lines_per_item=2,
        leading=21,
    )

    y_right = png_section_title(draw, "Project highlights", right_x, y, col_w, accent, section_font)
    for pr in profile.projects[:2]:
        draw.text((right_x, y_right), fit_pil_text(draw, pr.name, font_for(15, bold=True), col_w), fill=text_color, font=font_for(15, bold=True))
        y_right += 22
        y_right = draw_png_wrapped(draw, pr.details, right_x, y_right, col_w, body_font, text_color, leading=21, max_lines=2)
        y_right += 2

    y = max(y_left, y_right) + 2
    y = png_section_title(draw, "Education and Language", margin, y, content_w, accent, section_font)
    edu_x = margin
    lang_x = margin + int(content_w * 0.62)
    for edu in profile.education[:2]:
        draw.text((edu_x, y), fit_pil_text(draw, edu.period.replace(" - ", "–"), font_for(14, bold=True), 100), fill=text_color, font=font_for(14, bold=True))
        draw.text((edu_x + 110, y), fit_pil_text(draw, edu.degree, font_for(15, bold=True), 360), fill=text_color, font=font_for(15, bold=True))
        y += 22
        draw.text((edu_x + 110, y), fit_pil_text(draw, edu.school, font_for(14), 360), fill=text_color, font=font_for(14))
        y += 21

    ly = y - 86
    draw.text((lang_x, ly), "Languages", fill=text_color, font=font_for(15, bold=True))
    ly += 24
    for lang in profile.languages[:3]:
        draw.text((lang_x, ly), fit_pil_text(draw, lang, font_for(14), width - lang_x - margin), fill=text_color, font=font_for(14))
        ly += 22


def generate_png(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "preview.png"
    mix = color_mix(profile.slug)

    width = 1240
    height = 1754
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    draw_png_resume(draw, profile, mix, width, height)

    image.save(out_file, format="PNG", optimize=True)
    return out_file


def draw_marketing_variant_pdf(profile: RoleProfile, mix: dict[str, tuple[int, int, int]], out_file: Path) -> None:
    page_w, page_h = A4
    c = canvas.Canvas(str(out_file), pagesize=A4)
    c.setTitle(f"{profile.role_title} A4 Light Resume Template")

    accent = mix["accent"]
    text = mix["text"]
    m = 26
    sidebar_w = 176
    right_x = m + sidebar_w + 22
    right_w = page_w - right_x - m

    # Main frame
    c.setFillColor(Color(1, 1, 1))
    c.rect(m, m, page_w - m * 2, page_h - m * 2, fill=1, stroke=0)
    c.setFillColor(Color(0.965, 0.972, 0.985))
    c.rect(m, m, sidebar_w, page_h - m * 2, fill=1, stroke=0)
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.2)
    c.line(m + sidebar_w, m, m + sidebar_w, page_h - m)

    # Header (right)
    hy = page_h - 50
    c.setFillColor(to_pdf_color(text))
    c.setFont("Helvetica-Bold", 25)
    c.drawString(right_x, hy, profile.person_name)
    c.setFont("Helvetica", 11.6)
    c.drawString(right_x, hy - 14, "Marketing Specialist")
    c.setStrokeColor(to_pdf_color(accent))
    c.line(right_x, hy - 22, right_x + right_w, hy - 22)

    # Sidebar content
    sy = page_h - 62
    sy = pdf_section_title(c, m + 12, sy, sidebar_w - 24, "Personal details", accent)
    c.setFont("Helvetica-Bold", 8.3)
    labels = ["Name", "Address", "Phone", "Email", "Website", "LinkedIn"]
    values = [profile.person_name, profile.location, profile.phone, profile.email, profile.website, profile.linkedin]
    for label, value in zip(labels, values):
        c.drawString(m + 12, sy, label)
        sy = draw_pdf_wrapped(
            c,
            m + 12,
            sy - 10,
            value,
            sidebar_w - 24,
            font_name="Helvetica",
            font_size=8.1,
            leading=9.3,
            max_lines=2,
        )
        sy -= 4

    sy = pdf_section_title(c, m + 12, sy, sidebar_w - 24, "Core skills", accent)
    sy = draw_pdf_bullets(
        c,
        m + 12,
        sy,
        profile.core_skills[:6],
        sidebar_w - 24,
        accent,
        max_items=6,
        max_lines_per_item=1,
        font_size=8.0,
        leading=9.0,
    )

    sy = pdf_section_title(c, m + 12, sy, sidebar_w - 24, "Success highlights", accent)
    sy = draw_pdf_bullets(
        c,
        m + 12,
        sy,
        marketing_success_highlights(profile),
        sidebar_w - 24,
        accent,
        max_items=3,
        max_lines_per_item=2,
        font_size=7.9,
        leading=8.9,
    )

    sy = pdf_section_title(c, m + 12, sy, sidebar_w - 24, "Languages", accent)
    c.setFont("Helvetica", 8.0)
    for lang in profile.languages[:3]:
        c.drawString(m + 12, sy, fit_pdf_text(lang, "Helvetica", 8.0, sidebar_w - 24))
        sy -= 10

    # Right column content
    y = hy - 32
    y = pdf_section_title(c, right_x, y, right_w, "Profile", accent)
    y = draw_pdf_wrapped(
        c,
        right_x,
        y,
        profile.summary,
        right_w,
        font_name="Helvetica",
        font_size=9.1,
        leading=10.8,
        max_lines=6,
    )

    y -= 4
    y = pdf_section_title(c, right_x, y, right_w, "Work experience", accent)
    year_x = right_x
    tl_x = right_x + 100
    c.setStrokeColor(Color(0.70, 0.74, 0.79))
    c.setLineWidth(0.7)
    c.line(tl_x, y + 8, tl_x, y - 236)

    for exp in profile.experience[:2]:
        c.setFillColor(to_pdf_color(text))
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(year_x, y, fit_pdf_text(exp.period.replace(" - ", " - "), "Helvetica-Bold", 8.6, 92))
        c.setFillColor(to_pdf_color(accent))
        c.circle(tl_x, y + 2.2, 1.9, stroke=0, fill=1)
        c.setFillColor(to_pdf_color(text))
        c.setFont("Helvetica-Bold", 8.9)
        c.drawString(tl_x + 10, y, fit_pdf_text(exp.title, "Helvetica-Bold", 8.9, right_w - 114))
        y -= 10
        c.setFont("Helvetica-Oblique", 8.2)
        c.drawString(tl_x + 10, y, fit_pdf_text(f"{exp.company}, {exp.location}", "Helvetica-Oblique", 8.2, right_w - 114))
        y -= 10
        y = draw_pdf_bullets(
            c,
            tl_x + 10,
            y,
            exp.bullets,
            right_w - 114,
            accent,
            max_items=3,
            max_lines_per_item=3,
            font_size=8.2,
            leading=9.7,
        )
        y -= 2

    y = pdf_section_title(c, right_x, y, right_w, "Skills in practice", accent)
    for skill_name, skill_desc in marketing_skill_descriptions(profile):
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(right_x, y, fit_pdf_text(skill_name, "Helvetica-Bold", 8.6, 118))
        y = draw_pdf_wrapped(
            c,
            right_x + 122,
            y,
            skill_desc,
            right_w - 122,
            font_name="Helvetica",
            font_size=8.1,
            leading=9.3,
            max_lines=2,
        )
        y -= 2

    y = pdf_section_title(c, right_x, y, right_w, "Education and certifications", accent)
    for edu in profile.education[:2]:
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(right_x, y, fit_pdf_text(edu.degree, "Helvetica-Bold", 8.6, right_w - 132))
        c.setFont("Helvetica", 8.0)
        c.drawRightString(right_x + right_w, y, fit_pdf_text(edu.period, "Helvetica", 8.0, 128))
        y -= 10
        c.setFont("Helvetica-Oblique", 7.9)
        c.drawString(right_x, y, fit_pdf_text(edu.school, "Helvetica-Oblique", 7.9, right_w))
        y -= 10

    y -= 1
    y = pdf_section_title(c, right_x, y, right_w, "Tools", accent)
    y = draw_pdf_wrapped(
        c,
        right_x,
        y,
        ", ".join(profile.tools[:12]),
        right_w,
        font_name="Helvetica",
        font_size=8.2,
        leading=9.5,
        max_lines=4,
    )

    c.showPage()
    c.save()


def draw_marketing_variant_png(profile: RoleProfile, mix: dict[str, tuple[int, int, int]], out_file: Path) -> None:
    width, height = 1240, 1754
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    accent = mix["accent"]
    text = mix["text"]
    m = 54
    sidebar_w = 306
    right_x = m + sidebar_w + 30
    right_w = width - right_x - m

    # Canvas + sidebar
    draw.rectangle((m, m, width - m, height - m), fill=(255, 255, 255), outline=(224, 228, 235), width=1)
    draw.rectangle((m, m, m + sidebar_w, height - m), fill=(246, 249, 253))
    draw.line((m + sidebar_w, m, m + sidebar_w, height - m), fill=accent, width=3)

    # Header
    draw.text((right_x, 86), profile.person_name, fill=text, font=font_for(50, bold=True))
    draw.text((right_x, 142), "Marketing Specialist", fill=text, font=font_for(24))
    draw.line((right_x, 180, right_x + right_w, 180), fill=accent, width=3)

    # Sidebar
    section_font = font_for(21, bold=True)
    body_font = font_for(16)
    y = 108
    y = png_section_title(draw, "Personal details", m + 18, y, sidebar_w - 36, accent, section_font)
    labels = ["Name", "Address", "Phone", "Email", "Website", "LinkedIn"]
    values = [profile.person_name, profile.location, profile.phone, profile.email, profile.website, profile.linkedin]
    for label, value in zip(labels, values):
        draw.text((m + 18, y), label, fill=(70, 76, 86), font=font_for(14, bold=True))
        y += 21
        y = draw_png_wrapped(draw, value, m + 18, y, sidebar_w - 36, font_for(15), text, leading=20, max_lines=2)
        y += 4

    y = png_section_title(draw, "Core skills", m + 18, y, sidebar_w - 36, accent, section_font)
    y = draw_png_bullets(
        draw,
        profile.core_skills[:6],
        m + 18,
        y,
        sidebar_w - 36,
        accent,
        font_for(15),
        text,
        max_items=6,
        max_lines_per_item=2,
        leading=21,
    )

    y = png_section_title(draw, "Success highlights", m + 18, y, sidebar_w - 36, accent, section_font)
    y = draw_png_bullets(
        draw,
        marketing_success_highlights(profile),
        m + 18,
        y,
        sidebar_w - 36,
        accent,
        font_for(14),
        text,
        max_items=3,
        max_lines_per_item=3,
        leading=20,
    )

    y = png_section_title(draw, "Languages", m + 18, y, sidebar_w - 36, accent, section_font)
    for lang in profile.languages[:3]:
        draw.text((m + 18, y), fit_pil_text(draw, lang, font_for(15), sidebar_w - 36), fill=text, font=font_for(15))
        y += 21

    # Right content
    y = 200
    y = png_section_title(draw, "Profile", right_x, y, right_w, accent, section_font)
    y = draw_png_wrapped(draw, profile.summary, right_x, y, right_w, body_font, text, leading=22, max_lines=6)
    y += 6

    y = png_section_title(draw, "Work experience", right_x, y, right_w, accent, section_font)
    year_x = right_x
    tl_x = right_x + 142
    draw.line((tl_x, y + 8, tl_x, y + 600), fill=(181, 188, 198), width=2)
    for exp in profile.experience[:2]:
        draw.text((year_x, y), fit_pil_text(draw, exp.period.replace(" - ", " - "), font_for(15, bold=True), 132), fill=text, font=font_for(15, bold=True))
        draw.ellipse((tl_x - 4, y + 8, tl_x + 4, y + 16), fill=accent)
        draw.text((tl_x + 14, y), fit_pil_text(draw, exp.title, font_for(17, bold=True), right_w - 158), fill=text, font=font_for(17, bold=True))
        y += 22
        draw.text((tl_x + 14, y), fit_pil_text(draw, f"{exp.company}, {exp.location}", font_for(15), right_w - 158), fill=(55, 61, 71), font=font_for(15))
        y += 21
        y = draw_png_bullets(
            draw,
            exp.bullets,
            tl_x + 14,
            y,
            right_w - 158,
            accent,
            font_for(15),
            text,
            max_items=3,
            max_lines_per_item=3,
            leading=21,
        )
        y += 4

    y = png_section_title(draw, "Skills in practice", right_x, y, right_w, accent, section_font)
    for skill_name, skill_desc in marketing_skill_descriptions(profile):
        draw.text((right_x, y), fit_pil_text(draw, skill_name, font_for(15, bold=True), 154), fill=text, font=font_for(15, bold=True))
        y = draw_png_wrapped(
            draw,
            skill_desc,
            right_x + 160,
            y,
            right_w - 160,
            font_for(14),
            text,
            leading=20,
            max_lines=2,
        )
        y += 2

    y = png_section_title(draw, "Education and certifications", right_x, y, right_w, accent, section_font)
    for edu in profile.education[:2]:
        draw.text((right_x, y), fit_pil_text(draw, edu.degree, font_for(15, bold=True), right_w - 150), fill=text, font=font_for(15, bold=True))
        draw.text((right_x + right_w - 140, y), fit_pil_text(draw, edu.period, font_for(14), 140), fill=(70, 76, 86), font=font_for(14))
        y += 21
        draw.text((right_x, y), fit_pil_text(draw, edu.school, font_for(15), right_w), fill=(70, 76, 86), font=font_for(15))
        y += 21

    y = png_section_title(draw, "Tools", right_x, y, right_w, accent, section_font)
    _ = draw_png_wrapped(draw, ", ".join(profile.tools[:12]), right_x, y, right_w, font_for(15), text, leading=21, max_lines=4)

    image.save(out_file, format="PNG", optimize=True)


def generate_marketing_variant(profile: RoleProfile) -> tuple[Path, Path] | None:
    if profile.slug != "marketing-manager":
        return None
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "sample-a4-light.pdf"
    png_path = out_dir / "preview-a4-light.png"
    mix = color_mix(profile.slug)
    draw_marketing_variant_pdf(profile, mix, pdf_path)
    draw_marketing_variant_png(profile, mix, png_path)
    return pdf_path, png_path


def generate_manifest() -> Path:
    manifest_path = OUTPUT_ROOT / "manifest.json"
    required_sections = [
        "Header with role + contact details",
        "Professional summary",
        "Work experience with measurable achievements",
        "Education and qualifications",
        "Skills section",
        "Additional sections (projects/certifications/languages)",
    ]
    data: dict[str, dict[str, object]] = {}
    for profile in PROFILES:
        item: dict[str, object] = {
            "role_title": profile.role_title,
            "template": "classic-two-color-v1",
            "pdf": f"/assets/examples/{profile.slug}/sample.pdf",
            "preview": f"/assets/examples/{profile.slug}/preview.png",
            "colors": color_mix(profile.slug),
            "required_sections": required_sections,
        }
        if profile.slug == "marketing-manager":
            item["variants"] = {
                "a4_light": {
                    "label": "A4 light sidebar variant",
                    "pdf": "/assets/examples/marketing-manager/sample-a4-light.pdf",
                    "preview": "/assets/examples/marketing-manager/preview-a4-light.png",
                }
            }
        data[profile.slug] = item
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return manifest_path


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        generate_pdf(profile)
        generate_png(profile)
        generate_marketing_variant(profile)
    generate_manifest()
    print(f"Generated classic two-color assets for {len(PROFILES)} roles in {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
