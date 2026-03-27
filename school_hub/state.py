"""Application State for School Hub.

This module contains the main Reflex State that manages the application's data and UI state.
Following Reflex best practices, heavy data is stored in backend-only variables (prefixed with _).
"""

from typing import Union
import reflex as rx
from datetime import datetime
from school_hub.models import KidGradesDTO
from school_hub.services.mock_service import MockMonitoringService
from school_hub.services.credential_manager import CredentialManager, StudentProfile
from school_hub.services.connection_tester import ConnectionTester


class AppState(rx.State):
    """Main application state managing UI tabs and student data."""

    # --- UI State (sent to frontend) ---
    current_tab: str = "feed"
    last_synced: str = ""
    calendar_filter_kid: str = "All"
    calendar_filter_event_type: str = "All"
    _profiles_version: int = 0  # Internal counter to invalidate profile cache

    # Profile form state
    profile_form_kid_name: str = ""
    profile_form_provider: str = "Librus"
    profile_form_login: str = ""
    profile_form_password: str = ""

    # Edit mode tracking
    profile_edit_mode: bool = False
    profile_edit_kid_name: str = ""

    # Connection test feedback
    profile_connection_message: str = ""
    profile_connection_success: bool = False

    # --- Backend-only data (NOT sent to frontend - uses _ prefix) ---
    _kids_data: list[KidGradesDTO] = []
    _credential_manager: CredentialManager = None
    _connection_tester: ConnectionTester = None

    def __init__(self, *args, **kwargs):
        """Initialize state and load mock data."""
        super().__init__(*args, **kwargs)
        self._credential_manager = CredentialManager()
        self._connection_tester = ConnectionTester()
        self._load_initial_data()

    def _load_initial_data(self):
        """Load mock data and set initial timestamp."""
        service = MockMonitoringService()
        self._kids_data = service.get_all_data()
        self.last_synced = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def kids_data(self) -> list[KidGradesDTO]:
        """Public property to access kids data."""
        return self._kids_data

    def set_current_tab(self, tab: str):
        """Change the current active tab.

        Args:
            tab: One of 'feed', 'calendar', 'children', 'settings'
        """
        self.current_tab = tab

    def refresh_data(self):
        """Refresh data from the monitoring service and update timestamp."""
        service = MockMonitoringService()
        self._kids_data = service.get_all_data()
        self.last_synced = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.var
    def get_sorted_feed(self) -> list[dict[str, str]]:
        """Get unified feed of grades and news, sorted by date (newest first).

        Returns:
            List of dictionaries with type='grade' or type='news' and all relevant fields
        """
        feed_items = []

        # Collect all grades from all kids
        for kid in self._kids_data:
            for subject in kid.subjects:
                for period in subject.periods:
                    for grade in period.grades:
                        feed_items.append(
                            {
                                "type": "grade",
                                "kid_name": grade.kid_name,
                                "subject_name": grade.subject_name,
                                "value": grade.value,
                                "category": grade.category,
                                "weight": grade.weight,
                                "date": grade.date or "",
                                "date_sort_key": str(grade.date_sort_key),
                                "comment": grade.comment or "",
                                "is_retake": str(grade.is_retake),
                            }
                        )

        # Collect all news from all kids
        for kid in self._kids_data:
            for news in kid.news:
                feed_items.append(
                    {
                        "type": "news",
                        "kid_name": news.kid_name,
                        "sender": news.sender,
                        "subject": news.subject,
                        "content": news.content,
                        "date": news.date,
                        "date_sort_key": str(news.date_sort_key),
                    }
                )

        # Sort by date_sort_key descending (newest first)
        feed_items.sort(key=lambda x: int(x.get("date_sort_key", "0")), reverse=True)

        return feed_items

    @rx.var
    def get_quick_stats(self) -> list[dict[str, str]]:
        """Get quick stats summary for all kids.

        Returns:
            List of dictionaries with kid_name, provider, recent_summary, and avatar
        """
        stats = []

        # Avatar mapping for each kid
        avatars = {
            "Anna": "👧",
            "Ben": "👦",
            "Clara": "👧",
            "David": "👦",
        }

        for kid in self._kids_data:
            # Count recent grades
            grade_count = 0
            for subject in kid.subjects:
                for period in subject.periods:
                    grade_count += len(period.grades)

            # Count news
            news_count = len(kid.news)

            # Build summary
            summary_parts = []
            if grade_count > 0:
                summary_parts.append(
                    f"{grade_count} Grade{'s' if grade_count != 1 else ''}"
                )
            if news_count > 0:
                summary_parts.append(f"{news_count} News")

            recent_summary = ", ".join(summary_parts) if summary_parts else "No Updates"

            stats.append(
                {
                    "kid_name": kid.kid_name,
                    "provider": kid.provider,
                    "recent_summary": recent_summary,
                    "avatar": avatars.get(kid.kid_name, "👤"),
                }
            )

        return stats

    @rx.var
    def get_all_calendar_events(self) -> list[dict[str, str]]:
        """Get all calendar events from all kids, sorted by date (oldest first).

        Returns:
            List of dictionaries with all calendar event fields
        """
        events = []

        # Collect all calendar events from all kids
        for kid in self._kids_data:
            for event in kid.calendar_events:
                events.append(
                    {
                        "kid_name": event.kid_name,
                        "date_sort_key": str(event.date_sort_key),
                        "display_date": event.display_date,
                        "time_range": event.time_range,
                        "room": event.room,
                        "subject": event.subject,
                        "event_type": event.event_type,
                        "description": event.description,
                        "teacher": event.teacher,
                        "color_theme": event.color_theme,
                    }
                )

        # Sort by date_sort_key ascending (oldest first for calendar view)
        events.sort(key=lambda x: int(x.get("date_sort_key", "0")))

        return events

    @rx.var
    def get_filtered_calendar_events(self) -> list[dict[str, str]]:
        """Get calendar events filtered by kid and event type.

        Returns:
            Filtered list of calendar events
        """
        events = self.get_all_calendar_events

        # Filter by kid name
        if self.calendar_filter_kid != "All":
            events = [e for e in events if e["kid_name"] == self.calendar_filter_kid]

        # Filter by event type
        if self.calendar_filter_event_type != "All":
            events = [
                e for e in events if e["event_type"] == self.calendar_filter_event_type
            ]

        return events

    @rx.var
    def get_grouped_calendar_events(
        self,
    ) -> list[dict[str, Union[str, list[dict[str, str]]]]]:
        """Group filtered calendar events by display_date.

        Returns:
            List of dictionaries with 'date' and 'events' keys
        """
        events = self.get_filtered_calendar_events
        grouped = {}

        # Group events by display_date
        for event in events:
            date = event["display_date"]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(event)

        # Convert to list format
        result = [{"date": date, "events": events} for date, events in grouped.items()]

        return result

    @rx.var
    def get_calendar_events_with_headers(self) -> list[dict[str, str]]:
        """Get calendar events with date headers flattened for single foreach.

        Returns:
            Flattened list where first event of each date has show_date_header='true'
        """
        events = self.get_filtered_calendar_events
        if not events:
            return []

        result = []
        last_date = None

        for event in events:
            current_date = event["display_date"]
            # Add flag to show date header for first event of each date
            event_copy = event.copy()
            event_copy["show_date_header"] = (
                "true" if current_date != last_date else "false"
            )
            result.append(event_copy)
            last_date = current_date

        return result

    def set_calendar_filter_kid(self, kid_name: str):
        """Set the calendar filter for kid name.

        Args:
            kid_name: Kid name to filter by, or "All" for no filter
        """
        self.calendar_filter_kid = kid_name

    def set_calendar_filter_event_type(self, event_type: str):
        """Set the calendar filter for event type.

        Args:
            event_type: Event type to filter by, or "All" for no filter
        """
        self.calendar_filter_event_type = event_type

    # --- Profile Management Methods ---

    @rx.var
    def get_profiles(self) -> list[dict[str, str]]:
        """Get all student profiles for UI display (without passwords).

        Returns:
            List of profile dictionaries with kid_name, provider, and login (NO passwords)
        """
        # Access _profiles_version to make this computed var depend on it
        _ = self._profiles_version

        profiles = self._credential_manager.load_profiles()
        # Return profiles without passwords for security
        return [
            {
                "kid_name": profile.kid_name,
                "provider": profile.provider,
                "login": profile.login,
            }
            for profile in profiles
        ]

    def add_profile(self, kid_name: str, provider: str, login: str, password: str):
        """Add a new student profile.

        Args:
            kid_name: Name of the student
            provider: Provider name ("Librus" or "Vulcan")
            login: Login username/email
            password: Login password
        """
        profile = StudentProfile(
            kid_name=kid_name, provider=provider, login=login, password=password
        )
        self._credential_manager.save_profile(profile)
        # Increment version to invalidate cached computed var
        self._profiles_version += 1

    def update_profile(self, kid_name: str, provider: str, login: str, password: str):
        """Update an existing student profile.

        Args:
            kid_name: Name of the student (used as identifier)
            provider: Provider name ("Librus" or "Vulcan")
            login: Login username/email
            password: Login password
        """
        profile = StudentProfile(
            kid_name=kid_name, provider=provider, login=login, password=password
        )
        self._credential_manager.save_profile(profile)
        # Increment version to invalidate cached computed var
        self._profiles_version += 1

    def delete_profile(self, kid_name: str):
        """Delete a student profile.

        Args:
            kid_name: Name of the student whose profile should be deleted
        """
        self._credential_manager.delete_profile(kid_name)

        # Increment version to invalidate cached computed var
        self._profiles_version += 1

    # --- Profile Form Handlers ---

    def set_profile_form_kid_name(self, value: str):
        """Set the kid name in the profile form."""
        self.profile_form_kid_name = value

    def set_profile_form_provider(self, value: str):
        """Set the provider in the profile form."""
        self.profile_form_provider = value

    def set_profile_form_login(self, value: str):
        """Set the login in the profile form."""
        self.profile_form_login = value

    def set_profile_form_password(self, value: str):
        """Set the password in the profile form."""
        self.profile_form_password = value

    def save_profile_from_form(self):
        """Save the profile from the form data (handles both add and edit modes).

        Tests connection before saving. Only saves if connection test passes.
        """
        if (
            self.profile_form_kid_name
            and self.profile_form_login
            and self.profile_form_password
        ):
            # Test connection first
            success, message = self._connection_tester.test_connection(
                provider=self.profile_form_provider,
                login=self.profile_form_login,
                password=self.profile_form_password,
                kid_name=self.profile_form_kid_name,
            )

            # Update connection feedback
            self.profile_connection_success = success
            self.profile_connection_message = message

            # Only save if connection test passed
            if not success:
                return

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
            self.profile_connection_message = ""
            self.profile_connection_success = False

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
            self.profile_form_password = profile.password

            # Set edit mode
            self.profile_edit_mode = True
            self.profile_edit_kid_name = kid_name

    def cancel_profile_form(self):
        """Cancel the form and reset all state."""
        self.profile_form_kid_name = ""
        self.profile_form_provider = "Librus"
        self.profile_form_login = ""
        self.profile_form_password = ""
        self.profile_edit_mode = False
        self.profile_edit_kid_name = ""
        self.profile_connection_message = ""
        self.profile_connection_success = False

    def test_profile_connection(self):
        """Test the connection with current form data without saving."""
        # Validate required fields
        if (
            not self.profile_form_kid_name
            or not self.profile_form_login
            or not self.profile_form_password
        ):
            self.profile_connection_message = (
                "Please fill in all fields before testing connection."
            )
            self.profile_connection_success = False
            return

        # Test connection
        success, message = self._connection_tester.test_connection(
            provider=self.profile_form_provider,
            login=self.profile_form_login,
            password=self.profile_form_password,
            kid_name=self.profile_form_kid_name,
        )

        # Update connection feedback
        self.profile_connection_success = success
        self.profile_connection_message = message
