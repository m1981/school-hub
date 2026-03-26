"""View components for different tabs.

Each view is a placeholder that will be implemented in future sprints.
"""

import reflex as rx
from school_hub.state import AppState


def feed_view() -> rx.Component:
    """Feed/Dashboard view - placeholder for Sprint 3."""
    return rx.vstack(
        rx.heading("School Hub", size="8", weight="bold"),
        rx.text(
            f"Last synced: {AppState.last_synced}",
            size="2",
            color="gray.10",
        ),
        rx.text(
            "Feed view - Coming in Sprint 3",
            size="4",
            color="gray.11",
            margin_top="2rem",
        ),
        spacing="3",
        padding="1.5rem",
        width="100%",
    )


def calendar_view() -> rx.Component:
    """Calendar view - placeholder for Sprint 4."""
    return rx.vstack(
        rx.heading("Calendar", size="8", weight="bold"),
        rx.text(
            "Calendar view - Coming in Sprint 4",
            size="4",
            color="gray.11",
            margin_top="2rem",
        ),
        spacing="3",
        padding="1.5rem",
        width="100%",
    )


def children_view() -> rx.Component:
    """Children/detailed view - placeholder."""
    return rx.vstack(
        rx.heading("Children", size="8", weight="bold"),
        rx.text(
            "Detailed children view - Coming soon",
            size="4",
            color="gray.11",
            margin_top="2rem",
        ),
        spacing="3",
        padding="1.5rem",
        width="100%",
    )


def settings_view() -> rx.Component:
    """Settings/Profile management - placeholder for Sprint 5."""
    return rx.vstack(
        rx.heading("Settings", size="8", weight="bold"),
        rx.text(
            "Profile management - Coming in Sprint 5",
            size="4",
            color="gray.11",
            margin_top="2rem",
        ),
        spacing="3",
        padding="1.5rem",
        width="100%",
    )


def render_current_view() -> rx.Component:
    """Render the appropriate view based on current_tab state.
    
    Uses rx.cond for reactive rendering (not Python if/else).
    """
    return rx.cond(
        AppState.current_tab == "feed",
        feed_view(),
        rx.cond(
            AppState.current_tab == "calendar",
            calendar_view(),
            rx.cond(
                AppState.current_tab == "children",
                children_view(),
                settings_view(),
            ),
        ),
    )

