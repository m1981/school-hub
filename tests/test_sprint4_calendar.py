"""Sprint 4: Calendar View & Filtering - Unit Tests.

Tests for calendar event filtering logic and data aggregation.
Following TDD principles: Write tests first, then implement.
"""

import pytest

from school_hub.state import AppState
from school_hub.services.mock_service import MockMonitoringService

pytestmark = pytest.mark.unit


class TestCalendarFiltering:
    """Test calendar filtering logic."""

    def test_get_all_calendar_events_returns_list(self):
        """Should return a list of all calendar events from all kids."""
        # Given
        state = AppState()

        # When
        events = state.get_all_calendar_events

        # Then
        assert isinstance(events, list)
        assert len(events) > 0

    def test_calendar_events_have_required_fields(self):
        """Should return events with all required fields."""
        # Given
        state = AppState()

        # When
        events = state.get_all_calendar_events

        # Then
        if len(events) > 0:
            event = events[0]
            assert "kid_name" in event
            assert "date_sort_key" in event
            assert "display_date" in event
            assert "time_range" in event
            assert "room" in event
            assert "subject" in event
            assert "event_type" in event
            assert "description" in event
            assert "teacher" in event
            assert "color_theme" in event

    def test_calendar_events_sorted_by_date(self):
        """Should return events sorted by date_sort_key (oldest first for calendar)."""
        # Given
        state = AppState()

        # When
        events = state.get_all_calendar_events

        # Then
        if len(events) > 1:
            for i in range(len(events) - 1):
                current_key = int(events[i]["date_sort_key"])
                next_key = int(events[i + 1]["date_sort_key"])
                assert current_key <= next_key, (
                    "Events should be sorted chronologically"
                )

    def test_filter_calendar_by_kid_name(self):
        """Should filter events by specific kid name."""
        # Given
        state = AppState()
        state.calendar_filter_kid = "Anna"

        # When
        events = state.get_filtered_calendar_events

        # Then
        for event in events:
            assert event["kid_name"] == "Anna"

    def test_filter_calendar_by_event_type(self):
        """Should filter events by specific event type."""
        # Given
        state = AppState()
        state.calendar_filter_event_type = "Sprawdzian"

        # When
        events = state.get_filtered_calendar_events

        # Then
        for event in events:
            assert event["event_type"] == "Sprawdzian"

    def test_filter_calendar_by_both_kid_and_event_type(self):
        """Should filter events by both kid name and event type."""
        # Given
        state = AppState()
        state.calendar_filter_kid = "Ben"
        state.calendar_filter_event_type = "Kartkówka"

        # When
        events = state.get_filtered_calendar_events

        # Then
        for event in events:
            assert event["kid_name"] == "Ben"
            assert event["event_type"] == "Kartkówka"

    def test_filter_all_shows_all_events(self):
        """Should show all events when filters are set to 'All'."""
        # Given
        state = AppState()
        state.calendar_filter_kid = "All"
        state.calendar_filter_event_type = "All"

        # When
        filtered_events = state.get_filtered_calendar_events
        all_events = state.get_all_calendar_events

        # Then
        assert len(filtered_events) == len(all_events)

    def test_set_calendar_filter_kid(self):
        """Should update calendar kid filter."""
        # Given
        state = AppState()

        # When
        state.set_calendar_filter_kid("Clara")

        # Then
        assert state.calendar_filter_kid == "Clara"

    def test_set_calendar_filter_event_type(self):
        """Should update calendar event type filter."""
        # Given
        state = AppState()

        # When
        state.set_calendar_filter_event_type("Zadania")

        # Then
        assert state.calendar_filter_event_type == "Zadania"

    def test_get_grouped_calendar_events(self):
        """Should group events by display_date."""
        # Given
        state = AppState()

        # When
        grouped = state.get_grouped_calendar_events

        # Then
        assert isinstance(grouped, list)
        # Each group should have a date and events list
        for group in grouped:
            assert "date" in group
            assert "events" in group
            assert isinstance(group["events"], list)


class TestCalendarMockData:
    """Test that mock service provides calendar events."""

    def test_mock_service_provides_calendar_events(self):
        """Should ensure mock service includes calendar events for all kids."""
        # Given
        service = MockMonitoringService()

        # When
        kids_data = service.get_all_data()

        # Then
        assert len(kids_data) == 4
        # At least some kids should have calendar events
        total_events = sum(len(kid.calendar_events) for kid in kids_data)
        assert total_events > 0, "Mock service should provide calendar events"

    def test_calendar_events_have_valid_data(self):
        """Should ensure calendar events have valid, non-empty data."""
        # Given
        service = MockMonitoringService()

        # When
        kids_data = service.get_all_data()

        # Then
        for kid in kids_data:
            for event in kid.calendar_events:
                assert event.kid_name == kid.kid_name
                assert event.date_sort_key > 0
                assert len(event.display_date) > 0
                assert len(event.subject) > 0
                assert len(event.event_type) > 0
