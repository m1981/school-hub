"""Sprint 3 Tests: The "School Hub" Feed (UI Binding).
TDD Red phase – these tests define expected behaviour before implementation.
"""

import pytest

from school_hub.state import AppState

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# AppState feed methods tests
# ---------------------------------------------------------------------------


def test_get_sorted_feed_returns_list():
    """AppState.get_sorted_feed should return a list of feed items."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    # Then
    assert isinstance(feed, list)


def test_get_sorted_feed_merges_grades_and_news():
    """Feed should contain both grades and news from all kids."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    # Then - should have items from both grades and news
    assert len(feed) > 0
    # Check that we have both types in the feed
    has_grades = any(item.get("type") == "grade" for item in feed)
    has_news = any(item.get("type") == "news" for item in feed)
    assert has_grades, "Feed should contain grades"
    assert has_news, "Feed should contain news"


def test_get_sorted_feed_is_sorted_by_date():
    """Feed items should be sorted by date_sort_key (newest first)."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    # Then - verify descending order
    for i in range(len(feed) - 1):
        current_key = int(feed[i].get("date_sort_key", "0"))
        next_key = int(feed[i + 1].get("date_sort_key", "0"))
        assert current_key >= next_key, (
            f"Feed not sorted: {current_key} should be >= {next_key}"
        )


def test_get_sorted_feed_includes_all_kids():
    """Feed should include items from all 4 kids."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    kids_in_feed = {item.get("kid_name") for item in feed}
    # Then
    assert "Anna" in kids_in_feed
    assert "Ben" in kids_in_feed
    assert "Clara" in kids_in_feed
    assert "David" in kids_in_feed


def test_get_sorted_feed_grade_item_structure():
    """Grade items in feed should have required fields."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    grade_items = [item for item in feed if item.get("type") == "grade"]
    # Then - check first grade item structure
    assert len(grade_items) > 0, "Should have at least one grade"
    grade = grade_items[0]
    assert "kid_name" in grade
    assert "subject_name" in grade
    assert "value" in grade
    assert "category" in grade
    assert "date" in grade
    assert "date_sort_key" in grade
    assert "type" in grade


def test_get_sorted_feed_news_item_structure():
    """News items in feed should have required fields."""
    # Given
    state = AppState()
    # When
    feed = state.get_sorted_feed
    news_items = [item for item in feed if item.get("type") == "news"]
    # Then - check first news item structure
    assert len(news_items) > 0, "Should have at least one news item"
    news = news_items[0]
    assert "kid_name" in news
    assert "sender" in news
    assert "subject" in news
    assert "content" in news
    assert "date" in news
    assert "date_sort_key" in news
    assert "type" in news


def test_get_quick_stats_returns_all_kids():
    """AppState.get_quick_stats should return stats for all 4 kids."""
    # Given
    state = AppState()
    # When
    stats = state.get_quick_stats
    # Then
    assert len(stats) == 4
    names = [s["kid_name"] for s in stats]
    assert "Anna" in names
    assert "Ben" in names
    assert "Clara" in names
    assert "David" in names


def test_get_quick_stats_includes_recent_updates():
    """Each kid's stats should include a summary of recent updates."""
    # Given
    state = AppState()
    # When
    stats = state.get_quick_stats
    # Then - each stat should have required fields
    for stat in stats:
        assert "kid_name" in stat
        assert "provider" in stat
        assert "recent_summary" in stat  # e.g., "2 Grades, 1 News"
        assert "avatar" in stat  # emoji or icon
