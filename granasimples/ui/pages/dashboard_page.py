import base64

import flet as ft

from granasimples.services.dashboard_service import DashboardService
from granasimples.ui.theme import BORDER, CARD, ROXO, SUBTEXTO, TEXTO, VERDE, VERMELHO, is_mobile, money


class DashboardPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.dashboard = DashboardService()

    def build(self) -> ft.Control:
        print("[DEBUG] DashboardPage.build executado")
        resumo, top_categorias = self._load_data()
        metric_cards = [
            self._metric_panel("Receitas do mês", resumo["receitas"], VERDE),
            self._metric_panel("Despesas do mês", resumo["despesas"], VERMELHO),
            self._metric_panel("Saldo do mês", resumo["saldo"], TEXTO),
            self._metric_panel("Gasto no cartão", resumo["cartoes"], ROXO),
        ]
        metrics_layout = (
            ft.Column(metric_cards, spacing=12)
            if is_mobile(self.page)
            else ft.Row(metric_cards, spacing=16, run_spacing=16, wrap=True, vertical_alignment=ft.CrossAxisAlignment.START)
        )

        return ft.Column(
            [
                ft.Text("GranaSimples", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
                ft.Text("Controle financeiro simples, rápido e sem complicação.", color=SUBTEXTO, size=15),
                metrics_layout,
                self._top_categories_panel(top_categorias),
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

    def _metric_panel(self, title: str, value: float, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, color=SUBTEXTO, size=13, weight=ft.FontWeight.W_500),
                    ft.Text(money(value), color=color, size=27, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            bgcolor=CARD,
            border=ft.border.all(1, BORDER),
            border_radius=12,
            padding=20,
            width=None if is_mobile(self.page) else 245,
        )

    def _top_categories_panel(self, items: list[dict]) -> ft.Container:
        rows = self._insight_rows(items)
        return ft.Container(
            content=ft.Row(
                [
                    self._donut_chart(items),
                    ft.Column(
                        [
                            ft.Text("Despesas por categoria", size=16, weight=ft.FontWeight.BOLD, color=TEXTO),
                            *(rows or [ft.Text("Nenhuma despesa no mês atual.", color=SUBTEXTO)]),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=28,
                wrap=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=CARD,
            border=ft.border.all(1, BORDER),
            border_radius=12,
            padding=20,
        )

    def _donut_chart(self, items: list[dict]) -> ft.Container:
        total = sum(float(item["total"] or 0) for item in items[:3])
        # TODO: Futuro módulo Planejamento Mensal / Metas e Previsões:
        # despesas fixas recorrentes, meta de sobra mensal e previsão de saldo futuro.
        return ft.Container(
            content=ft.Stack(
                [
                    ft.Image(
                        src=self._donut_svg_src(items),
                        width=196,
                        height=196,
                        fit=ft.BoxFit.CONTAIN,
                        anti_alias=True,
                    ),
                    ft.Container(
                        left=42,
                        top=42,
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Total gasto", color=SUBTEXTO, size=12),
                                    ft.Text(money(total), color=TEXTO, size=18, weight=ft.FontWeight.BOLD),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=2,
                            ),
                            alignment=ft.Alignment(0, 0),
                            bgcolor=CARD,
                            border=ft.border.all(1, BORDER),
                            border_radius=72,
                            width=112,
                            height=112,
                        ),
                    ),
                ],
                width=196,
                height=196,
            ),
            width=196,
            height=196,
        )

    def _donut_svg_src(self, items: list[dict]) -> str:
        chart_colors = ["#8A05BE", "#A855F7", "#C084FC", "#7E22CE"]
        values = [float(item["total"] or 0) for item in items[:3]]
        total = sum(values)
        radius = 74
        stroke = 28
        circumference = 2 * 3.14159265 * radius
        circles = [
            f'<circle cx="98" cy="98" r="{radius}" fill="none" stroke="#24112E" stroke-width="{stroke}" />'
        ]

        if total <= 0:
            circles.append(
                f'<circle cx="98" cy="98" r="{radius}" fill="none" stroke="{ROXO}" stroke-width="{stroke}" '
                f'stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="0" '
                'transform="rotate(-90 98 98)" filter="url(#glow)" />'
            )
        else:
            offset = 0.0
            gap = 5.0
            for index, value in enumerate(values):
                if value <= 0:
                    continue
                segment = max((value / total * circumference) - gap, 0)
                color = chart_colors[index % len(chart_colors)]
                circles.append(
                    f'<circle cx="98" cy="98" r="{radius}" fill="none" stroke="{color}" stroke-width="{stroke}" '
                    f'stroke-linecap="round" stroke-dasharray="{segment:.2f} {circumference:.2f}" '
                    f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 98 98)" filter="url(#glow)" />'
                )
                offset += value / total * circumference

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="196" height="196" viewBox="0 0 196 196">'
            '<defs><filter id="glow" x="-25%" y="-25%" width="150%" height="150%">'
            '<feGaussianBlur stdDeviation="2.8" result="blur"/>'
            '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
            '</filter></defs>'
            + "".join(circles)
            + "</svg>"
        )
        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"

    def _insight_rows(self, items: list[dict]) -> list[ft.Control]:
        rows: list[ft.Control] = []
        chart_colors = ["#8A05BE", "#A855F7", "#C084FC", "#22C55E"]
        total_geral = sum(float(item["total"] or 0) for item in items[:3])
        name_width = 110 if is_mobile(self.page) else 155
        value_width = 92 if is_mobile(self.page) else 108
        for index, item in enumerate(items[:3]):
            total = float(item["total"] or 0)
            percent = (total / total_geral * 100) if total_geral else 0
            label, label_color = self._impact_label(percent)
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(width=10, height=10, border_radius=10, bgcolor=chart_colors[index % len(chart_colors)]),
                            ft.Text(str(item["nome"]), width=name_width, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS, color=TEXTO),
                            ft.Text(f"{percent:.0f}%", color=SUBTEXTO, size=12, width=42),
                            ft.Text(money(total), color=TEXTO, weight=ft.FontWeight.BOLD, width=value_width),
                            ft.Container(
                                ft.Text(label, color=label_color, size=11, weight=ft.FontWeight.BOLD),
                                border=ft.border.all(1, label_color),
                                border_radius=16,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        tight=True,
                    ),
                    padding=ft.padding.symmetric(vertical=4),
                ),
            )
        return rows

    def _impact_label(self, percent: float) -> tuple[str, str]:
        if percent > 60:
            return "Alto impacto", VERMELHO
        if percent >= 30:
            return "Atenção", "#F59E0B"
        return "Controlado", VERDE
