import flet as ft

from granasimples.ui.theme import BORDER, CARD, SUBTEXTO, TABLE_BG, TEXTO, VERDE, VERMELHO


def dropdown_options(rows: list[dict], label_field: str = "nome") -> list[ft.dropdown.Option]:
    return [ft.dropdown.Option(str(row["id"]), str(row[label_field])) for row in rows]


def show_message(page: ft.Page, message: str, error: bool = False) -> None:
    page.snack_bar = ft.SnackBar(
        ft.Text(message, color=TEXTO),
        bgcolor=VERMELHO if error else VERDE,
    )
    page.snack_bar.open = True
    page.update()


def section_title(title: str) -> ft.Text:
    return ft.Text(title, size=30, weight=ft.FontWeight.BOLD, color=TEXTO)


def ellipsis_text(value: str, width: int | None = None, expand: bool = False, **kwargs) -> ft.Text:
    kwargs.setdefault("color", TEXTO)
    return ft.Text(
        value,
        width=width,
        expand=expand,
        max_lines=1,
        no_wrap=True,
        overflow=ft.TextOverflow.ELLIPSIS,
        **kwargs,
    )


def header_cell(value: str, width: int | None = None, expand: bool = False) -> ft.Text:
    return ellipsis_text(value, width=width, expand=expand, weight=ft.FontWeight.BOLD, color=SUBTEXTO, size=12)


def table_header(cells: list[ft.Control]) -> ft.Container:
    return ft.Container(
        content=ft.Row(cells, spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=TABLE_BG,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=10, vertical=10),
        border=ft.border.all(1, BORDER),
    )


def detail_row(label: str, value: str, value_color: str = TEXTO) -> ft.Row:
    return ft.Row(
        [
            ft.Text(label, color=SUBTEXTO, size=12, width=94),
            ft.Text(value, color=value_color, size=13, expand=True, no_wrap=False),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def mobile_record_card(title: str, details: list[tuple[str, str] | tuple[str, str, str]], status, actions: list[ft.Control]) -> ft.Container:
    detail_controls: list[ft.Control] = []
    for detail in details:
        if len(detail) == 3:
            label, value, color = detail
        else:
            label, value = detail
            color = TEXTO
        detail_controls.append(detail_row(label, value, color))

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(title, color=TEXTO, size=15, weight=ft.FontWeight.BOLD, expand=True),
                        status_label(status),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                *detail_controls,
                ft.Row(actions, spacing=4, alignment=ft.MainAxisAlignment.END),
            ],
            spacing=10,
        ),
        bgcolor=CARD,
        border=ft.border.all(1, BORDER),
        border_radius=10,
        padding=14,
    )


def is_active_value(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "falso", "inativo", "inactive", "no", "nao", ""}
    return bool(value)


def _normalize_filter_value(value: str | None) -> str:
    return (value or "").strip().lower()


def status_label(active) -> ft.Container:
    is_active = is_active_value(active)
    color = VERDE if is_active else SUBTEXTO
    bgcolor = "#12251A" if is_active else CARD
    return ft.Container(
        ft.Text("Ativo" if is_active else "Inativo", size=12, color=color, weight=ft.FontWeight.BOLD),
        bgcolor=bgcolor,
        border=ft.border.all(1, BORDER),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        width=76,
    )


def edit_button(on_click) -> ft.IconButton:
    return ft.IconButton(
        ft.Icons.EDIT_OUTLINED,
        tooltip="Editar",
        icon_color=SUBTEXTO,
        icon_size=18,
        on_click=on_click,
    )


def delete_button(on_click) -> ft.IconButton:
    return ft.IconButton(
        ft.Icons.DELETE_OUTLINE,
        tooltip="Remover ou inativar",
        icon_color=SUBTEXTO,
        icon_size=18,
        on_click=on_click,
    )


def toggle_active_button(active, on_click) -> ft.IconButton:
    is_active = is_active_value(active)
    return ft.IconButton(
        ft.Icons.TOGGLE_ON_OUTLINED if is_active else ft.Icons.TOGGLE_OFF_OUTLINED,
        tooltip="Inativar registro" if is_active else "Reativar registro",
        icon_color=VERDE if is_active else SUBTEXTO,
        icon_size=20,
        on_click=on_click,
    )


def filter_rows(rows, text="", tipo="", status="todos"):
    text = (text or "").strip().lower()
    tipo = (tipo or "").strip().lower()
    status = (status or "todos").strip().lower()

    result = list(rows)
    if status == "ativos":
        result = [r for r in result if is_active_value(r.get("ativo", 1))]
    elif status == "inativos":
        result = [r for r in result if not is_active_value(r.get("ativo", 1))]

    if tipo and tipo != "todos":
        result = [r for r in result if str(r.get("tipo", "")).lower() == tipo]

    if text:
        result = [
            r for r in result
            if text in " ".join(str(v).lower() for v in r.values() if v)
        ]

    return result


def confirm_delete(
    page: ft.Page,
    on_confirm,
    message: str = "Sem vínculos, o registro será excluído. Com vínculos, será inativado.",
) -> None:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Remover ou inativar"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: _close_dialog(page, dialog)),
            ft.ElevatedButton(
                "Confirmar",
                bgcolor=VERMELHO,
                color=TEXTO,
                on_click=lambda _: _confirm_and_close(page, dialog, on_confirm),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    _open_dialog(page, dialog)


def _open_dialog(page: ft.Page, dialog: ft.AlertDialog) -> None:
    if hasattr(page, "overlay") and dialog not in page.overlay:
        page.overlay.append(dialog)
    page.dialog = dialog
    dialog.open = True
    page.update()


def _confirm_and_close(page: ft.Page, dialog: ft.AlertDialog, on_confirm) -> None:
    print("[GranaSimples][UI] Confirmacao de remocao acionada.")
    dialog.open = False
    on_confirm()
    page.update()


def _close_dialog(page: ft.Page, dialog: ft.AlertDialog) -> None:
    dialog.open = False
    page.update()
