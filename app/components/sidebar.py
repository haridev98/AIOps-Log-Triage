import reflex as rx
from app.states.state import AIOpsState
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def nav_item(icon: str, text: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, size=20, class_name="transition-colors duration-200"),
            rx.el.span(text, class_name="font-medium"),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 rounded-lg bg-blue-100 dark:bg-blue-500/20 px-3 py-2 text-blue-600 dark:text-blue-300 transition-all hover:text-blue-700 dark:hover:text-blue-200",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 dark:text-gray-400 transition-all hover:text-gray-900 dark:hover:text-white",
            ),
        ),
        href="#",
        on_click=lambda: AIOpsState.set_active_page(text),
    )


def theme_toggle() -> rx.Component:
    return rx.el.button(
        rx.icon(
            tag=rx.cond(ThemeState.is_dark, "sun", "moon"),
            size=20,
            class_name="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors",
        ),
        on_click=ThemeState.toggle_theme,
        class_name="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("binary", size=32, class_name="text-blue-600"),
                    class_name="p-2 bg-blue-100 dark:bg-blue-500/20 rounded-lg",
                ),
                rx.el.h1(
                    "AIOps Triage",
                    class_name="text-xl font-bold text-gray-800 dark:text-white",
                ),
                class_name="flex items-center gap-3 border-b border-gray-200 dark:border-gray-700 px-4 py-6",
            ),
            rx.el.nav(
                nav_item(
                    "layout-dashboard",
                    "Dashboard",
                    AIOpsState.active_page == "Dashboard",
                ),
                nav_item("siren", "Incidents", AIOpsState.active_page == "Incidents"),
                rx.cond(
                    (AuthState.logged_in_user != None)
                    & (AuthState.logged_in_user["role"] == "admin"),
                    nav_item(
                        "users",
                        "User Management",
                        AIOpsState.active_page == "User Management",
                    ),
                    None,
                ),
                class_name="flex flex-col gap-1 p-4 flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.logged_in_user['username']}",
                        class_name="h-10 w-10 rounded-full",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.logged_in_user["username"],
                            class_name="font-semibold text-sm text-gray-800 dark:text-white",
                        ),
                        rx.el.p(
                            AuthState.logged_in_user["email"],
                            class_name="text-xs text-gray-500 dark:text-gray-400",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    theme_toggle(),
                    rx.el.button(
                        rx.icon(
                            "log-out",
                            size=20,
                            class_name="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors",
                        ),
                        on_click=AuthState.handle_logout,
                        class_name="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between p-4 border-t border-gray-200 dark:border-gray-700",
            ),
        ),
        class_name="hidden md:flex flex-col h-screen w-72 border-r bg-white dark:bg-gray-800 dark:border-gray-700",
    )