**1. Do NOT write the whole application at once.**
We will build this application iteratively, feature by feature, following strict TDD principles. I will act as the Product Owner. You will act as the Developer.

**2. The TDD Cycle (Red-Green-Refactor):**
For every feature or component we build, you must follow this exact sequence:
*   **Step 1 (Test First):** Write the `pytest` unit test for the specific function, scraper, or state logic we are working on. (The test must fail initially).
*   **Step 2 (Implementation):** Write the minimal Python/Reflex code required to make that specific test pass.
*   **Step 3 (Refactor):** Clean up the code, ensure it adheres to the "Thin Client" and "No DB" constraints, and verify it matches the UI mockups.

**3. Agile Sprints (Our Roadmap):**
We will execute this project in the following micro-sprints. **Do not proceed to the next sprint until I explicitly say "Sprint X Approved."**

*   **✅ Sprint 1: Core Domain & Mock Data (The Foundation) - COMPLETE**
    *   *Goal:* Define the exact Pydantic DTOs (GradeDTO, CalendarEventDTO, etc.) from Chapter 1.
    *   *TDD Task:* Create a `MockMonitoringService` that generates dummy data for Anna, Ben, Clara, and David (matching the UI mockups). Write a test asserting the mock service returns the correct number of items.
    *   *Status:* All 12 tests passing ✓
    *   *Commits:* 77c7e99, ff61ca1 (fixed to use pydantic.BaseModel instead of deprecated rx.Base)
    *   *Deliverables:*
        - `school_hub/models.py` - 6 DTOs using pydantic.BaseModel
        - `school_hub/services/mock_service.py` - MockMonitoringService with data for 4 kids
        - `tests/test_sprint1_domain.py` - 12 unit tests

*   **✅ Sprint 2: The Reflex UI Shell & Navigation - COMPLETE**
    *   *Goal:* Build the mobile-first layout (dark mode, max-width container) and the bottom navigation bar.
    *   *TDD Task:* Implement the `AppState` with a `current_tab` variable. Write a test asserting that changing the tab state correctly updates the active view.
    *   *Status:* All 7 tests passing ✓
    *   *Commits:* 5877190
    *   *Deliverables:*
        - `school_hub/state.py` - AppState with tab navigation and data loading
        - `school_hub/components/navigation.py` - Bottom navigation bar
        - `school_hub/components/views.py` - View components with reactive rendering
        - `school_hub/school_hub.py` - Main app with mobile-first layout
        - `tests/test_sprint2_navigation.py` - 7 unit tests

*   **✅ Sprint 3: The "School Hub" Feed (UI Binding) - COMPLETE**
    *   *Goal:* Build the "Quick Stats" and "Today's Summary" lists using the mock data.
    *   *TDD Task:* Write a test for the `AppState.get_sorted_feed()` method to ensure it correctly merges and sorts grades/news from all 4 kids using the `date_sort_key`. Then build the UI components (`rx.card`, `rx.hstack`) to render them.
    *   *Status:* All 8 tests passing ✓
    *   *Commits:* 2dda6eb
    *   *Deliverables:*
        - `AppState.get_sorted_feed` - Computed property merging/sorting grades and news
        - `AppState.get_quick_stats` - Computed property for kid summaries
        - Quick Stats cards with horizontal scroll
        - Feed cards with conditional rendering (blue=grades, orange=news)
        - Refresh button functionality
        - `tests/test_sprint3_feed.py` - 8 unit tests

*   **✅ Sprint 4: The Calendar View & Filtering - COMPLETE**
    *   *Goal:* Build the Calendar UI with the horizontal filter pills.
    *   *TDD Task:* Write tests for `AppState.filter_calendar(kid_name, event_type)`. Ensure the logic correctly filters the mock data. Then build the UI to render the grouped dates.
    *   *Status:* All 12 tests passing ✓
    *   *Commits:* 71e8f64
    *   *Deliverables:*
        - `CalendarEventDTO` added to `KidGradesDTO.calendar_events`
        - Mock calendar events for all 4 kids (7 total events)
        - `AppState.calendar_filter_kid` and `AppState.calendar_filter_event_type` state vars
        - `AppState.get_all_calendar_events` - Aggregates all calendar events
        - `AppState.get_filtered_calendar_events` - Filters by kid and event type
        - `AppState.get_calendar_events_with_headers` - Flattened list with date headers
        - `AppState.set_calendar_filter_kid` and `AppState.set_calendar_filter_event_type` methods
        - Calendar view with horizontal filter pills (Kids: All, Anna, Ben, Clara, David)
        - Calendar view with event type filters (All, Sprawdzian, Kartkówka, Zadania)
        - Calendar event cards with color-coded borders, time, room, teacher info
        - `tests/test_sprint4_calendar.py` - 12 unit tests

*   **✅ Sprint 5: Profile Management (Settings) - COMPLETE**
    *   *Goal:* Build the UI to add/edit student profiles and securely store credentials locally.
    *   *TDD Task:* Write tests for a `CredentialManager` class that encrypts/decrypts a local JSON file. Then build the Reflex form (`rx.dialog`, `rx.input`) to interact with it.
    *   *Status:* All 13 tests passing ✓
    *   *Commits:* [pending]
    *   *Deliverables:*
        - `school_hub/services/credential_manager.py` - CredentialManager with Fernet encryption
        - `StudentProfile` DTO for credentials
        - `AppState.get_profiles` - Computed var returning profiles without passwords
        - `AppState.add_profile`, `update_profile`, `delete_profile` - CRUD operations
        - Profile form state variables and handlers
        - Settings view with profile cards, add/edit/delete functionality
        - Empty state UI when no profiles exist
        - `tests/test_sprint5_profiles.py` - 13 unit tests (8 CredentialManager + 5 AppState)

*   **Sprint 6: The Scraper Adapters (The Real Data)**
    *   *Goal:* Implement the actual `LibrusScraper` and `VulcanScraper` using `BeautifulSoup`.
    *   *TDD Task:* I will provide you with raw HTML snippets. You will write tests that pass these snippets into your parsers and assert they output the correct DTOs. Only then will you write the parsing logic.
    *   *Status:* Not started

**"Acknowledge these instructions. If you understand the Agile/TDD protocol and the Sprint roadmap, reply ONLY with: 'Protocol accepted. Ready to begin Sprint 1: Core Domain & Mock Data. Please provide the command to start.'"**

***

## Current Progress Summary

**Completed Sprints:** 5 of 6 (83%)
**Total Tests:** 52/52 passing ✓ (unit tests only, Playwright tests excluded)
**Code Quality:** Clean ✓
**Compilation:** Clean, no warnings ✓

### Key Technical Decisions
1. **Framework Compliance:** Using `pydantic.BaseModel` (not deprecated `rx.Base`)
2. **State Management:** Backend-only data with `_` prefix, computed properties with `@rx.var`
3. **UI Patterns:** Reactive rendering with `rx.cond`, not Python if/else
4. **Testing:** Unit tests before implementation (strict TDD), Playwright for GUI verification

### Git History
```
71e8f64 - Sprint 4: Calendar View & Filtering
ff61ca1 - FIX: Replace deprecated rx.Base with pydantic.BaseModel
bde4d77 - FIX: Use rx.Base instead of pydantic.BaseModel for DTOs (reverted)
2dda6eb - Sprint 3: School Hub Feed with Quick Stats and Activity Feed
5877190 - Sprint 2: Reflex UI Shell & Navigation
77c7e99 - Sprint 1: Implement Core Domain & Mock Data
```

### Next Steps
Ready to proceed with **Sprint 6: The Scraper Adapters (The Real Data)** upon approval.

***

### Why this approach guarantees success:
1.  **Context Window Management:** LLMs forget things if you ask for too much code at once. By breaking it into Sprints, the LLM stays laser-focused on one specific task (e.g., just the Calendar UI, or just the Librus parser).
2.  **Testable UI:** By forcing Sprint 1 to be "Mock Data", you can actually run the Reflex app and see the UI (Sprints 2-5) working perfectly *before* you ever write a single line of complex web-scraping code (Sprint 6).
3.  **Quality Control:** If the LLM hallucinates or writes bad code, you catch it immediately in that specific Sprint, rather than trying to debug a 2,000-line monolithic file.
