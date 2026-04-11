# GEO Audit Report: Pitch My CV

**Audit Date:** 2026-04-11  
**URL:** https://pitchcv.app  
**Business Type:** SaaS / content-led marketing site for resume optimization  
**Pages in sitemap:** 43  
**Deep-dive pages:** `/`, `/careers/software-engineer-resume`, `/tools/ats-checker`, `/resume-keyword-optimization`, `/about`, `/contact`

---

## Executive Summary

**Overall GEO Score: 47/100 (Poor)**

Pitch My CV has a solid traditional SEO baseline: static SSR HTML, clean canonicals and metadata, a working `robots.txt`, a valid sitemap, and clean URLs. The GEO layer is much weaker. The site does not publish `llms.txt`, has minimal entity linking via `sameAs`, has weak off-site brand confirmation, and most key pages are not yet citation-ready for LLM retrieval.

The strongest content type is the role-specific career guide. Pages like `/careers/software-engineer-resume` are crawlable, structured, and useful. The weakest areas are trust pages (`/about`, `/contact`), author trust signals, and brand/entity verification outside the domain, which makes the site useful but not yet highly authoritative for systems like ChatGPT, Perplexity, and Gemini.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---:|---:|---:|
| AI Citability & Visibility | 47/100 | 25% | 11.8 |
| Brand Authority Signals | 18/100 | 20% | 3.6 |
| Content Quality & E-E-A-T | 44/100 | 20% | 8.8 |
| Technical Foundations | 80/100 | 15% | 12.0 |
| Structured Data | 61/100 | 10% | 6.1 |
| Platform Optimization | 46/100 | 10% | 4.6 |
| **Overall GEO Score** |  |  | **46.9/100** |

---

## Critical Issues

No critical issues were found in the current live state:

- the site serves SSR HTML;
- `robots.txt` does not block key AI crawlers;
- structured data are present;
- key pages return `200 OK`.

---

## High Priority Issues

1. **No `llms.txt` or `llms-full.txt`**
   - The tool returned `404` for `https://pitchcv.app/llms.txt`.
   - This is a direct GEO gap because AI crawlers are not given an explicit machine-readable page map.

2. **Weak entity graph**
   - The homepage contains only one `sameAs` link, pointing to Trustpilot.
   - No reliable confirmation was found for Wikipedia, Wikidata, LinkedIn company entity, GitHub organization, Product Hunt, or Crunchbase.
   - This leaves ChatGPT, Gemini, and Perplexity with very weak entity verification signals.

3. **Almost no author-level trust signals**
   - On article and career pages, `author` is defined as `Organization`, not `Person`.
   - There are no author pages, bios, credentials, `knowsAbout`, `worksFor`, or external profiles.
   - This materially hurts E-E-A-T and expert citability.

4. **Low citability on key commercial pages**
   - Homepage average citability: **25.2**
   - ATS tool page: **31.3**
   - Resume keyword guide: **30.5**
   - Most blocks are too short, too generic, or too marketing-led to be good self-contained answer blocks.

5. **No security headers on the live deployment**
   - `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy` were all absent.
   - This is likely a deployment issue, but it lowers the trust baseline.

---

## Medium Priority Issues

1. **`/about` and `/contact` are too thin**
   - `/about`: about 83 words
   - `/contact`: about 20 words
   - No founder/team data, address, company background, editorial standards, or proof points.

2. **Almost no outbound citations or references**
   - The checked article and career pages exposed `0` external links.
   - The content is useful, but it is not strongly supported by external sources or research references.

3. **Missing GEO-critical schema components**
   - No `WebSite + SearchAction`
   - No `Person` schema for authors
   - No `speakable`
   - `sameAs` coverage is minimal

4. **Schema strategy contains low-value legacy patterns**
   - `FAQPage` can still help AI semantics, but its Google rich result value is heavily restricted.
   - Upload widgets on many pages use `HowTo` microdata, which is now low-value for Google rich results.

5. **Brand mention layer is mostly unconfirmed**
   - Wikipedia and Wikidata are absent
   - Reddit brand signals were not found
   - LinkedIn company entity was not confirmed
   - Search surfaced a possible YouTube channel, but it could not be treated as a verified official asset

---

## Low Priority Issues

1. **Homepage H1 collapses poorly in raw text extraction**
   - The extracted H1 reads as `Match your resumeto any jobin seconds`.
   - This is fine visually, but parser-friendly DOM text could be cleaner.

2. **No trust schema on trust pages**
   - `/about` and `/contact` do not contain schema blocks.

3. **Limited depth in the content hub**
   - There are useful resource pages and a blog hub, but the topical authority layer is still shallow for a broader resume optimization entity.

---

## Category Deep Dives

### AI Citability & Visibility (47/100)

#### Strengths

- All major AI crawlers are effectively allowed through `robots.txt`.
- The sitemap is declared in `robots.txt`.
- Career guides are substantially more citable than the homepage and the ATS checker page.

#### Gaps

- `llms.txt` is fully absent.
- Commercial and utility pages contain very few self-contained 120-170 word answer blocks.
- The homepage FAQ is the strongest block type, but it is still not especially data-rich or authoritative.

#### Citability snapshots

| Page | Avg score | Blocks | Notes |
|---|---:|---:|---|
| `/` | 25.2 | 16 | Too many short review and CTA blocks |
| `/careers/software-engineer-resume` | 49.7 | 9 | Best content type on the site |
| `/tools/ats-checker` | 31.3 | 3 | Too thin for AI citation |
| `/resume-keyword-optimization` | 30.5 | 11 | Useful, but low in original data |

#### AI crawler access

`robots.txt`:

```txt
User-agent: *
Allow: /
Disallow: /scan
Sitemap: https://pitchcv.app/sitemap.xml
```

Result:

- GPTBot - allowed
- OAI-SearchBot - allowed by default
- ChatGPT-User - allowed by default
- ClaudeBot - allowed by default
- PerplexityBot - allowed by default
- CCBot / Google-Extended / Amazonbot / Applebot-Extended - allowed by default

#### Priority Actions

1. **[HIGH]** Publish `llms.txt` and `llms-full.txt` at the site root.
2. **[HIGH]** Rewrite homepage, tool, and article sections into answer-first blocks: question -> 40-70 word answer -> supporting bullets or tables.
3. **[MEDIUM]** Add more citation-ready passages with concrete numbers, timeframes, and examples.

---

### Brand Authority Signals (18/100)

#### What was found

- The homepage includes `Organization.sameAs`, but only one link is present.
- Wikipedia page: not confirmed.
- Wikidata entity: not confirmed.
- Reddit brand mentions: not confirmed.
- LinkedIn company entity: not confirmed.
- Search surfaced a possible YouTube channel, but it was not verifiable as an official brand asset from the site or schema.

#### Why this matters

The tool treats brand mentions as a separate major category because LLMs often rely on cross-platform confirmation, not only on-site content. Right now, Pitch My CV has very few external anchors, so the brand entity remains weak even though the site itself is technically accessible.

#### Priority Actions

1. **[HIGH]** Expand `sameAs` to real LinkedIn, YouTube, GitHub, Crunchbase, Product Hunt, or other verified brand profiles.
2. **[HIGH]** Build a stronger verified entity layer before expecting strong LLM trust.
3. **[MEDIUM]** Strengthen review and profile presence and connect it through schema.

---

### Content Quality & E-E-A-T (44/100)

#### Strengths

- Career pages contain practical, structured, human-readable advice.
- `datePublished` and `dateModified` exist on content pages.
- The content is SSR and readable without JavaScript.
- The contact page at least exposes working contact emails.

#### Gaps

- Almost all content is published by `Organization` rather than named experts.
- There are no author bios, credentials, editorial standards, or expert profiles.
- There is little first-hand data, research, or case-study style evidence.
- Articles contain no external citations.
- `/about` and `/contact` are not strong trust pages for AI systems.

#### E-E-A-T quick read

| Dimension | Score | Evidence |
|---|---:|---|
| Experience | 9/25 | Useful advice, but very little first-hand evidence or original data |
| Expertise | 12/25 | Role-specific content is strong, but there are no named experts |
| Authoritativeness | 8/25 | Weak external validation of both brand and authors |
| Trustworthiness | 15/25 | HTTPS, privacy, terms, and contact exist, but trust pages are thin |

#### Priority Actions

1. **[HIGH]** Introduce named authors and author pages for guides and articles.
2. **[HIGH]** Add external citations, benchmark sources, and case-based examples.
3. **[HIGH]** Expand `/about` and `/contact` with ownership, team, process, and editorial trust information.
4. **[MEDIUM]** Expose visible "last updated" stamps in body content, not only in JSON-LD.

---

### Technical Foundations (80/100)

#### Strengths

- Static HTML with a strong SSR baseline.
- `200 OK` on all representative pages.
- `robots.txt` and `sitemap.xml` are in place.
- Canonical, viewport, OG, Twitter, and `lang="en"` are present.
- URL structure is clean and human-readable.

#### Gaps

- Security headers are absent on the live domain.
- `llms.txt` is absent.
- IndexNow/Bing webmaster integration cannot be confirmed externally.

#### Technical notes

| Check | Status | Notes |
|---|---|---|
| SSR / crawlable HTML | Good | Core content is visible without JS |
| Robots.txt | Good | AI crawlers are not blocked |
| XML Sitemap | Good | 43 URLs discovered |
| Meta tags | Good | Title, description, canonical, OG, Twitter all present |
| Mobile baseline | Good | Viewport present, responsive layout patterns visible |
| Security headers | Poor | All major security headers missing |

#### Priority Actions

1. **[HIGH]** Configure security headers at the CDN/server layer.
2. **[HIGH]** Publish `llms.txt` and `llms-full.txt`.
3. **[MEDIUM]** Validate real-world Core Web Vitals with PSI or CrUX.

---

### Structured Data (61/100)

#### What already exists

- Homepage: `Organization`, `WebSite`, `WebPage`, `SoftwareApplication`, `FAQPage`, and review markup.
- Content pages: `Article`, `BreadcrumbList`, `FAQPage`, and `Organization`.
- `datePublished` and `dateModified` are present on most important content pages.

#### Main gaps

- `sameAs` contains only one link.
- No `WebSite + SearchAction`
- No `Person` schema for authors
- No `speakable`
- Trust pages have no schema
- Many pages use `HowTo` microdata around the upload widget, but this is now low-value

#### GEO-critical schema assessment

| Schema | Status | GEO Impact | Notes |
|---|---|---|---|
| Organization + sameAs | Partial | Critical | Only 1 `sameAs` link, weak entity graph |
| Person (author) | Missing | High | No editorial person layer |
| Article + dateModified | Partial | High | Dates exist, but `author` is `Organization` |
| speakable | Missing | Medium | No explicit voice/AI targeting |
| BreadcrumbList | Present | Low | Implemented well on content pages |
| WebSite + SearchAction | Missing | Low | Missed opportunity |

#### Priority Actions

1. **[HIGH]** Expand `Organization` schema with richer `sameAs`, `contactPoint`, `foundingDate`, and `description`.
2. **[HIGH]** Add `WebSite` with `SearchAction`.
3. **[HIGH]** Add `Person` schema and author linkage on content templates.
4. **[MEDIUM]** Add `speakable` to the strongest answer-first sections.
5. **[LOW]** Re-evaluate repeated `HowTo` markup around upload widgets.

---

### Platform Optimization (46/100)

#### Platform scores

| Platform | Score | Why |
|---|---:|---|
| Google AI Overviews | 60/100 | Good HTML structure and FAQ patterns, but weak sourcing and answer-target depth |
| ChatGPT Web Search | 38/100 | Crawler access is fine, but entity recognition and author trust are weak |
| Perplexity AI | 33/100 | Weak community and external validation signals |
| Google Gemini | 52/100 | Some long-form content and schema, but weak ecosystem and knowledge graph signals |
| Bing Copilot | 45/100 | Structured content exists, but LinkedIn and Microsoft ecosystem signals are missing |

**Platform Readiness Average: 46/100**

#### Cross-platform synergies

1. **Expand `sameAs` and verified external profiles** - helps ChatGPT, Gemini, Bing, and partly Perplexity.
2. **Add named authors and bios** - helps Google AIO, ChatGPT, and Gemini.
3. **Publish `llms.txt` and improve answer blocks** - helps LLM retrieval systems across platforms.

#### Priority Actions

1. **[HIGH]** Build the entity layer with verified external profiles and schema linkage.
2. **[HIGH]** Rewrite key landing and article sections for answer-first extraction.
3. **[MEDIUM]** Add reusable definition, comparison, and checklist blocks on commercial pages.

---

## Quick Wins

1. Publish `llms.txt` and `llms-full.txt` at the site root. Drafts are already included in this folder.
2. Add `WebSite + SearchAction` and expand `Organization.sameAs`.
3. Introduce named authors and author bio patterns in content templates.
4. Strengthen `/about` and `/contact` with real company and trust details.
5. Rewrite homepage, tool, and article sections into more citation-ready answer blocks.

---

## Execution Roadmap

### Phase 1 - Entity and machine-readable layer

- [ ] Publish `llms.txt` and `llms-full.txt`
- [ ] Add `SearchAction` to the homepage schema
- [ ] Expand `Organization.sameAs` to real external profiles
- [ ] Add `contactPoint` and richer organization metadata

### Phase 2 - E-E-A-T hardening

- [ ] Add named authors to guides and articles
- [ ] Create author bio blocks or author pages
- [ ] Expand `/about` and `/contact`
- [ ] Show visible "updated" dates in body content

### Phase 3 - Citability uplift

- [ ] Rewrite homepage FAQ and core commercial copy into concise answer blocks
- [ ] Add data-backed examples and comparisons to articles
- [ ] Improve explanatory content on tool pages

### Phase 4 - Deployment trust and off-site authority

- [ ] Configure security headers at the server or CDN layer
- [ ] Confirm real external profiles and connect them through schema
- [ ] Build off-site brand presence where AI systems look for entity proof

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| `https://pitchcv.app/` | Match your resume to any job in seconds | low citability, no llms, weak sameAs, no security headers |
| `https://pitchcv.app/careers/software-engineer-resume` | Software Engineer Resume Guide: ATS, Skills + Examples | no Person author, no external citations, partial schema |
| `https://pitchcv.app/tools/ats-checker` | Free ATS Resume Checker & Scanner | thin content, low citability, weak schema |
| `https://pitchcv.app/resume-keyword-optimization` | Resume Keyword Optimization Guide | no Person author, weak originality signals, no external citations |
| `https://pitchcv.app/about` | About Pitch My CV | thin trust page, no schema, little company depth |
| `https://pitchcv.app/contact` | Contact Pitch My CV | ultra-thin trust page, no schema, no entity reinforcement |

---

## Companion Files

- Recommended `llms.txt`: `./llms.txt`
- Recommended `llms-full.txt`: `./llms-full.txt`
- Raw artifacts: `./artifacts/*.json`
