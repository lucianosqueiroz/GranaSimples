import flet as ft

from granasimples.services.cartao_service import CartaoService
from granasimples.ui.controls import confirm_delete, delete_button, edit_button, ellipsis_text, header_cell, is_active_value, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import card, money, primary_button


class CartoesPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = CartaoService()
        self.editing_id: int | None = None

    def build(self) -> ft.Control:
        nome = ft.TextField(label="Nome", width=320)
        digitos = ft.TextField(label="4 últimos dígitos", width=320, max_length=4)
        vencimento = ft.TextField(label="Vencimento", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        fechamento = ft.TextField(label="Fechamento", width=150, read_only=True)
        limite = ft.TextField(label="Limite total", width=320, hint_text="R$ 0,00", keyboard_type=ft.KeyboardType.NUMBER)
        filtro_texto = ft.TextField(label="Filtrar", hint_text="Nome ou final", width=220)
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
        rows_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

        def atualizar_fechamento(_=None):
            try:
                fechamento.value = str(self.service.calcular_fechamento(vencimento.value))
            except Exception:
                fechamento.value = ""
            self.page.update()

        def refresh_rows(update_page: bool = True):
            rows = [
                table_header(
                    [
                        header_cell("Nome", expand=True),
                        header_cell("Final", width=64),
                        header_cell("Venc.", width=58),
                        header_cell("Fech.", width=58),
                        header_cell("Limite", width=112),
                        header_cell("Usado", width=112),
                        header_cell("Status", width=76),
                        header_cell("Ações", width=96),
                    ]
                )
            ]
            items = self.service.list_with_limite_usado(False)
            status = (filtro_status.value or "ativos").strip().lower()
            if status == "ativos":
                items = [item for item in items if is_active_value(item.get("ativo", 1))]
            elif status == "inativos":
                items = [item for item in items if not is_active_value(item.get("ativo", 1))]

            texto = (filtro_texto.value or "").strip().lower()
            if texto:
                items = [item for item in items if texto in " ".join(str(value).lower() for value in item.values() if value is not None)]
            for item in items:
                def editar(_, item=item):
                    self.editing_id = item["id"]
                    nome.value = item["nome"]
                    digitos.value = item["ultimos_digitos"]
                    vencimento.value = str(item["dia_vencimento"])
                    fechamento.value = str(item["dia_fechamento"])
                    limite.value = money(item["limite_total"])
                    self.page.update()

                def remover(item=item):
                    print(f"[GranaSimples][UI] Remover cartão id={item['id']}")
                    action = self.service.remove(item["id"])
                    show_message(self.page, "Cartao excluido." if action == "deleted" else "Cartao inativado.")
                    self.refresh_app()

                def alternar(item=item):
                    active = is_active_value(item["ativo"])
                    self.service.set_active(item["id"], not active)
                    show_message(self.page, "Registro reativado." if not active else "Registro inativado.")
                    refresh_rows()

                rows.append(
                    ft.Row(
                        [
                            ellipsis_text(item["nome"], expand=True, weight=ft.FontWeight.W_500),
                            ellipsis_text(item["ultimos_digitos"], width=64),
                            ellipsis_text(str(item["dia_vencimento"]), width=58),
                            ellipsis_text(str(item["dia_fechamento"]), width=58),
                            ellipsis_text(money(item["limite_total"]), width=112),
                            ellipsis_text(money(item["limite_usado"]), width=112),
                            status_label(item["ativo"]),
                            edit_button(editar),
                            toggle_active_button(item["ativo"], lambda _, alternar=alternar: alternar()),
                            delete_button(lambda _, remover=remover: confirm_delete(self.page, remover)),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            if len(rows) == 1:
                rows.append(ft.Text("Nenhum cartão cadastrado."))
            rows_column.controls = rows
            if update_page:
                self.page.update()

        def salvar(_):
            try:
                self.service.save(nome.value, digitos.value, vencimento.value, fechamento.value, limite.value, self.editing_id)
                show_message(self.page, "Cartão salvo.")
                self.refresh_app()
            except Exception as exc:
                show_message(self.page, str(exc), True)

        vencimento.on_change = atualizar_fechamento
        filtro_texto.on_change = lambda _: refresh_rows()
        filtro_status.on_change = lambda _: refresh_rows()
        refresh_rows(False)

        return ft.Column(
            [
                section_title("Cartões"),
                ft.Row(
                    [
                        ft.Container(
                            card(
                                ft.Column(
                                    [nome, digitos, ft.Row([vencimento, fechamento], spacing=20), limite, primary_button("Salvar", salvar)],
                                    spacing=16,
                                )
                            ),
                            width=380,
                        ),
                        card(
                            ft.Column([ft.Row([filtro_texto, filtro_status], wrap=True, spacing=10), rows_column], spacing=12),
                            expand=True,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )
