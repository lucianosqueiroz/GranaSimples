import flet as ft

FUNDO = "#0B0B0F"
CARD = "#15161C"
ROXO = "#8A05BE"
TEXTO = "#FFFFFF"
SUBTEXTO = "#A1A1AA"
VERDE = "#22C55E"
VERMELHO = "#EF4444"
BORDER = "#27272A"
TABLE_BG = "#101116"


def apply_theme(page: ft.Page) -> None:
    page.title = "GranaSimples"
    page.bgcolor = FUNDO
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ROXO)
    page.padding = 0
    page.window_min_width = 980
    page.window_min_height = 680


def card(content: ft.Control, expand: bool = False) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=12,
        padding=20,
        expand=expand,
        border=ft.border.all(1, BORDER),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=14,
            color="#66000000",
            offset=ft.Offset(0, 4),
        ),
    )


def primary_button(text: str, on_click) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text,
        bgcolor=ROXO,
        color=TEXTO,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=18, vertical=14),
        ),
    )


def money(value: float | int | None) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


SUCCESS_COLOR = VERDE
