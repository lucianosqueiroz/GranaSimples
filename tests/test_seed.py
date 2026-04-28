import importlib


def setup_seed(tmp_path, monkeypatch):
    monkeypatch.setenv("GRANASIMPLES_DB_PATH", str(tmp_path / "seed.db"))
    import granasimples.core.config as config
    import granasimples.core.database as database
    import granasimples.core.seed as seed

    importlib.reload(config)
    importlib.reload(database)
    importlib.reload(seed)
    database.init_db()
    return database, seed


def count_rows(database, table: str) -> int:
    with database.db_connection() as conn:
        return conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()["total"]


def test_seed_prod_nao_insere_dados(tmp_path, monkeypatch):
    database, seed = setup_seed(tmp_path, monkeypatch)

    inserted = seed.seed_database("prod")

    assert inserted is False
    assert count_rows(database, "pessoas") == 0
    assert count_rows(database, "lancamentos") == 0


def test_seed_dev_insere_dados(tmp_path, monkeypatch):
    database, seed = setup_seed(tmp_path, monkeypatch)

    inserted = seed.seed_database("dev")

    assert inserted is True
    assert count_rows(database, "pessoas") == 3
    assert count_rows(database, "contas") == 2
    assert count_rows(database, "cartoes") == 1
    assert count_rows(database, "categorias") == 4
    assert count_rows(database, "subcategorias") == 4
    assert count_rows(database, "lancamentos") == 3


def test_seed_demo_insere_dados(tmp_path, monkeypatch):
    database, seed = setup_seed(tmp_path, monkeypatch)

    inserted = seed.seed_database("demo")

    assert inserted is True
    assert count_rows(database, "pessoas") == 5
    assert count_rows(database, "contas") == 3
    assert count_rows(database, "cartoes") == 2
    assert count_rows(database, "categorias") == 10
    assert count_rows(database, "subcategorias") == 14
    assert count_rows(database, "lancamentos") == 10
    assert count_rows(database, "orcamentos") == 7


def test_seed_nao_duplica_dados(tmp_path, monkeypatch):
    database, seed = setup_seed(tmp_path, monkeypatch)

    first = seed.seed_database("demo")
    second = seed.seed_database("demo")

    assert first is True
    assert second is False
    assert count_rows(database, "lancamentos") == 10
    assert count_rows(database, "orcamentos") == 7
