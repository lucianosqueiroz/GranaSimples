import flet as ft

from granasimples.ui.pages.cartoes_page import CartoesPage
from granasimples.ui.pages.categorias_page import CategoriasPage
from granasimples.ui.pages.configuracoes_page import ConfiguracoesPage
from granasimples.ui.pages.contas_page import ContasPage
from granasimples.ui.pages.dashboard_page import DashboardPage
from granasimples.ui.pages.lancamentos_page import LancamentosPage
from granasimples.ui.pages.pessoas_page import PessoasPage
from granasimples.ui.pages.subcategorias_page import SubcategoriasPage
from granasimples.ui.theme import BORDER, CARD, FUNDO, ROXO, SUBTEXTO, TEXTO, apply_theme, content_padding, is_mobile


class GranaSimplesApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.content = ft.Container(expand=True, bgcolor=FUNDO)
        self.selected_index = 0
        self.rail: ft.NavigationRail | None = None
        self.destinations = [
            (ft.Icons.DASHBOARD_OUTLINED, ft.Icons.DASHBOARD, "Dashboard"),
            (ft.Icons.GROUP_OUTLINED, ft.Icons.GROUP_OUTLINED, "Pessoas"),
            (ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "Contas"),
            (ft.Icons.CATEGORY_OUTLINED, ft.Icons.CATEGORY_OUTLINED, "Categorias"),
            (ft.Icons.ACCOUNT_TREE_OUTLINED, ft.Icons.ACCOUNT_TREE_OUTLINED, "Subcategorias"),
            (ft.Icons.CREDIT_CARD, ft.Icons.CREDIT_CARD, "Cartões"),
            (ft.Icons.SWAP_VERT, ft.Icons.SWAP_VERT, "Lançamentos"),
            (ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS_OUTLINED, "Configurações"),
        ]

    def build(self) -> None:
        apply_theme(self.page)
        self.page.on_resize = self._resize
        self._mount_shell()
        self._render()

    def _mount_shell(self) -> None:
        self.page.controls.clear()
        if is_mobile(self.page):
            self.rail = None
            self.page.add(
                ft.Column(
                    [
                        self.content,
                        self._mobile_nav(),
                    ],
                    expand=True,
                    spacing=0,
                )
            )
            return

        self.rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=124,
            min_extended_width=220,
            bgcolor=CARD,
            indicator_color=ROXO,
            selected_label_text_style=ft.TextStyle(color=TEXTO, size=11, weight=ft.FontWeight.BOLD),
            unselected_label_text_style=ft.TextStyle(color=SUBTEXTO, size=11),
            destinations=[
                ft.NavigationRailDestination(icon=icon, selected_icon=selected_icon, label=label)
                for icon, selected_icon, label in self.destinations
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

    def _mobile_nav(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        selected_icon if index == self.selected_index else icon,
                        tooltip=label,
                        icon_color=ROXO if index == self.selected_index else SUBTEXTO,
                        bgcolor="#22112C" if index == self.selected_index else None,
                        on_click=lambda _, selected=index: self._navigate_to(selected),
                    )
                    for index, (icon, selected_icon, label) in enumerate(self.destinations)
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=4,
                alignment=ft.MainAxisAlignment.START,
            ),
            height=58,
            bgcolor=CARD,
            border=ft.border.only(top=ft.BorderSide(1, BORDER)),
            padding=ft.padding.symmetric(horizontal=8, vertical=6),
        )

    def _resize(self, event: ft.ControlEvent) -> None:
        self._mount_shell()
        self._render()

    def _navigate(self, event: ft.ControlEvent) -> None:
        self.selected_index = event.control.selected_index
        self._render()

    def _navigate_to(self, index: int) -> None:
        self.selected_index = index
        self._mount_shell()
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
        if self.rail:
            self.rail.selected_index = self.selected_index
        padding = content_padding(self.page)
        self.content.padding = ft.padding.symmetric(horizontal=padding, vertical=padding)
        self.content.content = pages[self.selected_index]()
        self.page.update()
