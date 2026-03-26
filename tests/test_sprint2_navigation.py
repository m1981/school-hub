"""Sprint 2 Tests: Reflex UI Shell & Navigation.
TDD Red phase – these tests define expected behaviour before implementation.
"""

import pytest
import reflex as rx
from school_hub.state import AppState


# ---------------------------------------------------------------------------
# AppState tab navigation tests
# ---------------------------------------------------------------------------


def test_app_state_default_tab_is_feed():
    """AppState should initialize with 'feed' as the default current_tab."""
    # Given / When
    state = AppState()
    # Then
    assert state.current_tab == "feed"


def test_app_state_can_change_tab():
    """AppState should allow changing the current_tab."""
    # Given
    state = AppState()
    # When
    state.set_current_tab("calendar")
    # Then
    assert state.current_tab == "calendar"


def test_app_state_valid_tab_values():
    """AppState should support all valid tab values: feed, calendar, children, settings."""
    # Given
    state = AppState()
    valid_tabs = ["feed", "calendar", "children", "settings"]
    
    # When / Then
    for tab in valid_tabs:
        state.set_current_tab(tab)
        assert state.current_tab == tab


def test_app_state_loads_mock_data_on_init():
    """AppState should load mock data from MockMonitoringService on initialization."""
    # Given / When
    state = AppState()
    # Then
    assert len(state.kids_data) == 4
    assert state.kids_data[0].kid_name in ["Anna", "Ben", "Clara", "David"]


def test_app_state_has_last_synced_timestamp():
    """AppState should track the last sync timestamp."""
    # Given / When
    state = AppState()
    # Then
    assert state.last_synced is not None
    assert isinstance(state.last_synced, str)
    assert len(state.last_synced) > 0


def test_app_state_refresh_data_updates_timestamp():
    """AppState.refresh_data() should update the last_synced timestamp."""
    # Given
    state = AppState()
    original_timestamp = state.last_synced

    # When
    import time
    time.sleep(1.1)  # Wait just over 1 second to ensure timestamp changes
    state.refresh_data()

    # Then
    assert state.last_synced != original_timestamp


def test_app_state_kids_data_is_backend_only():
    """Verify that _kids_data uses underscore prefix (backend-only variable)."""
    # Given / When
    state = AppState()
    
    # Then - check that we have the backend variable
    assert hasattr(state, "_kids_data")
    # And the public property
    assert hasattr(state, "kids_data")

