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

```mermaid
graph TB
    subgraph "Frontend (Browser)"
        UI[Reflex UI Components]
        NAV[Bottom Navigation]
        FEED[Feed View]
        CAL[Calendar View]
        CHILD[Children View]
        SET[Settings View]
    end

    subgraph "Backend (Python/Reflex State)"
        STATE[AppState]
        COMPUTED[Computed Properties]
        BACKEND_DATA[_kids_data Backend Storage]
    end

    subgraph "Services Layer"
        MOCK[MockMonitoringService]
        LIBRUS[LibrusScraper<br/>Not Implemented]
        VULCAN[VulcanScraper<br/>Not Implemented]
    end

    subgraph "Data Models (Pydantic)"
        DTO[DTOs: GradeDTO<br/>NewsDTO<br/>CalendarEventDTO<br/>KidGradesDTO]
    end

    subgraph "External Systems (Future)"
        LIB_SYS[Librus Portal]
        VUL_SYS[Vulcan Portal]
    end

    UI --> NAV
    NAV --> FEED
    NAV --> CAL
    NAV --> CHILD
    NAV --> SET

    FEED --> STATE
    CAL --> STATE
    CHILD --> STATE
    SET --> STATE

    STATE --> COMPUTED
    STATE --> BACKEND_DATA
    COMPUTED --> BACKEND_DATA

    STATE --> MOCK
    STATE -.Future.-> LIBRUS
    STATE -.Future.-> VULCAN

    MOCK --> DTO
    LIBRUS -.-> DTO
    VULCAN -.-> DTO

    LIBRUS -.-> LIB_SYS
    VULCAN -.-> VUL_SYS

    style UI fill:#e3f2fd,stroke:#1976d2,color:#000
    style STATE fill:#fff3e0,stroke:#f57c00,color:#000
    style MOCK fill:#e8f5e9,stroke:#388e3c,color:#000
    style DTO fill:#f3e5f5,stroke:#7b1fa2,color:#000
    style LIBRUS fill:#e0e0e0,stroke:#757575,color:#000,stroke-dasharray: 5 5
    style VULCAN fill:#e0e0e0,stroke:#757575,color:#000,stroke-dasharray: 5 5

```

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

```mermaid
classDiagram
    class KidGradesDTO {
        +str kid_name
        +str provider
        +list~SubjectDTO~ subjects
        +list~NewsDTO~ news
        +str last_synced
    }

    class SubjectDTO {
        +str name
        +list~PeriodDTO~ periods
    }

    class PeriodDTO {
        +str name
        +list~GradeDTO~ grades
        +Optional~str~ empty_message
    }

    class GradeDTO {
        +str kid_name
        +str subject_name
        +str value
        +str category
        +str weight
        +Optional~str~ date
        +int date_sort_key
        +Optional~str~ comment
        +bool is_retake
        +Optional~str~ previous_value
    }

    class NewsDTO {
        +str kid_name
        +str date
        +int date_sort_key
        +str sender
        +str subject
        +str content
    }

    class CalendarEventDTO {
        +str kid_name
        +int date_sort_key
        +str display_date
        +str time_range
        +str room
        +str subject
        +str event_type
        +str description
        +str teacher
        +str color_theme
    }

    KidGradesDTO "1" *-- "many" SubjectDTO
    KidGradesDTO "1" *-- "many" NewsDTO
    SubjectDTO "1" *-- "many" PeriodDTO
    PeriodDTO "1" *-- "many" GradeDTO

    note for GradeDTO "Denormalized with kid_name\nand subject_name for easy\ndashboard rendering"
    note for NewsDTO "Denormalized with kid_name\nfor unified feed"

```

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

```mermaid
classDiagram
    class AppState {
        **UI State (Frontend)**
        +str current_tab
        +str last_synced

        **Backend Storage**
        -list~KidGradesDTO~ _kids_data

        **Properties**
        +kids_data property
        +get_sorted_feed @rx.var
        +get_quick_stats @rx.var

        **Methods**
        +__init__()
        +_load_initial_data()
        +set_current_tab(tab: str)
        +refresh_data()
    }

    class ComputedProperties {
        <<interface>>
        +get_sorted_feed() list~dict~
        +get_quick_stats() list~dict~
    }

    class UIState {
        <<interface>>
        +current_tab str
        +last_synced str
    }

    class BackendStorage {
        <<interface>>
        -_kids_data list~KidGradesDTO~
    }

    AppState ..|> ComputedProperties
    AppState ..|> UIState
    AppState ..|> BackendStorage

    note for AppState "Reflex State manages both\nfrontend UI state and\nbackend data storage"

    note for BackendStorage "Variables with _ prefix\nare backend-only\n(not sent to frontend)"

    note for ComputedProperties "@rx.var decorator makes\nproperties reactive and\nserializable for frontend"

```

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

```mermaid
graph TD
    APP[app.py: Main App]
    INDEX[index: Main Layout]

    subgraph "Navigation"
        BOTTOM_NAV[bottom_navigation]
        NAV_ITEM[bottom_nav_item x4]
    end

    subgraph "Views"
        RENDER_VIEW[render_current_view]
        FEED_V[feed_view]
        CAL_V[calendar_view]
        CHILD_V[children_view]
        SET_V[settings_view]
    end

    subgraph "Feed Components"
        QUICK_STAT[quick_stat_card]
        FEED_CARD[feed_card]
    end

    APP --> INDEX
    INDEX --> RENDER_VIEW
    INDEX --> BOTTOM_NAV

    BOTTOM_NAV --> NAV_ITEM

    RENDER_VIEW -->|rx.cond| FEED_V
    RENDER_VIEW -->|rx.cond| CAL_V
    RENDER_VIEW -->|rx.cond| CHILD_V
    RENDER_VIEW -->|rx.cond| SET_V

    FEED_V -->|rx.foreach| QUICK_STAT
    FEED_V -->|rx.foreach| FEED_CARD

    NAV_ITEM -.on_click.-> STATE_SET_TAB[AppState.set_current_tab]
    FEED_V -.reads.-> STATE_FEED[AppState.get_sorted_feed]
    FEED_V -.reads.-> STATE_STATS[AppState.get_quick_stats]

    style APP fill:#e3f2fd,stroke:#1976d2,color:#000
    style INDEX fill:#e3f2fd,stroke:#1976d2,color:#000
    style FEED_V fill:#c8e6c9,stroke:#388e3c,color:#000
    style STATE_SET_TAB fill:#fff3e0,stroke:#f57c00,color:#000
    style STATE_FEED fill:#fff3e0,stroke:#f57c00,color:#000
    style STATE_STATS fill:#fff3e0,stroke:#f57c00,color:#000

```

## 5-8. Sequence Diagrams

### 5. Application Initialization
Shows the startup flow: Browser loads → AppState.__init__() → MockService → DTOs → Computed properties → Render

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Reflex
    participant AppState
    participant MockService
    participant DTOs

    User->>Browser: Navigate to localhost:3000
    Browser->>Reflex: Load Application
    Reflex->>AppState: __init__()

    activate AppState
    AppState->>AppState: _load_initial_data()
    AppState->>MockService: get_all_data()

    activate MockService
    MockService->>DTOs: Create KidGradesDTO for Anna
    MockService->>DTOs: Create KidGradesDTO for Ben
    MockService->>DTOs: Create KidGradesDTO for Clara
    MockService->>DTOs: Create KidGradesDTO for David
    MockService-->>AppState: list[KidGradesDTO]
    deactivate MockService

    AppState->>AppState: Store in _kids_data
    AppState->>AppState: Set last_synced timestamp
    AppState->>AppState: Set current_tab = "feed"
    deactivate AppState

    Reflex->>AppState: get_sorted_feed (computed)
    activate AppState
    AppState->>AppState: Merge grades & news
    AppState->>AppState: Sort by date_sort_key
    AppState-->>Reflex: list[dict] feed items
    deactivate AppState

    Reflex->>AppState: get_quick_stats (computed)
    activate AppState
    AppState->>AppState: Count grades per kid
    AppState->>AppState: Count news per kid
    AppState-->>Reflex: list[dict] stats
    deactivate AppState

    Reflex->>Browser: Render Feed View
    Browser-->>User: Display School Hub

    Note over Browser,User: Shows:<br/>- Quick Stats (4 kids)<br/>- Recent Activity Feed<br/>- Bottom Navigation

```

### 6. User Changes Tab
Shows reactive navigation: Click tab → set_current_tab() → State update via WebSocket → Re-render → View changes
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant NavigationComponent
    participant AppState
    participant ViewComponent

    User->>Browser: Click "Calendar" tab
    Browser->>NavigationComponent: on_click event
    NavigationComponent->>AppState: set_current_tab("calendar")

    activate AppState
    AppState->>AppState: current_tab = "calendar"
    AppState-->>Browser: State updated (WebSocket)
    deactivate AppState

    Browser->>Browser: Re-render triggered
    Browser->>ViewComponent: render_current_view()

    activate ViewComponent
    ViewComponent->>ViewComponent: rx.cond(current_tab == "calendar")
    ViewComponent-->>Browser: calendar_view() component
    deactivate ViewComponent

    Browser->>NavigationComponent: Update active tab style
    activate NavigationComponent
    NavigationComponent->>NavigationComponent: rx.cond highlights "calendar"
    NavigationComponent-->>Browser: Calendar tab in blue/bold
    deactivate NavigationComponent

    Browser-->>User: Display Calendar View

    Note over User,Browser: Tab changes are instant<br/>via WebSocket state sync

```

### 7. User Refreshes Data
Shows data refresh flow: Click refresh → refresh_data() → MockService → Update state → Recompute feeds → Re-render
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant FeedView
    participant AppState
    participant MockService
    participant DTOs

    User->>Browser: Click refresh button
    Browser->>FeedView: on_click event
    FeedView->>AppState: refresh_data()

    activate AppState
    AppState->>MockService: get_all_data()

    activate MockService
    MockService->>DTOs: Create fresh KidGradesDTO objects
    MockService-->>AppState: list[KidGradesDTO]
    deactivate MockService

    AppState->>AppState: Update _kids_data
    AppState->>AppState: Update last_synced timestamp
    AppState-->>Browser: State updated (WebSocket)
    deactivate AppState

    Browser->>Browser: Re-render triggered

    Browser->>AppState: get_sorted_feed (computed)
    activate AppState
    AppState->>AppState: Recalculate feed from new data
    AppState-->>Browser: Updated feed items
    deactivate AppState

    Browser->>AppState: get_quick_stats (computed)
    activate AppState
    AppState->>AppState: Recalculate stats from new data
    AppState-->>Browser: Updated stats
    deactivate AppState

    Browser->>FeedView: Re-render with new data
    Browser-->>User: Display updated feed

    Note over Browser,User: New timestamp shown:<br/>"Last synced: 2026-03-26 23:00:15"

```

### 8. Feed Rendering Details
Shows how the feed view assembles: get_quick_stats → rx.foreach → get_sorted_feed → rx.foreach → Conditional rendering for grades vs news

```mermaid
sequenceDiagram
    participant Browser
    participant FeedView
    participant AppState
    participant QuickStatCard
    participant FeedCard

    Browser->>FeedView: Render feed_view()

    activate FeedView

    FeedView->>AppState: Access get_quick_stats
    activate AppState
    AppState->>AppState: Iterate _kids_data
    AppState->>AppState: Count grades/news per kid
    AppState-->>FeedView: [{kid_name, provider, recent_summary, avatar}...]
    deactivate AppState

    FeedView->>FeedView: rx.foreach(get_quick_stats, quick_stat_card)

    loop For each kid stat
        FeedView->>QuickStatCard: Render card
        activate QuickStatCard
        QuickStatCard-->>FeedView: Card component (avatar, name, summary)
        deactivate QuickStatCard
    end

    FeedView->>AppState: Access get_sorted_feed
    activate AppState
    AppState->>AppState: Collect all grades from all kids
    AppState->>AppState: Collect all news from all kids
    AppState->>AppState: Sort by date_sort_key DESC
    AppState-->>FeedView: [{type, kid_name, value/content, date...}...]
    deactivate AppState

    FeedView->>FeedView: rx.foreach(get_sorted_feed, feed_card)

    loop For each feed item
        FeedView->>FeedCard: Render card with item
        activate FeedCard
        FeedCard->>FeedCard: rx.cond(item.type == "grade")

        alt Grade
            FeedCard-->>FeedView: Blue card with badge
        else News
            FeedCard-->>FeedView: Orange card with content
        end
        deactivate FeedCard
    end

    deactivate FeedView

    FeedView-->>Browser: Complete feed layout

    Note over Browser,FeedView: Horizontal scroll for stats<br/>Vertical scroll for feed items

```

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

```mermaid
sequenceDiagram
    participant User
    participant AppState
    participant MonitoringService
    participant LibrusScraper
    participant VulcanScraper
    participant LibrusPortal
    participant VulcanPortal
    participant DTOs

    User->>AppState: refresh_data()

    activate AppState
    AppState->>MonitoringService: get_all_data()

    activate MonitoringService

    Note over MonitoringService: Load credentials for 4 kids

    par Anna (Librus)
        MonitoringService->>LibrusScraper: fetch_data(anna_credentials)
        activate LibrusScraper
        LibrusScraper->>LibrusPortal: Login with credentials
        LibrusPortal-->>LibrusScraper: Session cookie
        LibrusScraper->>LibrusPortal: GET /grades
        LibrusPortal-->>LibrusScraper: HTML response
        LibrusScraper->>LibrusScraper: Parse with BeautifulSoup
        LibrusScraper->>LibrusScraper: Calculate date_sort_key
        LibrusScraper->>DTOs: Create KidGradesDTO
        LibrusScraper-->>MonitoringService: Anna's data
        deactivate LibrusScraper
    end

    par Ben (Vulcan)
        MonitoringService->>VulcanScraper: fetch_data(ben_credentials)
        activate VulcanScraper
        VulcanScraper->>VulcanPortal: Login with credentials
        VulcanPortal-->>VulcanScraper: Session token
        VulcanScraper->>VulcanPortal: GET /api/grades
        VulcanPortal-->>VulcanScraper: HTML/JSON response
        VulcanScraper->>VulcanScraper: Parse data
        VulcanScraper->>VulcanScraper: Calculate date_sort_key
        VulcanScraper->>DTOs: Create KidGradesDTO
        VulcanScraper-->>MonitoringService: Ben's data
        deactivate VulcanScraper
    end

    Note over MonitoringService: Same for Clara and David

    MonitoringService-->>AppState: list[KidGradesDTO]
    deactivate MonitoringService

    AppState->>AppState: Update _kids_data
    AppState->>AppState: Update last_synced
    deactivate AppState

    AppState-->>User: Fresh data displayed

    Note over User,DTOs: Scrapers normalize different<br/>provider formats into<br/>unified DTOs

```

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

```mermaid
graph TB
    subgraph "Frontend (Browser)"
        UI[UI Components]
        WS_CLIENT[WebSocket Client]
    end

    subgraph "Backend (Python Server)"
        WS_SERVER[WebSocket Server]
        STATE[AppState Instance]

        subgraph "State Variables"
            UI_STATE[current_tab<br/>last_synced<br/>PUBLIC]
            BACKEND_STATE[_kids_data<br/>PRIVATE]
        end

        subgraph "Computed Properties"
            COMP1[@rx.var<br/>get_sorted_feed]
            COMP2[@rx.var<br/>get_quick_stats]
        end

        subgraph "Event Handlers"
            HANDLER1[set_current_tab]
            HANDLER2[refresh_data]
        end
    end

    UI -->|User Action| WS_CLIENT
    WS_CLIENT -->|Event| WS_SERVER
    WS_SERVER --> HANDLER1
    WS_SERVER --> HANDLER2

    HANDLER1 --> UI_STATE
    HANDLER2 --> BACKEND_STATE
    HANDLER2 --> UI_STATE

    STATE --> UI_STATE
    STATE --> BACKEND_STATE
    STATE --> COMP1
    STATE --> COMP2

    COMP1 --> BACKEND_STATE
    COMP2 --> BACKEND_STATE

    UI_STATE -->|Serialized| WS_SERVER
    COMP1 -->|Serialized| WS_SERVER
    COMP2 -->|Serialized| WS_SERVER
    BACKEND_STATE -.NOT sent.-> WS_SERVER

    WS_SERVER -->|State Update| WS_CLIENT
    WS_CLIENT -->|Re-render| UI

    style UI_STATE fill:#c8e6c9,stroke:#388e3c,color:#000
    style BACKEND_STATE fill:#ffcdd2,stroke:#c62828,color:#000
    style COMP1 fill:#fff9c4,stroke:#f57f17,color:#000
    style COMP2 fill:#fff9c4,stroke:#f57f17,color:#000
    style WS_CLIENT fill:#e3f2fd,stroke:#1976d2,color:#000
    style WS_SERVER fill:#e3f2fd,stroke:#1976d2,color:#000

```
---

## 11. Settings View - Add New Student Flow

**Purpose**: Detailed specification for adding a new student profile with credentials.

**User Story**: As a parent, I want to add a new student profile so that I can monitor their school data from Librus or Vulcan.

**Flow**:
1. User clicks "Add New Student" button in Settings view
2. Dialog opens with empty form
3. User fills in: Student Name, Provider (radio: Librus/Vulcan), Login, Password
4. User clicks "Save Profile"
5. System validates input (all fields required)
6. System encrypts and saves credentials to `credentials.json`
7. Dialog closes
8. Profile card appears in the list

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant SettingsView
    participant Dialog
    participant AppState
    participant CredentialManager
    participant FileSystem

    User->>Browser: Click "Add New Student" button
    Browser->>SettingsView: Trigger dialog
    SettingsView->>Dialog: Open dialog (rx.dialog.root)

    activate Dialog
    Dialog-->>Browser: Display form with empty fields
    deactivate Dialog

    User->>Browser: Fill form fields
    Browser->>AppState: set_profile_form_kid_name("Emma")
    Browser->>AppState: set_profile_form_provider("Librus")
    Browser->>AppState: set_profile_form_login("emma@example.com")
    Browser->>AppState: set_profile_form_password("secret123")

    User->>Browser: Click "Save Profile"
    Browser->>AppState: save_profile_from_form()

    activate AppState
    AppState->>AppState: Validate fields (all required)

    alt All fields valid
        AppState->>AppState: add_profile(kid_name, provider, login, password)

        activate AppState
        AppState->>CredentialManager: save_profile(StudentProfile)

        activate CredentialManager
        CredentialManager->>CredentialManager: load_profiles()
        CredentialManager->>CredentialManager: Check if kid_name exists
        CredentialManager->>CredentialManager: Append new profile to list
        CredentialManager->>CredentialManager: Encrypt profiles list
        CredentialManager->>FileSystem: Write to credentials.json
        CredentialManager-->>AppState: Success
        deactivate CredentialManager

        AppState->>AppState: Increment _profiles_version
        AppState->>AppState: Clear form fields
        deactivate AppState

        AppState-->>Browser: State updated (WebSocket)
        deactivate AppState

        Browser->>Dialog: Close dialog (rx.dialog.close)
        Browser->>SettingsView: Re-render with new profile
        Browser->>AppState: get_profiles (computed)

        activate AppState
        AppState->>CredentialManager: load_profiles()
        activate CredentialManager
        CredentialManager->>FileSystem: Read credentials.json
        CredentialManager->>CredentialManager: Decrypt data
        CredentialManager-->>AppState: List[StudentProfile]
        deactivate CredentialManager
        AppState-->>Browser: Profiles without passwords
        deactivate AppState

        Browser-->>User: Display new profile card
    else Missing required fields
        AppState-->>Browser: No action (validation failed)
        Browser-->>User: Form remains open
    end

    Note over User,FileSystem: Credentials stored encrypted<br/>with Fernet symmetric encryption
```

**Validation Rules**:
- `kid_name`: Required, non-empty string
- `provider`: Required, must be "Librus" or "Vulcan"
- `login`: Required, non-empty string
- `password`: Required, non-empty string

**Security Considerations**:
- Passwords encrypted with Fernet before storage
- Encryption key stored in `.encryption.key` file
- `get_profiles` computed var NEVER returns passwords to frontend
- Form state cleared immediately after save

**UI Components**:
```python
# Dialog structure (already implemented in views.py)
rx.dialog.root(
    rx.dialog.trigger(rx.button("Add New Student")),
    rx.dialog.content(
        rx.dialog.title("Add New Student"),
        rx.vstack(
            rx.input(on_change=AppState.set_profile_form_kid_name),
            rx.radio(["Librus", "Vulcan"], on_change=AppState.set_profile_form_provider),
            rx.input(on_change=AppState.set_profile_form_login),
            rx.input(type="password", on_change=AppState.set_profile_form_password),
        ),
        rx.button("Save Profile", on_click=AppState.save_profile_from_form),
    )
)
```

---

## 12. Settings View - Edit Student Profile Flow

**Purpose**: Detailed specification for editing an existing student profile.

**User Story**: As a parent, I want to edit a student's credentials when they change their password or if I made a typo.

**Current Status**: ⚠️ **INCOMPLETE** - `open_edit_profile_dialog` is a placeholder

**Required Implementation**:

### 12.1 State Variables (Add to AppState)
```python
# Edit mode tracking
profile_edit_mode: bool = False
profile_edit_kid_name: str = ""  # Original kid_name being edited
```

### 12.2 Event Handlers (Update in AppState)

```python
def open_edit_profile_dialog(self, kid_name: str):
    """Open the edit dialog and populate form with existing profile data.

    Args:
        kid_name: Name of the student whose profile should be edited
    """
    # Load existing profile
    profile = self._credential_manager.get_profile(kid_name)

    if profile:
        # Populate form with existing data
        self.profile_form_kid_name = profile.kid_name
        self.profile_form_provider = profile.provider
        self.profile_form_login = profile.login
        self.profile_form_password = profile.password  # Pre-fill for editing

        # Set edit mode
        self.profile_edit_mode = True
        self.profile_edit_kid_name = kid_name

def save_profile_from_form(self):
    """Save the profile from the form data (handles both add and edit)."""
    if (
        self.profile_form_kid_name
        and self.profile_form_login
        and self.profile_form_password
    ):
        if self.profile_edit_mode:
            # Edit mode: update existing profile
            self.update_profile(
                kid_name=self.profile_form_kid_name,
                provider=self.profile_form_provider,
                login=self.profile_form_login,
                password=self.profile_form_password,
            )
        else:
            # Add mode: create new profile
            self.add_profile(
                kid_name=self.profile_form_kid_name,
                provider=self.profile_form_provider,
                login=self.profile_form_login,
                password=self.profile_form_password,
            )

        # Clear form and reset edit mode
        self.profile_form_kid_name = ""
        self.profile_form_provider = "Librus"
        self.profile_form_login = ""
        self.profile_form_password = ""
        self.profile_edit_mode = False
        self.profile_edit_kid_name = ""

def cancel_profile_form(self):
    """Cancel the form and reset all state."""
    self.profile_form_kid_name = ""
    self.profile_form_provider = "Librus"
    self.profile_form_login = ""
    self.profile_form_password = ""
    self.profile_edit_mode = False
    self.profile_edit_kid_name = ""
```

### 12.3 UI Component Updates (Update in views.py)

```python
def add_profile_dialog() -> rx.Component:
    """Dialog for adding/editing a student profile."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=18),
                " Add New Student",
                size="3",
                color_scheme="blue",
            ),
        ),
        rx.dialog.content(
            # Dynamic title based on edit mode
            rx.cond(
                AppState.profile_edit_mode,
                rx.dialog.title("Edit Student Profile"),
                rx.dialog.title("Add New Student"),
            ),
            rx.dialog.description(
                "Enter the student's information and provider credentials.",
                size="2",
                margin_bottom="1rem",
            ),
            rx.vstack(
                # Student Name
                rx.vstack(
                    rx.text("Student Name", size="2", weight="bold"),
                    rx.input(
                        placeholder="e.g., Anna",
                        value=AppState.profile_form_kid_name,
                        on_change=AppState.set_profile_form_kid_name,
                        size="3",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                # Provider Selection
                rx.vstack(
                    rx.text("School Provider", size="2", weight="bold"),
                    rx.radio(
                        ["Librus", "Vulcan"],
                        value=AppState.profile_form_provider,
                        on_change=AppState.set_profile_form_provider,
                        size="2",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                # Login
                rx.vstack(
                    rx.text("Login", size="2", weight="bold"),
                    rx.input(
                        placeholder="username or email",
                        value=AppState.profile_form_login,
                        on_change=AppState.set_profile_form_login,
                        size="3",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                # Password
                rx.vstack(
                    rx.text("Password", size="2", weight="bold"),
                    rx.input(
                        type="password",
                        placeholder="••••••••",
                        value=AppState.profile_form_password,
                        on_change=AppState.set_profile_form_password,
                        size="3",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                spacing="4",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        on_click=AppState.cancel_profile_form,
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        # Dynamic button text
                        rx.cond(
                            AppState.profile_edit_mode,
                            "Update Profile",
                            "Save Profile",
                        ),
                        on_click=AppState.save_profile_from_form,
                        color_scheme="blue",
                    ),
                ),
                spacing="3",
                margin_top="1rem",
                justify="end",
            ),
            max_width="450px",
        ),
        # Control dialog open state programmatically
        open=AppState.profile_edit_mode | (AppState.profile_form_kid_name != ""),
    )
```

### 12.4 Edit Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant ProfileCard
    participant Dialog
    participant AppState
    participant CredentialManager
    participant FileSystem

    User->>Browser: Click "Edit" icon on profile card
    Browser->>ProfileCard: on_click event
    ProfileCard->>AppState: open_edit_profile_dialog("TestKid")

    activate AppState
    AppState->>CredentialManager: get_profile("TestKid")

    activate CredentialManager
    CredentialManager->>FileSystem: Read credentials.json
    CredentialManager->>CredentialManager: Decrypt data
    CredentialManager->>CredentialManager: Find profile by kid_name
    CredentialManager-->>AppState: StudentProfile(kid_name, provider, login, password)
    deactivate CredentialManager

    AppState->>AppState: profile_form_kid_name = "TestKid"
    AppState->>AppState: profile_form_provider = "Librus"
    AppState->>AppState: profile_form_login = "test@example.com"
    AppState->>AppState: profile_form_password = "existing_password"
    AppState->>AppState: profile_edit_mode = True
    AppState->>AppState: profile_edit_kid_name = "TestKid"
    AppState-->>Browser: State updated (WebSocket)
    deactivate AppState

    Browser->>Dialog: Open dialog with pre-filled form
    Dialog-->>User: Display form with existing data

    User->>Browser: Modify fields (e.g., change password)
    Browser->>AppState: set_profile_form_password("new_password")

    User->>Browser: Click "Update Profile"
    Browser->>AppState: save_profile_from_form()

    activate AppState
    AppState->>AppState: Check profile_edit_mode == True
    AppState->>AppState: update_profile(kid_name, provider, login, password)

    activate AppState
    AppState->>CredentialManager: save_profile(StudentProfile)

    activate CredentialManager
    CredentialManager->>CredentialManager: load_profiles()
    CredentialManager->>CredentialManager: Find existing profile by kid_name
    CredentialManager->>CredentialManager: Replace with updated profile
    CredentialManager->>CredentialManager: Encrypt profiles list
    CredentialManager->>FileSystem: Write to credentials.json
    CredentialManager-->>AppState: Success
    deactivate CredentialManager

    AppState->>AppState: Increment _profiles_version
    deactivate AppState

    AppState->>AppState: Clear form fields
    AppState->>AppState: profile_edit_mode = False
    AppState->>AppState: profile_edit_kid_name = ""
    AppState-->>Browser: State updated (WebSocket)
    deactivate AppState

    Browser->>Dialog: Close dialog
    Browser->>ProfileCard: Re-render with updated data
    Browser-->>User: Display updated profile card

    Note over User,FileSystem: Updated credentials<br/>encrypted and saved
```

### 12.5 Key Differences: Add vs Edit

| Aspect | Add Mode | Edit Mode |
|--------|----------|-----------|
| Dialog Title | "Add New Student" | "Edit Student Profile" |
| Button Text | "Save Profile" | "Update Profile" |
| Form Pre-fill | Empty fields | Populated with existing data |
| State Flag | `profile_edit_mode = False` | `profile_edit_mode = True` |
| Operation | `add_profile()` | `update_profile()` |
| Validation | Check for duplicate kid_name | Allow same kid_name (updating) |

### 12.6 Edge Cases to Handle

1. **User clicks Edit but profile no longer exists**: Show error message or silently fail
2. **User changes kid_name during edit**: This changes the profile identity - should be prevented or handled carefully
3. **User clicks Cancel**: Clear form and reset `profile_edit_mode`
4. **Multiple rapid clicks on Edit**: Debounce or disable button during operation

---

## 13. Settings View - Delete Profile Flow

**Purpose**: Specification for deleting a student profile (already implemented).

**User Story**: As a parent, I want to remove a student profile when they graduate or change schools.

**Current Implementation**: ✅ **COMPLETE** in `AppState.delete_profile()`

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant ProfileCard
    participant AppState
    participant CredentialManager
    participant FileSystem

    User->>Browser: Click "Delete" icon (trash-2)
    Browser->>ProfileCard: on_click event
    ProfileCard->>AppState: delete_profile("TestKid")

    activate AppState
    AppState->>CredentialManager: delete_profile("TestKid")

    activate CredentialManager
    CredentialManager->>CredentialManager: load_profiles()
    CredentialManager->>FileSystem: Read credentials.json
    CredentialManager->>CredentialManager: Decrypt data
    CredentialManager->>CredentialManager: Filter out profile with kid_name="TestKid"
    CredentialManager->>CredentialManager: Encrypt remaining profiles
    CredentialManager->>FileSystem: Write to credentials.json
    CredentialManager-->>AppState: Success
    deactivate CredentialManager

    AppState->>AppState: Increment _profiles_version
    AppState-->>Browser: State updated (WebSocket)
    deactivate AppState

    Browser->>Browser: Re-render triggered
    Browser->>AppState: get_profiles (computed)

    activate AppState
    AppState->>CredentialManager: load_profiles()
    CredentialManager-->>AppState: Updated list (without deleted profile)
    AppState-->>Browser: Profiles without passwords
    deactivate AppState

    Browser-->>User: Profile card removed from list

    Note over User,FileSystem: No confirmation dialog<br/>(consider adding for safety)
```

**Potential Enhancement**: Add confirmation dialog before deletion
```python
# Future improvement
def confirm_delete_profile(self, kid_name: str):
    """Show confirmation dialog before deleting."""
    self.delete_confirm_kid_name = kid_name
    self.delete_confirm_open = True

def execute_delete_profile(self):
    """Execute the deletion after confirmation."""
    if self.delete_confirm_kid_name:
        self.delete_profile(self.delete_confirm_kid_name)
        self.delete_confirm_kid_name = ""
        self.delete_confirm_open = False
```

---

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `models.py` | DTOs (Pydantic) | Data structure |
| `state.py` | AppState | State management |
| `services/mock_service.py` | Mock data generator | Service layer |
| `services/credential_manager.py` | Encrypted credential storage | Service layer |
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

7. **Security**: Credentials encrypted with Fernet, never sent to frontend
