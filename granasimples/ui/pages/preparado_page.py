import flet as ft

from granasimples.ui.controls import section_title
from granasimples.ui.theme import SUBTEXTO, card


class PreparadoPage:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    def build(self) -> ft.Control:
        return ft.Column(
            [
                section_title(self.title),
                card(ft.Text(self.description, color=SUBTEXTO)),
            ],
            spacing=16,
        )
