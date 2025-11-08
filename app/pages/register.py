import reflex as rx
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def register_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Create an Account",
                    class_name="text-2xl font-bold text-center text-gray-900 dark:text-white",
                ),
                rx.el.p(
                    "Join AIOps Triage to start monitoring your systems.",
                    class_name="text-sm text-gray-500 dark:text-gray-400 text-center",
                ),
                class_name="space-y-2",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder="Your Username",
                            name="username",
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg dark:text-white",
                        ),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder="m@example.com",
                            name="email",
                            type="email",
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg dark:text-white",
                        ),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder="Password",
                            name="password",
                            type="password",
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg dark:text-white",
                        ),
                        class_name="space-y-1",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.icon("badge-alert", size=16, class_name="text-red-600"),
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-sm text-red-600 dark:text-red-300",
                            ),
                            class_name="flex items-center gap-2 p-2 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 rounded-lg",
                        ),
                        None,
                    ),
                    rx.el.button(
                        "Sign Up",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition-colors",
                    ),
                    class_name="space-y-4",
                ),
                on_submit=AuthState.handle_register,
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="font-semibold text-blue-600 hover:underline dark:text-blue-400",
                ),
                class_name="text-sm text-center text-gray-500 dark:text-gray-400",
            ),
            class_name="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 font-['Raleway']",
    )


def register_page() -> rx.Component:
    return register_page_content()