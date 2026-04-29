from datetime import date

import flet as ft

from granasimples.core.constants import MEIO_CARTAO, MEIO_CONTA, TIPO_DESPESA, TIPO_RECEITA
from granasimples.services.cartao_service import CartaoService
from granasimples.services.categoria_service import CategoriaService
from granasimples.services.conta_service import ContaService
from granasimples.services.lancamento_service import LancamentoService
from granasimples.services.pessoa_service import PessoaService
from granasimples.services.subcategoria_service import SubcategoriaService
from granasimples.ui.controls import dropdown_options, ellipsis_text, filter_rows, header_cell, is_active_value, section_title, show_message, status_label, table_header, toggle_active_button
from granasimples.ui.theme import BORDER, SUCCESS_COLOR, SUBTEXTO, TEXTO, VERMELHO, card, field_width, form_width, is_mobile, money, primary_button, responsive_form_list_layout, secondary_button, style_form_controls


def data_br(value: str | None = None) -> str:
    if not value:
        hoje = date.today()
        return f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year:04d}"
    ano, mes, dia = value.split("-")
    return f"{dia}/{mes}/{ano}"


def format_money_input(value: str | None) -> str:
    raw = (value or "").replace("R$", "").replace(" ", "")
    if not raw:
        return ""
    try:
        if "," in raw:
            number = float(raw.replace(".", "").replace(",", "."))
        else:
            number = float(raw)
    except ValueError:
        return value or ""
    return money(number)


class LancamentosPage:
    def __init__(self, page: ft.Page, refresh_app) -> None:
        self.page = page
        self.refresh_app = refresh_app
        self.service = LancamentoService()
        self.categorias = CategoriaService()
        self.subcategorias = SubcategoriaService()
        self.contas = ContaService()
        self.cartoes = CartaoService()
        self.pessoas = PessoaService()
        self.list_container = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO)
        self._render_list = lambda: None

    def _on_filter_change(self, e):
        self._render_list()

    def build(self) -> ft.Control:
        tipo = ft.Dropdown(
            label="Tipo",
            value=TIPO_DESPESA,
            options=[
                ft.dropdown.Option(TIPO_DESPESA, "Despesa"),
                ft.dropdown.Option(TIPO_RECEITA, "Receita"),
            ],
        )
        meio = ft.Dropdown(
            label="Meio financeiro",
            value=MEIO_CONTA,
            options=[
                ft.dropdown.Option(MEIO_CONTA, "Conta"),
                ft.dropdown.Option(MEIO_CARTAO, "Cartão"),
            ],
        )
        data_lancamento = ft.TextField(label="Data", value=data_br(), hint_text="DD/MM/AAAA")
        valor = ft.TextField(label="Valor", hint_text="R$ 0,00", keyboard_type=ft.KeyboardType.NUMBER)
        descricao = ft.TextField(label="Descrição", hint_text="Opcional")
        categoria = ft.Dropdown(label="Categoria")
        subcategoria = ft.Dropdown(label="Subcategoria")
        pessoa = ft.Dropdown(label="Pessoa/Centro", hint_text="Opcional")
        conta = ft.Dropdown(label="Conta")
        cartao = ft.Dropdown(label="Cartão")
        observacoes = ft.TextField(label="Observações", multiline=True, min_lines=2, max_lines=3)
        filtro_texto = ft.TextField(label="Filtrar", hint_text="Categoria, meio ou descrição", width=260)
        filtro_tipo = ft.Dropdown(
            label="Tipo",
            value="",
            options=[
                ft.dropdown.Option("", "Todos"),
                ft.dropdown.Option(TIPO_RECEITA, "Receitas"),
                ft.dropdown.Option(TIPO_DESPESA, "Despesas"),
            ],
            width=140,
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

        fields = [
            tipo,
            meio,
            data_lancamento,
            valor,
            categoria,
            subcategoria,
            pessoa,
            conta,
            cartao,
            descricao,
            observacoes,
        ]
        for field in fields:
            field.width = field_width(self.page)
        style_form_controls(fields + [filtro_texto, filtro_tipo, filtro_status])
        observacoes.height = 96

        def update_dynamic_fields(update_page: bool = True) -> None:
            if tipo.value == TIPO_RECEITA:
                meio.value = MEIO_CONTA
                meio.disabled = True
            else:
                meio.disabled = False

            categoria.options = dropdown_options(self.categorias.list_by_tipo(tipo.value))
            if categoria.value and not any(option.key == categoria.value for option in categoria.options):
                categoria.value = None

            subcategoria.visible = bool(categoria.value)
            subcategoria.options = [ft.dropdown.Option("", "Sem subcategoria")]
            if categoria.value:
                subcategoria.options += dropdown_options(self.subcategorias.list_by_categoria(categoria.value))
            if subcategoria.value and not any(option.key == subcategoria.value for option in subcategoria.options):
                subcategoria.value = ""

            pessoa.options = [ft.dropdown.Option("", "Sem pessoa/centro")] + dropdown_options(self.pessoas.list_all())
            conta.options = dropdown_options(self.contas.list_all())
            cartao.options = dropdown_options(self.cartoes.list_all())
            conta.visible = meio.value == MEIO_CONTA
            cartao.visible = meio.value == MEIO_CARTAO

            if update_page:
                self.page.update()

        def reset_form(update_page: bool = False) -> None:
            tipo.value = TIPO_DESPESA
            meio.value = MEIO_CONTA
            data_lancamento.value = data_br()
            valor.value = ""
            descricao.value = ""
            categoria.value = None
            subcategoria.value = ""
            pessoa.value = ""
            conta.value = None
            cartao.value = None
            observacoes.value = ""
            update_dynamic_fields(update_page=False)
            if update_page:
                self.page.update()

        def refresh_list(update_page: bool = True) -> None:
            rows = [
                table_header(
                    [
                        header_cell("Data", width=92),
                        header_cell("Tipo", width=82),
                        header_cell("Categoria", width=130),
                        header_cell("Subcategoria", width=120),
                        header_cell("Meio financeiro", expand=True),
                        header_cell("Valor", width=118),
                        header_cell("Status", width=88),
                        header_cell("Ações", width=76),
                    ]
                )
            ]
            items = filter_rows(self.service.list_all(False), filtro_texto.value, filtro_tipo.value, filtro_status.value)
            for item in items:
                sinal = "+" if item["tipo"] == TIPO_RECEITA else "-"
                color = SUCCESS_COLOR if item["tipo"] == TIPO_RECEITA else VERMELHO
                bg_color = "#12251A" if item["tipo"] == TIPO_RECEITA else "#2A1215"
                destino = item["conta_nome"] if item["meio_financeiro"] == MEIO_CONTA else item["cartao_nome"]

                def alternar(item=item):
                    try:
                        active = is_active_value(item["ativo"])
                        self.service.set_active(item["id"], not active)
                        show_message(self.page, "Lançamento reativado." if not active else "Lançamento inativado.")
                        refresh_list()
                        self.refresh_app()
                    except Exception as exc:
                        show_message(self.page, str(exc), True)

                rows.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ellipsis_text(data_br(item["data"]), width=92, color=SUBTEXTO),
                                ft.Container(
                                    ft.Text(item["tipo"], color=color, size=12, weight=ft.FontWeight.BOLD),
                                    bgcolor=bg_color,
                                    border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    width=82,
                                ),
                                ellipsis_text(item["categoria_nome"], width=130, weight=ft.FontWeight.W_500),
                                ellipsis_text(item["subcategoria_nome"] or "-", width=120, color=SUBTEXTO),
                                ellipsis_text(destino or item["meio_financeiro"], expand=True, color=TEXTO),
                                ellipsis_text(f"{sinal} {money(item['valor'])}", width=118, color=color, weight=ft.FontWeight.BOLD),
                                ft.Container(status_label(item["ativo"]), width=88),
                                toggle_active_button(item["ativo"], lambda _, alternar=alternar: alternar()),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
                    )
                )
            if len(rows) == 1:
                rows.append(ft.Text("Nenhum lançamento cadastrado."))
            self.list_container.controls = rows
            if update_page:
                self.page.update()

        def on_tipo_change(_):
            categoria.value = None
            subcategoria.value = ""
            update_dynamic_fields()

        def on_categoria_change(_):
            subcategoria.value = ""
            update_dynamic_fields()

        def on_meio_change(_):
            update_dynamic_fields()

        def on_valor_blur(_):
            valor.value = format_money_input(valor.value)
            self.page.update()

        def salvar(_):
            try:
                self.service.save(
                    tipo=tipo.value,
                    meio_financeiro=meio.value,
                    data_lancamento=data_lancamento.value,
                    valor=valor.value,
                    categoria_id=categoria.value,
                    descricao=descricao.value,
                    subcategoria_id=subcategoria.value,
                    pessoa_id=pessoa.value,
                    conta_id=conta.value,
                    cartao_id=cartao.value,
                    observacoes=observacoes.value,
                )
                reset_form()
                refresh_list()
                show_message(self.page, "Lançamento salvo.")
                self.refresh_app()
            except Exception as exc:
                show_message(self.page, str(exc), True)

        def novo_lancamento(_):
            reset_form(update_page=True)

        tipo.on_change = on_tipo_change
        meio.on_change = on_meio_change
        categoria.on_change = on_categoria_change
        valor.on_blur = on_valor_blur
        self._render_list = refresh_list
        filtro_texto.on_change = self._on_filter_change
        filtro_tipo.on_change = self._on_filter_change
        filtro_tipo.on_select = self._on_filter_change
        filtro_status.on_change = self._on_filter_change
        filtro_status.on_select = self._on_filter_change

        update_dynamic_fields(update_page=False)
        refresh_list(update_page=False)

        form = card(
            ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                tipo,
                                meio,
                                data_lancamento,
                                valor,
                                categoria,
                                subcategoria,
                                pessoa,
                                conta,
                                cartao,
                                descricao,
                                observacoes,
                            ],
                            spacing=12,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        height=360 if is_mobile(self.page) else 450,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=16, color=SUBTEXTO),
                            ft.Text("Role para ver mais campos", size=11, color=SUBTEXTO),
                        ],
                        spacing=4,
                    ),
                    ft.Row(
                        [
                            primary_button("Salvar lançamento", salvar),
                            secondary_button("Novo lançamento", novo_lancamento, icon=ft.Icons.ADD),
                        ],
                        spacing=10,
                        wrap=True,
                    ),
                ],
                spacing=14,
            )
        )
        form.width = form_width(self.page, 368)
        list_card = card(
            ft.Column(
                [
                    ft.Text("Últimos lançamentos", weight=ft.FontWeight.BOLD, size=16, color=TEXTO),
                    ft.Row([filtro_texto, filtro_tipo, filtro_status], wrap=True, spacing=10),
                    self.list_container,
                ],
                spacing=12,
            ),
            expand=True,
        )

        return ft.Column(
            [
                section_title("Lançamentos"),
                responsive_form_list_layout(self.page, form, list_card),
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
