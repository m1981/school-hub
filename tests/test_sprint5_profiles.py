"""Sprint 5: Profile Management & Credential Storage Tests.

This test suite follows TDD principles:
1. Test the CredentialManager for secure local storage
2. Test AppState profile management methods
3. Verify profile CRUD operations
"""

import pytest
from school_hub.services.credential_manager import CredentialManager, StudentProfile


class TestCredentialManager:
    """Test suite for secure credential storage."""

    @pytest.fixture
    def temp_credentials_file(self, tmp_path):
        """Create a temporary credentials file path."""
        return tmp_path / "test_credentials.json"

    @pytest.fixture
    def credential_manager(self, temp_credentials_file):
        """Create a CredentialManager instance with temp file."""
        return CredentialManager(str(temp_credentials_file))

    def test_credential_manager_initializes_empty_file(
        self, credential_manager, temp_credentials_file
    ):
        """Test that CredentialManager creates an empty file if it doesn't exist."""
        # The file should be created during initialization
        assert temp_credentials_file.exists()

        # Should return empty list for new file
        profiles = credential_manager.load_profiles()
        assert profiles == []

    def test_save_single_profile(self, credential_manager):
        """Test saving a single student profile."""
        profile = StudentProfile(
            kid_name="Anna",
            provider="Librus",
            login="anna.test@example.com",
            password="test_password_123",
        )

        credential_manager.save_profile(profile)

        # Load and verify
        profiles = credential_manager.load_profiles()
        assert len(profiles) == 1
        assert profiles[0].kid_name == "Anna"
        assert profiles[0].provider == "Librus"
        assert profiles[0].login == "anna.test@example.com"
        assert profiles[0].password == "test_password_123"

    def test_save_multiple_profiles(self, credential_manager):
        """Test saving multiple student profiles."""
        profiles_to_save = [
            StudentProfile(
                kid_name="Anna",
                provider="Librus",
                login="anna@test.com",
                password="pass1",
            ),
            StudentProfile(
                kid_name="Ben",
                provider="Vulcan",
                login="ben@test.com",
                password="pass2",
            ),
            StudentProfile(
                kid_name="Clara",
                provider="Librus",
                login="clara@test.com",
                password="pass3",
            ),
        ]

        for profile in profiles_to_save:
            credential_manager.save_profile(profile)

        # Load and verify
        loaded_profiles = credential_manager.load_profiles()
        assert len(loaded_profiles) == 3
        assert loaded_profiles[0].kid_name == "Anna"
        assert loaded_profiles[1].kid_name == "Ben"
        assert loaded_profiles[2].kid_name == "Clara"

    def test_update_existing_profile(self, credential_manager):
        """Test updating an existing profile (same kid_name)."""
        # Save initial profile
        profile1 = StudentProfile(
            kid_name="Anna",
            provider="Librus",
            login="anna@old.com",
            password="old_password",
        )
        credential_manager.save_profile(profile1)

        # Update with new credentials
        profile2 = StudentProfile(
            kid_name="Anna",
            provider="Vulcan",  # Changed provider
            login="anna@new.com",  # Changed login
            password="new_password",  # Changed password
        )
        credential_manager.save_profile(profile2)

        # Should only have one profile (updated)
        profiles = credential_manager.load_profiles()
        assert len(profiles) == 1
        assert profiles[0].kid_name == "Anna"
        assert profiles[0].provider == "Vulcan"
        assert profiles[0].login == "anna@new.com"
        assert profiles[0].password == "new_password"

    def test_delete_profile(self, credential_manager):
        """Test deleting a profile by kid_name."""
        # Save multiple profiles
        profiles = [
            StudentProfile(
                kid_name="Anna",
                provider="Librus",
                login="anna@test.com",
                password="pass1",
            ),
            StudentProfile(
                kid_name="Ben",
                provider="Vulcan",
                login="ben@test.com",
                password="pass2",
            ),
        ]
        for profile in profiles:
            credential_manager.save_profile(profile)

        # Delete Anna
        credential_manager.delete_profile("Anna")

        # Verify only Ben remains
        remaining = credential_manager.load_profiles()
        assert len(remaining) == 1
        assert remaining[0].kid_name == "Ben"

    def test_get_profile_by_name(self, credential_manager):
        """Test retrieving a specific profile by kid_name."""
        # Save profiles
        profiles = [
            StudentProfile(
                kid_name="Anna",
                provider="Librus",
                login="anna@test.com",
                password="pass1",
            ),
            StudentProfile(
                kid_name="Ben",
                provider="Vulcan",
                login="ben@test.com",
                password="pass2",
            ),
        ]
        for profile in profiles:
            credential_manager.save_profile(profile)

        # Get specific profile
        anna_profile = credential_manager.get_profile("Anna")
        assert anna_profile is not None
        assert anna_profile.kid_name == "Anna"
        assert anna_profile.provider == "Librus"

        # Try non-existent profile
        missing_profile = credential_manager.get_profile("NonExistent")
        assert missing_profile is None

    def test_credentials_are_encrypted(self, credential_manager, temp_credentials_file):
        """Test that passwords are not stored in plain text."""
        profile = StudentProfile(
            kid_name="Anna",
            provider="Librus",
            login="anna@test.com",
            password="super_secret_password",
        )
        credential_manager.save_profile(profile)

        # Read raw file content
        with open(temp_credentials_file, "r") as f:
            raw_content = f.read()

        # Password should NOT appear in plain text
        assert "super_secret_password" not in raw_content

        # But we should be able to decrypt it
        loaded = credential_manager.load_profiles()
        assert loaded[0].password == "super_secret_password"

    def test_file_persistence_across_instances(self, temp_credentials_file):
        """Test that data persists across different CredentialManager instances."""
        # Create first instance and save data
        manager1 = CredentialManager(str(temp_credentials_file))
        profile = StudentProfile(
            kid_name="Anna", provider="Librus", login="anna@test.com", password="pass1"
        )
        manager1.save_profile(profile)

        # Create second instance and load data
        manager2 = CredentialManager(str(temp_credentials_file))
        profiles = manager2.load_profiles()

        assert len(profiles) == 1
        assert profiles[0].kid_name == "Anna"


class TestAppStateProfileManagement:
    """Test suite for profile management in AppState."""

    @pytest.fixture
    def temp_state(self, tmp_path):
        """Create an AppState with isolated credential storage."""
        from school_hub.state import AppState

        # Create a state instance
        state = AppState()
        # Override the credential manager with a temp file
        temp_creds_file = tmp_path / "test_state_credentials.json"
        state._credential_manager = CredentialManager(str(temp_creds_file))
        return state

    def test_app_state_has_profiles_list(self, temp_state):
        """Test that AppState has a profiles property."""
        # Should have a method or property to access profiles
        assert hasattr(temp_state, "get_profiles") or hasattr(temp_state, "profiles")

    def test_app_state_can_add_profile(self, temp_state):
        """Test that AppState can add a new profile."""
        initial_count = len(temp_state.get_profiles)

        # Add a profile
        temp_state.add_profile(
            kid_name="TestKid",
            provider="Librus",
            login="test@example.com",
            password="test_pass",
        )

        # Verify it was added
        profiles = temp_state.get_profiles
        assert len(profiles) == initial_count + 1

        # Find the new profile
        new_profile = next((p for p in profiles if p["kid_name"] == "TestKid"), None)
        assert new_profile is not None
        assert new_profile["provider"] == "Librus"
        assert new_profile["login"] == "test@example.com"

    def test_app_state_can_update_profile(self, temp_state):
        """Test that AppState can update an existing profile."""
        # Add initial profile
        temp_state.add_profile(
            kid_name="TestKid",
            provider="Librus",
            login="old@example.com",
            password="old_pass",
        )

        # Update the profile
        temp_state.update_profile(
            kid_name="TestKid",
            provider="Vulcan",  # Changed
            login="new@example.com",  # Changed
            password="new_pass",  # Changed
        )

        # Verify update
        profiles = temp_state.get_profiles
        updated_profile = next(
            (p for p in profiles if p["kid_name"] == "TestKid"), None
        )
        assert updated_profile is not None
        assert updated_profile["provider"] == "Vulcan"
        assert updated_profile["login"] == "new@example.com"

    def test_app_state_can_delete_profile(self, temp_state):
        """Test that AppState can delete a profile."""
        # Add a profile
        temp_state.add_profile(
            kid_name="TestKid",
            provider="Librus",
            login="test@example.com",
            password="test_pass",
        )

        initial_count = len(temp_state.get_profiles)

        # Delete the profile
        temp_state.delete_profile("TestKid")

        # Verify deletion
        profiles = temp_state.get_profiles
        assert len(profiles) == initial_count - 1

        # Verify it's actually gone
        deleted_profile = next(
            (p for p in profiles if p["kid_name"] == "TestKid"), None
        )
        assert deleted_profile is None

    def test_app_state_profiles_do_not_expose_passwords(self, temp_state):
        """Test that get_profiles computed var does NOT return passwords (security)."""
        # Add a profile with password
        temp_state.add_profile(
            kid_name="TestKid",
            provider="Librus",
            login="test@example.com",
            password="super_secret",
        )

        # Get profiles for UI
        profiles = temp_state.get_profiles
        test_profile = next((p for p in profiles if p["kid_name"] == "TestKid"), None)

        # Password should NOT be in the returned dict (security best practice)
        assert "password" not in test_profile
        assert "super_secret" not in str(test_profile)
