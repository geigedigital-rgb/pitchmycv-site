# Cursor Instruction: Programmatic Career Resume SEO Page System

This document defines how to generate scalable SEO pages for a resume optimization platform.

The system is designed to generate career-specific resume pages that target real Google queries such as:

- data analyst resume
- product manager resume
- software engineer CV
- marketing manager resume
- nurse CV

These pages are not blog posts.

They are **career landing pages** designed to capture search intent and convert visitors into resume scans.

The system must generate high-quality pages that:

- rank in Google
- avoid thin content
- avoid AI spam patterns
- remain useful to real job seekers.

The pages must follow modern SEO best practices (2026).

---

# PRIMARY GOAL

Create helpful, profession-specific pages explaining how to create a resume for a specific job.

Each page should help a user understand:

- what recruiters expect
- how to structure their resume
- which skills matter
- how to pass ATS systems.

The page must convert readers into users who scan their resume using the platform.

---

# CORE PRINCIPLES

## Human-first content

All content must be written for real job seekers.

Avoid generic advice.

Each page must include profession-specific insights.

---

## Avoid thin content

Do not generate pages that only swap the profession name.

Each page must contain:

- profession-specific responsibilities
- role-specific skills
- realistic resume examples
- profession-specific hiring expectations.

Minimum content length:

900 words.

Preferred length:

1000–1500 words.

---

# STRUCTURAL CONSISTENCY

All pages follow the same structure.

However, the wording must be unique across pages.

Avoid repeating:

- intro patterns
- advice wording
- FAQ questions
- CTA phrases.

The structure must remain stable while wording varies.

---

# SEO URL STRUCTURE

The website must follow a clear hierarchical URL structure so that Google can easily understand page relationships and rank the site correctly.

All career pages must be located inside a dedicated directory.

Correct structure:

/careers/[profession]-resume

Examples:

/careers/data-analyst-resume  
/careers/product-manager-resume  
/careers/software-engineer-resume  
/careers/marketing-manager-resume  
/careers/nurse-resume  

This structure allows Google to understand that all pages belong to the **career resume guide category**.

The category page must exist:

/careers

The category page should list all profession resume guides.

Breadcrumb structure:

Home > Career Guides > [Profession] Resume

Example breadcrumb:

Home > Career Guides > Data Analyst Resume

Slug rules:

- use lowercase letters
- use hyphens instead of spaces
- avoid unnecessary words
- keep URLs short and readable

Examples of correct slugs:

data-analyst-resume  
product-manager-resume  
software-engineer-resume  

Incorrect examples:

resume-for-data-analyst-job-2024-best-guide  
how-to-write-a-data-analyst-resume-guide  

---

# PAGE STRUCTURE

## H1
[PROFESSION] Resume: Complete Guide

Example:

Data Analyst Resume: Complete Guide

---

## Intro (120–180 words)

Explain:

- what the profession does
- why resumes matter in this field
- why many candidates fail ATS screening.

Use different intro angles across pages.

Possible angles include:

- recruiter expectations
- competitive job market
- ATS rejection risks
- common resume mistakes.

Do not reuse identical intro wording across pages.

---

## SECTION 1 — What Recruiters Look for in a [PROFESSION] Resume

Explain:

- key skills recruiters expect
- typical responsibilities
- achievements hiring managers want to see.

Use profession-specific examples.

---

## SECTION 2 — Example Structure of a [PROFESSION] Resume

Explain the typical structure:

Summary  
Skills  
Experience  
Education  

Provide a realistic example of how these sections may look.

---

## SECTION 3 — Key Skills for a [PROFESSION] Resume

List 10–15 relevant skills.

Explain when and why to include them.

Avoid generic skill lists.

---

## SECTION 4 — Common Resume Mistakes for [PROFESSION]

Explain common mistakes such as:

- missing keywords
- vague experience descriptions
- weak achievements
- poor formatting.

Make the mistakes specific to the profession.

---

## SECTION 5 — How to Optimize Your Resume for ATS

Explain how to pass ATS systems.

Discuss:

- keyword matching
- section structure
- ATS parsing rules
- formatting best practices.

Use examples relevant to the profession.

---

## SECTION 6 — Resume Summary Examples

Provide 3 strong resume summary examples for this profession.

Each summary must be unique.

---

## SECTION 7 — FAQ

Write 4–5 questions such as:

- How long should a [PROFESSION] resume be?
- What skills should a [PROFESSION] include?
- What keywords should appear in a [PROFESSION] resume?
- How to optimize a resume for ATS?

Ensure questions vary across pages.

---

## ON THIS PAGE NAVIGATION (MANDATORY UX)

Each career page must include an **On this page** navigation block.

Design and behavior rules:

- The block must stay visible while the user scrolls the article (sticky behavior on desktop).
- The currently read section must be highlighted in the navigation (active state follows scroll position).
- Active item should use both visual highlight and accessibility state (`aria-current`).
- The navigation can be:
  - **multi-item** (recommended): 3–8 anchors for key sections, or
  - **single-item personalized block**: one custom anchor if the page format is intentionally short/special.
- Link labels should be human-readable and role-specific (not generic repeated labels).

If sticky behavior or active highlighting is missing, the page does not pass UX quality.

---

## DEPTH ADVICE BLOCKS (MANDATORY)

Each career page must include at least one short **deep guidance block** that makes the reader pause and evaluate their resume quality from a recruiter perspective.

Purpose:

- add human, practical coaching tone
- avoid generic AI-style filler
- increase perceived value and readability

Placement:

- near the beginning of the page (after intro or before first major section)

Format:

- short heading + 4–8 lines of plain language text
- use natural, non-robotic phrasing
- include a reflection prompt (for example: what the reader notices first, what a recruiter sees first, what message is clear in first seconds)

Variation rule:

- rotate patterns across pages so blocks are not repetitive
- do not repeat the exact same wording on many pages

Recommended pattern starters:

- **Thought experiment**
- **Quick exercise**
- **Try this**

Quality rule:

- block must contain role-relevant depth (not generic motivation text)
- block should help the user self-audit resume clarity in the first scan

---

# Upload zone  (MANDATORY COMPONENT)

Every career page must include a **Upload zone ** UPLOAD_BLOCK.md .

This form allows users to upload or paste their resume and run an ATS scan.

The form must appear after the introductory sections of the page.

The form title must dynamically include the profession.

Example:

Check your Data Analyst resume for job compatibility

Or:

Check your Product Manager resume against job requirements

The form label must clearly reference the profession.

Example form title pattern:

Check your [PROFESSION] resume against job requirements

Form functionality should include:

- resume upload
- resume paste input
- optional job description input
- scan / analyze button.

The form is the primary conversion element on the page.

---

# SEO ELEMENTS

Generate metadata for each page.

## Slug

Example:

/careers/data-analyst-resume

---

## Meta Title

50–60 characters.

Must contain the primary keyword naturally.

Example:

Data Analyst Resume Guide (Skills, Tips + Example)

---

## Meta Description

140–160 characters.

Clearly explain what the page provides.

Hard rule:

- every career page meta description must be between 140 and 160 characters (inclusive)
- if length is outside this range, the page fails QA and must be revised.

Example:

Learn how to write a strong data analyst resume. Discover key skills, recruiter expectations, and ATS optimization tips.

---

## Social Description Consistency

For every career detail page (`/careers/[profession]-resume`):

- `meta name="description"`, `meta property="og:description"`, and `meta name="twitter:description"` must use the same text
- this shared description must stay within 140–160 characters
- the wording should match search intent (ATS + recruiter/HR expectations + practical value).

For the category page (`/careers`):

- keep `description`, `og:description`, and `twitter:description` aligned in intent and wording
- include explicit ATS + HR/recruiter + mistakes + interview-chance framing.

---

## Canonical URL

Construct using base domain + slug.

---

## Career Category Intro Intent (`/careers`)

The category page intro must target search intent, not only generic copy.

Required intent signals in the intro paragraph:

- role-based resume guides / career resume guides
- what ATS checks first
- what HR/recruiters check first
- common mistakes that reduce interview chances
- practical examples or actionable tips.

The intro should remain human, concise, and readable (avoid robotic keyword stuffing).

---

## Breadcrumbs

Example:

Home > Career Guides > Data Analyst Resume

---

# IMAGE SEO

Each page may include 1–3 images.

Provide for each image:

- image purpose
- file name
- alt text
- caption.

Example:

File name  
data-analyst-resume-example.webp

Alt text  
Example layout of a data analyst resume showing summary, skills, experience, and projects.

Alt text must:

- describe the image accurately
- match page context
- avoid keyword stuffing.

Technical image SEO rules:

- use SEO-friendly file names with lowercase + hyphens only (no colons or special symbols)
- prefer modern format for inline page images (`.webp`) with reasonable compression
- keep social preview images (`og:image`, `twitter:image`) in broadly compatible format (typically `.png`)
- include explicit `width` and `height` on `<img>` to reduce layout shift (CLS)

---

# INTERNAL LINKING

Each page should suggest 3–5 internal links.

Examples:

- related profession resume pages
- ATS guide
- resume checklist
- resume mistakes guide
- resume summary guide.

Links must be contextually relevant.

---

# STRUCTURED DATA SUPPORT

Ensure content can support:

- Article schema
- Breadcrumb schema
- FAQ schema.

Structured data must always match visible page content.

---

# DUPLICATION PREVENTION

Before generating content:

Review summaries of previously generated pages.

Avoid repeating:

- identical intro patterns
- identical CTA wording
- identical FAQ questions
- repeated example wording.

Rewrite sections if similarity is too high.

---

# CONTENT VARIATION STRATEGY

Rotate writing patterns across pages.

Vary:

- intro framing
- recruiter advice
- examples
- CTA language
- FAQ wording.

The structure must remain consistent but wording must differ.

---

# QUALITY GATE

Before finalizing the page, verify:

1. The page contains profession-specific advice.
2. The page exceeds 900 words.
3. The intro differs from existing pages.
4. FAQ questions differ from other pages.
5. CTA wording is not reused across many pages.
6. Image alt texts are descriptive.
7. SEO metadata fields exist.
8. Meta description length is 140–160 characters (inclusive).
9. `/careers` intro includes explicit ATS + HR/recruiter + mistakes + interview-chance intent signals.
10. `description`, `og:description`, and `twitter:description` are synchronized on career pages.

If any check fails, revise the page.

---

# OUTPUT ORDER

Return content in this order:

1. slug  
2. meta title  
3. meta description  
4. canonical URL  
5. breadcrumbs  
6. full page content  
7. image SEO suggestions  
8. internal link suggestions  
9. schema recommendations  
10. quality self-check summary

---

# SYSTEM OBJECTIVE

Generate scalable SEO career pages targeting queries like:

"[PROFESSION] resume"  
"[PROFESSION] CV"

The pages should:

- rank in Google
- avoid thin content
- provide genuine value
- convert readers into resume scans using the Upload zone .

This system must remain safe for long-term programmatic SEO.