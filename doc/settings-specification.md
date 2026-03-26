# Settings View - Complete Specification

## Overview

This document provides detailed specifications for the Settings view profile management functionality, including the "Add New Student" and "Edit Student Profile" features.

## Current Implementation Status

### ✅ Completed Features
1. **Settings View Layout** - Profile list with cards showing student info
2. **Add New Student Dialog** - Form with all required fields
3. **Delete Profile** - Remove student profiles with encrypted credential cleanup
4. **Credential Storage** - Encrypted local storage using Fernet
5. **Profile Display** - Secure display without exposing passwords

### ⚠️ Incomplete Features
1. **Edit Profile Dialog** - Currently just a placeholder (`open_edit_profile_dialog`)
2. **Form Pre-population** - Edit mode needs to load existing data
3. **Dialog State Management** - Need to track edit vs add mode

## Architecture Reference

All detailed sequence diagrams and specifications have been added to:
- **File**: `/Users/michal/PycharmProjects/school-hub/doc/architecture-diagrams.md`
- **Sections**:
  - Section 11: Add New Student Flow
  - Section 12: Edit Student Profile Flow (with implementation guide)
  - Section 13: Delete Profile Flow

## Implementation Checklist for Edit Functionality

### Step 1: Add State Variables to `AppState` (state.py)

```python
# Add these to the AppState class
profile_edit_mode: bool = False
profile_edit_kid_name: str = ""  # Original kid_name being edited
```

### Step 2: Update Event Handlers in `AppState` (state.py)

#### 2.1 Update `open_edit_profile_dialog`
Replace the placeholder with:
```python
def open_edit_profile_dialog(self, kid_name: str):
    """Open the edit dialog and populate form with existing profile data."""
    profile = self._credential_manager.get_profile(kid_name)

    if profile:
        self.profile_form_kid_name = profile.kid_name
        self.profile_form_provider = profile.provider
        self.profile_form_login = profile.login
        self.profile_form_password = profile.password
        self.profile_edit_mode = True
        self.profile_edit_kid_name = kid_name
```

#### 2.2 Update `save_profile_from_form`
Replace existing implementation with:
```python
def save_profile_from_form(self):
    """Save the profile from the form data (handles both add and edit)."""
    if (
        self.profile_form_kid_name
        and self.profile_form_login
        and self.profile_form_password
    ):
        if self.profile_edit_mode:
            # Edit mode: update existing profile
            self.update_profile(
                kid_name=self.profile_form_kid_name,
                provider=self.profile_form_provider,
                login=self.profile_form_login,
                password=self.profile_form_password,
            )
        else:
            # Add mode: create new profile
            self.add_profile(
                kid_name=self.profile_form_kid_name,
                provider=self.profile_form_provider,
                login=self.profile_form_login,
                password=self.profile_form_password,
            )

        # Clear form and reset edit mode
        self.profile_form_kid_name = ""
        self.profile_form_provider = "Librus"
        self.profile_form_login = ""
        self.profile_form_password = ""
        self.profile_edit_mode = False
        self.profile_edit_kid_name = ""
```

#### 2.3 Add `cancel_profile_form`
```python
def cancel_profile_form(self):
    """Cancel the form and reset all state."""
    self.profile_form_kid_name = ""
    self.profile_form_provider = "Librus"
    self.profile_form_login = ""
    self.profile_form_password = ""
    self.profile_edit_mode = False
    self.profile_edit_kid_name = ""
```

### Step 3: Update UI Components in `views.py`

#### 3.1 Update `add_profile_dialog` function
Key changes:
1. Add `value` prop to all inputs for pre-population
2. Add dynamic title using `rx.cond`
3. Add dynamic button text using `rx.cond`
4. Add `on_click=AppState.cancel_profile_form` to Cancel button
5. Add `open` prop to control dialog state programmatically

See full implementation in `architecture-diagrams.md` Section 12.3.

### Step 4: Testing Checklist

#### Manual Testing
- [ ] Click "Add New Student" - dialog opens with empty form
- [ ] Fill form and save - profile appears in list
- [ ] Click "Edit" on existing profile - dialog opens with pre-filled data
- [ ] Modify fields and save - profile updates correctly
- [ ] Click "Cancel" in edit mode - form resets, dialog closes
- [ ] Click "Delete" - profile removed from list
- [ ] Restart app - profiles persist (encrypted)

#### Unit Tests (Future Sprint)
- [ ] Test `open_edit_profile_dialog` loads correct profile
- [ ] Test `save_profile_from_form` in add mode
- [ ] Test `save_profile_from_form` in edit mode
- [ ] Test `cancel_profile_form` resets all state
- [ ] Test form validation (empty fields)

## Key Design Decisions

### 1. Single Dialog for Add and Edit
**Rationale**: Reduces code duplication, uses conditional rendering for differences
**Trade-off**: Slightly more complex state management

### 2. Edit Mode Flag
**Rationale**: Clear distinction between add and edit operations
**Alternative**: Could use separate dialogs (more code, clearer separation)

### 3. Password Pre-fill in Edit Mode
**Rationale**: User can see/modify existing password
**Security Note**: Password never sent to frontend in `get_profiles`, only loaded when editing

### 4. No Confirmation on Delete
**Current**: Immediate deletion
**Recommendation**: Add confirmation dialog for safety (see Section 13 for implementation)

### 5. kid_name as Identity
**Current**: kid_name is the unique identifier
**Limitation**: Changing kid_name during edit creates new profile
**Recommendation**: Consider preventing kid_name changes in edit mode

## Security Considerations

1. **Encryption**: All credentials encrypted with Fernet before storage
2. **Key Storage**: Encryption key in `.encryption.key` (add to .gitignore)
3. **Frontend Isolation**: `get_profiles` computed var strips passwords
4. **Form State**: Cleared immediately after save
5. **File Permissions**: Consider setting restrictive permissions on credentials.json

## Data Flow Summary

### Add Flow
```
User Input → Form State → add_profile() → CredentialManager.save_profile()
→ Encrypt → credentials.json → Increment _profiles_version → Re-render
```

### Edit Flow
```
Click Edit → get_profile() → Decrypt → Populate Form → User Modifies
→ update_profile() → CredentialManager.save_profile() → Encrypt
→ credentials.json → Increment _profiles_version → Re-render
```

### Delete Flow
```
Click Delete → delete_profile() → CredentialManager.delete_profile()
→ Filter profiles → Encrypt → credentials.json → Increment _profiles_version
→ Re-render
```

## References

- **Main Specification**: `/Users/michal/PycharmProjects/school-hub/doc/specification.md` (Section 4.4)
- **Architecture Diagrams**: `/Users/michal/PycharmProjects/school-hub/doc/architecture-diagrams.md` (Sections 11-13)
- **Project Plan**: `/Users/michal/PycharmProjects/school-hub/doc/project-plan.md` (Sprint 5)
- **Implementation Files**:
  - State: `school_hub/state.py`
  - Views: `school_hub/components/views.py`
  - Credential Manager: `school_hub/services/credential_manager.py`
  - Models: `school_hub/models.py`

## Next Steps

1. **Implement Edit Functionality**: Follow checklist above
2. **Write Unit Tests**: Test edit flow thoroughly
3. **Add Confirmation Dialogs**: For delete operations
4. **Consider Enhancements**:
   - Prevent kid_name changes during edit
   - Add form validation feedback
   - Add success/error notifications
   - Add profile avatar selection
   - Add "Test Connection" button to verify credentials

---

**Document Version**: 1.0
**Last Updated**: 2024
**Status**: Complete specification, implementation pending
