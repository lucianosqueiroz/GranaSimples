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
    page.window_min_width = 360
    page.window_min_height = 680


def is_mobile(page: ft.Page) -> bool:
    width = getattr(page, "window_width", None) or getattr(page, "width", None) or 1200
    return width < 700


def is_tablet(page: ft.Page) -> bool:
    width = getattr(page, "window_width", None) or getattr(page, "width", None) or 1200
    return 700 <= width < 1000


def content_padding(page: ft.Page) -> int:
    if is_mobile(page):
        return 12
    if is_tablet(page):
        return 18
    return 24


def responsive_padding(page: ft.Page) -> int:
    return content_padding(page)


def field_width(page: ft.Page, desktop: int = 320) -> int | None:
    if is_mobile(page):
        return None
    if is_tablet(page):
        return min(desktop, 300)
    return desktop


def form_width(page: ft.Page, desktop: int = 380) -> int | None:
    return None if is_mobile(page) or is_tablet(page) else desktop


def responsive_form_list_layout(page: ft.Page, form: ft.Control, listing: ft.Control, spacing: int = 16) -> ft.Control:
    if is_mobile(page) or is_tablet(page):
        if hasattr(form, "expand"):
            form.expand = False
        if hasattr(listing, "expand"):
            listing.expand = False
        return ft.Column([form, listing], spacing=spacing, scroll=ft.ScrollMode.AUTO, expand=True)
    return ft.Row(
        [form, listing],
        spacing=spacing,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


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


def primary_button(text: str, on_click, width: int = 180) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text,
        bgcolor=ROXO,
        color=TEXTO,
        on_click=on_click,
        width=width,
        height=44,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=18, vertical=12),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
        ),
    )


def secondary_button(text: str, on_click, icon=None, width: int = 180) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        text,
        icon=icon,
        icon_color=SUBTEXTO,
        on_click=on_click,
        width=width,
        height=44,
        style=ft.ButtonStyle(
            color=SUBTEXTO,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, BORDER),
            padding=ft.padding.symmetric(horizontal=18, vertical=12),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
        ),
    )


def style_form_controls(controls: list[ft.Control]) -> None:
    for control in controls:
        if isinstance(control, (ft.TextField, ft.Dropdown)):
            control.height = max(control.height or 0, 58)
            control.content_padding = ft.padding.only(left=12, right=12, top=16, bottom=10)


def money(value: float | int | None) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


SUCCESS_COLOR = VERDE
