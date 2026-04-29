import flet as ft

from granasimples.services.conta_service import ContaService
from granasimples.services.base_service import parse_float
from granasimples.ui.controls import confirm_delete, delete_button, edit_button, ellipsis_text, header_cell, is_active_value, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, money, primary_button


class ContasPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = ContaService()
        self.editing_id: int | None = None

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
            rows = [
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
            items = self.service.list_all(False)
            status = (filtro_status.value or "ativos").strip().lower()
            if status == "ativos":
                items = [item for item in items if is_active_value(item.get("ativo", 1))]
            elif status == "inativos":
                items = [item for item in items if not is_active_value(item.get("ativo", 1))]

            tipo_filtro = (filtro_tipo.value or "").strip().lower()
            if tipo_filtro and tipo_filtro != "todos":
                items = [item for item in items if str(item.get("tipo", "")).strip().lower() == tipo_filtro]

            texto = (filtro_texto.value or "").strip().lower()
            if texto:
                items = [item for item in items if texto in " ".join(str(value).lower() for value in item.values() if value is not None)]
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
                    show_message(self.page, "Conta excluida." if action == "deleted" else "Conta inativada.")
                    refresh_rows()

                def alternar(item=item):
                    active = is_active_value(item["ativo"])
                    self.service.set_active(item["id"], not active)
                    show_message(self.page, "Registro reativado." if not active else "Registro inativado.")
                    refresh_rows()

                rows.append(
                    ft.Row(
                        [
                            ellipsis_text(item["nome"], expand=True),
                            ellipsis_text(item["tipo"], width=100),
                            ellipsis_text(money(item["saldo_atual"]), width=130),
                            status_label(item["ativo"]),
                            edit_button(editar),
                            toggle_active_button(item["ativo"], lambda _, alternar=alternar: alternar()),
                            delete_button(lambda _, remover=remover: confirm_delete(self.page, remover)),
                        ],
                        spacing=8,
                    )
                )
            if len(rows) == 1:
                rows.append(ft.Text("Nenhuma conta cadastrada."))
            rows_column.controls = rows
            if update_page:
                self.page.update()

        filtro_texto.on_change = lambda _: refresh_rows()
        filtro_tipo.on_change = lambda _: refresh_rows()
        filtro_status.on_change = lambda _: refresh_rows()
        refresh_rows(False)

        return ft.Column(
            [
                section_title("Contas"),
                ft.Row(
                    [
                        ft.Container(card(ft.Column([nome, tipo, saldo, primary_button("Salvar", salvar)], spacing=16)), width=380),
                        card(
                            ft.Column(
                                [ft.Row([filtro_texto, filtro_tipo, filtro_status], wrap=True, spacing=10), rows_column],
                                spacing=12,
                            ),
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
