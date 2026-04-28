import flet as ft

from granasimples.services.dashboard_service import DashboardService
from granasimples.ui.controls import section_title
from granasimples.ui.theme import SUCCESS_COLOR, card, money


class DashboardPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.dashboard = DashboardService()

    def build(self) -> ft.Control:
        resumo = self.dashboard.resumo_mes_atual()
        top_categorias = self.dashboard.top_categorias_despesa()
        has_data = any(float(resumo.get(key, 0)) for key in ["receitas", "despesas", "saldo", "cartoes"])
        cards = ft.Row(
            [
                self._metric("Receita do mês", money(resumo["receitas"]), SUCCESS_COLOR, "#ECFDF5", ft.Icons.ARROW_UPWARD),
                self._metric("Despesa do mês", money(resumo["despesas"]), "#DC2626", "#FEF2F2", ft.Icons.ARROW_DOWNWARD),
                self._metric("Saldo do mês", money(resumo["saldo"]), "#334155", "#F1F5F9", ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED),
                self._metric("Gasto no cartão", money(resumo["cartoes"]), "#2563EB", "#EFF6FF", ft.Icons.CREDIT_CARD),
            ],
            wrap=True,
            spacing=18,
            run_spacing=18,
        )

        return ft.Column(
            [
                section_title("GranaSimples"),
                ft.Text("Controle financeiro simples, rápido e sem complicação.", color="#64748B", size=15),
                cards,
                *(
                    []
                    if has_data
                    else [
                        card(
                            ft.Text(
                                "Nenhum lançamento ainda. Comece cadastrando seus gastos.",
                                color="#4B5563",
                                size=15,
                            )
                        )
                    ]
                ),
                card(
                    ft.Column(
                        [
                            ft.Text("Top 3 categorias de despesa", size=16, weight=ft.FontWeight.BOLD),
                            *(self._category_bars(top_categorias) or [ft.Text("Nenhuma despesa no mês atual.", color="#6B7280")]),
                        ],
                        spacing=14,
                    )
                ),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        )

    def _metric(self, title: str, value: str, color: str, icon_bg: str, icon: str) -> ft.Container:
        metric = card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                ft.Icon(icon, color=color, size=22),
                                bgcolor=icon_bg,
                                border_radius=10,
                                padding=10,
                            ),
                        ],
                    ),
                    ft.Text(title, color="#64748B", size=13, weight=ft.FontWeight.W_500),
                    ft.Text(value, size=27, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=12,
            ),
        )
        metric.width = 245
        metric.height = 150
        return metric

    def _category_bars(self, items: list[dict]) -> list[ft.Control]:
        if not items:
            return []
        max_total = max(float(item["total"]) for item in items) or 1
        rows = []
        for item in items:
            total = float(item["total"])
            rows.append(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(item["nome"], expand=True, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS, color="#334155"),
                                ft.Text(money(total), weight=ft.FontWeight.BOLD, color="#DC2626"),
                            ]
                        ),
                        ft.ProgressBar(value=total / max_total, color="#DC2626", bgcolor="#FEE2E2", height=8),
                    ],
                    spacing=5,
                )
            )
        return rows
