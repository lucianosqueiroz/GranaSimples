import flet as ft

from granasimples.services.categoria_service import CategoriaService
from granasimples.services.subcategoria_service import SubcategoriaService
from granasimples.ui.controls import confirm_delete, delete_button, dropdown_options, edit_button, ellipsis_text, filter_rows, header_cell, is_active_value, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, primary_button


class SubcategoriasPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = SubcategoriaService()
        self.categorias = CategoriaService()
        self.editing_id: int | None = None
        self._render_list = lambda: None

    def _on_filter_change(self, e):
        self._render_list()

    def build(self) -> ft.Control:
        categoria = ft.Dropdown(label="Categoria", options=dropdown_options(self.categorias.list_all()), width=320)
        nome = ft.TextField(label="Nome", width=320)
        filtro_texto = ft.TextField(label="Filtrar", hint_text="Nome ou categoria", width=240)
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
                self.service.save(categoria.value, nome.value, self.editing_id)
                show_message(self.page, "Subcategoria salva.")
                self.refresh_app()
            except Exception as exc:
                show_message(self.page, str(exc), True)

        rows_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

        def refresh_rows(update_page: bool = True):
            rows = [
                table_header(
                    [
                        header_cell("Nome", expand=True),
                        header_cell("Categoria", width=180),
                        header_cell("Status", width=76),
                        header_cell("Ações", width=96),
                    ]
                )
            ]
            items = filter_rows(self.service.list_with_categoria(False), filtro_texto.value, "", filtro_status.value)
            for item in items:
                def editar(_, item=item):
                    self.editing_id = item["id"]
                    categoria.value = str(item["categoria_id"])
                    nome.value = item["nome"]
                    self.page.update()

                def remover(item=item):
                    print(f"[GranaSimples][UI] Remover subcategoria id={item['id']}")
                    action = self.service.remove(item["id"])
                    show_message(self.page, "Subcategoria excluida." if action == "deleted" else "Subcategoria inativada.")
                    self.refresh_app()

                def alternar(item=item):
                    active = is_active_value(item["ativo"])
                    self.service.set_active(item["id"], not active)
                    show_message(self.page, "Registro reativado." if not active else "Registro inativado.")
                    refresh_rows()

                rows.append(
                    ft.Row(
                        [
                            ellipsis_text(item["nome"], expand=True),
                            ellipsis_text(item["categoria_nome"], width=180),
                            status_label(item["ativo"]),
                            edit_button(editar),
                            toggle_active_button(item["ativo"], lambda _, alternar=alternar: alternar()),
                            delete_button(lambda _, remover=remover: confirm_delete(self.page, remover)),
                        ],
                        spacing=8,
                    )
                )
            if len(rows) == 1:
                rows.append(ft.Text("Nenhuma subcategoria cadastrada."))
            rows_column.controls = rows
            if update_page:
                self.page.update()

        self._render_list = refresh_rows
        filtro_texto.on_change = self._on_filter_change
        filtro_status.on_change = self._on_filter_change
        filtro_status.on_select = self._on_filter_change
        refresh_rows(False)

        return ft.Column(
            [
                section_title("Subcategorias"),
                ft.Row(
                    [
                        ft.Container(card(ft.Column([categoria, nome, primary_button("Salvar", salvar)], spacing=16)), width=380),
                        card(
                            ft.Column([ft.Row([filtro_texto, filtro_status], wrap=True, spacing=10), rows_column], spacing=12),
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
