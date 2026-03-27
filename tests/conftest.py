"""Pytest configuration and shared fixtures for school-hub tests.

This file provides:
- Shared fixtures across all test modules
- Pytest hooks for better test organization
- Custom markers configuration
"""

import pytest


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Register custom markers
    config.addinivalue_line(
        "markers", "unit: Unit tests - fast, isolated, no external dependencies"
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests - may use files, network, or external resources",
    )
    config.addinivalue_line(
        "markers", "ui: UI tests - require Playwright and running application"
    )
    config.addinivalue_line(
        "markers", "slow: Slow running tests - may take several seconds"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically based on test location."""
    for item in items:
        # Auto-mark UI tests
        if "ui" in item.nodeid:
            item.add_marker(pytest.mark.ui)
            item.add_marker(pytest.mark.slow)

        # Auto-mark integration tests based on file name patterns
        if any(pattern in item.nodeid for pattern in ["scraper", "connection_tester"]):
            if not any(mark.name == "integration" for mark in item.iter_markers()):
                item.add_marker(pytest.mark.integration)


# Shared fixtures can be added here
@pytest.fixture
def sample_kid_name():
    """Provide a sample kid name for testing."""
    return "TestStudent"


@pytest.fixture
def sample_provider():
    """Provide a sample provider for testing."""
    return "Librus"
