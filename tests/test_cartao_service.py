import importlib


def setup_cartao(tmp_path, monkeypatch):
    monkeypatch.setenv("GRANASIMPLES_DB_PATH", str(tmp_path / "cartao.db"))
    import granasimples.core.config as config
    import granasimples.core.database as database

    importlib.reload(config)
    importlib.reload(database)
    database.init_db()

    from granasimples.services.cartao_service import CartaoService
    from granasimples.services.configuracao_service import ConfiguracaoService

    return CartaoService(), ConfiguracaoService()


def test_fechamento_do_cartao_usa_dias_configurados(tmp_path, monkeypatch):
    cartoes, configuracoes = setup_cartao(tmp_path, monkeypatch)
    configuracoes.save(9, 80)

    cartao_id = cartoes.save("Cartão Teste", "1234", 20, "", 1000)
    cartao = cartoes.get_by_id(cartao_id)

    assert cartao["dia_fechamento"] == 11


def test_fechamento_do_cartao_recalcula_ao_alterar_configuracao(tmp_path, monkeypatch):
    cartoes, configuracoes = setup_cartao(tmp_path, monkeypatch)
    configuracoes.save(5, 80)

    assert cartoes.calcular_fechamento(20) == 15
