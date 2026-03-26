**1. Do NOT write the whole application at once.**
We will build this application iteratively, feature by feature, following strict TDD principles. I will act as the Product Owner. You will act as the Developer.

**2. The TDD Cycle (Red-Green-Refactor):**
For every feature or component we build, you must follow this exact sequence:
*   **Step 1 (Test First):** Write the `pytest` unit test for the specific function, scraper, or state logic we are working on. (The test must fail initially).
*   **Step 2 (Implementation):** Write the minimal Python/Reflex code required to make that specific test pass.
*   **Step 3 (Refactor):** Clean up the code, ensure it adheres to the "Thin Client" and "No DB" constraints, and verify it matches the UI mockups.

**3. Agile Sprints (Our Roadmap):**
We will execute this project in the following micro-sprints. **Do not proceed to the next sprint until I explicitly say "Sprint X Approved."**

*   **Sprint 1: Core Domain & Mock Data (The Foundation)**
    *   *Goal:* Define the exact `rx.Base` DTOs (GradeDTO, CalendarEventDTO, etc.) from Chapter 1.
    *   *TDD Task:* Create a `MockMonitoringService` that generates dummy data for Anna, Ben, Clara, and David (matching the UI mockups). Write a test asserting the mock service returns the correct number of items.
*   **Sprint 2: The Reflex UI Shell & Navigation**
    *   *Goal:* Build the mobile-first layout (dark mode, max-width container) and the bottom navigation bar.
    *   *TDD Task:* Implement the `AppState` with a `current_tab` variable. Write a test asserting that changing the tab state correctly updates the active view.
*   **Sprint 3: The "School Hub" Feed (UI Binding)**
    *   *Goal:* Build the "Quick Stats" and "Today's Summary" lists using the mock data.
    *   *TDD Task:* Write a test for the `AppState.get_sorted_feed()` method to ensure it correctly merges and sorts grades/news from all 4 kids using the `date_sort_key`. Then build the UI components (`rx.card`, `rx.hstack`) to render them.
*   **Sprint 4: The Calendar View & Filtering**
    *   *Goal:* Build the Calendar UI with the horizontal filter pills.
    *   *TDD Task:* Write tests for `AppState.filter_calendar(kid_name, event_type)`. Ensure the logic correctly filters the mock data. Then build the UI to render the grouped dates.
*   **Sprint 5: Profile Management (Settings)**
    *   *Goal:* Build the UI to add/edit student profiles and securely store credentials locally.
    *   *TDD Task:* Write tests for a `CredentialManager` class that encrypts/decrypts a local JSON file. Then build the Reflex form (`rx.dialog`, `rx.input`) to interact with it.
*   **Sprint 6: The Scraper Adapters (The Real Data)**
    *   *Goal:* Implement the actual `LibrusScraper` and `VulcanScraper` using `BeautifulSoup`.
    *   *TDD Task:* I will provide you with raw HTML snippets. You will write tests that pass these snippets into your parsers and assert they output the correct DTOs. Only then will you write the parsing logic.

**"Acknowledge these instructions. If you understand the Agile/TDD protocol and the Sprint roadmap, reply ONLY with: 'Protocol accepted. Ready to begin Sprint 1: Core Domain & Mock Data. Please provide the command to start.'"**

***

### Why this approach guarantees success:
1.  **Context Window Management:** LLMs forget things if you ask for too much code at once. By breaking it into Sprints, the LLM stays laser-focused on one specific task (e.g., just the Calendar UI, or just the Librus parser).
2.  **Testable UI:** By forcing Sprint 1 to be "Mock Data", you can actually run the Reflex app and see the UI (Sprints 2-5) working perfectly *before* you ever write a single line of complex web-scraping code (Sprint 6).
3.  **Quality Control:** If the LLM hallucinates or writes bad code, you catch it immediately in that specific Sprint, rather than trying to debug a 2,000-line monolithic file.