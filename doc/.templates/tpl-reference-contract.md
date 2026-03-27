<!--
LLM INSTRUCTION BLOCK
MOTIVATION: This file is the strict, machine-readable truth for data structures and external boundaries. It is highly technical and DESCRIPTIVE.
CONTENTS: Data Transfer Objects (DTOs), Database Schemas, or REST/GraphQL endpoint definitions.
DO'S:
- DO use exact data types (e.g., `str`, `int`, `Optional[datetime]`).
- DO note which fields are nullable, unique, or indexed.
- DO provide a raw JSON/Code example of the payload.
DON'TS:
- DO NOT explain the UI or user journey here.
- DO NOT leave ambiguity regarding data formats (e.g., specify if a date is ISO8601 or YYYYMMDD).
-->

# 💾 Data Contract: [Entity / Integration Name]

**Type:** [Database Schema | REST API | Internal DTO]
**Source of Truth:** [e.g., `models.py` or External Provider Docs]

## 1. Schema Definition: `[ModelName]`

| Field Name | Type | Required | Default | Description / Constraints |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `UUID` | Yes | Auto | Primary Key |
| `[field_name]` | `[type]` | [Yes/No] | `[val]` | [What does this represent?] |
| `[field_name]` | `[type]` | [Yes/No] | `[val]` | [What does this represent?] |

## 2. Validation Rules
*   **[Field Name]:** [e.g., Must be greater than 0, Must match Regex `^[A-Z]+$`]
*   **[Field Name]:** [e.g., Cannot be updated after creation]

## 3. Example Payload / State
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "[field_name]": "example_value",
  "[field_name]": null
}
