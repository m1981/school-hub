"""Connection Tester for Librus/Vulcan credentials validation.

This module provides functionality to test if credentials are valid by attempting
to login and checking if the student name appears in the loaded page content.
"""

from typing import Tuple
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class ConnectionTester:
    """Tests connection to Librus/Vulcan and validates credentials."""

    def __init__(self, timeout: int = 30000):
        """Initialize the connection tester.

        Args:
            timeout: Maximum time to wait for operations in milliseconds (default: 30000)
        """
        self.timeout = timeout

    def test_librus_connection(
        self, login: str, password: str, kid_name: str
    ) -> Tuple[bool, str]:
        """Test Librus connection and verify student name appears in the page.

        Args:
            login: Librus login username/email
            password: Librus password
            kid_name: Expected student name to find in the page

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Librus login page
                page.goto("https://synergia.librus.pl/loguj", timeout=self.timeout)

                # Fill in credentials
                page.fill('input[name="login"]', login)
                page.fill('input[name="passwd"]', password)

                # Click login button
                page.click('button[type="submit"]')

                # Wait for navigation after login
                page.wait_for_load_state("networkidle", timeout=self.timeout)

                # Get page content
                content = page.content()

                # Close browser
                browser.close()

                # Check if student name appears in the content
                if self._check_student_name_in_content(content, kid_name):
                    return True, "Connection successful! Student name found in page."
                else:
                    return (
                        False,
                        f"Login succeeded but student name '{kid_name}' not found in page. Please verify the student name.",
                    )

        except PlaywrightTimeoutError:
            return False, "Connection timeout. Please check your internet connection."
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

    def test_vulcan_connection(
        self, login: str, password: str, kid_name: str
    ) -> Tuple[bool, str]:
        """Test Vulcan connection and verify student name appears in the page.

        Args:
            login: Vulcan login username/email
            password: Vulcan password
            kid_name: Expected student name to find in the page

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Vulcan login page
                # Note: Vulcan has multiple regional instances, this is a common one
                page.goto("https://uonetplus.vulcan.net.pl/", timeout=self.timeout)

                # Fill in credentials
                # Note: Vulcan login form may vary by region
                page.fill('input[type="text"]', login)
                page.fill('input[type="password"]', password)

                # Click login button
                page.click('button[type="submit"]')

                # Wait for navigation after login
                page.wait_for_load_state("networkidle", timeout=self.timeout)

                # Get page content
                content = page.content()

                # Close browser
                browser.close()

                # Check if student name appears in the content
                if self._check_student_name_in_content(content, kid_name):
                    return True, "Connection successful! Student name found in page."
                else:
                    return (
                        False,
                        f"Login succeeded but student name '{kid_name}' not found in page. Please verify the student name.",
                    )

        except PlaywrightTimeoutError:
            return False, "Connection timeout. Please check your internet connection."
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

    def _check_student_name_in_content(self, content: str, kid_name: str) -> bool:
        """Check if student name appears in the HTML content.

        Args:
            content: HTML content to search
            kid_name: Student name to find

        Returns:
            True if student name is found, False otherwise
        """
        # Normalize the content and name for comparison
        content_lower = content.lower()
        kid_name_lower = kid_name.lower()

        # Check for exact match
        if kid_name_lower in content_lower:
            return True

        # Check for partial matches (first name or last name)
        name_parts = kid_name.split()
        for part in name_parts:
            if len(part) >= 3 and part.lower() in content_lower:
                return True

        return False

    def test_connection(
        self, provider: str, login: str, password: str, kid_name: str
    ) -> Tuple[bool, str]:
        """Test connection based on provider type.

        Args:
            provider: Provider name ("Librus" or "Vulcan")
            login: Login username/email
            password: Login password
            kid_name: Expected student name to find in the page

        Returns:
            Tuple of (success: bool, message: str)
        """
        if provider == "Librus":
            return self.test_librus_connection(login, password, kid_name)
        elif provider == "Vulcan":
            return self.test_vulcan_connection(login, password, kid_name)
        else:
            return False, f"Unknown provider: {provider}"
