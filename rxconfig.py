import reflex as rx

config = rx.Config(
    app_name="school_hub",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
