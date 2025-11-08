import reflex as rx
from typing import TypedDict, Literal
from app.states.auth_state import AuthState, User

_DEFAULT_USER = {"username": "", "email": "", "password_hash": "", "role": "user"}


class UserManagementState(rx.State):
    users: list[User] = []
    is_modal_open: bool = False
    modal_mode: Literal["add", "edit"] = "add"
    current_user_email: str = ""
    error_message: str = ""

    @rx.var
    def current_user(self) -> User:
        if self.modal_mode == "edit":
            for user in self.users:
                if user["email"] == self.current_user_email:
                    return user
        return _DEFAULT_USER

    @rx.event
    async def load_users(self):
        auth_state = await self.get_state(AuthState)
        self.users = auth_state.users

    def _reset_modal(self):
        self.is_modal_open = False
        self.current_user_email = ""
        self.error_message = ""

    @rx.event
    def open_add_modal(self):
        self.modal_mode = "add"
        self.is_modal_open = True
        self.current_user_email = ""
        self.error_message = ""

    @rx.event
    def open_edit_modal(self, user: User):
        self.modal_mode = "edit"
        self.is_modal_open = True
        self.current_user_email = user["email"]
        self.error_message = ""

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.error_message = ""
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "").strip()
        role = form_data.get("role", "user")
        if not username or (self.modal_mode == "add" and (not email)):
            self.error_message = "Username and email are required."
            return
        if self.modal_mode == "add" and (not password):
            self.error_message = "Password is required for new users."
            return
        auth_state = await self.get_state(AuthState)
        if self.modal_mode == "add":
            if any((u["email"] == email for u in auth_state.users)):
                self.error_message = "Email already exists."
                return
            yield AuthState.add_user(
                dict(username=username, email=email, password=password, role=role)
            )
        else:
            yield AuthState.edit_user(
                dict(
                    username=username,
                    email=self.current_user_email,
                    password=password,
                    role=role,
                )
            )
        self._reset_modal()
        yield UserManagementState.load_users

    @rx.event
    async def delete_user(self, email: str):
        yield AuthState.delete_user(email)
        yield UserManagementState.load_users