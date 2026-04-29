import flet as ft

from granasimples.services.dashboard_service import DashboardService
from granasimples.ui.controls import section_title
from granasimples.ui.theme import SUCCESS_COLOR, card, money


class DashboardPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.dashboard = DashboardService()

    def build(self) -> ft.Control:
        resumo, top_categorias = self._load_data()

        return ft.Column(
            [
                section_title("GranaSimples"),
                ft.Text("Controle financeiro simples, rapido e sem complicacao.", color="#64748B", size=15),
                ft.Row(
                    [
                        self._metric("Receitas do mes", resumo["receitas"], SUCCESS_COLOR),
                        self._metric("Despesas do mes", resumo["despesas"], "#DC2626"),
                        self._metric("Saldo do mes", resumo["saldo"], "#334155"),
                        self._metric("Gasto no cartao", resumo["cartoes"], "#2563EB"),
                    ],
                    wrap=True,
                    spacing=16,
                    run_spacing=16,
                ),
                card(
                    ft.Column(
                        [
                            ft.Text("Top 3 categorias de despesas", size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            *(self._category_rows(top_categorias) or [ft.Text("Nenhuma despesa no mes atual.", color="#64748B")]),
                        ],
                        spacing=12,
                    )
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _load_data(self) -> tuple[dict[str, float], list[dict]]:
        try:
            resumo = self.dashboard.resumo_mes_atual()
            top_categorias = self.dashboard.top_categorias_despesa()
            return {
                "receitas": float(resumo.get("receitas", 0)),
                "despesas": float(resumo.get("despesas", 0)),
                "saldo": float(resumo.get("saldo", 0)),
                "cartoes": float(resumo.get("cartoes", 0)),
            }, top_categorias
        except Exception as exc:
            print(f"[GranaSimples][Dashboard] Falha ao carregar dados: {exc}")
            return {"receitas": 0, "despesas": 0, "saldo": 0, "cartoes": 0}, []

    def _metric(self, title: str, value: float, color: str) -> ft.Container:
        metric = card(
            ft.Column(
                [
                    ft.Text(title, color="#64748B", size=13, weight=ft.FontWeight.W_500),
                    ft.Text(money(value), size=27, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=10,
            )
        )
        metric.width = 245
        metric.height = 120
        return metric

    def _category_rows(self, items: list[dict]) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for item in items[:3]:
            rows.append(
                ft.Row(
                    [
                        ft.Text(str(item["nome"]), expand=True, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS, color="#334155"),
                        ft.Text(money(item["total"]), weight=ft.FontWeight.BOLD, color="#DC2626"),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        return rows
