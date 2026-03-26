# School Hub - Architecture Diagrams Guide

This document explains the architecture, API structure, and key flows of the School Hub application using the Mermaid diagrams above.

## 1. System Architecture Overview

**Purpose**: Shows the high-level structure of the application.

**Key Components**:
- **Frontend (Browser)**: Reflex UI components rendered in the browser
- **Backend (Python/Reflex State)**: Server-side state management with AppState
- **Services Layer**: MockMonitoringService (current) + future scrapers
- **Data Models**: Pydantic DTOs for structured data
- **External Systems**: Librus/Vulcan portals (Sprint 6)

**Key Insights**:
- Currently using MockMonitoringService for testing
- Future scrapers will replace mock with real data
- No database - all data in memory (_kids_data)
- Clean separation: UI → State → Services → DTOs

## 2. Data Model Structure

**Purpose**: Shows the relationship between DTOs (Data Transfer Objects).

**Key Relationships**:
- `KidGradesDTO` is the root container per child
- Each kid has multiple `SubjectDTO` records
- Each subject has multiple `PeriodDTO` records (e.g., "OKRES 1")
- Each period has multiple `GradeDTO` records
- `NewsDTO` is stored separately at the kid level

**Key Design Decisions**:
- **Denormalization**: GradeDTO includes `kid_name` and `subject_name` for easy dashboard rendering
- **Sort Keys**: Integer fields (YYYYMMDD) for cross-provider sorting
- **Flat Structure**: NewsDTO and CalendarEventDTO are denormalized for unified feeds

## 3. AppState API Structure

**Purpose**: Explains the Reflex State pattern and available APIs.

**State Categories**:
1. **UI State** (sent to frontend):
   - `current_tab`: Which view is active
   - `last_synced`: Timestamp of last data refresh

2. **Backend Storage** (stays on server):
   - `_kids_data`: List of KidGradesDTO objects (prefix `_` means backend-only)

3. **Computed Properties** (`@rx.var` decorator):
   - `get_sorted_feed`: Merges and sorts all grades/news
   - `get_quick_stats`: Summarizes data per kid

4. **Event Handlers**:
   - `set_current_tab(tab)`: Changes active view
   - `refresh_data()`: Reloads data from service

**Key Pattern**: Backend-only variables use `_` prefix to avoid WebSocket serialization overhead.

## 4. Component Hierarchy

**Purpose**: Shows how UI components are structured and connected.

**Component Tree**:
```
app.py
└── index()
    ├── render_current_view()
    │   ├── feed_view() [active based on current_tab]
    │   │   ├── quick_stat_card (×4, via rx.foreach)
    │   │   └── feed_card (×many, via rx.foreach)
    │   ├── calendar_view()
    │   ├── children_view()
    │   └── settings_view()
    └── bottom_navigation()
        └── bottom_nav_item (×4)
```

**Key Patterns**:
- `rx.cond()` for conditional rendering (not Python if/else)
- `rx.foreach()` for list rendering
- Event handlers connect UI to State methods

## 5-8. Sequence Diagrams

### 5. Application Initialization
Shows the startup flow: Browser loads → AppState.__init__() → MockService → DTOs → Computed properties → Render

### 6. User Changes Tab
Shows reactive navigation: Click tab → set_current_tab() → State update via WebSocket → Re-render → View changes

### 7. User Refreshes Data
Shows data refresh flow: Click refresh → refresh_data() → MockService → Update state → Recompute feeds → Re-render

### 8. Feed Rendering Details
Shows how the feed view assembles: get_quick_stats → rx.foreach → get_sorted_feed → rx.foreach → Conditional rendering for grades vs news

## 9. Future Data Flow (Sprint 6)

**Purpose**: Shows how real scraping will work.

**Flow**:
1. User triggers refresh
2. MonitoringService loads credentials for 4 kids
3. **Parallel scraping**: LibrusScraper and VulcanScraper fetch data simultaneously
4. Each scraper:
   - Logs in to the portal
   - Fetches HTML
   - Parses with BeautifulSoup
   - Normalizes dates to `date_sort_key`
   - Creates DTOs
5. All data merged back to AppState

**Key Design**: Scrapers act as adapters, normalizing different provider formats into unified DTOs.

## 10. State Management Pattern

**Purpose**: Explains Reflex's WebSocket-based reactive state.

**How It Works**:
1. **User Action** → WebSocket event sent to backend
2. **Event Handler** updates state variables
3. **State Changes** trigger serialization
4. **WebSocket** sends only changed data to frontend
5. **Frontend** re-renders affected components

**Key Rules**:
- ✅ Public variables (no `_`) are sent to frontend
- ❌ Private variables (`_` prefix) stay on backend
- ✅ `@rx.var` properties are computed and serialized
- ✅ Only changed state is sent (efficient)

---

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `models.py` | DTOs (Pydantic) | Data structure |
| `state.py` | AppState | State management |
| `services/mock_service.py` | Mock data generator | Service layer |
| `components/navigation.py` | Bottom nav bar | UI component |
| `components/views.py` | View components | UI component |
| `school_hub.py` | Main app | Entry point |

## Key Architectural Principles

1. **No Database**: All data in memory (Reflex State)
2. **Thin Client**: Browser only renders, no business logic
3. **Denormalization**: DTOs include parent context for easy rendering
4. **Reactive UI**: WebSocket-based state synchronization
5. **TDD**: Tests before implementation for all features
6. **Clean Separation**: UI → State → Services → DTOs
