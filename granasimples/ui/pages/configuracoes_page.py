import flet as ft

from granasimples.services.configuracao_service import ConfiguracaoService
from granasimples.ui.controls import section_title, show_message
from granasimples.ui.theme import SUBTEXTO, TEXTO, card, primary_button


class ConfiguracoesPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = ConfiguracaoService()

    def build(self) -> ft.Control:
        dias_fechamento = ft.TextField(
            label="Dias padrão de fechamento do cartão",
            value=str(self.service.get_dias_fechamento_cartao()),
            width=320,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        percentual_alerta = ft.TextField(
            label="Percentual de alerta de orçamento",
            value=str(self.service.get_percentual_alerta_orcamento()),
            width=320,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def salvar(_):
            try:
                self.service.save(dias_fechamento.value, percentual_alerta.value)
                show_message(self.page, "Configurações salvas.")
            except Exception as exc:
                show_message(self.page, str(exc), True)

        return ft.Column(
            [
                section_title("Configurações"),
                ft.Container(
                    card(
                        ft.Column(
                            [
                                ft.Text("Padrões do sistema", size=16, weight=ft.FontWeight.BOLD, color=TEXTO),
                                dias_fechamento,
                                ft.Column(
                                    [
                                        percentual_alerta,
                                        ft.Text("Informe apenas o número. Exemplo: 80 para 80%.", size=12, color=SUBTEXTO),
                                    ],
                                    spacing=4,
                                ),
                                primary_button("Salvar configurações", salvar),
                            ],
                            spacing=16,
                        )
                    ),
                    width=420,
                ),
            ],
            spacing=20,
        )
