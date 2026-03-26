"""School Hub - Unified School Monitoring Platform.

Mobile-first dashboard for monitoring multiple children across school providers.
Built with Reflex framework following TDD and Clean Code principles.
"""

import reflex as rx
from school_hub.state import AppState
from school_hub.components.navigation import bottom_navigation
from school_hub.components.views import render_current_view


def index() -> rx.Component:
    """Main application layout with mobile-first design."""
    return rx.box(
        # Main content area
        rx.box(
            render_current_view(),
            padding_bottom="5rem",  # Space for bottom nav
            min_height="100vh",
        ),
        # Bottom navigation (fixed)
        bottom_navigation(),
        # Mobile-first container
        max_width="400px",
        margin="0 auto",
        bg="gray.1",
        min_height="100vh",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
    )
)
app.add_page(index, title="School Hub")
