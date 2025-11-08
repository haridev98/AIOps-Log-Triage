import reflex as rx
from app.states.state import AIOpsState
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState
from app.components.sidebar import sidebar
from app.components.dashboard import dashboard_content
from app.components.incidents import incidents_page
from app.components.user_management import user_management_page
from app.pages.login import login_page
from app.pages.register import register_page


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                sidebar(),
                rx.el.main(
                    rx.match(
                        AIOpsState.active_page,
                        ("Dashboard", dashboard_content()),
                        ("Incidents", incidents_page()),
                        ("User Management", user_management_page()),
                        dashboard_content(),
                    ),
                    class_name="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950",
                ),
                class_name="flex min-h-screen w-full bg-white dark:bg-gray-900",
            ),
            login_page(),
        ),
        class_name=ThemeState.theme,
        style={"fontFamily": "Raleway"},
    )


app = rx.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    theme=rx.theme(appearance="light", accent_color="blue"),
)
app.add_page(index, on_load=[AuthState.check_login, AIOpsState.on_load_event])
app.add_page(login_page, route="/login", on_load=AuthState.check_not_authed)
app.add_page(register_page, route="/register", on_load=AuthState.check_not_authed)