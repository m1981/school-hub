<!--
LLM INSTRUCTION BLOCK
MOTIVATION: This file captures the "WHY" behind a major technical decision. It prevents circular debates months later. It is HISTORICAL and IMMUTABLE once accepted.
CONTENTS: Context, the Decision made, Alternatives considered, and Consequences (Good and Bad).
DO'S:
- DO be objective. List the pros and cons of the chosen solution.
- DO explicitly list the alternatives that were rejected and why.
- DO use the status flags: [proposed | accepted | rejected | superseded].
DON'TS:
- DO NOT edit an ADR once its status is "accepted". If a decision changes later, create a NEW ADR and mark the old one as "superseded".
- DO NOT write ADRs for trivial things (e.g., "We used a `for` loop"). Only write them for architectural shifts, library choices, or data modeling paradigms.
-->

# ADR [000X]: [Short Noun Phrase Describing Decision]

**Date:** [YYYY-MM-DD]
**Status:** [proposed | accepted | rejected | superseded by ADR-XXXX]

## 1. Context
[What is the problem we are facing? What is the technical or business constraint forcing us to make a decision? Keep it to 2-3 paragraphs.]

## 2. Decision
[What is the exact change or technology we are adopting? E.g., "We will use BeautifulSoup4 instead of Selenium for scraping Librus."]

## 3. Alternatives Considered
*   **[Alternative 1]:** [Why was it rejected? E.g., "Selenium: Rejected because it requires a heavy WebDriver, which is too slow for our serverless deployment."]
*   **[Alternative 2]:** [Why was it rejected?]

## 4. Consequences
### Positive (Pros)
*   [Benefit 1, e.g., Faster execution time]
*   [Benefit 2, e.g., Lower memory footprint]

### Negative (Cons / Risks)
*   [Risk 1, e.g., Cannot execute JavaScript, so if the target site becomes an SPA, this scraper will break.]
*   [Risk 2, e.g., Requires manual handling of session cookies.]
