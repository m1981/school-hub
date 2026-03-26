"""View components for different tabs.

Each view is a placeholder that will be implemented in future sprints.
"""

import reflex as rx
from school_hub.state import AppState


def quick_stat_card(stat) -> rx.Component:
    """Render a single quick stat card."""
    return rx.vstack(
        rx.text(stat.avatar, size="7"),
        rx.text(stat.kid_name, size="2", weight="bold"),
        rx.text(
            stat.recent_summary,
            size="1",
            color="gray.10",
        ),
        rx.text(
            stat.provider,
            size="1",
            color="blue.9",
        ),
        align="center",
        padding="1rem",
        bg="gray.3",
        border_radius="8px",
        min_width="100px",
    )


def feed_card(item) -> rx.Component:
    """Render a single feed item (grade or news)."""
    # Use rx.cond to check type and render accordingly
    return rx.cond(
        item.type == "grade",
        # Grade card
        rx.card(
            rx.hstack(
                # Left border color indicator
                rx.box(
                    width="4px",
                    height="100%",
                    bg="blue.7",
                    border_radius="2px",
                ),
                # Content
                rx.vstack(
                    rx.hstack(
                        rx.text(item.kid_name, weight="bold", size="2"),
                        rx.spacer(),
                        rx.text(item.date, size="1", color="gray.10"),
                    ),
                    rx.text(item.subject_name, size="3", color="gray.11"),
                    rx.hstack(
                        rx.badge(rx.text("Grade: ", item.value), color_scheme="blue"),
                        rx.text("• ", item.category, size="1", color="gray.10"),
                        rx.text("• Weight: ", item.weight, size="1", color="gray.10"),
                    ),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            size="2",
        ),
        # News card
        rx.card(
            rx.hstack(
                # Left border color indicator
                rx.box(
                    width="4px",
                    height="100%",
                    bg="orange.7",
                    border_radius="2px",
                ),
                # Content
                rx.vstack(
                    rx.hstack(
                        rx.text(item.kid_name, weight="bold", size="2"),
                        rx.spacer(),
                        rx.text(item.date, size="1", color="gray.10"),
                    ),
                    rx.text(item.subject, size="3", weight="medium"),
                    rx.text(item.content, size="2", color="gray.11"),
                    rx.text("From: ", item.sender, size="1", color="gray.10"),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            size="2",
        ),
    )


def feed_view() -> rx.Component:
    """Feed/Dashboard view with Quick Stats and Today's Summary."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("School Hub", size="8", weight="bold"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh-cw", size=18),
                on_click=AppState.refresh_data,
                variant="ghost",
                size="2",
            ),
            width="100%",
        ),
        rx.text(
            "Last synced: ", AppState.last_synced,
            size="1",
            color="gray.10",
        ),
        # Quick Stats (horizontal scroll)
        rx.scroll_area(
            rx.hstack(
                rx.foreach(
                    AppState.get_quick_stats,
                    quick_stat_card,
                ),
                spacing="3",
            ),
            type="hover",
            scrollbars="horizontal",
        ),
        # Today's Summary heading
        rx.heading("Recent Activity", size="5", margin_top="1.5rem"),
        # Feed items
        rx.vstack(
            rx.foreach(
                AppState.get_sorted_feed,
                feed_card,
            ),
            spacing="3",
            width="100%",
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

