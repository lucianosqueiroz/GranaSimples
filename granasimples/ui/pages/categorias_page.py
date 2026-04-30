import flet as ft

from granasimples.core.constants import TIPO_DESPESA, TIPO_RECEITA
from granasimples.services.categoria_service import CategoriaService
from granasimples.ui.controls import confirm_delete, delete_button, edit_button, ellipsis_text, filter_rows, header_cell, is_active_value, mobile_record_card, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, field_width, fit_mobile_controls, form_width, is_mobile, primary_button, responsive_form_list_layout, style_form_controls


class CategoriasPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = CategoriaService()
        self.editing_id: int | None = None
        self._render_list = lambda: None

    def _on_filter_change(self, e):
        self._render_list()

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
        style_form_controls([nome, tipo, filtro_texto, filtro_tipo, filtro_status])
        nome.width = field_width(self.page)
        tipo.width = field_width(self.page, 180)
        fit_mobile_controls(self.page, [nome, tipo, filtro_texto, filtro_tipo, filtro_status])

        def salvar(_):
            try:
                self.service.save(nome.value, tipo.value, self.editing_id)
                show_message(self.page, "Categoria salva.")
                self.refresh_app()
            except Exception as exc:
                show_message(self.page, str(exc), True)

        rows_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

        def refresh_rows(update_page: bool = True):
            mobile = is_mobile(self.page)
            rows = [] if mobile else [
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
                    action = self.service.remove(item["id"])
                    show_message(self.page, "Categoria excluída." if action == "deleted" else "Categoria inativada.")
                    self.refresh_app()

                def alternar(item=item):
                    active = is_active_value(item["ativo"])
                    self.service.set_active(item["id"], not active)
                    show_message(self.page, "Registro reativado." if not active else "Registro inativado.")
                    refresh_rows()

                actions = [
                    edit_button(editar),
                    toggle_active_button(item["ativo"], lambda _, alternar=alternar: alternar()),
                    delete_button(lambda _, remover=remover: confirm_delete(self.page, remover)),
                ]
                if mobile:
                    rows.append(
                        mobile_record_card(item["nome"], [("Tipo", item["tipo"])], item["ativo"], actions)
                    )
                else:
                    rows.append(
                        ft.Row(
                            [
                                ellipsis_text(item["nome"], expand=True),
                                ellipsis_text(item["tipo"], width=100),
                                status_label(item["ativo"]),
                                *actions,
                            ],
                            spacing=8,
                        )
                    )
            if not items:
                rows.append(ft.Text("Nenhuma categoria cadastrada."))
            rows_column.controls = rows
            if update_page:
                self.page.update()

        self._render_list = refresh_rows
        filtro_texto.on_change = self._on_filter_change
        filtro_tipo.on_change = self._on_filter_change
        filtro_tipo.on_select = self._on_filter_change
        filtro_status.on_change = self._on_filter_change
        filtro_status.on_select = self._on_filter_change
        refresh_rows(False)

        form_card = ft.Container(card(ft.Column([nome, tipo, primary_button("Salvar", salvar)], spacing=16)), width=form_width(self.page))
        list_card = card(
            ft.Column([ft.Row([filtro_texto, filtro_tipo, filtro_status], wrap=True, spacing=10), rows_column], spacing=12),
            expand=True,
        )

        return ft.Column(
            [
                section_title("Categorias"),
                responsive_form_list_layout(self.page, form_card, list_card),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
