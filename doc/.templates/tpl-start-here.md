<!--
LLM INSTRUCTION BLOCK
MOTIVATION: This is the Level 0 (30-second) onboarding document. It establishes the "Ubiquitous Language" (Domain-Driven Design) for the entire project.
CONTENTS: Executive summary, core domain dictionary, and high-level system context.
DO'S:
- DO strictly enforce the vocabulary defined here across all code, variables, and other documentation.
- DO keep descriptions brief. This is a map, not the territory.
DON'TS:
- DO NOT put implementation details, API endpoints, or sprint tasks here.
- DO NOT invent synonyms in the codebase (e.g., if this file says "Student", do not use "Pupil" in the code).
-->

# 🚀 Project Overview & Domain Dictionary

## 1. Executive Summary
[1-2 sentences explaining what this application is, who it is for, and the primary problem it solves.]

## 2. Ubiquitous Language (The Dictionary)
*To prevent translation errors between business and engineering, these terms MUST be used exactly as written in all code, database schemas, and discussions.*

*   **[Domain Entity 1]** (e.g., `StudentProfile`): [Definition. E.g., A local representation of a user, containing encrypted credentials.]
*   **[Domain Entity 2]** (e.g., `GradeDTO`): [Definition. E.g., A standardized data transfer object representing a single academic mark.]
*   **[Domain Action]** (e.g., `Scrape`): [Definition. E.g., The act of fetching and parsing raw HTML from an external provider.]

## 3. High-Level System Context
*   **Frontend/UI:** [e.g., Reflex (Python)]
*   **Backend/State:** [e.g., Reflex State / FastAPI]
*   **Storage:** [e.g., Local JSON / SQLite / Pocketbase]
*   **External Integrations:** [e.g., Librus Synergia, Vulcan UONET+]

## 4. Navigation Guide
*   Looking for **What** to build? ➡️ `/1-product-specs/`
*   Looking for **How** it works? ➡️ `/2-architecture/`
*   Looking for **Current Tasks**? ➡️ `execution-plan.md`


```
/docs
├── .templates/                   ← LLM & Human instruction templates (tpl-*.md)
├── 00-START-HERE.md              ← Level 0: Executive Summary & Domain Dictionary
├── execution-plan.md             ← TEMPORAL: Active sprint tracker & AI prompt driver
│
├── /1-product-specs              ← THE "WHAT & WHY" (Prescriptive / The Law)
│   ├── 01-feature-catalog.md
│   └── /features                 ← Uses tpl-feature-spec.md
│
├── /2-architecture               ← THE "HOW" (Descriptive / The Reflection)
│   ├── 01-system-context.md
│   └── /components               ← Uses tpl-component-card.md
│
├── /3-reference                  ← THE "STRICT CONTRACTS" (Machine/Dev Reference)
│   ├── api-contracts.md          ← Uses tpl-reference-contract.md
│   └── database-schema.md
│
└── /4-decisions                  ← THE "HISTORICAL WHY" (Immutable once accepted)
    ├── adr-0001-use-reflex.md    ← Uses tpl-adr.md
    └── adr-0002-bs4-scraper.md
```
