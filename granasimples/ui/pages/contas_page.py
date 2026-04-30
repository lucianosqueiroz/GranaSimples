import flet as ft

from granasimples.services.conta_service import ContaService
from granasimples.services.base_service import parse_float
from granasimples.ui.controls import confirm_delete, delete_button, edit_button, ellipsis_text, filter_rows, header_cell, is_active_value, mobile_record_card, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, field_width, fit_mobile_controls, form_width, is_mobile, money, primary_button, responsive_form_list_layout, style_form_controls


class ContasPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = ContaService()
        self.editing_id: int | None = None
        self._render_list = lambda: None

    def _on_filter_change(self, e):
        self._render_list()

    def build(self) -> ft.Control:
        nome = ft.TextField(label="Nome", width=320)
        tipo = ft.Dropdown(
            label="Tipo",
            value="banco",
            options=[
                ft.dropdown.Option("banco", "Banco"),
                ft.dropdown.Option("carteira", "Carteira"),
                ft.dropdown.Option("outro", "Outro"),
            ],
            width=320,
        )
        saldo = ft.TextField(label="Saldo atual", value=money(0), width=320, keyboard_type=ft.KeyboardType.NUMBER)
        filtro_texto = ft.TextField(label="Filtrar", hint_text="Nome ou tipo", width=220)
        tipos_cadastrados = sorted({str(item["tipo"]) for item in self.service.list_all(False)})
        filtro_tipo = ft.Dropdown(
            label="Tipo",
            value="",
            options=[ft.dropdown.Option("", "Todos")] + [ft.dropdown.Option(tipo_item, tipo_item) for tipo_item in tipos_cadastrados],
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
        style_form_controls([nome, tipo, saldo, filtro_texto, filtro_tipo, filtro_status])
        nome.width = field_width(self.page)
        tipo.width = field_width(self.page)
        saldo.width = field_width(self.page)
        fit_mobile_controls(self.page, [nome, tipo, saldo, filtro_texto, filtro_tipo, filtro_status])

        def formatar_saldo(_):
            try:
                saldo.value = money(parse_float(saldo.value, "Saldo atual"))
            except Exception:
                saldo.value = money(0)
            self.page.update()

        saldo.on_blur = formatar_saldo

        def salvar(_):
            try:
                self.service.save(nome.value, tipo.value, saldo.value, self.editing_id)
                show_message(self.page, "Conta salva.")
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
                        header_cell("Saldo", width=130),
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
                    saldo.value = money(item["saldo_atual"])
                    self.page.update()

                def remover(item=item):
                    print(f"[GranaSimples][UI] Remover conta id={item['id']}")
                    action = self.service.remove(item["id"])
                    show_message(self.page, "Conta excluída." if action == "deleted" else "Conta inativada.")
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
                        mobile_record_card(item["nome"], [("Tipo", item["tipo"]), ("Saldo", money(item["saldo_atual"]))], item["ativo"], actions)
                    )
                else:
                    rows.append(
                        ft.Row(
                            [
                                ellipsis_text(item["nome"], expand=True),
                                ellipsis_text(item["tipo"], width=100),
                                ellipsis_text(money(item["saldo_atual"]), width=130),
                                status_label(item["ativo"]),
                                *actions,
                            ],
                            spacing=8,
                        )
                    )
            if not items:
                rows.append(ft.Text("Nenhuma conta cadastrada."))
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

        form_card = ft.Container(card(ft.Column([nome, tipo, saldo, primary_button("Salvar", salvar)], spacing=16)), width=form_width(self.page))
        list_card = card(
            ft.Column(
                [ft.Row([filtro_texto, filtro_tipo, filtro_status], wrap=True, spacing=10), rows_column],
                spacing=12,
            ),
            expand=True,
        )

        return ft.Column(
            [
                section_title("Contas"),
                responsive_form_list_layout(self.page, form_card, list_card),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
