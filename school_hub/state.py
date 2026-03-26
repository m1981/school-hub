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

