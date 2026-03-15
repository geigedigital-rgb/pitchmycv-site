# Career Position Validation Instruction

This project generates SEO career pages automatically.

The system must reference the file:

career_positions_list.md

This file contains the list of target professions.

Before generating a new page, Cursor must check this file.

---

# RULES

1. Always check the profession list first.

2. Do not generate a page if a page already exists for that profession.

3. Each profession must have only ONE page.

4. The URL slug must follow this format:

/careers/[profession]-resume

Example:

/careers/data-analyst-resume
/careers/product-manager-resume
/careers/software-engineer-resume

---

# GENERATION LOGIC

When creating a new page:

1. Read the file:
career_positions_list.md

2. Find professions that do not yet have pages.

3. Generate a page only for professions without existing pages.

4. After generating a page, mark that profession as completed.

---

# DUPLICATE PREVENTION

Before creating a page:

Check if a page already exists with:

/careers/[profession]-resume

If it exists:

DO NOT generate another page.

Move to the next profession.

---

# SYSTEM GOAL

Ensure the system continuously generates new career pages without duplicates.

Each profession must produce exactly one SEO page.