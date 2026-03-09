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


def pdf_section_title(c: canvas.Canvas, x: float, y: float, width: float, title: str, accent: tuple[int, int, int]) -> float:
    c.setStrokeColor(to_pdf_color(accent))
    c.setLineWidth(1.1)
    c.line(x, y, x + width, y)
    c.setFont("Helvetica-Bold", 9.3)
    c.setFillColor(Color(0, 0, 0))
    c.drawString(x, y - 10, title.upper())
    return y - 18


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


def draw_pdf_header(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], page_w: float, page_h: float, top_bar: bool) -> float:
    if top_bar:
        c.setFillColor(to_pdf_color(mix["primary"]))
        c.rect(0, page_h - 58, page_w, 58, fill=1, stroke=0)
        c.setFillColor(Color(1, 1, 1))
        c.setFont("Helvetica-Bold", 23)
        c.drawString(36, page_h - 36, profile.person_name.upper())
        c.setFont("Helvetica", 10)
        c.drawString(36, page_h - 51, profile.role_title)
        c.setFillColor(Color(0, 0, 0))
        y = page_h - 72
    else:
        c.setFillColor(to_pdf_color(mix["primary"]))
        c.rect(36, page_h - 70, page_w - 72, 4, fill=1, stroke=0)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 21)
        c.drawString(36, page_h - 44, profile.person_name.upper())
        c.setFont("Helvetica", 10.5)
        c.drawString(36, page_h - 59, profile.role_title)
        y = page_h - 82

    contacts = (
        f"{profile.location}  |  {profile.phone}  |  {profile.email}\n"
        f"{profile.website}  |  {profile.linkedin}"
    )
    c.setFont("Helvetica", 8.7)
    c.drawString(36, y, contacts.splitlines()[0])
    c.drawString(36, y - 11, contacts.splitlines()[1])
    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(0.8)
    c.line(36, y - 17, page_w - 36, y - 17)
    return y - 25


def draw_pdf_template_a(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float, page_h: float) -> None:
    left_x, left_w = 36, 160
    right_x, right_w = 212, 348
    bottom = 36

    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(1.1)
    c.line(left_x + left_w, bottom, left_x + left_w, start_y)

    y = start_y - 2
    y = pdf_section_title(c, left_x, y, left_w - 10, "Personal details", mix["primary"])
    c.setFont("Helvetica", 8.2)
    for row in [profile.location, profile.phone, profile.email, profile.website]:
        c.drawString(left_x, y, row)
        y -= 10

    y -= 3
    y = pdf_section_title(c, left_x, y, left_w - 10, "Core skills", mix["secondary"])
    y = pdf_bullet_lines(c, left_x, y, profile.core_skills[:6], 22, mix["secondary"])

    y -= 2
    y = pdf_section_title(c, left_x, y, left_w - 10, "Tools", mix["tertiary"])
    y = pdf_paragraph(c, left_x, y, ", ".join(profile.tools), 27, size=8.0, leading=9.5)

    y -= 2
    y = pdf_section_title(c, left_x, y, left_w - 10, "Languages", mix["quaternary"])
    for lang in profile.languages[:3]:
        c.setFont("Helvetica", 8.2)
        c.drawString(left_x, y, lang)
        y -= 10

    y -= 1
    y = pdf_section_title(c, left_x, y, left_w - 10, "Certifications", mix["primary"])
    y = pdf_bullet_lines(c, left_x, y, profile.certifications[:2], 24, mix["primary"], size=7.9, leading=9.3)

    y = start_y - 2
    y = pdf_section_title(c, right_x, y, right_w, "Professional summary", mix["primary"])
    y = pdf_paragraph(c, right_x, y, profile.summary, 80)

    y -= 2
    y = pdf_section_title(c, right_x, y, right_w, "Work experience", mix["secondary"])
    for idx, exp in enumerate(profile.experience[:2]):
        accent = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        c.setFont("Helvetica-Bold", 9.1)
        c.drawString(right_x, y, exp.title)
        c.setFont("Helvetica", 8.1)
        c.drawRightString(right_x + right_w, y, exp.period)
        y -= 10
        c.setFont("Helvetica-Oblique", 8.0)
        c.drawString(right_x, y, f"{exp.company}, {exp.location}")
        y -= 10
        y = pdf_bullet_lines(c, right_x, y, exp.bullets[:3], 71, mix[accent], size=8.0, leading=9.5)
        y -= 1

    y = pdf_section_title(c, right_x, y, right_w, "Education", mix["tertiary"])
    for edu in profile.education[:2]:
        c.setFont("Helvetica-Bold", 8.9)
        c.drawString(right_x, y, edu.degree)
        c.setFont("Helvetica", 8.1)
        c.drawRightString(right_x + right_w, y, edu.period)
        y -= 10
        c.setFont("Helvetica-Oblique", 8.0)
        c.drawString(right_x, y, edu.school)
        y -= 9
        y = pdf_paragraph(c, right_x, y, edu.details, 75, size=8.0, leading=9.3)
        y -= 1

    y = pdf_section_title(c, right_x, y, right_w, "Projects", mix["quaternary"])
    for pr in profile.projects[:2]:
        c.setFont("Helvetica-Bold", 8.8)
        c.drawString(right_x, y, pr.name)
        y -= 9
        y = pdf_paragraph(c, right_x, y, pr.details, 76, size=8.0, leading=9.2)
        y -= 1


def draw_pdf_template_b(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float, page_h: float) -> None:
    left_x, left_w = 36, 146
    right_x, right_w = 198, 362
    panel_top = page_h - 72
    panel_bottom = 42

    c.setFillColor(Color(0.97, 0.97, 0.97))
    c.rect(left_x, panel_bottom, left_w, panel_top - panel_bottom, fill=1, stroke=0)
    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(1.0)
    c.line(left_x + left_w, panel_bottom, left_x + left_w, panel_top)

    y = start_y - 2
    y = pdf_section_title(c, left_x + 8, y, left_w - 16, "Personal details", mix["primary"])
    c.setFont("Helvetica", 8.0)
    for row in [profile.location, profile.phone, profile.email, profile.linkedin]:
        c.drawString(left_x + 8, y, row)
        y -= 10

    y -= 2
    y = pdf_section_title(c, left_x + 8, y, left_w - 16, "Interests", mix["tertiary"])
    y = pdf_paragraph(c, left_x + 8, y, ", ".join(profile.interests), 21, size=7.9, leading=9.1)

    y -= 2
    y = pdf_section_title(c, left_x + 8, y, left_w - 16, "Skill level", mix["quaternary"])
    for idx, rate in enumerate(profile.skill_ratings[:5]):
        c.setFont("Helvetica", 7.9)
        c.drawString(left_x + 8, y, rate.name)
        dot_x = left_x + 82
        for j in range(5):
            color_key = ("primary", "secondary", "tertiary", "quaternary", "primary")[j]
            dot = mix[color_key] if j < rate.level else (220, 220, 220)
            c.setFillColor(to_pdf_color(dot))
            c.circle(dot_x + j * 10, y + 2, 2.2, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        y -= 11

    y_main = start_y - 2
    y_main = pdf_section_title(c, right_x, y_main, right_w, "Profile", mix["primary"])
    y_main = pdf_paragraph(c, right_x, y_main, profile.summary, 81)

    y_main -= 2
    y_main = pdf_section_title(c, right_x, y_main, right_w, "Work experience", mix["secondary"])
    timeline_x = right_x + 57
    c.setStrokeColor(to_pdf_color(mix["secondary"]))
    c.setLineWidth(0.9)
    c.line(timeline_x, y_main + 6, timeline_x, y_main - 170)
    for idx, exp in enumerate(profile.experience[:2]):
        accent = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        c.setFont("Helvetica", 8.0)
        c.drawString(right_x, y_main, exp.period)
        c.setFillColor(to_pdf_color(mix[accent]))
        c.circle(timeline_x, y_main + 2.5, 2.4, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 9.0)
        c.drawString(timeline_x + 12, y_main, exp.title)
        y_main -= 10
        c.setFont("Helvetica-Oblique", 7.9)
        c.drawString(timeline_x + 12, y_main, f"{exp.company}, {exp.location}")
        y_main -= 9
        y_main = pdf_bullet_lines(c, timeline_x + 12, y_main, exp.bullets[:3], 61, mix[accent], size=7.9, leading=9.1)
        y_main -= 2

    y_main = pdf_section_title(c, right_x, y_main, right_w, "Education and qualifications", mix["tertiary"])
    edu_x_line = right_x + 57
    c.setStrokeColor(to_pdf_color(mix["tertiary"]))
    c.line(edu_x_line, y_main + 6, edu_x_line, y_main - 85)
    for idx, edu in enumerate(profile.education[:2]):
        accent = ("tertiary", "quaternary")[idx % 2]
        c.setFont("Helvetica", 7.9)
        c.drawString(right_x, y_main, edu.period)
        c.setFillColor(to_pdf_color(mix[accent]))
        c.circle(edu_x_line, y_main + 2.3, 2.2, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 8.8)
        c.drawString(edu_x_line + 12, y_main, edu.degree)
        y_main -= 9
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(edu_x_line + 12, y_main, edu.school)
        y_main -= 9
        y_main = pdf_paragraph(c, edu_x_line + 12, y_main, edu.details, 60, size=7.8, leading=8.8)
        y_main -= 2

    y_main = pdf_section_title(c, right_x, y_main, right_w, "Projects and certifications", mix["quaternary"])
    for pr in profile.projects[:1]:
        c.setFont("Helvetica-Bold", 8.8)
        c.drawString(right_x, y_main, pr.name)
        y_main -= 9
        y_main = pdf_paragraph(c, right_x, y_main, pr.details, 79, size=7.9, leading=9.0)
    y_main = pdf_bullet_lines(c, right_x, y_main, profile.certifications[:2], 78, mix["quaternary"], size=7.8, leading=8.9)


def draw_pdf_template_c(c: canvas.Canvas, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], start_y: float, page_w: float) -> None:
    x_left = 36
    x_mid = 160
    x_text = 178
    x_right = page_w - 36

    y = start_y - 2
    y = pdf_section_title(c, x_left, y, x_right - x_left, "Personal details", mix["primary"])
    c.setFont("Helvetica-Bold", 8.1)
    labels = ["Name", "Address", "Phone", "Email", "Website", "LinkedIn"]
    values = [profile.person_name, profile.location, profile.phone, profile.email, profile.website, profile.linkedin]
    for label, value in zip(labels, values):
        c.drawString(x_left, y, label)
        c.setFont("Helvetica", 8.1)
        c.drawString(x_left + 92, y, value)
        c.setFont("Helvetica-Bold", 8.1)
        y -= 9

    y -= 2
    y = pdf_section_title(c, x_left, y, x_right - x_left, "Profile", mix["secondary"])
    y = pdf_paragraph(c, x_left, y, profile.summary, 109, size=8.2, leading=9.5)

    y -= 2
    y = pdf_section_title(c, x_left, y, x_right - x_left, "Work experience", mix["tertiary"])
    c.setStrokeColor(to_pdf_color(mix["tertiary"]))
    c.setLineWidth(0.9)
    timeline_top = y + 6
    c.line(x_mid, timeline_top, x_mid, timeline_top - 170)
    for idx, exp in enumerate(profile.experience[:2]):
        accent = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        c.setFont("Helvetica", 8.1)
        c.drawString(x_left, y, exp.period)
        c.setFillColor(to_pdf_color(mix[accent]))
        c.circle(x_mid, y + 2.2, 2.2, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 8.9)
        c.drawString(x_text, y, exp.title)
        y -= 9
        c.setFont("Helvetica-Oblique", 7.9)
        c.drawString(x_text, y, f"{exp.company}, {exp.location}")
        y -= 9
        y = pdf_bullet_lines(c, x_text, y, exp.bullets[:3], 67, mix[accent], size=7.9, leading=9.0)
        y -= 1

    y = pdf_section_title(c, x_left, y, x_right - x_left, "Education and qualifications", mix["quaternary"])
    c.setStrokeColor(to_pdf_color(mix["quaternary"]))
    c.line(x_mid, y + 6, x_mid, y - 82)
    for idx, edu in enumerate(profile.education[:2]):
        accent = ("quaternary", "primary")[idx % 2]
        c.setFont("Helvetica", 8.0)
        c.drawString(x_left, y, edu.period)
        c.setFillColor(to_pdf_color(mix[accent]))
        c.circle(x_mid, y + 2.2, 2.2, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        c.setFont("Helvetica-Bold", 8.8)
        c.drawString(x_text, y, edu.degree)
        y -= 9
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(x_text, y, edu.school)
        y -= 9
        y = pdf_paragraph(c, x_text, y, edu.details, 66, size=7.8, leading=8.8)
        y -= 1

    y = pdf_section_title(c, x_left, y, x_right - x_left, "Skills and additional information", mix["primary"])
    for idx, rate in enumerate(profile.skill_ratings[:5]):
        c.setFont("Helvetica-Bold", 8.1)
        c.drawString(x_left, y, rate.name)
        dot_x = x_left + 88
        for j in range(5):
            key = ("primary", "secondary", "tertiary", "quaternary", "primary")[j]
            dot = mix[key] if j < rate.level else (222, 222, 222)
            c.setFillColor(to_pdf_color(dot))
            c.circle(dot_x + j * 9, y + 2, 2.0, stroke=0, fill=1)
        c.setFillColor(Color(0, 0, 0))
        if idx < len(profile.languages):
            c.setFont("Helvetica", 7.8)
            c.drawString(x_left + 155, y, profile.languages[idx])
        y -= 10

    y -= 2
    c.setFont("Helvetica-Bold", 8.1)
    c.drawString(x_left, y, "Certifications")
    y -= 9
    y = pdf_bullet_lines(c, x_left, y, profile.certifications[:2], 46, mix["secondary"], size=7.8, leading=8.8)


def generate_pdf(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "sample.pdf"
    page_w, page_h = A4
    mix = color_mix(profile.slug)

    c = canvas.Canvas(str(out_file), pagesize=A4)
    c.setTitle(f"{profile.role_title} Resume Example")

    use_top_bar = profile.template == "B"
    start_y = draw_pdf_header(c, profile, mix, page_w, page_h, top_bar=use_top_bar)
    if profile.template == "A":
        draw_pdf_template_a(c, profile, mix, start_y, page_h)
    elif profile.template == "B":
        draw_pdf_template_b(c, profile, mix, start_y, page_h)
    else:
        draw_pdf_template_c(c, profile, mix, start_y, page_w)

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


def draw_png_header(
    draw: ImageDraw.ImageDraw,
    profile: RoleProfile,
    mix: dict[str, tuple[int, int, int]],
    width: int,
    top_bar: bool,
) -> int:
    if top_bar:
        draw.rectangle((0, 0, width, 92), fill=mix["primary"])
        draw.text((54, 20), profile.person_name.upper(), fill=(255, 255, 255), font=font_for(40, bold=True))
        draw.text((54, 62), profile.role_title, fill=(255, 255, 255), font=font_for(20))
        y = 116
    else:
        draw.rectangle((54, 54, width - 54, 62), fill=mix["primary"])
        draw.text((54, 78), profile.person_name.upper(), fill=(0, 0, 0), font=font_for(40, bold=True))
        draw.text((54, 124), profile.role_title, fill=(0, 0, 0), font=font_for(20))
        y = 156
    draw.text((54, y), f"{profile.location}  |  {profile.phone}  |  {profile.email}", fill=(0, 0, 0), font=font_for(16))
    draw.text((54, y + 24), f"{profile.website}  |  {profile.linkedin}", fill=(0, 0, 0), font=font_for(16))
    draw.line((54, y + 54, width - 54, y + 54), fill=mix["secondary"], width=2)
    return y + 74


def draw_png_template_a(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, height: int, start_y: int) -> None:
    left_x, left_w = 54, 300
    right_x, right_w = 388, width - 442
    body_font = font_for(16)
    section_font = font_for(18, bold=True)

    draw.line((left_x + left_w, start_y, left_x + left_w, height - 70), fill=mix["secondary"], width=3)

    y = start_y + 6
    y = png_section_title(draw, "Personal details", left_x, y, left_w - 20, mix["primary"], section_font)
    for row in [profile.location, profile.phone, profile.email, profile.website]:
        draw.text((left_x, y), row, fill=(0, 0, 0), font=body_font)
        y += 24

    y += 4
    y = png_section_title(draw, "Core skills", left_x, y, left_w - 20, mix["secondary"], section_font)
    y = png_bullets(draw, profile.core_skills[:6], left_x, y, 24, mix["secondary"], body_font, leading=21)

    y += 4
    y = png_section_title(draw, "Tools", left_x, y, left_w - 20, mix["tertiary"], section_font)
    y = png_paragraph(draw, ", ".join(profile.tools), left_x, y, 30, body_font, leading=21)

    y += 4
    y = png_section_title(draw, "Languages", left_x, y, left_w - 20, mix["quaternary"], section_font)
    for lang in profile.languages[:3]:
        draw.text((left_x, y), lang, fill=(0, 0, 0), font=body_font)
        y += 22

    yr = start_y + 6
    yr = png_section_title(draw, "Professional summary", right_x, yr, right_w, mix["primary"], section_font)
    yr = png_paragraph(draw, profile.summary, right_x, yr, 70, body_font, leading=22)

    yr += 5
    yr = png_section_title(draw, "Work experience", right_x, yr, right_w, mix["secondary"], section_font)
    for idx, exp in enumerate(profile.experience[:2]):
        key = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        draw.text((right_x, yr), exp.title, fill=(0, 0, 0), font=font_for(17, bold=True))
        draw.text((right_x + right_w - 170, yr), exp.period, fill=(0, 0, 0), font=font_for(15))
        yr += 21
        draw.text((right_x, yr), f"{exp.company}, {exp.location}", fill=(40, 40, 40), font=font_for(15))
        yr += 20
        yr = png_bullets(draw, exp.bullets[:3], right_x, yr, 64, mix[key], body_font, leading=21)
        yr += 3

    yr = png_section_title(draw, "Education", right_x, yr, right_w, mix["tertiary"], section_font)
    for edu in profile.education[:2]:
        draw.text((right_x, yr), edu.degree, fill=(0, 0, 0), font=font_for(17, bold=True))
        draw.text((right_x + right_w - 160, yr), edu.period, fill=(0, 0, 0), font=font_for(14))
        yr += 20
        draw.text((right_x, yr), edu.school, fill=(38, 38, 38), font=font_for(15))
        yr += 19
        yr = png_paragraph(draw, edu.details, right_x, yr, 68, body_font, leading=21)
        yr += 2

    yr = png_section_title(draw, "Projects", right_x, yr, right_w, mix["quaternary"], section_font)
    for pr in profile.projects[:2]:
        draw.text((right_x, yr), pr.name, fill=(0, 0, 0), font=font_for(16, bold=True))
        yr += 20
        yr = png_paragraph(draw, pr.details, right_x, yr, 68, body_font, leading=21)
        yr += 2


def draw_png_template_b(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, start_y: int) -> None:
    left_x, left_w = 54, 290
    right_x, right_w = 378, width - 432
    draw.rectangle((left_x, start_y, left_x + left_w, 1680), fill=(246, 246, 246))
    draw.line((left_x + left_w, start_y, left_x + left_w, 1680), fill=mix["secondary"], width=3)

    section_font = font_for(18, bold=True)
    body_font = font_for(16)

    y = start_y + 10
    y = png_section_title(draw, "Personal details", left_x + 12, y, left_w - 24, mix["primary"], section_font)
    for row in [profile.location, profile.phone, profile.email, profile.linkedin]:
        draw.text((left_x + 12, y), row, fill=(0, 0, 0), font=body_font)
        y += 24

    y += 6
    y = png_section_title(draw, "Interests", left_x + 12, y, left_w - 24, mix["tertiary"], section_font)
    y = png_paragraph(draw, ", ".join(profile.interests), left_x + 12, y, 23, body_font, leading=22)

    y += 6
    y = png_section_title(draw, "Skill level", left_x + 12, y, left_w - 24, mix["quaternary"], section_font)
    for rate in profile.skill_ratings[:5]:
        draw.text((left_x + 12, y), rate.name, fill=(0, 0, 0), font=font_for(15))
        dx = left_x + 136
        for j in range(5):
            color_key = ("primary", "secondary", "tertiary", "quaternary", "primary")[j]
            dot = mix[color_key] if j < rate.level else (222, 222, 222)
            dot_x = dx + j * 20
            draw.ellipse((dot_x, y + 6, dot_x + 8, y + 14), fill=dot)
        y += 24

    yr = start_y + 10
    yr = png_section_title(draw, "Profile", right_x, yr, right_w, mix["primary"], section_font)
    yr = png_paragraph(draw, profile.summary, right_x, yr, 71, body_font, leading=22)

    yr += 6
    yr = png_section_title(draw, "Work experience", right_x, yr, right_w, mix["secondary"], section_font)
    timeline_x = right_x + 92
    draw.line((timeline_x, yr, timeline_x, yr + 500), fill=mix["secondary"], width=2)
    for idx, exp in enumerate(profile.experience[:2]):
        key = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        draw.text((right_x, yr), exp.period, fill=(0, 0, 0), font=font_for(15))
        draw.ellipse((timeline_x - 4, yr + 8, timeline_x + 4, yr + 16), fill=mix[key])
        draw.text((timeline_x + 16, yr), exp.title, fill=(0, 0, 0), font=font_for(17, bold=True))
        yr += 21
        draw.text((timeline_x + 16, yr), f"{exp.company}, {exp.location}", fill=(35, 35, 35), font=font_for(15))
        yr += 20
        yr = png_bullets(draw, exp.bullets[:3], timeline_x + 16, yr, 56, mix[key], body_font, leading=21)
        yr += 4

    yr = png_section_title(draw, "Education", right_x, yr, right_w, mix["tertiary"], section_font)
    for idx, edu in enumerate(profile.education[:2]):
        key = ("tertiary", "quaternary")[idx % 2]
        draw.text((right_x, yr), edu.period, fill=(0, 0, 0), font=font_for(15))
        draw.ellipse((timeline_x - 4, yr + 8, timeline_x + 4, yr + 16), fill=mix[key])
        draw.text((timeline_x + 16, yr), edu.degree, fill=(0, 0, 0), font=font_for(16, bold=True))
        yr += 20
        draw.text((timeline_x + 16, yr), edu.school, fill=(40, 40, 40), font=font_for(15))
        yr += 19
        yr = png_paragraph(draw, edu.details, timeline_x + 16, yr, 55, body_font, leading=21)
        yr += 4

    yr = png_section_title(draw, "Projects and certifications", right_x, yr, right_w, mix["quaternary"], section_font)
    for pr in profile.projects[:1]:
        draw.text((right_x, yr), pr.name, fill=(0, 0, 0), font=font_for(16, bold=True))
        yr += 20
        yr = png_paragraph(draw, pr.details, right_x, yr, 70, body_font, leading=21)
    yr = png_bullets(draw, profile.certifications[:2], right_x, yr, 68, mix["quaternary"], body_font, leading=21)


def draw_png_template_c(draw: ImageDraw.ImageDraw, profile: RoleProfile, mix: dict[str, tuple[int, int, int]], width: int, start_y: int) -> None:
    section_font = font_for(18, bold=True)
    body_font = font_for(16)
    x_left = 54
    x_mid = 292
    x_text = 316
    x_right = width - 54
    y = start_y + 8

    y = png_section_title(draw, "Personal details", x_left, y, x_right - x_left, mix["primary"], section_font)
    labels = ["Name", "Address", "Phone", "Email", "Website", "LinkedIn"]
    values = [profile.person_name, profile.location, profile.phone, profile.email, profile.website, profile.linkedin]
    for label, value in zip(labels, values):
        draw.text((x_left, y), label, fill=(30, 30, 30), font=font_for(15, bold=True))
        draw.text((x_left + 140, y), value, fill=(0, 0, 0), font=body_font)
        y += 23

    y += 6
    y = png_section_title(draw, "Profile", x_left, y, x_right - x_left, mix["secondary"], section_font)
    y = png_paragraph(draw, profile.summary, x_left, y, 112, body_font, leading=22)

    y += 5
    y = png_section_title(draw, "Work experience", x_left, y, x_right - x_left, mix["tertiary"], section_font)
    draw.line((x_mid, y, x_mid, y + 460), fill=mix["tertiary"], width=2)
    for idx, exp in enumerate(profile.experience[:2]):
        key = ("primary", "secondary", "tertiary", "quaternary")[idx % 4]
        draw.text((x_left, y), exp.period, fill=(0, 0, 0), font=font_for(15))
        draw.ellipse((x_mid - 4, y + 8, x_mid + 4, y + 16), fill=mix[key])
        draw.text((x_text, y), exp.title, fill=(0, 0, 0), font=font_for(17, bold=True))
        y += 21
        draw.text((x_text, y), f"{exp.company}, {exp.location}", fill=(35, 35, 35), font=font_for(15))
        y += 20
        y = png_bullets(draw, exp.bullets[:3], x_text, y, 68, mix[key], body_font, leading=21)
        y += 4

    y = png_section_title(draw, "Education and qualifications", x_left, y, x_right - x_left, mix["quaternary"], section_font)
    draw.line((x_mid, y, x_mid, y + 220), fill=mix["quaternary"], width=2)
    for idx, edu in enumerate(profile.education[:2]):
        key = ("quaternary", "primary")[idx % 2]
        draw.text((x_left, y), edu.period, fill=(0, 0, 0), font=font_for(15))
        draw.ellipse((x_mid - 4, y + 8, x_mid + 4, y + 16), fill=mix[key])
        draw.text((x_text, y), edu.degree, fill=(0, 0, 0), font=font_for(16, bold=True))
        y += 20
        draw.text((x_text, y), edu.school, fill=(35, 35, 35), font=font_for(15))
        y += 19
        y = png_paragraph(draw, edu.details, x_text, y, 66, body_font, leading=21)
        y += 4

    y = png_section_title(draw, "Skills", x_left, y, x_right - x_left, mix["primary"], section_font)
    for idx, rate in enumerate(profile.skill_ratings[:5]):
        draw.text((x_left, y), rate.name, fill=(0, 0, 0), font=font_for(15, bold=True))
        dx = x_left + 150
        for j in range(5):
            key = ("primary", "secondary", "tertiary", "quaternary", "primary")[j]
            dot = mix[key] if j < rate.level else (220, 220, 220)
            draw.ellipse((dx + j * 22, y + 6, dx + j * 22 + 8, y + 14), fill=dot)
        if idx < len(profile.languages):
            draw.text((x_left + 290, y), profile.languages[idx], fill=(30, 30, 30), font=font_for(14))
        y += 24


def generate_png(profile: RoleProfile) -> Path:
    out_dir = OUTPUT_ROOT / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "preview.png"
    mix = color_mix(profile.slug)

    width = 1240
    height = 1754
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    top_bar = profile.template == "B"
    start_y = draw_png_header(draw, profile, mix, width, top_bar=top_bar)
    if profile.template == "A":
        draw_png_template_a(draw, profile, mix, width, height, start_y)
    elif profile.template == "B":
        draw_png_template_b(draw, profile, mix, width, start_y)
    else:
        draw_png_template_c(draw, profile, mix, width, start_y)

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
            "template": profile.template,
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
    print(f"Generated enriched assets for {len(PROFILES)} roles in {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
