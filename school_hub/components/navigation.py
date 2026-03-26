"""Bottom Navigation Component for School Hub.

Mobile-first navigation bar with 4 tabs: Feed, Calendar, Children, Settings.
"""

import reflex as rx
from school_hub.state import AppState


def bottom_nav_item(icon: str, label: str, tab_value: str) -> rx.Component:
    """Create a single navigation item.

    Args:
        icon: Emoji or icon character
        label: Display text for the tab
        tab_value: Internal value for the tab

    Returns:
        A clickable navigation item
    """
    return rx.vstack(
        rx.text(
            icon,
            size="6",
        ),
        rx.text(
            label,
            size="1",
            color=rx.cond(
                AppState.current_tab == tab_value,
                "blue.9",
                "gray.9",
            ),
            weight=rx.cond(
                AppState.current_tab == tab_value,
                "bold",
                "regular",
            ),
        ),
        align="center",
        spacing="1",
        on_click=AppState.set_current_tab(tab_value),
        cursor="pointer",
        _hover={"opacity": 0.8},
    )


def bottom_navigation() -> rx.Component:
    """Bottom navigation bar with 4 tabs."""
    return rx.box(
        rx.hstack(
            bottom_nav_item("🏠", "Feed", "feed"),
            bottom_nav_item("📅", "Calendar", "calendar"),
            bottom_nav_item("👨‍👩‍👧‍👦", "Children", "children"),
            bottom_nav_item("⚙️", "Settings", "settings"),
            justify="between",
            width="100%",
            padding="1rem",
        ),
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        bg="gray.2",
        border_top="1px solid",
        border_color="gray.4",
        z_index="1000",
    )
