import reflex as rx
from typing import TypedDict, Literal
import hashlib


class User(TypedDict):
    username: str
    email: str
    password_hash: str
    role: Literal["admin", "user"]


class AuthState(rx.State):
    users: list[User] = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
            "role": "admin",
        }
    ]
    logged_in_user: User | None = None
    error_message: str = ""

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_user is not None

    @rx.event
    def handle_register(self, form_data: dict):
        self.error_message = ""
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "").strip()
        if not username or not email or (not password):
            self.error_message = "All fields are required."
            return
        if any((u["email"] == email for u in self.users)):
            self.error_message = "Email already registered."
            return
        new_user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            role="user",
        )
        self.users.append(new_user)
        return rx.redirect("/login")

    @rx.event
    def handle_login(self, form_data: dict):
        self.error_message = ""
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "").strip()
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        password_hash = self._hash_password(password)
        for user in self.users:
            if user["email"] == email and user["password_hash"] == password_hash:
                self.logged_in_user = user
                return rx.redirect("/")
        self.error_message = "Invalid credentials. Please try again."

    @rx.event
    def handle_logout(self):
        self.logged_in_user = None
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def add_user(self, user_data: dict):
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=self._hash_password(user_data["password"]),
            role=user_data["role"],
        )
        self.users.append(new_user)

    @rx.event
    def edit_user(self, user_data: dict):
        email = user_data["email"]
        for i, u in enumerate(self.users):
            if u["email"] == email:
                self.users[i]["username"] = user_data["username"]
                self.users[i]["role"] = user_data["role"]
                if user_data["password"]:
                    self.users[i]["password_hash"] = self._hash_password(
                        user_data["password"]
                    )
                break

    @rx.event
    def delete_user(self, email: str):
        self.users = [u for u in self.users if u["email"] != email]

    @rx.event
    def check_not_authed(self):
        if self.is_authenticated:
            return rx.redirect("/")