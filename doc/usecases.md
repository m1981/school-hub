# Unified School Monitoring Platform - Specification

## Section 1: Domain Understanding & Glossary
**Context:** A locally hosted, unified dashboard built with the Reflex framework to aggregate school data for a family with 4 children. The children's schools utilize two different Polish school management systems: Librus and Vulcan.
**Core Value Proposition:** Eliminates the daily friction of logging into multiple accounts across different platforms. Provides parents with a single, consolidated, and fast "pane of glass" to monitor grades, attendance, timetables, and school news for all their children simultaneously.

### Domain Glossary
| Term | Definition |
| :--- | :--- |
| **Provider** | The external school management system (specifically Librus or Vulcan). |
| **Student Profile** | A local representation of a specific child, linked to one or more Provider accounts. |
| **Unified Dashboard** | The primary aggregated view showing recent activity (grades, messages, schedule) across all Student Profiles. |
| **Sync Engine** | The background process responsible for authenticating with Providers and fetching/scraping the latest data. |
| **School Event** | A generic term for any actionable data point fetched from a Provider (e.g., a new grade, an unread message, a timetable change). |

## Section 2: Business Rules & Constraints
*   **BR-1 (Local Caching):** To prevent account lockouts and reduce latency, data fetched from Providers must be cached locally. The UI reads from the local cache, not directly from the Providers.
*   **BR-2 (Read-Only Interaction):** The platform is strictly for monitoring. Actions that alter state on the Provider side (e.g., sending a message to a teacher, signing an excuse note) must be performed in the native Provider applications.
*   **BR-3 (Credential Security):** Provider credentials must be stored securely (encrypted) on the local host machine.
*   **Constraint-1 (Technology Stack):** The application (both frontend UI and backend logic) must be built entirely in Python using the Reflex framework.
*   **Constraint-2 (Deployment):** The system is designed for local network deployment (e.g., home server, local PC) and does not require public internet ingress.

## Section 3: Scope Definition (In/Out List)
| Topic | In | Out |
| :--- | :--- | :--- |
| Aggregation of grades, attendance, and timetables | X | |
| Aggregation of school news and unread messages | X | |
| Multi-child unified dashboard view | X | |
| Local caching and background data synchronization | X | |
| Sending messages to teachers or school staff | | X |
| Modifying attendance (e.g., writing excuse notes) | | X |
| Cloud hosting or multi-tenant SaaS architecture | | X |

## Section 4: Actor-Goal List
| Primary Actor | User-Level Goal |
| :--- | :--- |
| **Parent** | View unified daily summary for all children. |
| **Parent** | View detailed academic status for a specific child. |
| **Parent** | Manage Student Profiles and Provider credentials. |
| **Parent** | Manually trigger a data synchronization. |
| **Sync Engine (System)** | Fetch and normalize data from Providers on a schedule. |

---

## Section 5: Fully Dressed Use Cases

### Use Case 1: View Unified Daily Summary
*   **Primary Actor:** Parent
*   **Scope:** Unified School Monitoring Platform
*   **Level:** User Goal
*   **Stakeholders & Interests:**
    *   *Parent:* Wants a quick, at-a-glance understanding of any new grades, upcoming tests, or unread messages across all 4 children without switching contexts.
*   **Preconditions:** Parent is accessing the local application. At least one Student Profile is configured with valid Provider credentials. Initial data sync has occurred.
*   **Minimal Guarantees:** System displays the last known cached state of the data with a timestamp of the last successful sync.
*   **Success Guarantees:** System presents an aggregated, chronological view of recent School Events for all configured children.
*   **Trigger:** Parent navigates to the application's main dashboard.

**Main Success Scenario (MSS):**
1. Parent requests the unified dashboard.
2. System retrieves the latest cached School Events (grades, messages, timetable changes) for all active Student Profiles.
3. System sorts and formats the data into a unified timeline, grouped by child.
4. System presents the unified dashboard to the Parent.

**Extensions:**
*   **2a. Stale Data Detected:**
    *   2a1. System detects that the local cache is older than the defined refresh threshold.
    *   2a2. System initiates a background sync via the *Sync Engine*.
    *   2a3. System displays the currently cached data with a "Syncing..." indicator and continues to step 3.
*   **2b. No Profiles Configured:**
    *   2b1. System detects zero active Student Profiles.
    *   2b2. System prompts Parent to execute "Manage Student Profiles".
    *   2b3. Use case ends.


### Use Case 2: Manage Student Profiles
*   **Primary Actor:** Parent
*   **Scope:** Unified School Monitoring Platform
*   **Level:** User Goal
*   **Stakeholders & Interests:**
    *   *Parent:* Wants to add, update, or remove children and their associated Librus/Vulcan login details securely.
*   **Preconditions:** Parent is accessing the local application.
*   **Minimal Guarantees:** Existing valid credentials are not overwritten unless explicitly confirmed.
*   **Success Guarantees:** System securely stores the updated credentials and associates them with the correct child's profile.
*   **Trigger:** Parent requests to manage profiles/settings.

**Main Success Scenario (MSS):**
1. Parent requests to add a new Student Profile.
2. System requests child's name, Provider selection (Librus or Vulcan), and Provider credentials.
3. Parent provides the requested profile and credential data.
4. System validates the credentials by attempting a test authentication with the selected Provider.
5. System encrypts and saves the credentials locally based on *BR-3*.
6. System confirms successful profile creation to the Parent.
7. System triggers an initial data sync for the new profile.

**Extensions:**
*   **1a. Update Existing Profile:**
    *   1a1. Parent requests to update an existing profile (e.g., password changed).
    *   1a2. System requests new credentials.
    *   1a3. Return to MSS Step 3.
*   **4a. Authentication Failure:**
    *   4a1. System fails to authenticate with the Provider (invalid username/password or Provider outage).
    *   4a2. System alerts the Parent of the failure.
    *   4a3. System prompts Parent to re-enter credentials or cancel.
    *   4a4. Return to MSS Step 3.

**Technology and Data Variations:**
*   **Step 4:** Vulcan and Librus require entirely different authentication payloads and endpoints. The System abstracts this complexity behind a unified validation interface.


### Use Case 3: View Detailed Academic Status
*   **Primary Actor:** Parent
*   **Scope:** Unified School Monitoring Platform
*   **Level:** User Goal
*   **Stakeholders & Interests:**
    *   *Parent:* Wants to examine the specific details of one child's performance, such as viewing all grades for a specific subject, checking attendance percentages, or seeing the full weekly timetable, without navigating the provider's native interface.
*   **Preconditions:** Parent is accessing the local application. The target Student Profile has successfully synchronized data at least once.
*   **Minimal Guarantees:** The system displays the child's basic identity information and the timestamp of the last successful data sync.
*   **Success Guarantees:** The system presents a segmented, detailed view of the selected child's grades (organized by subject), attendance statistics, and current timetable based on local cache.
*   **Trigger:** Parent selects a specific child's avatar or name from the unified dashboard or children list.

**Main Success Scenario (MSS):**
1. Parent requests the detailed view for a specific child.
2. System retrieves all cached academic data related to the selected Student Profile.
3. System groups individual grades by subject and calculates temporary current averages based on *Local Grade Average Rules*.
4. System compiles attendance data into summary statistics (e.g., present percentage, unexcused absences count).
5. System presents the detailed academic data segmented by category (Grades, Attendance, Timetable) to the Parent.

**Extensions:**
*   **2a. Data Corruption Detected:**
    *   2a1. System encounters errors reading the cached data structure for that child.
    *   2a2. System flags the profile as requiring a full re-sync.
    *   2a3. System initiates a background sync via the *Sync Engine*.
    *   2a4. System informs the Parent that data is regenerating and unavailable momentarily.
    *   2a5. Use case ends.
*   **3a. Non-Standard Grade Formats:**
    *   3a1. System encounters grade data that cannot be numerically averaged (e.g., descriptive feedback only).
    *   3a2. System bypasses the average calculation for that specific subject.
    *   3a3. System displays raw grade entries only for that subject and continues to MSS Step 4.

**Technology and Data Variations:**
*   **Step 2:** The depth of available data depends on the Provider. Librus might provide different attendance details than Vulcan. The system normalizes these into a generic local data structure for display.
*   **Step 3:** *Local Grade Average Rules* are defined within the application to approximate the student's standing, as official averages are often complex calculations performed only on the Provider's servers at the end of a term. The local average is an *estimate* for monitoring purposes.


Here is the fully dressed use case for the background synchronization process. As a commercial-grade developer, I treat this as a critical system-level use case. Background syncs are often the most fragile part of an aggregation app because external APIs change or rate-limit you.

Notice how I reference external rules like *Rate Limiting Policy* and *Unified Event Schema* to keep the steps clean (Hub-and-Spoke model).

***

### Use Case 4: Execute Background Data Synchronization
*   **Primary Actor:** Sync Engine (System)
*   **Scope:** Unified School Monitoring Platform
*   **Level:** System Goal / Subfunction
*   **Stakeholders & Interests:**
    *   *Parent:* Wants the dashboard to load instantly with fresh data without waiting for real-time scraping.
    *   *Providers (Librus/Vulcan):* Require respectful polling to prevent server strain and IP bans.
*   **Preconditions:** The application backend is running. At least one Student Profile is configured with valid credentials. The host machine has active internet access.
*   **Minimal Guarantees:** Existing cached data remains intact and available to the UI if the synchronization process fails or is interrupted. Sync errors are logged locally.
*   **Success Guarantees:** The local data cache is updated with the latest grades, messages, attendance, and timetable changes. The system "Last Synced" timestamp is updated.
*   **Trigger:** The internal system scheduler reaches the defined *Sync Interval* (e.g., every 30 minutes during school hours) OR the Parent manually requests a refresh from the UI.

**Main Success Scenario (MSS):**
1. System identifies all active Student Profiles requiring synchronization based on the *Rate Limiting Policy*.
2. System retrieves and decrypts the Provider credentials for the target profiles.
3. System authenticates a secure session with the respective Provider (Librus or Vulcan) for each profile.
4. System fetches the raw current state of grades, timetable, attendance, and messages.
5. System normalizes the disparate raw Provider data into the standard *Unified Event Schema*.
6. System compares the normalized data against the local cache to identify new, modified, or deleted records.
7. System commits the differences to the local cache and updates the global "Last Synced" timestamp.

**Extensions:**
*   **3a. Authentication Rejected (e.g., password changed externally):**
    *   3a1. System detects an unauthorized response from the Provider.
    *   3a2. System flags the specific Student Profile as "Authentication Failed".
    *   3a3. System generates a system alert for the Parent.
    *   3a4. System skips to the next available Student Profile (Return to MSS Step 2).
*   **4a. Provider Unreachable or Timeout:**
    *   4a1. System fails to establish a connection or times out during data retrieval.
    *   4a2. System logs a temporary network error.
    *   4a3. System aborts the sync for the current profile and applies an exponential backoff for the next retry attempt based on the *Rate Limiting Policy*.
*   **5a. Unrecognized Data Structure (Provider API/UI update):**
    *   5a1. System fails to parse the fetched data because the Provider altered their underlying HTML or API response format.
    *   5a2. System logs a critical parser error.
    *   5a3. System discards the malformed payload to protect the integrity of the local cache.
    *   5a4. System alerts the Parent that the Provider integration requires a developer update.

**Technology and Data Variations:**
*   **Step 1:** In a Reflex framework architecture, this is typically handled by an `asyncio` background task managed by the Reflex state, rather than an OS-level CRON job.
*   **Step 3 & 4:** Data retrieval strategies vary heavily. Vulcan may expose a structured JSON API, whereas Librus may require authenticated HTTP requests simulating browser behavior and subsequent HTML DOM parsing (scraping) using libraries like `BeautifulSoup` or `lxml`.
*   **Step 5:** Normalization involves mapping provider-specific enums (e.g., Librus's attendance codes vs. Vulcan's attendance codes) into a single unified set of enums understood by the Reflex frontend.

***

### Developer Notes (The "Spokes"):
If we were building out the full technical specification document, the capitalized terms above would link to these definitions:
*   **Rate Limiting Policy:** A business rule dictating that the System must not ping Librus/Vulcan more than once every 15 minutes per account, and adds a random jitter of 1-45 seconds between requests to avoid bot detection.
*   **Unified Event Schema:** The internal Python `pydantic` or Reflex `rx.Model` data class definition that ensures a "Grade" looks the exact same to the UI regardless of whether it came from Librus or Vulcan.
