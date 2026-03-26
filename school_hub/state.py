"""Application State for School Hub.

This module contains the main Reflex State that manages the application's data and UI state.
Following Reflex best practices, heavy data is stored in backend-only variables (prefixed with _).
"""

import reflex as rx
from datetime import datetime
from school_hub.models import KidGradesDTO
from school_hub.services.mock_service import MockMonitoringService


class AppState(rx.State):
    """Main application state managing UI tabs and student data."""
    
    # --- UI State (sent to frontend) ---
    current_tab: str = "feed"
    last_synced: str = ""
    
    # --- Backend-only data (NOT sent to frontend - uses _ prefix) ---
    _kids_data: list[KidGradesDTO] = []
    
    def __init__(self, *args, **kwargs):
        """Initialize state and load mock data."""
        super().__init__(*args, **kwargs)
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
                        feed_items.append({
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
                        })

        # Collect all news from all kids
        for kid in self._kids_data:
            for news in kid.news:
                feed_items.append({
                    "type": "news",
                    "kid_name": news.kid_name,
                    "sender": news.sender,
                    "subject": news.subject,
                    "content": news.content,
                    "date": news.date,
                    "date_sort_key": str(news.date_sort_key),
                })

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
                summary_parts.append(f"{grade_count} Grade{'s' if grade_count != 1 else ''}")
            if news_count > 0:
                summary_parts.append(f"{news_count} News")

            recent_summary = ", ".join(summary_parts) if summary_parts else "No Updates"

            stats.append({
                "kid_name": kid.kid_name,
                "provider": kid.provider,
                "recent_summary": recent_summary,
                "avatar": avatars.get(kid.kid_name, "👤"),
            })

        return stats

