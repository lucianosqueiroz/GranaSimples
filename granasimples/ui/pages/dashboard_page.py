import flet as ft

from granasimples.services.dashboard_service import DashboardService
from granasimples.ui.theme import money


class DashboardPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.dashboard = DashboardService()

    def build(self) -> ft.Control:
        print("[DEBUG] DashboardPage.build executado")
        resumo, top_categorias = self._load_data()

        return ft.Column(
            [
                ft.Text("GranaSimples", size=30, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("Controle financeiro simples, rapido e sem complicacao.", color="#64748B", size=15),
                ft.Row(
                    [
                        self._metric_panel("Receitas do mes", resumo["receitas"], "#16A34A"),
                        self._metric_panel("Despesas do mes", resumo["despesas"], "#DC2626"),
                        self._metric_panel("Saldo do mes", resumo["saldo"], "#334155"),
                        self._metric_panel("Gasto no cartao", resumo["cartoes"], "#2563EB"),
                    ],
                    spacing=16,
                    run_spacing=16,
                    wrap=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                self._top_categories_panel(top_categorias),
            ],
            spacing=20,
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

    def _metric_panel(self, title: str, value: float, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, color="#64748B", size=13, weight=ft.FontWeight.W_500),
                    ft.Text(money(value), color=color, size=27, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            padding=20,
            width=245,
        )

    def _top_categories_panel(self, items: list[dict]) -> ft.Container:
        rows = self._top_category_rows(items)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Top 3 categorias", size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    *(rows or [ft.Text("Nenhuma despesa no mes atual.", color="#64748B")]),
                ],
                spacing=12,
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            padding=20,
        )

    def _top_category_rows(self, items: list[dict]) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for item in items[:3]:
            rows.append(
                ft.Row(
                    [
                        ft.Text(str(item["nome"]), expand=True, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS, color="#334155"),
                        ft.Text(money(item["total"]), color="#DC2626", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        return rows
