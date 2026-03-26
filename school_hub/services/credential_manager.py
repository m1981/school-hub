"""Credential Manager for secure local storage of student profiles.

This module provides encrypted storage for student credentials in a local JSON file.
Uses Fernet symmetric encryption from the cryptography library.
"""

import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from cryptography.fernet import Fernet


class StudentProfile(BaseModel):
    """Represents a student profile with provider credentials."""

    kid_name: str
    provider: str  # "Librus" or "Vulcan"
    login: str
    password: str


class CredentialManager:
    """Manages encrypted storage of student profiles in a local JSON file."""

    def __init__(self, credentials_file: str = "credentials.json"):
        """Initialize the CredentialManager.

        Args:
            credentials_file: Path to the credentials file (default: credentials.json)
        """
        self.credentials_file = Path(credentials_file)
        self._encryption_key = self._get_or_create_encryption_key()
        self._cipher = Fernet(self._encryption_key)

        # Create empty file if it doesn't exist
        if not self.credentials_file.exists():
            self._save_encrypted_data([])

    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create an encryption key for this installation.

        The key is stored in a .key file next to the credentials file.
        This is a simple approach for local storage. For production,
        consider using system keyring or environment variables.

        Returns:
            Encryption key as bytes
        """
        key_file = self.credentials_file.parent / ".encryption.key"

        if key_file.exists():
            with open(key_file, "rb") as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            # Ensure parent directory exists
            key_file.parent.mkdir(parents=True, exist_ok=True)
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def _save_encrypted_data(self, profiles: list[StudentProfile]):
        """Save profiles to encrypted JSON file.

        Args:
            profiles: List of StudentProfile objects to save
        """
        # Convert profiles to dictionaries
        profiles_data = [profile.model_dump() for profile in profiles]

        # Serialize to JSON
        json_data = json.dumps(profiles_data)

        # Encrypt
        encrypted_data = self._cipher.encrypt(json_data.encode())

        # Ensure parent directory exists
        self.credentials_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(self.credentials_file, "wb") as f:
            f.write(encrypted_data)

    def _load_encrypted_data(self) -> list[StudentProfile]:
        """Load profiles from encrypted JSON file.

        Returns:
            List of StudentProfile objects
        """
        if not self.credentials_file.exists():
            return []

        try:
            # Read encrypted data
            with open(self.credentials_file, "rb") as f:
                encrypted_data = f.read()

            # Decrypt
            decrypted_data = self._cipher.decrypt(encrypted_data)

            # Parse JSON
            profiles_data = json.loads(decrypted_data.decode())

            # Convert to StudentProfile objects
            return [StudentProfile(**profile) for profile in profiles_data]
        except Exception:
            # If decryption fails or file is corrupted, return empty list
            return []

    def load_profiles(self) -> list[StudentProfile]:
        """Load all student profiles.

        Returns:
            List of StudentProfile objects
        """
        return self._load_encrypted_data()

    def save_profile(self, profile: StudentProfile):
        """Save or update a student profile.

        If a profile with the same kid_name exists, it will be updated.
        Otherwise, a new profile will be added.

        Args:
            profile: StudentProfile object to save
        """
        profiles = self.load_profiles()

        # Check if profile already exists (by kid_name)
        existing_index = None
        for i, existing_profile in enumerate(profiles):
            if existing_profile.kid_name == profile.kid_name:
                existing_index = i
                break

        if existing_index is not None:
            # Update existing profile
            profiles[existing_index] = profile
        else:
            # Add new profile
            profiles.append(profile)

        self._save_encrypted_data(profiles)

    def delete_profile(self, kid_name: str):
        """Delete a student profile by kid_name.

        Args:
            kid_name: Name of the student whose profile should be deleted
        """
        profiles = self.load_profiles()
        profiles = [p for p in profiles if p.kid_name != kid_name]
        self._save_encrypted_data(profiles)

    def get_profile(self, kid_name: str) -> Optional[StudentProfile]:
        """Get a specific student profile by kid_name.

        Args:
            kid_name: Name of the student

        Returns:
            StudentProfile object if found, None otherwise
        """
        profiles = self.load_profiles()
        for profile in profiles:
            if profile.kid_name == kid_name:
                return profile
        return None
