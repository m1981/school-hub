<!--
LLM INSTRUCTION BLOCK
MOTIVATION: This file defines the "What" and "Why" of a single feature. It is the absolute source of truth for QA and Development. It is PRESCRIPTIVE.
CONTENTS: YAML Frontmatter (Status), Metadata, User Stories (INVEST), BDD Scenarios (Given/When/Then), and out-of-scope boundaries.
DO'S:
- DO use the Ubiquitous Language defined in 00-START-HERE.md.
- DO write BDD scenarios that can be directly translated to Pytest/Playwright.
- DO update the `status:` flag in the YAML frontmatter as work progresses.
DON'TS:
- DO NOT mention UI frameworks (e.g., "Reflex"), database names (e.g., "Postgres"), or technical implementations. Keep it purely behavioral.
-->

---
id: [F-XXX]
title: [Feature Name]
status: [draft | in-development | live]
last_updated: [YYYY-MM-DD]
---

# 🎯 [Feature Name]

## 1. Executive Summary
[1-2 sentences explaining what this feature does and the business value it provides.]

## 2. User Stories
* **As a** [Persona], **I want** [Action] **so that** [Benefit/Value].

## 3. Acceptance Criteria (BDD Scenarios)

### Scenario: [Happy Path / Primary Use Case]
*   **Given** [Initial context/state]
*   **When** [User action or event trigger]
*   **Then** [Expected observable system state]

### Scenario: [Exception / Edge Case]
*   **Given** [Initial context/state]
*   **When** [User action or event trigger]
*   **Then** [Expected error or alternative state]

## 4. Boundaries (Out of Scope)
*   [Explicitly state what this feature will NOT do to prevent scope creep]
