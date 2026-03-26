# The Lean Specification Framework (`spec-lean.md`)

## 1. The Big Picture (Motivations & Discoveries)
Traditional documentation (monolithic Word documents, scattered Wikis, or chaotic Jira backlogs) fails in modern web development. It rots quickly, creates silos between Product and Engineering, and becomes impossible to navigate.

This framework ensures our specifications are:
*   **Frictionless:** Living exactly where the code lives (Docs-as-Code) to prevent context-switching.
*   **Layered:** Catering to different audiences, from a 30-second stakeholder overview to a 15-minute developer deep-dive (Progressive Disclosure).
*   **Defensive:** Explicitly defining what we *should not* build to prevent scope creep (YAGNI).
*   **Action-Oriented:** Documenting user *journeys* and data *flows* rather than static lists of features.

## 2. Core Principles
1.  **Docs-as-Code:** Specs are Markdown files in Git. They are reviewed in PRs alongside the code they describe.
2.  **Progressive Disclosure:** Information is layered (Level 0 to Level 3). Readers are never overwhelmed; they are guided.
3.  **Ubiquitous Language:** Product, Engineering, and Database schemas must use the exact same terminology.
4.  **YAGNI (You Aren't Gonna Need It):** We only document what we are actively building.
5.  **Text-Based Visuals:** Architecture and flows use Mermaid.js or ASCII. No static images (PNG/JPG) allowed.

---

## 3. Repository Structure
All documentation lives in the `/specs` directory at the root of the repository.

```text
/specs
  ├── 00-START-HERE.md           # Level 0: Onboarding & Routing
  ├── 01-system-context.md       # Level 1: The Map & C4 Context
  ├── 02-domain-and-logic.md     # Level 2: DDD, Business Rules, State
  ├── 03-architecture-adrs.md    # Level 3: Tech Stack & Decisions
  ├── quick-reference.md         # Cheat Sheet: Responsibility Matrix & DB Map
  ├── /journeys                  # BDD Scenarios & User/Dev Flows
  └── /technical                 # API Contracts & DB Schemas
```

---

## 4. Document Blueprints & Strict Templates
*Note to Developers and AI Assistants: When creating or updating these files, you MUST use the exact Markdown headers (H1, H2) provided below.*

### A. `00-START-HERE.md` (The Hook & Routing)
*   **Purpose:** 60-second onboarding for new devs or stakeholders.
*   **Template:**
    *   `# 🚀 START HERE - [Project Name]`
    *   `## 🎯 What Is This?` (One sentence summary)
    *   `## 🧩 Problem / Solution Matrix` (Markdown table of business value)
    *   `## ⚡ Quick Start` (CLI commands to run locally)
    *   `## 🗺️ Where to Go Next?` (Routing table based on reader goal)

### B. `01-system-context.md` (The Map)
*   **Purpose:** Define system boundaries, external integrations, and out-of-scope items.
*   **Template:**
    *   `# 🗺️ System Context`
    *   `## 🏗️ High-Level Architecture` (Mermaid `graph TB` block showing UI -> API -> DB -> 3rd Party)
    *   `## 🎭 Primary Actors & Goals` (Markdown table of user roles)
    *   `## 🛑 The YAGNI Parking Lot (Out of Scope)` (Strict bulleted list of exclusions)
    *   `## 🗺️ Where to Go Next?`

### C. `02-domain-and-logic.md` (The Brain)
*   **Purpose:** Shared mental model for complex business logic and data lifecycles.
*   **Template:**
    *   `# 🧠 Domain & Core Logic`
    *   `## 📖 Ubiquitous Language` (Glossary of core entities)
    *   `## 🔄 Data State Transitions` (Mermaid `stateDiagram-v2` block for core entities, e.g., Order Status)
    *   `## ⚙️ Core Algorithms & Background Jobs` (Cron jobs, complex calculations, data processing)
    *   `## 🗺️ Where to Go Next?`

### D. `03-architecture-adrs.md` (The Decisions)
*   **Purpose:** Document technical choices to prevent future debates.
*   **Template:**
    *   `# 🏛️ Architecture & Decisions`
    *   `## 🛠️ Tech Stack` (Frontend, Backend, DB, Infrastructure)
    *   `## 📏 Non-Functional Requirements (NFRs)` (Performance, Security, Scalability targets)
    *   `## 📜 Architecture Decision Records (ADRs)` (Format: Context -> Decision -> Consequences)
    *   `## 🗺️ Where to Go Next?`

### E. `/journeys/[journey-name].md` (The Behavior)
*   **Purpose:** Action-oriented flows replacing static feature lists. Bridges UX and Engineering.
*   **Template:**
    *   `# 🚶 Journey: [Name]`
    *   `## 🎯 Goal & Prerequisites`
    *   `## 🔄 The Flow` (Mermaid `sequenceDiagram` block showing User -> UI -> API -> DB)
    *   `## 💾 Data & State Changes` (What tables/states are mutated)
    *   `## 🐛 Edge Cases & Error Handling`
    *   `## 🗺️ Where to Go Next?`

---

## 5. The Golden Rules of Maintenance
1. **The PR Rule:** No Pull Request is approved if it changes system behavior, database schemas, or architecture without a corresponding update to the `/specs` folder.
2. **The Routing Rule:** Never leave the reader at a dead end. Every markdown file MUST end with a `## 🗺️ Where to Go Next?` table linking to related documents.
3. **The Diagram Rule:** If a flow or architecture changes, update the Mermaid code. Do not use external diagramming tools that cannot be version-controlled.

---

## 6. 🤖 LLM Generation Enforcements (STRICT)
*When an AI/LLM is instructed to generate or update documentation based on this framework, it MUST obey the following constraints:*

1.  **Anti-Hallucination:** Do NOT invent features, tech stacks, or database columns that were not explicitly provided in the prompt or codebase. If a required detail is missing, insert `[TBD: Requires Human Input]` instead of guessing.
2.  **Tone & Style:** Use a concise, highly technical, engineering-focused tone. NO marketing fluff. NO introductory filler phrases (e.g., "Here is the document you requested..."). Output ONLY the Markdown.
3.  **Formatting:**
    *   Use bullet points and Markdown tables aggressively to maximize readability.
    *   Keep paragraphs under 3 sentences.
4.  **Mermaid Constraints:**
    *   Use ONLY standard, widely supported Mermaid syntax (`graph TD`, `sequenceDiagram`, `stateDiagram-v2`).
    *   Do not use complex styling or experimental Mermaid features that might break markdown renderers.
5.  **YAGNI Enforcement:** If the prompt mentions a feature as "future", "planned", or "maybe," it MUST be placed in the `## 🛑 The YAGNI Parking Lot (Out of Scope)` section and excluded from all architecture diagrams and current journeys.
