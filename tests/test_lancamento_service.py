import importlib


def setup_services(tmp_path, monkeypatch):
    monkeypatch.setenv("GRANASIMPLES_DB_PATH", str(tmp_path / "test.db"))
    import granasimples.core.config as config
    import granasimples.core.database as database

    importlib.reload(config)
    importlib.reload(database)
    database.init_db()

    from granasimples.services.cartao_service import CartaoService
    from granasimples.services.categoria_service import CategoriaService
    from granasimples.services.conta_service import ContaService
    from granasimples.services.lancamento_service import LancamentoService
    from granasimples.services.subcategoria_service import SubcategoriaService

    return CategoriaService(), SubcategoriaService(), ContaService(), CartaoService(), LancamentoService()


def test_receita_entra_somente_em_conta_e_atualiza_saldo(tmp_path, monkeypatch):
    categorias, _, contas, _, lancamentos = setup_services(tmp_path, monkeypatch)
    categoria_id = categorias.save("Salário", "receita")
    conta_id = contas.save("Banco", "banco", 10)

    lancamentos.save("receita", "conta", "2026-04-27", "100", categoria_id, conta_id=conta_id)

    conta = contas.get_by_id(conta_id)
    assert conta["saldo_atual"] == 110


def test_receita_nao_pode_ser_lancada_em_cartao(tmp_path, monkeypatch):
    categorias, _, _, cartoes, lancamentos = setup_services(tmp_path, monkeypatch)
    categoria_id = categorias.save("Salário", "receita")
    cartao_id = cartoes.save("Nubank", "1234", 10, 5, 1000)

    try:
        lancamentos.save("receita", "cartao", "2026-04-27", "100", categoria_id, cartao_id=cartao_id)
    except ValueError as exc:
        assert "Receita deve ser lançada somente em conta" in str(exc)
    else:
        raise AssertionError("Receita em cartão deveria falhar.")


def test_despesa_em_cartao_calcula_limite_usado_sem_conta(tmp_path, monkeypatch):
    categorias, _, _, cartoes, lancamentos = setup_services(tmp_path, monkeypatch)
    categoria_id = categorias.save("Mercado", "despesa")
    cartao_id = cartoes.save("Visa", "5678", 20, 10, 2000)

    lancamentos.save("despesa", "cartao", "2026-04-27", "250,50", categoria_id, cartao_id=cartao_id)

    assert cartoes.limite_usado(cartao_id) == 250.5


def test_subcategoria_opcional_e_categoria_compativel(tmp_path, monkeypatch):
    categorias, subcategorias, contas, _, lancamentos = setup_services(tmp_path, monkeypatch)
    categoria_despesa = categorias.save("Casa", "despesa")
    categoria_receita = categorias.save("Freela", "receita")
    subcategoria_id = subcategorias.save(categoria_despesa, "Aluguel")
    conta_id = contas.save("Carteira", "carteira", 500)

    lancamentos.save("despesa", "conta", "2026-04-27", 100, categoria_despesa, conta_id=conta_id)

    try:
        lancamentos.save(
            "despesa",
            "conta",
            "2026-04-27",
            100,
            categoria_receita,
            subcategoria_id=subcategoria_id,
            conta_id=conta_id,
        )
    except ValueError as exc:
        assert "Categoria incompatível" in str(exc)
    else:
        raise AssertionError("Categoria incompatível deveria falhar.")


def test_data_brasileira_e_valor_monetario(tmp_path, monkeypatch):
    categorias, _, contas, _, lancamentos = setup_services(tmp_path, monkeypatch)
    categoria_id = categorias.save("Mercado", "despesa")
    conta_id = contas.save("Carteira", "carteira", 1000)

    lancamento_id = lancamentos.save(
        "despesa",
        "conta",
        "27/04/2026",
        "R$ 1.234,56",
        categoria_id,
        conta_id=conta_id,
    )

    lancamento = next(item for item in lancamentos.list_all() if item["id"] == lancamento_id)
    conta = contas.get_by_id(conta_id)
    assert lancamento["data"] == "2026-04-27"
    assert lancamento["valor"] == 1234.56
    assert round(conta["saldo_atual"], 2) == -234.56
