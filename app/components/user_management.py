import reflex as rx
from app.states.user_management_state import UserManagementState, User


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            user["username"],
            class_name="px-4 py-3 font-medium text-gray-800 dark:text-gray-100",
        ),
        rx.el.td(
            user["email"], class_name="px-4 py-3 text-gray-600 dark:text-gray-400"
        ),
        rx.el.td(
            rx.el.div(
                user["role"].capitalize(),
                class_name=rx.cond(
                    user["role"] == "admin",
                    "w-fit text-xs font-semibold rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300 px-2 py-0.5",
                    "w-fit text-xs font-semibold rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-0.5",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "pencil", size=16, class_name="text-gray-500 dark:text-gray-400"
                    ),
                    on_click=lambda: UserManagementState.open_edit_modal(user),
                    class_name="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors",
                ),
                rx.radix.primitives.dialog.root(
                    rx.radix.primitives.dialog.trigger(
                        rx.el.button(
                            rx.icon("trash-2", size=16, class_name="text-red-500"),
                            class_name="p-1.5 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-md transition-colors",
                        )
                    ),
                    rx.radix.primitives.dialog.content(
                        rx.radix.primitives.dialog.title(
                            "Confirm Deletion",
                            class_name="text-lg font-bold text-gray-900 dark:text-white",
                        ),
                        rx.radix.primitives.dialog.description(
                            f"Are you sure you want to delete user {user['username']}?",
                            class_name="text-gray-600 dark:text-gray-400",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-200 dark:hover:bg-gray-500 transition-colors",
                                )
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Delete",
                                    on_click=lambda: UserManagementState.delete_user(
                                        user["email"]
                                    ),
                                    class_name="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors",
                                )
                            ),
                            class_name="flex justify-end gap-3 mt-4",
                        ),
                        class_name="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg w-full max-w-sm",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3 text-right",
        ),
        class_name="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50/50 dark:hover:bg-gray-700/50",
    )


def user_management_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", size=16, class_name="mr-2"),
                "Add User",
                on_click=UserManagementState.open_add_modal,
                class_name="flex items-center bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.match(
                    UserManagementState.modal_mode,
                    ("add", "Add New User"),
                    ("edit", "Edit User"),
                    "User",
                ),
                class_name="text-xl font-bold mb-4 text-gray-900 dark:text-white",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder="john_doe",
                            name="username",
                            default_value=UserManagementState.current_user[
                                "username"
                            ].to_string(),
                            key=UserManagementState.current_user[
                                "username"
                            ].to_string(),
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg mt-1 dark:text-white",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder="user@example.com",
                            name="email",
                            type="email",
                            default_value=UserManagementState.current_user[
                                "email"
                            ].to_string(),
                            key=UserManagementState.current_user["email"].to_string(),
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg mt-1 disabled:opacity-50 dark:text-white",
                            disabled=UserManagementState.modal_mode == "edit",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.el.input(
                            placeholder=rx.cond(
                                UserManagementState.modal_mode == "edit",
                                "Leave blank to keep current password",
                                "Enter password",
                            ),
                            name="password",
                            type="password",
                            class_name="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg mt-1 dark:text-white",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Role",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300",
                        ),
                        rx.select.root(
                            rx.select.trigger(
                                class_name="w-full text-left flex items-center justify-between px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg mt-1 dark:bg-gray-700 dark:text-white"
                            ),
                            rx.select.content(
                                rx.select.item("User", value="user"),
                                rx.select.item("Admin", value="admin"),
                                class_name="bg-white dark:bg-gray-700 border dark:border-gray-600",
                            ),
                            name="role",
                            default_value=UserManagementState.current_user[
                                "role"
                            ].to_string(),
                            key=UserManagementState.current_user["role"].to_string(),
                        ),
                    ),
                    rx.cond(
                        UserManagementState.error_message != "",
                        rx.el.div(
                            UserManagementState.error_message,
                            class_name="text-sm text-red-600 p-2 bg-red-50 dark:bg-red-500/20 dark:text-red-300 rounded-lg",
                        ),
                        None,
                    ),
                    class_name="flex flex-col gap-4",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-200 dark:hover:bg-gray-500 transition-colors",
                        )
                    ),
                    rx.el.button(
                        "Save User",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors",
                    ),
                    class_name="flex justify-end gap-3 mt-6",
                ),
                on_submit=UserManagementState.handle_submit,
            ),
            class_name="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg w-full max-w-lg",
        ),
        open=UserManagementState.is_modal_open,
        on_open_change=UserManagementState.set_is_modal_open,
    )


def user_management_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "User Management",
                    class_name="text-3xl font-bold text-gray-900 dark:text-white",
                ),
                rx.el.p(
                    "Manage users and their permissions.",
                    class_name="text-gray-600 dark:text-gray-400",
                ),
            ),
            user_management_modal(),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Username",
                            class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600 dark:text-gray-400",
                        ),
                        rx.el.th(
                            "Email",
                            class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600 dark:text-gray-400",
                        ),
                        rx.el.th(
                            "Role",
                            class_name="px-4 py-3 text-left text-sm font-semibold text-gray-600 dark:text-gray-400",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-4 py-3 text-right text-sm font-semibold text-gray-600 dark:text-gray-400",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(UserManagementState.users, user_row)),
                class_name="w-full table-auto",
            ),
            class_name="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden",
        ),
        on_mount=UserManagementState.load_users,
        class_name="flex-1 p-8 overflow-y-auto",
    )