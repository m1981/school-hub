<!--
LLM INSTRUCTION BLOCK
MOTIVATION: This file defines the "How" for a specific internal module or service. It replaces heavy UML with a pragmatic "API Contract". It is DESCRIPTIVE.
CONTENTS: Responsibility, Inputs, Outputs, Throws, and Dependencies mapped to architecture colors.
DO'S:
- DO keep it concise. This should take a human 2 minutes to read.
- DO use the standard visual color emojis (🔵 UI, 🟠 Domain, 🟣 Infra, 🟢 DB).
- DO update this file immediately if the code signature changes.
DON'TS:
- DO NOT include business justification or user stories here (those belong in /1-product-specs).
-->

# ⚙️ [Component/Service Name]

**Description:** [One sentence technical description of what this module does.]

## Contract Definitions

*   **Responsibility:** [What is the single responsibility of this module?]
*   **Input:** `[Data Type]` - [Description]
*   **Output:** `[Data Type]` - [Description]
*   **Throws/Errors:** `[Exception Types]`
*   **Dependencies:**
    *   [Emoji] `[Dependency 1]`
    *   [Emoji] `[Dependency 2]`

## Internal Flow (Optional)
[If complex, insert a Mermaid.js sequence diagram here. Otherwise, leave blank.]
