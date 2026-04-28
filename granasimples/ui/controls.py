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


def status_label(active: bool) -> ft.Container:
    color = ft.Colors.GREEN_700 if active else ft.Colors.GREY_700
    bgcolor = "#DCFCE7" if active else "#F3F4F6"
    return ft.Container(
        ft.Text("Ativo" if active else "Inativo", size=12, color=color, weight=ft.FontWeight.BOLD),
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
        tooltip="Remover",
        icon_color="#94A3B8",
        icon_size=18,
        on_click=on_click,
    )


def toggle_active_button(active: bool, on_click) -> ft.IconButton:
    return ft.IconButton(
        ft.Icons.TOGGLE_ON_OUTLINED if active else ft.Icons.TOGGLE_OFF_OUTLINED,
        tooltip="Inativar" if active else "Reativar",
        icon_color="#16A34A" if active else "#94A3B8",
        icon_size=20,
        on_click=on_click,
    )


def filter_rows(rows: list[dict], text: str = "", tipo: str = "", status: str = "ativos") -> list[dict]:
    text = (text or "").strip().lower()
    tipo = (tipo or "").strip()
    status = status or "ativos"
    result = rows
    if status == "ativos":
        result = [row for row in result if bool(row.get("ativo", 1))]
    elif status == "inativos":
        result = [row for row in result if not bool(row.get("ativo", 1))]
    if tipo:
        result = [row for row in result if row.get("tipo") == tipo or row.get("categoria_tipo") == tipo]
    if text:
        result = [row for row in result if text in " ".join(str(value).lower() for value in row.values() if value is not None)]
    return result


def confirm_delete(page: ft.Page, on_confirm, message: str = "Tem certeza que deseja excluir?") -> None:
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar exclusão"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: _close_dialog(page, dialog)),
            ft.ElevatedButton(
                "Excluir",
                bgcolor=ft.Colors.RED_600,
                color=ft.Colors.WHITE,
                on_click=lambda _: _confirm_and_close(page, dialog, on_confirm),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    if hasattr(page, "open"):
        page.open(dialog)
    else:
        page.dialog = dialog
        dialog.open = True
        page.update()


def _confirm_and_close(page: ft.Page, dialog: ft.AlertDialog, on_confirm) -> None:
    print("[GranaSimples][UI] Confirmação de exclusão acionada.")
    if hasattr(page, "close"):
        page.close(dialog)
    else:
        dialog.open = False
    on_confirm()
    page.update()


def _close_dialog(page: ft.Page, dialog: ft.AlertDialog) -> None:
    if hasattr(page, "close"):
        page.close(dialog)
    else:
        dialog.open = False
    page.update()
