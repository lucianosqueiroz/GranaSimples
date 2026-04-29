import flet as ft

from granasimples.ui.pages.cartoes_page import CartoesPage
from granasimples.ui.pages.categorias_page import CategoriasPage
from granasimples.ui.pages.contas_page import ContasPage
from granasimples.ui.pages.configuracoes_page import ConfiguracoesPage
from granasimples.ui.pages.dashboard_page import DashboardPage
from granasimples.ui.pages.lancamentos_page import LancamentosPage
from granasimples.ui.pages.pessoas_page import PessoasPage
from granasimples.ui.pages.subcategorias_page import SubcategoriasPage
from granasimples.ui.theme import BORDER, CARD, FUNDO, ROXO, SUBTEXTO, TEXTO, apply_theme


class GranaSimplesApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.content = ft.Container(expand=True, padding=ft.padding.symmetric(horizontal=28, vertical=26), bgcolor=FUNDO)
        self.selected_index = 0

    def build(self) -> None:
        apply_theme(self.page)
        self.rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=96,
            min_extended_width=180,
            bgcolor=CARD,
            indicator_color=ROXO,
            selected_label_text_style=ft.TextStyle(color=TEXTO, weight=ft.FontWeight.BOLD),
            unselected_label_text_style=ft.TextStyle(color=SUBTEXTO),
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
                ft.NavigationRailDestination(icon=ft.Icons.GROUP_OUTLINED, label="Pessoas"),
                ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, label="Contas"),
                ft.NavigationRailDestination(icon=ft.Icons.CATEGORY_OUTLINED, label="Categorias"),
                ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_TREE_OUTLINED, label="Subcategorias"),
                ft.NavigationRailDestination(icon=ft.Icons.CREDIT_CARD, label="Cartões"),
                ft.NavigationRailDestination(icon=ft.Icons.SWAP_VERT, label="Lançamentos"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Configurações"),
            ],
            on_change=self._navigate,
        )
        self.page.add(
            ft.Row(
                [
                    ft.Container(
                        self.rail,
                        bgcolor=CARD,
                        border=ft.border.only(right=ft.BorderSide(1, BORDER)),
                    ),
                    self.content,
                ],
                expand=True,
                spacing=0,
            )
        )
        self._render()

    def _navigate(self, event: ft.ControlEvent) -> None:
        self.selected_index = event.control.selected_index
        self._render()

    def _render(self) -> None:
        pages = [
            DashboardPage(self.page).build,
            PessoasPage(self.page, self._render).build,
            ContasPage(self.page, self._render).build,
            CategoriasPage(self.page, self._render).build,
            SubcategoriasPage(self.page, self._render).build,
            CartoesPage(self.page, self._render).build,
            LancamentosPage(self.page, self._render).build,
            ConfiguracoesPage(self.page, self._render).build,
        ]
        if self.selected_index >= len(pages):
            self.selected_index = 0
            self.rail.selected_index = 0
        self.content.content = pages[self.selected_index]()
        self.page.update()
