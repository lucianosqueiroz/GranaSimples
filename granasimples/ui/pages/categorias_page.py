import flet as ft

from granasimples.core.constants import TIPO_DESPESA, TIPO_RECEITA
from granasimples.services.categoria_service import CategoriaService
from granasimples.ui.controls import confirm_delete, delete_button, edit_button, ellipsis_text, filter_rows, header_cell, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, primary_button


class CategoriasPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = CategoriaService()
        self.editing_id: int | None = None

    def build(self) -> ft.Control:
        nome = ft.TextField(label="Nome", width=320)
        tipo = ft.Dropdown(
            label="Tipo",
            value=TIPO_DESPESA,
            options=[ft.dropdown.Option(TIPO_DESPESA, "Despesa"), ft.dropdown.Option(TIPO_RECEITA, "Receita")],
            width=180,
        )
        filtro_texto = ft.TextField(label="Filtrar", hint_text="Nome", width=220)
        filtro_tipo = ft.Dropdown(
            label="Tipo",
            value="",
            options=[ft.dropdown.Option("", "Todos"), ft.dropdown.Option(TIPO_DESPESA, "Despesa"), ft.dropdown.Option(TIPO_RECEITA, "Receita")],
            width=150,
        )
        filtro_status = ft.Dropdown(
            label="Status",
            value="ativos",
            options=[
                ft.dropdown.Option("ativos", "Ativos"),
                ft.dropdown.Option("inativos", "Inativos"),
                ft.dropdown.Option("todos", "Todos"),
            ],
            width=130,
        )

        def salvar(_):
            try:
                self.service.save(nome.value, tipo.value, self.editing_id)
                show_message(self.page, "Categoria salva.")
                self.refresh_app()
            except Exception as exc:
                show_message(self.page, str(exc), True)

        rows_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

        def refresh_rows(update_page: bool = True):
            rows = [
                table_header(
                    [
                        header_cell("Nome", expand=True),
                        header_cell("Tipo", width=100),
                        header_cell("Status", width=76),
                        header_cell("Ações", width=96),
                    ]
                )
            ]
            items = filter_rows(self.service.list_all(False), filtro_texto.value, filtro_tipo.value, filtro_status.value)
            for item in items:
                def editar(_, item=item):
                    self.editing_id = item["id"]
                    nome.value = item["nome"]
                    tipo.value = item["tipo"]
                    self.page.update()

                def remover(item=item):
                    print(f"[GranaSimples][UI] Remover categoria id={item['id']}")
                    self.service.remove(item["id"])
                    show_message(self.page, "Categoria removida ou inativada.")
                    refresh_rows()

                def alternar(item=item):
                    self.service.set_active(item["id"], not bool(item["ativo"]))
                    show_message(self.page, "Status atualizado.")
                    refresh_rows()

                rows.append(
                    ft.Row(
                        [
                            ellipsis_text(item["nome"], expand=True),
                            ellipsis_text(item["tipo"], width=100),
                            status_label(bool(item["ativo"])),
                            edit_button(editar),
                            toggle_active_button(bool(item["ativo"]), lambda _, alternar=alternar: alternar()),
                            delete_button(lambda _, remover=remover: confirm_delete(self.page, remover)),
                        ],
                        spacing=8,
                    )
                )
            if len(rows) == 1:
                rows.append(ft.Text("Nenhuma categoria cadastrada."))
            rows_column.controls = rows
            if update_page:
                self.page.update()

        filtro_texto.on_change = refresh_rows
        filtro_tipo.on_change = refresh_rows
        filtro_status.on_change = refresh_rows
        refresh_rows(False)

        return ft.Column(
            [
                section_title("Categorias"),
                ft.Row(
                    [
                        ft.Container(card(ft.Column([nome, tipo, primary_button("Salvar", salvar)], spacing=16)), width=380),
                        card(
                            ft.Column([ft.Row([filtro_texto, filtro_tipo, filtro_status], wrap=True, spacing=10), rows_column], spacing=12),
                            expand=True,
                        ),
                    ],
                    spacing=16,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
