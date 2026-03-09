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
            "and lifecycle programs. Builds measurable funnel systems and aligns marketing execution with "
            "sales pipeline and revenue targets."
        ),
        core_skills=["Demand Generation", "Campaign Planning", "Funnel Analytics", "Content Strategy", "Team Leadership", "Budget Ownership"],
        tools=["GA4", "HubSpot", "Salesforce", "Google Ads", "Meta Ads", "Looker Studio", "Semrush", "Ahrefs"],
        experience=[
            ExperienceItem(
                period="2021 - Present",
                title="Marketing Manager",
                company="BrightMint",
                location="Warsaw",
                bullets=[
                    "Scaled MQL pipeline by 34% through segmented campaigns and channel testing.",
                    "Improved paid media ROAS from 2.1x to 3.3x in two quarters.",
                    "Built monthly funnel review process shared with GTM leadership.",
                ],
            ),
            ExperienceItem(
                period="2017 - 2021",
                title="Growth Specialist",
                company="NovaRetail",
                location="Krakow",
                bullets=[
                    "Increased non-brand organic traffic by 52% across regional content hubs.",
                    "Designed lifecycle nurture series that lifted SQL conversion by 14%.",
                    "Collaborated with sales to map campaign influence to closed-won opportunities.",
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


def pdf_section_title(c: canvas.Canvas, x: float, y: float, width: float, title: str, accent: tuple[int, int, int]) -> float:
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.0)
    c.line(x, y, x + width, y)
    c.setFont("Helvetica-Bold", 10.2)
    c.setFillColor(Color(0, 0, 0))
    c.drawString(x, y - 11, title.upper())
    return y - 20


def pdf_paragraph(c: canvas.Canvas, x: float, y: float, text: str, max_chars: int, size: float = 8.5, leading: float = 10.5) -> float:
    c.setFont("Helvetica", size)
    for line in wrap_words(text, max_chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def pdf_bullet_lines(
    c: canvas.Canvas,
    x: float,
    y: float,
    bullets: list[str],
    max_chars: int,
    accent: tuple[int, int, int],
    size: float = 8.2,
    leading: float = 10.0,
) -> float:
    for bullet in bullets:
        lines = wrap_words(bullet, max_chars)
        c.setFillColor(to_pdf_color(accent))
        c.circle(x + 2.5, y + 2.4, 1.7, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica", size)
        c.drawString(x + 8, y, lines[0])
        y -= leading
        for line in lines[1:]:
            c.drawString(x + 8, y, line)
            y -= leading
        y -= 1
    return y


def role_intro(profile: RoleProfile) -> str:
    return (
        f"{profile.role_title} with strong hands-on delivery across cross-functional teams. "
        f"{profile.summary}"
    )


def technology_rows(profile: RoleProfile) -> list[tuple[str, str]]:
    return [
        (profile.core_skills[0], f"Strong execution in {profile.core_skills[0].lower()} and {profile.core_skills[1].lower()}."),
        (profile.core_skills[2], f"Applied in complex projects with measurable results in {profile.role_title.lower()} roles."),
        ("Tooling", ", ".join(profile.tools[:6])),
        ("Certifications", ", ".join(profile.certifications[:2])),
    ]


def draw_pdf_resume(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], page_w: float, page_h: float) -> None:
    accent = mix["accent"]
    text = mix["text"]
    c.setFillColor(to_pdf_color(text))

    # Header
    c.setFont("Helvetica-Bold", 26)
    c.drawString(34, page_h - 40, profile.person_name.upper())
    intro_x = 210
    c.setFont("Helvetica", 9.5)
    intro_y = page_h - 29
    for line in wrap_words(role_intro(profile), 69):
        c.drawString(intro_x, intro_y, line)
        intro_y -= 11

    # Contact row
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.0)
    c.line(34, page_h - 74, page_w - 34, page_h - 74)
    c.setFont("Helvetica", 8.4)
    contact_items = [profile.website, profile.email, profile.linkedin, profile.phone]
    cx = 34
    for item in contact_items:
        c.drawString(cx, page_h - 89, item)
        cx += 135

    y = page_h - 108

    # Experience
    y = pdf_section_title(c, 34, y, page_w - 68, "Experience", accent)
    year_col = 88
    for exp in profile.experience[:3]:
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(34, y, exp.period.replace(" - ", "–"))
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(34 + year_col, y, exp.title)
        y -= 10
        c.setFont("Helvetica-Oblique", 8.2)
        c.drawString(34 + year_col, y, f"{exp.company}, {exp.location}")
        y -= 10
        y = pdf_bullet_lines(c, 34 + year_col, y, exp.bullets[:3], 72, accent, size=8.0, leading=9.4)
        y -= 2

    # Technology / core stack
    y = pdf_section_title(c, 34, y, page_w - 68, "Technology", accent)
    c.setFont("Helvetica-Bold", 8.7)
    tx_name = 34
    tx_desc = 170
    for name, desc in technology_rows(profile):
        c.drawString(tx_name, y, name)
        c.setFont("Helvetica", 8.3)
        for line in wrap_words(desc, 75):
            c.drawString(tx_desc, y, line)
            y -= 9
        y -= 2
        c.setFont("Helvetica-Bold", 8.7)

    # Two column section
    col_gap = 16
    col_w = (page_w - 68 - col_gap) / 2
    left_x = 34
    right_x = 34 + col_w + col_gap
    y -= 1
    y_left = pdf_section_title(c, left_x, y, col_w, "Leadership", accent)
    leadership = [
        f"Led initiatives in {profile.core_skills[0].lower()} and {profile.core_skills[3].lower()} for multi-team delivery.",
        f"Mentored peers on {profile.tools[0]}, {profile.tools[1]}, and reusable implementation standards.",
    ]
    y_left = pdf_bullet_lines(c, left_x, y_left, leadership, 45, accent, size=8.0, leading=9.3)

    y_right = pdf_section_title(c, right_x, y, col_w, "Project highlights", accent)
    for pr in profile.projects[:2]:
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(right_x, y_right, pr.name)
        y_right -= 9
        c.setFont("Helvetica", 8.0)
        for line in wrap_words(pr.details, 45):
            c.drawString(right_x, y_right, line)
            y_right -= 9
        y_right -= 2

    y = min(y_left, y_right) - 2

    # Education + Language
    y = pdf_section_title(c, 34, y, page_w - 68, "Education and Language", accent)
    edu_x = 34
    lang_x = 332
    ey = y
    for edu in profile.education[:2]:
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(edu_x, ey, edu.period.replace(" - ", "–"))
        c.drawString(edu_x + 58, ey, edu.degree)
        ey -= 9
        c.setFont("Helvetica-Oblique", 8.0)
        c.drawString(edu_x + 58, ey, edu.school)
        ey -= 8

    ly = y
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(lang_x, ly, "Languages")
    ly -= 10
    c.setFont("Helvetica", 8.2)
    for lang in profile.languages[:3]:
        c.drawString(lang_x, ly, lang)
        ly -= 9


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


def png_paragraph(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    max_chars: int,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int] = (0, 0, 0),
    leading: int = 24,
) -> int:
    for line in wrap_words(text, max_chars):
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
    return y + 40


def png_bullets(
    draw: ImageDraw.ImageDraw,
    bullets: list[str],
    x: int,
    y: int,
    max_chars: int,
    accent: tuple[int, int, int],
    font: ImageFont.ImageFont,
    leading: int = 22,
) -> int:
    for bullet in bullets:
        lines = wrap_words(bullet, max_chars)
        draw.ellipse((x, y + 8, x + 8, y + 16), fill=accent)
        draw.text((x + 14, y), lines[0], font=font, fill=(0, 0, 0))
        y += leading
        for line in lines[1:]:
            draw.text((x + 14, y), line, font=font, fill=(0, 0, 0))
            y += leading
        y += 2
    return y


def draw_png_resume(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, height: int) -> None:
    accent = mix["accent"]
    text_color = mix["text"]
    body_font = font_for(16)
    section_font = font_for(20, bold=True)

    # Header area
    draw.text((54, 54), profile.person_name.upper(), fill=text_color, font=font_for(44, bold=True))
    intro_y = 70
    for line in wrap_words(role_intro(profile), 67):
        draw.text((360, intro_y), line, fill=text_color, font=font_for(16))
        intro_y += 24
    draw.line((54, 148, width - 54, 148), fill=accent, width=3)

    # Contact row
    contacts = [profile.website, profile.email, profile.linkedin, profile.phone]
    cx = 54
    for item in contacts:
        draw.text((cx, 162), item, fill=text_color, font=font_for(14))
        cx += 285

    y = 206
    y = png_section_title(draw, "Experience", 54, y, width - 108, accent, section_font)
    year_col = 132
    for exp in profile.experience[:3]:
        draw.text((54, y), exp.period.replace(" - ", "–"), fill=text_color, font=font_for(15, bold=True))
        draw.text((54 + year_col, y), exp.title, fill=text_color, font=font_for(17, bold=True))
        y += 24
        draw.text((54 + year_col, y), f"{exp.company}, {exp.location}", fill=text_color, font=font_for(15))
        y += 22
        y = png_bullets(draw, exp.bullets[:3], 54 + year_col, y, 75, accent, body_font, leading=22)
        y += 4

    y = png_section_title(draw, "Technology", 54, y, width - 108, accent, section_font)
    name_x, desc_x = 54, 290
    for name, desc in technology_rows(profile):
        draw.text((name_x, y), name, fill=text_color, font=font_for(15, bold=True))
        y = png_paragraph(draw, desc, desc_x, y, 72, body_font, fill=text_color, leading=22)
        y += 2

    col_gap = 24
    col_w = (width - 108 - col_gap) // 2
    left_x = 54
    right_x = left_x + col_w + col_gap

    y_left = png_section_title(draw, "Leadership", left_x, y, col_w, accent, section_font)
    leadership = [
        f"Led initiatives in {profile.core_skills[0].lower()} and {profile.core_skills[3].lower()}.",
        f"Mentored teams on {profile.tools[0]}, {profile.tools[1]}, and delivery standards.",
    ]
    y_left = png_bullets(draw, leadership, left_x, y_left, 37, accent, body_font, leading=21)

    y_right = png_section_title(draw, "Project highlights", right_x, y, col_w, accent, section_font)
    for pr in profile.projects[:2]:
        draw.text((right_x, y_right), pr.name, fill=text_color, font=font_for(15, bold=True))
        y_right += 22
        y_right = png_paragraph(draw, pr.details, right_x, y_right, 37, body_font, fill=text_color, leading=21)
        y_right += 2

    y = max(y_left, y_right) + 2
    y = png_section_title(draw, "Education and Language", 54, y, width - 108, accent, section_font)
    edu_x = 54
    lang_x = 650
    for edu in profile.education[:2]:
        draw.text((edu_x, y), edu.period.replace(" - ", "–"), fill=text_color, font=font_for(14, bold=True))
        draw.text((edu_x + 110, y), edu.degree, fill=text_color, font=font_for(15, bold=True))
        y += 22
        draw.text((edu_x + 110, y), edu.school, fill=text_color, font=font_for(14))
        y += 21

    ly = y - 86
    draw.text((lang_x, ly), "Languages", fill=text_color, font=font_for(15, bold=True))
    ly += 24
    for lang in profile.languages[:3]:
        draw.text((lang_x, ly), lang, fill=text_color, font=font_for(14))
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
    data = {
        profile.slug: {
            "role_title": profile.role_title,
            "template": "classic-two-color-v1",
            "pdf": f"/assets/examples/{profile.slug}/sample.pdf",
            "preview": f"/assets/examples/{profile.slug}/preview.png",
            "colors": color_mix(profile.slug),
            "required_sections": required_sections,
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
    print(f"Generated classic two-color assets for {len(PROFILES)} roles in {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
