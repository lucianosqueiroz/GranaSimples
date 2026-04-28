from datetime import date
from typing import Any

from granasimples.core.database import db_connection
from granasimples.services.cartao_service import CartaoService
from granasimples.services.categoria_service import CategoriaService
from granasimples.services.conta_service import ContaService
from granasimples.services.lancamento_service import LancamentoService
from granasimples.services.pessoa_service import PessoaService
from granasimples.services.subcategoria_service import SubcategoriaService


VALID_SEED_MODES = {"prod", "dev", "demo"}


def seed_database(mode: str) -> bool:
    mode = (mode or "prod").strip().lower()
    if mode not in VALID_SEED_MODES:
        raise ValueError("Modo de seed inválido. Use prod, dev ou demo.")
    if mode == "prod" or not _database_is_empty():
        return False
    if mode == "dev":
        _seed_dev()
        return True
    _seed_demo()
    return True


def _database_is_empty() -> bool:
    tables = ["pessoas", "contas", "cartoes", "categorias", "subcategorias", "lancamentos", "orcamentos"]
    with db_connection() as conn:
        for table in tables:
            total = conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()["total"]
            if total:
                return False
    return True


def _seed_dev() -> None:
    pessoas = _seed_pessoas(
        [
            ("Luciano", "Pessoa"),
            ("Valentina", "Pessoa"),
            ("Família", "Centro de Custo"),
        ]
    )
    contas = _seed_contas(
        [
            ("Banco Itaú", "Conta Digital", 1250.50),
            ("Carteira", "Dinheiro", 80.00),
        ]
    )
    cartoes = _seed_cartoes(
        [
            ("Black Itaú", "9641", 20, 10, 5000.00),
        ]
    )
    categorias = _seed_categorias(
        [
            ("Salário", "receita"),
            ("Alimentação", "despesa"),
            ("Saúde", "despesa"),
            ("Lazer", "despesa"),
        ]
    )
    subcategorias = _seed_subcategorias(
        categorias,
        [
            ("Prefeitura", "Salário"),
            ("Supermercado", "Alimentação"),
            ("Restaurante", "Alimentação"),
            ("Farmácia", "Saúde"),
        ],
    )
    _seed_lancamentos(
        pessoas,
        contas,
        cartoes,
        categorias,
        subcategorias,
        [
            {
                "tipo": "receita",
                "meio": "conta",
                "data": date.today().isoformat(),
                "valor": 4955.00,
                "descricao": "Salário Prefeitura",
                "categoria": "Salário",
                "subcategoria": "Prefeitura",
                "pessoa": "Luciano",
                "conta": "Banco Itaú",
            },
            {
                "tipo": "despesa",
                "meio": "conta",
                "data": date.today().isoformat(),
                "valor": 183.00,
                "descricao": "Compra de supermercado",
                "categoria": "Alimentação",
                "subcategoria": "Supermercado",
                "pessoa": "Família",
                "conta": "Banco Itaú",
            },
            {
                "tipo": "despesa",
                "meio": "conta",
                "data": date.today().isoformat(),
                "valor": 22.50,
                "descricao": "Colírio",
                "categoria": "Saúde",
                "subcategoria": "Farmácia",
                "pessoa": "Valentina",
                "conta": "Banco Itaú",
            },
        ],
    )


def _seed_demo() -> None:
    hoje = date.today()
    pessoas = _seed_pessoas(
        [
            ("Luciano", "Pessoa"),
            ("Valentina", "Pessoa"),
            ("Casa", "Centro de Custo"),
            ("Família", "Centro de Custo"),
            ("Veículo", "Centro de Custo"),
        ]
    )
    contas = _seed_contas(
        [
            ("Banco Principal", "Conta Corrente", 2450.75),
            ("Carteira", "Dinheiro", 120.00),
            ("Reserva de Emergência", "Poupança", 3500.00),
        ]
    )
    cartoes = _seed_cartoes(
        [
            ("Cartão Azul", "1234", 15, 5, 4000.00),
            ("Cartão Black", "9641", 20, 10, 8000.00),
        ]
    )
    categorias = _seed_categorias(
        [
            ("Salário", "receita"),
            ("Renda Extra", "receita"),
            ("Alimentação", "despesa"),
            ("Moradia", "despesa"),
            ("Saúde", "despesa"),
            ("Transporte", "despesa"),
            ("Lazer", "despesa"),
            ("Educação", "despesa"),
            ("Cartão de Crédito", "despesa"),
            ("Serviços Digitais", "despesa"),
        ]
    )
    subcategorias = _seed_subcategorias(
        categorias,
        [
            ("Prefeitura", "Salário"),
            ("Perícia Judicial", "Renda Extra"),
            ("Supermercado", "Alimentação"),
            ("Restaurante", "Alimentação"),
            ("Aluguel", "Moradia"),
            ("Energia", "Moradia"),
            ("Farmácia", "Saúde"),
            ("Plano de Saúde", "Saúde"),
            ("Combustível", "Transporte"),
            ("Manutenção Veículo", "Transporte"),
            ("Cinema", "Lazer"),
            ("Curso Online", "Educação"),
            ("Assinaturas", "Serviços Digitais"),
            ("Hospedagem/Sistemas", "Serviços Digitais"),
        ],
    )
    _seed_lancamentos(
        pessoas,
        contas,
        cartoes,
        categorias,
        subcategorias,
        [
            _lancamento("receita", "conta", hoje, 5, 4955.00, "Salário Prefeitura", "Salário", "Prefeitura", "Luciano", conta="Banco Principal"),
            _lancamento("receita", "conta", hoje, 12, 850.00, "Perícia judicial", "Renda Extra", "Perícia Judicial", "Luciano", conta="Banco Principal"),
            _lancamento("despesa", "conta", hoje, 8, 1200.00, "Aluguel", "Moradia", "Aluguel", "Casa", conta="Banco Principal"),
            _lancamento("despesa", "conta", hoje, 10, 185.40, "Energia elétrica", "Moradia", "Energia", "Casa", conta="Banco Principal"),
            _lancamento("despesa", "conta", hoje, 11, 236.80, "Supermercado da semana", "Alimentação", "Supermercado", "Família", conta="Banco Principal"),
            _lancamento("despesa", "conta", hoje, 13, 48.90, "Farmácia", "Saúde", "Farmácia", "Valentina", conta="Banco Principal"),
            _lancamento("despesa", "cartao", hoje, 14, 96.70, "Restaurante fim de semana", "Alimentação", "Restaurante", "Família", cartao="Cartão Azul"),
            _lancamento("despesa", "cartao", hoje, 15, 220.00, "Combustível", "Transporte", "Combustível", "Veículo", cartao="Cartão Black"),
            _lancamento("despesa", "cartao", hoje, 16, 39.90, "Assinatura de streaming", "Serviços Digitais", "Assinaturas", "Família", cartao="Cartão Azul"),
            _lancamento("despesa", "cartao", hoje, 17, 79.90, "Curso online", "Educação", "Curso Online", "Luciano", cartao="Cartão Black"),
        ],
    )
    _seed_orcamentos(
        categorias,
        hoje.month,
        hoje.year,
        [
            ("Alimentação", 900.00, 80),
            ("Moradia", 1600.00, 80),
            ("Saúde", 400.00, 80),
            ("Transporte", 600.00, 80),
            ("Lazer", 300.00, 80),
            ("Educação", 250.00, 80),
            ("Serviços Digitais", 200.00, 80),
        ],
    )


def _seed_pessoas(items: list[tuple[str, str]]) -> dict[str, int]:
    service = PessoaService()
    return {nome: service.save(nome, tipo) for nome, tipo in items}


def _seed_contas(items: list[tuple[str, str, float]]) -> dict[str, int]:
    service = ContaService()
    return {nome: service.save(nome, tipo, saldo) for nome, tipo, saldo in items}


def _seed_cartoes(items: list[tuple[str, str, int, int, float]]) -> dict[str, int]:
    service = CartaoService()
    return {
        nome: service.save(nome, digitos, vencimento, fechamento, limite)
        for nome, digitos, vencimento, fechamento, limite in items
    }


def _seed_categorias(items: list[tuple[str, str]]) -> dict[str, int]:
    service = CategoriaService()
    return {nome: service.save(nome, tipo) for nome, tipo in items}


def _seed_subcategorias(categorias: dict[str, int], items: list[tuple[str, str]]) -> dict[str, int]:
    service = SubcategoriaService()
    return {nome: service.save(categorias[categoria], nome) for nome, categoria in items}


def _seed_lancamentos(
    pessoas: dict[str, int],
    contas: dict[str, int],
    cartoes: dict[str, int],
    categorias: dict[str, int],
    subcategorias: dict[str, int],
    items: list[dict[str, Any]],
) -> None:
    service = LancamentoService()
    for item in items:
        service.save(
            tipo=item["tipo"],
            meio_financeiro=item["meio"],
            data_lancamento=item["data"],
            valor=item["valor"],
            descricao=item["descricao"],
            categoria_id=categorias[item["categoria"]],
            subcategoria_id=subcategorias.get(item["subcategoria"]),
            pessoa_id=pessoas.get(item["pessoa"]),
            conta_id=contas.get(item.get("conta")),
            cartao_id=cartoes.get(item.get("cartao")),
        )


def _seed_orcamentos(categorias: dict[str, int], mes: int, ano: int, items: list[tuple[str, float, float]]) -> None:
    with db_connection() as conn:
        for categoria, valor, alerta in items:
            conn.execute(
                """
                INSERT INTO orcamentos (categoria_id, valor_previsto, percentual_alerta, mes, ano, ativo)
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (categorias[categoria], valor, alerta, mes, ano),
            )


def _lancamento(
    tipo: str,
    meio: str,
    base_date: date,
    day: int,
    valor: float,
    descricao: str,
    categoria: str,
    subcategoria: str,
    pessoa: str,
    conta: str | None = None,
    cartao: str | None = None,
) -> dict[str, Any]:
    data = date(base_date.year, base_date.month, day).isoformat()
    return {
        "tipo": tipo,
        "meio": meio,
        "data": data,
        "valor": valor,
        "descricao": descricao,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "pessoa": pessoa,
        "conta": conta,
        "cartao": cartao,
    }
