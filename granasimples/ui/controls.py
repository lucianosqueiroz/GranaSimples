import flet as ft


def dropdown_options(rows: list[dict], label_field: str = "nome") -> list[ft.dropdown.Option]:
    return [ft.dropdown.Option(str(row["id"]), str(row[label_field])) for row in rows]


def show_message(page: ft.Page, message: str, error: bool = False) -> None:
    page.snack_bar = ft.SnackBar(
        ft.Text(message),
        bgcolor=ft.Colors.RED_600 if error else ft.Colors.GREEN_600,
    )
    page.snack_bar.open = True
    page.update()


def section_title(title: str) -> ft.Text:
    return ft.Text(title, size=30, weight=ft.FontWeight.BOLD, color="#0F172A")


def ellipsis_text(value: str, width: int | None = None, expand: bool = False, **kwargs) -> ft.Text:
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
    return ellipsis_text(value, width=width, expand=expand, weight=ft.FontWeight.BOLD, color="#475569", size=12)


def table_header(cells: list[ft.Control]) -> ft.Container:
    return ft.Container(
        content=ft.Row(cells, spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#F8FAFC",
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=10, vertical=10),
    )


def is_active_value(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "falso", "inativo", "inactive", "no", "nao", ""}
    return bool(value)


def _normalize_filter_value(value: str | None) -> str:
    return (value or "").strip().lower()


def status_label(active) -> ft.Container:
    is_active = is_active_value(active)
    color = ft.Colors.GREEN_700 if is_active else ft.Colors.GREY_700
    bgcolor = "#DCFCE7" if is_active else "#F3F4F6"
    return ft.Container(
        ft.Text("Ativo" if is_active else "Inativo", size=12, color=color, weight=ft.FontWeight.BOLD),
        bgcolor=bgcolor,
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        width=76,
    )


def edit_button(on_click) -> ft.IconButton:
    return ft.IconButton(
        ft.Icons.EDIT_OUTLINED,
        tooltip="Editar",
        icon_color="#64748B",
        icon_size=18,
        on_click=on_click,
    )


def delete_button(on_click) -> ft.IconButton:
    return ft.IconButton(
        ft.Icons.DELETE_OUTLINE,
        tooltip="Remover ou inativar",
        icon_color="#94A3B8",
        icon_size=18,
        on_click=on_click,
    )


def toggle_active_button(active, on_click) -> ft.IconButton:
    is_active = is_active_value(active)
    return ft.IconButton(
        ft.Icons.TOGGLE_ON_OUTLINED if is_active else ft.Icons.TOGGLE_OFF_OUTLINED,
        tooltip="Inativar registro" if is_active else "Reativar registro",
        icon_color="#16A34A" if is_active else "#94A3B8",
        icon_size=20,
        on_click=on_click,
    )


def filter_rows(rows: list[dict], text: str = "", tipo: str = "", status: str = "ativos") -> list[dict]:
    text = (text or "").strip().lower()
    tipo = (tipo or "").strip()
    status = _normalize_filter_value(status) or "ativos"

    result = list(rows)
    if status in {"ativos", "ativo"}:
        result = [row for row in result if is_active_value(row.get("ativo", 1))]
    elif status in {"inativos", "inativo"}:
        result = [row for row in result if not is_active_value(row.get("ativo", 1))]

    tipo_normalizado = _normalize_filter_value(tipo)
    if tipo_normalizado and tipo_normalizado not in {"todos", "todas"}:
        result = [
            row
            for row in result
            if _normalize_filter_value(row.get("tipo")) == tipo_normalizado
            or _normalize_filter_value(row.get("categoria_tipo")) == tipo_normalizado
        ]

    if text:
        result = [row for row in result if text in " ".join(str(value).lower() for value in row.values() if value is not None)]
    return result


def confirm_delete(
    page: ft.Page,
    on_confirm,
    message: str = "Sem vinculos, o registro sera excluido. Com vinculos, sera inativado.",
) -> None:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Remover ou inativar"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: _close_dialog(page, dialog)),
            ft.ElevatedButton(
                "Confirmar",
                bgcolor=ft.Colors.RED_600,
                color=ft.Colors.WHITE,
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
