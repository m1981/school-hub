"""Sprint 3 Playwright Tests: GUI verification for the Feed View.

These tests verify the visual appearance and functionality of the feed UI components.
"""

import pytest
from playwright.sync_api import Page, expect
import subprocess
import time

pytestmark = [pytest.mark.ui, pytest.mark.slow]


@pytest.fixture(scope="module")
def reflex_app():
    """Start the Reflex app before tests and stop it after."""
    # Start Reflex in production mode
    process = subprocess.Popen(
        ["uv", "run", "reflex", "run", "--loglevel", "warning"],
        cwd="/Users/michal/PycharmProjects/school-hub",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start (check for port 3000)
    time.sleep(15)  # Give it time to compile and start

    yield process

    # Cleanup
    process.terminate()
    process.wait()


def test_feed_view_displays_header(page: Page, reflex_app):
    """Verify that the feed view displays the School Hub header."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Then
    expect(page.get_by_role("heading", name="School Hub")).to_be_visible(timeout=5000)


def test_feed_view_displays_quick_stats(page: Page, reflex_app):
    """Verify that quick stats cards are visible with kid names."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Then - should show all 4 kids
    expect(page.get_by_text("Anna")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Ben")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Clara")).to_be_visible(timeout=5000)
    expect(page.get_by_text("David")).to_be_visible(timeout=5000)

    # Take screenshot for verification
    page.screenshot(path="tests/screenshots/feed_quick_stats.png", full_page=True)


def test_feed_view_displays_recent_activity(page: Page, reflex_app):
    """Verify that the Recent Activity section is visible."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Then
    expect(page.get_by_role("heading", name="Recent Activity")).to_be_visible(
        timeout=5000
    )

    # Take screenshot
    page.screenshot(path="tests/screenshots/feed_recent_activity.png", full_page=True)


def test_bottom_navigation_visible(page: Page, reflex_app):
    """Verify that bottom navigation bar is visible with all tabs."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Then - check all tabs are visible
    expect(page.get_by_text("Feed")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Calendar")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Children")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Settings")).to_be_visible(timeout=5000)

    # Take screenshot
    page.screenshot(path="tests/screenshots/bottom_navigation.png", full_page=True)


def test_feed_cards_display_data(page: Page, reflex_app):
    """Verify that feed cards display grade and news data."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Then - check for badge text (grades)
    page.wait_for_selector("text=Grade:", timeout=5000)

    # Take full page screenshot
    page.screenshot(path="tests/screenshots/feed_full_page.png", full_page=True)
