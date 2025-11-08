import reflex as rx
from typing import Literal


class ThemeState(rx.State):
    theme: Literal["light", "dark"] = "light"

    @rx.event
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"

    @rx.var
    def is_dark(self) -> bool:
        return self.theme == "dark"