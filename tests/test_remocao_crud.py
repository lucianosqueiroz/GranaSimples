import importlib


def setup_services(tmp_path, monkeypatch):
    monkeypatch.setenv("GRANASIMPLES_DB_PATH", str(tmp_path / "remove.db"))
    import granasimples.core.config as config
    import granasimples.core.database as database

    importlib.reload(config)
    importlib.reload(database)
    database.init_db()

    from granasimples.services.cartao_service import CartaoService
    from granasimples.services.categoria_service import CategoriaService
    from granasimples.services.conta_service import ContaService
    from granasimples.services.lancamento_service import LancamentoService
    from granasimples.services.pessoa_service import PessoaService
    from granasimples.services.subcategoria_service import SubcategoriaService

    return {
        "cartoes": CartaoService(),
        "categorias": CategoriaService(),
        "contas": ContaService(),
        "database": database,
        "lancamentos": LancamentoService(),
        "pessoas": PessoaService(),
        "subcategorias": SubcategoriaService(),
    }


def count(database, table):
    with database.db_connection() as conn:
        return conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()["total"]


def test_remove_sem_vinculo_exclui_fisicamente(tmp_path, monkeypatch):
    s = setup_services(tmp_path, monkeypatch)
    pessoa_id = s["pessoas"].save("Teste", "Pessoa")
    conta_id = s["contas"].save("Carteira", "Dinheiro", 0)
    categoria_id = s["categorias"].save("Alimentação", "despesa")
    subcategoria_id = s["subcategorias"].save(categoria_id, "Mercado")
    cartao_id = s["cartoes"].save("Cartão", "1234", 20, "", 1000)

    assert s["pessoas"].remove(pessoa_id) == "deleted"
    assert s["contas"].remove(conta_id) == "deleted"
    assert s["subcategorias"].remove(subcategoria_id) == "deleted"
    assert s["categorias"].remove(categoria_id) == "deleted"
    assert s["cartoes"].remove(cartao_id) == "deleted"

    assert count(s["database"], "pessoas") == 0
    assert count(s["database"], "contas") == 0
    assert count(s["database"], "subcategorias") == 0
    assert count(s["database"], "categorias") == 0
    assert count(s["database"], "cartoes") == 0


def test_remove_com_vinculo_inativa(tmp_path, monkeypatch):
    s = setup_services(tmp_path, monkeypatch)
    pessoa_id = s["pessoas"].save("Família", "Centro de Custo")
    conta_id = s["contas"].save("Banco", "Conta", 500)
    categoria_id = s["categorias"].save("Mercado", "despesa")
    subcategoria_id = s["subcategorias"].save(categoria_id, "Supermercado")
    cartao_id = s["cartoes"].save("Cartão", "1234", 20, "", 1000)

    s["lancamentos"].save(
        "despesa",
        "conta",
        "2026-04-27",
        50,
        categoria_id,
        subcategoria_id=subcategoria_id,
        pessoa_id=pessoa_id,
        conta_id=conta_id,
    )
    s["lancamentos"].save(
        "despesa",
        "cartao",
        "2026-04-27",
        20,
        categoria_id,
        pessoa_id=pessoa_id,
        cartao_id=cartao_id,
    )

    assert s["pessoas"].remove(pessoa_id) == "inactivated"
    assert s["contas"].remove(conta_id) == "inactivated"
    assert s["subcategorias"].remove(subcategoria_id) == "inactivated"
    assert s["categorias"].remove(categoria_id) == "inactivated"
    assert s["cartoes"].remove(cartao_id) == "inactivated"

    assert not s["pessoas"].get_by_id(pessoa_id)["ativo"]
    assert not s["contas"].get_by_id(conta_id)["ativo"]
    assert not s["subcategorias"].get_by_id(subcategoria_id)["ativo"]
    assert not s["categorias"].get_by_id(categoria_id)["ativo"]
    assert not s["cartoes"].get_by_id(cartao_id)["ativo"]


def test_inativar_e_reativar_lancamento_reverte_e_reaplica_saldo(tmp_path, monkeypatch):
    s = setup_services(tmp_path, monkeypatch)
    conta_id = s["contas"].save("Banco", "Conta", 500)
    categoria_id = s["categorias"].save("Salario", "receita")

    lancamento_id = s["lancamentos"].save(
        "receita",
        "conta",
        "2026-04-27",
        100,
        categoria_id,
        conta_id=conta_id,
    )

    assert s["contas"].get_by_id(conta_id)["saldo_atual"] == 600

    s["lancamentos"].set_active(lancamento_id, False)
    assert not s["lancamentos"].repository.get_by_id(lancamento_id)["ativo"]
    assert s["contas"].get_by_id(conta_id)["saldo_atual"] == 500

    s["lancamentos"].set_active(lancamento_id, True)
    assert s["lancamentos"].repository.get_by_id(lancamento_id)["ativo"]
    assert s["contas"].get_by_id(conta_id)["saldo_atual"] == 600
