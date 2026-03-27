"""Unit tests for Connection Tester.

This test suite verifies the connection testing functionality for Librus/Vulcan.
"""

import pytest
from school_hub.services.connection_tester import ConnectionTester

pytestmark = pytest.mark.integration


class TestConnectionTester:
    """Test suite for ConnectionTester."""

    @pytest.fixture
    def connection_tester(self):
        """Create a ConnectionTester instance."""
        return ConnectionTester(timeout=30000)

    def test_check_student_name_in_content_exact_match(self, connection_tester):
        """Test that exact student name match is detected."""
        content = "<html><body>Welcome, Anna Kowalska</body></html>"
        assert connection_tester._check_student_name_in_content(
            content, "Anna Kowalska"
        )

    def test_check_student_name_in_content_case_insensitive(self, connection_tester):
        """Test that name matching is case-insensitive."""
        content = "<html><body>Welcome, ANNA KOWALSKA</body></html>"
        assert connection_tester._check_student_name_in_content(
            content, "anna kowalska"
        )

    def test_check_student_name_in_content_partial_match(self, connection_tester):
        """Test that partial name match (first or last name) is detected."""
        content = "<html><body>Student: Kowalska</body></html>"
        assert connection_tester._check_student_name_in_content(
            content, "Anna Kowalska"
        )

    def test_check_student_name_in_content_no_match(self, connection_tester):
        """Test that non-matching name returns False."""
        content = "<html><body>Welcome, John Smith</body></html>"
        assert not connection_tester._check_student_name_in_content(
            content, "Anna Kowalska"
        )

    def test_check_student_name_in_content_short_name_ignored(self, connection_tester):
        """Test that very short name parts (< 3 chars) are not matched partially."""
        content = "<html><body>Welcome to our site</body></html>"
        # "to" is in content but should not match as it's too short
        assert not connection_tester._check_student_name_in_content(content, "To Smith")

    def test_test_connection_unknown_provider(self, connection_tester):
        """Test that unknown provider returns error."""
        success, message = connection_tester.test_connection(
            provider="Unknown",
            login="test@example.com",
            password="password",
            kid_name="Test Student",
        )
        assert not success
        assert "Unknown provider" in message

    def test_test_connection_librus_routes_correctly(self, connection_tester):
        """Test that Librus provider routes to correct method."""
        # This will fail in actual connection but we're testing the routing
        success, message = connection_tester.test_connection(
            provider="Librus",
            login="test@example.com",
            password="password",
            kid_name="Test Student",
        )
        # Should attempt connection (will fail but that's expected in test)
        assert not success
        assert "Connection" in message or "failed" in message.lower()

    def test_test_connection_vulcan_routes_correctly(self, connection_tester):
        """Test that Vulcan provider routes to correct method."""
        # This will fail in actual connection but we're testing the routing
        success, message = connection_tester.test_connection(
            provider="Vulcan",
            login="test@example.com",
            password="password",
            kid_name="Test Student",
        )
        # Should attempt connection (will fail but that's expected in test)
        assert not success
        assert "Connection" in message or "failed" in message.lower()
