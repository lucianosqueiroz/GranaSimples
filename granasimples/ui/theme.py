import flet as ft

from granasimples.core.constants import AZUL_PRINCIPAL, FUNDO_CLARO, VERDE_PRINCIPAL


def apply_theme(page: ft.Page) -> None:
    page.title = "GranaSimples"
    page.bgcolor = ft.Colors.WHITE
    page.theme = ft.Theme(color_scheme_seed=AZUL_PRINCIPAL)
    page.padding = 0
    page.window_min_width = 980
    page.window_min_height = 680


def card(content: ft.Control, expand: bool = False) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=20,
        expand=expand,
        border=ft.border.all(1, "#EEF2F7"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=14,
            color="#14000000",
            offset=ft.Offset(0, 4),
        ),
    )


def primary_button(text: str, on_click) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text,
        bgcolor=AZUL_PRINCIPAL,
        color=ft.Colors.WHITE,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=18, vertical=14),
        ),
    )


def money(value: float | int | None) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


SUCCESS_COLOR = VERDE_PRINCIPAL
