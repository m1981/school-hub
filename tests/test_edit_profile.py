"""Unit tests for Edit Profile functionality.

This test suite verifies the edit profile feature in AppState.
"""

import pytest
from school_hub.state import AppState
from school_hub.services.credential_manager import CredentialManager, StudentProfile
from unittest.mock import Mock

pytestmark = pytest.mark.unit


class TestEditProfile:
    """Test suite for edit profile functionality."""

    @pytest.fixture
    def temp_credentials_file(self, tmp_path):
        """Create a temporary credentials file path."""
        return tmp_path / "test_credentials.json"

    @pytest.fixture
    def app_state(self, temp_credentials_file):
        """Create an AppState instance with temp credential manager."""
        state = AppState()
        state._credential_manager = CredentialManager(str(temp_credentials_file))
        # Mock the connection tester to avoid actual network calls
        state._connection_tester = Mock()
        state._connection_tester.test_connection.return_value = (
            True,
            "Connection successful!",
        )
        return state

    def test_open_edit_profile_dialog_populates_form(self, app_state):
        """Test that opening edit dialog populates form with existing data."""
        # First, add a profile
        profile = StudentProfile(
            kid_name="Anna",
            provider="Librus",
            login="anna@test.com",
            password="test_password",
        )
        app_state._credential_manager.save_profile(profile)

        # Open edit dialog
        app_state.open_edit_profile_dialog("Anna")

        # Verify form is populated
        assert app_state.profile_form_kid_name == "Anna"
        assert app_state.profile_form_provider == "Librus"
        assert app_state.profile_form_login == "anna@test.com"
        assert app_state.profile_form_password == "test_password"
        assert app_state.profile_edit_mode is True
        assert app_state.profile_edit_kid_name == "Anna"

    def test_open_edit_profile_dialog_nonexistent_profile(self, app_state):
        """Test that opening edit dialog for non-existent profile does nothing."""
        # Try to open edit dialog for non-existent profile
        app_state.open_edit_profile_dialog("NonExistent")

        # Form should remain empty
        assert app_state.profile_form_kid_name == ""
        assert app_state.profile_edit_mode is False

    def test_save_profile_from_form_in_edit_mode(self, app_state):
        """Test that saving in edit mode updates existing profile."""
        # First, add a profile
        profile = StudentProfile(
            kid_name="Anna",
            provider="Librus",
            login="anna@old.com",
            password="old_password",
        )
        app_state._credential_manager.save_profile(profile)

        # Open edit dialog and modify
        app_state.open_edit_profile_dialog("Anna")
        app_state.profile_form_login = "anna@new.com"
        app_state.profile_form_password = "new_password"

        # Save
        app_state.save_profile_from_form()

        # Verify profile was updated
        profiles = app_state._credential_manager.load_profiles()
        assert len(profiles) == 1
        assert profiles[0].kid_name == "Anna"
        assert profiles[0].login == "anna@new.com"
        assert profiles[0].password == "new_password"

        # Verify form was cleared and edit mode reset
        assert app_state.profile_form_kid_name == ""
        assert app_state.profile_edit_mode is False
        assert app_state.profile_edit_kid_name == ""

    def test_save_profile_from_form_in_add_mode(self, app_state):
        """Test that saving in add mode creates new profile."""
        # Set form data (not in edit mode)
        app_state.profile_form_kid_name = "Ben"
        app_state.profile_form_provider = "Vulcan"
        app_state.profile_form_login = "ben@test.com"
        app_state.profile_form_password = "test_password"

        # Save
        app_state.save_profile_from_form()

        # Verify profile was created
        profiles = app_state._credential_manager.load_profiles()
        assert len(profiles) == 1
        assert profiles[0].kid_name == "Ben"
        assert profiles[0].provider == "Vulcan"

        # Verify form was cleared
        assert app_state.profile_form_kid_name == ""

    def test_cancel_profile_form_resets_all_state(self, app_state):
        """Test that canceling form resets all state variables."""
        # Set up some form state
        app_state.profile_form_kid_name = "Anna"
        app_state.profile_form_provider = "Librus"
        app_state.profile_form_login = "anna@test.com"
        app_state.profile_form_password = "password"
        app_state.profile_edit_mode = True
        app_state.profile_edit_kid_name = "Anna"
        app_state.profile_connection_message = "Some message"
        app_state.profile_connection_success = True

        # Cancel
        app_state.cancel_profile_form()

        # Verify all state is reset
        assert app_state.profile_form_kid_name == ""
        assert app_state.profile_form_provider == "Librus"
        assert app_state.profile_form_login == ""
        assert app_state.profile_form_password == ""
        assert app_state.profile_edit_mode is False
        assert app_state.profile_edit_kid_name == ""
        assert app_state.profile_connection_message == ""
        assert app_state.profile_connection_success is False

    def test_save_profile_with_failed_connection_test(self, app_state):
        """Test that saving fails if connection test fails."""
        # Mock connection test to fail
        app_state._connection_tester.test_connection.return_value = (
            False,
            "Connection failed: Invalid credentials",
        )

        # Set form data
        app_state.profile_form_kid_name = "Anna"
        app_state.profile_form_provider = "Librus"
        app_state.profile_form_login = "anna@test.com"
        app_state.profile_form_password = "wrong_password"

        # Try to save
        app_state.save_profile_from_form()

        # Verify profile was NOT created
        profiles = app_state._credential_manager.load_profiles()
        assert len(profiles) == 0

        # Verify error message is set
        assert (
            app_state.profile_connection_message
            == "Connection failed: Invalid credentials"
        )
        assert app_state.profile_connection_success is False

    def test_test_profile_connection_success(self, app_state):
        """Test the test_profile_connection method with successful connection."""
        # Set form data
        app_state.profile_form_kid_name = "Anna"
        app_state.profile_form_provider = "Librus"
        app_state.profile_form_login = "anna@test.com"
        app_state.profile_form_password = "password"

        # Test connection
        app_state.test_profile_connection()

        # Verify connection tester was called
        app_state._connection_tester.test_connection.assert_called_once_with(
            provider="Librus",
            login="anna@test.com",
            password="password",
            kid_name="Anna",
        )

        # Verify success state
        assert app_state.profile_connection_success is True
        assert "successful" in app_state.profile_connection_message.lower()

    def test_test_profile_connection_missing_fields(self, app_state):
        """Test that connection test fails if fields are missing."""
        # Leave form empty
        app_state.profile_form_kid_name = ""
        app_state.profile_form_login = ""
        app_state.profile_form_password = ""

        # Test connection
        app_state.test_profile_connection()

        # Verify error message
        assert "fill in all fields" in app_state.profile_connection_message.lower()
        assert app_state.profile_connection_success is False

        # Verify connection tester was NOT called
        app_state._connection_tester.test_connection.assert_not_called()
