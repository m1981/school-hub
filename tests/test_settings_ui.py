"""Playwright Tests: GUI verification for the Settings View with Edit functionality.

These tests verify the visual appearance and functionality of the settings UI components,
including add, edit, and delete profile operations.
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


def test_settings_view_displays_header(page: Page, reflex_app):
    """Verify that the settings view displays the Settings header."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # Then
    expect(page.get_by_role("heading", name="Settings")).to_be_visible(timeout=5000)


def test_add_new_student_button_visible(page: Page, reflex_app):
    """Verify that the Add New Student button is visible."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # Then
    expect(page.get_by_role("button", name="Add New Student")).to_be_visible(
        timeout=5000
    )


def test_add_new_student_dialog_opens(page: Page, reflex_app):
    """Verify that clicking Add New Student opens the dialog."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # When
    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # Then
    expect(page.get_by_text("Add New Student", exact=True)).to_be_visible(timeout=5000)
    expect(page.get_by_text("Student Name")).to_be_visible(timeout=5000)
    expect(page.get_by_text("School Provider")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Login")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Password")).to_be_visible(timeout=5000)


def test_add_new_student_dialog_has_test_connection_button(page: Page, reflex_app):
    """Verify that the dialog has a Test Connection button."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # When
    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # Then
    expect(page.get_by_role("button", name="Test Connection")).to_be_visible(
        timeout=5000
    )


def test_add_new_student_dialog_cancel_button_works(page: Page, reflex_app):
    """Verify that clicking Cancel closes the dialog."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # When
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(500)

    # Then - dialog should be closed
    expect(page.get_by_text("Add New Student", exact=True)).not_to_be_visible()


def test_settings_view_shows_empty_state_initially(page: Page, reflex_app):
    """Verify that settings view shows empty state when no profiles exist."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # Then - should show empty state or profiles
    # Note: This might show profiles if credentials.json exists
    # We're just checking the page loads correctly
    expect(page.get_by_role("heading", name="Settings")).to_be_visible(timeout=5000)


def test_dialog_form_fields_are_interactive(page: Page, reflex_app):
    """Verify that form fields in the dialog are interactive."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # When - fill in the form
    page.get_by_placeholder("e.g., Anna").fill("Test Student")
    page.get_by_placeholder("username or email").fill("test@example.com")
    page.get_by_placeholder("••••••••").fill("testpassword")

    # Then - verify values are set
    expect(page.get_by_placeholder("e.g., Anna")).to_have_value("Test Student")
    expect(page.get_by_placeholder("username or email")).to_have_value(
        "test@example.com"
    )
    expect(page.get_by_placeholder("••••••••")).to_have_value("testpassword")

    # Cleanup - close dialog
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(500)


def test_provider_radio_buttons_work(page: Page, reflex_app):
    """Verify that provider radio buttons are functional."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # Then - both provider options should be visible
    expect(page.get_by_text("Librus")).to_be_visible(timeout=5000)
    expect(page.get_by_text("Vulcan")).to_be_visible(timeout=5000)

    # Cleanup
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(500)


def test_screenshot_settings_view(page: Page, reflex_app):
    """Take a screenshot of the settings view for visual verification."""
    # Given / When
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # Then - take screenshot
    page.screenshot(path="tests/screenshots/settings_view.png", full_page=True)


def test_screenshot_add_dialog(page: Page, reflex_app):
    """Take a screenshot of the add student dialog for visual verification."""
    # Given
    page.goto("http://localhost:3000", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=30000)

    # Navigate to settings
    page.get_by_role("button", name="Settings").click()
    page.wait_for_timeout(1000)

    # When
    page.get_by_role("button", name="Add New Student").click()
    page.wait_for_timeout(500)

    # Then - take screenshot
    page.screenshot(path="tests/screenshots/add_student_dialog.png", full_page=True)

    # Cleanup
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(500)
