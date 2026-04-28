from granasimples.ui.controls import filter_rows


def test_filter_status_inativos_sem_texto():
    rows = [
        {"nome": "Ativo", "ativo": 1},
        {"nome": "Inativo", "ativo": 0},
    ]

    assert filter_rows(rows, status="inativos") == [{"nome": "Inativo", "ativo": 0}]


def test_filter_status_todos_sem_texto():
    rows = [
        {"nome": "Ativo", "ativo": 1},
        {"nome": "Inativo", "ativo": 0},
    ]

    assert filter_rows(rows, status="todos") == rows


def test_filter_tipo_sem_texto():
    rows = [
        {"nome": "Luciano", "tipo": "Pessoa", "ativo": 1},
        {"nome": "Casa", "tipo": "Centro de Custo", "ativo": 1},
        {"nome": "Arquivo", "tipo": "Pessoa", "ativo": 0},
    ]

    assert filter_rows(rows, tipo="Pessoa", status="ativos") == [{"nome": "Luciano", "tipo": "Pessoa", "ativo": 1}]


def test_filter_tipo_e_status_todos_sem_texto():
    rows = [
        {"nome": "Luciano", "tipo": "Pessoa", "ativo": 1},
        {"nome": "Casa", "tipo": "Centro de Custo", "ativo": 1},
        {"nome": "Arquivo", "tipo": "Pessoa", "ativo": 0},
    ]

    assert filter_rows(rows, tipo="Pessoa", status="todos") == [
        {"nome": "Luciano", "tipo": "Pessoa", "ativo": 1},
        {"nome": "Arquivo", "tipo": "Pessoa", "ativo": 0},
    ]


def test_filter_texto_combina_com_status_quando_preenchido():
    rows = [
        {"nome": "Banco", "ativo": 1},
        {"nome": "Carteira", "ativo": 0},
        {"nome": "Banco antigo", "ativo": 0},
    ]

    assert filter_rows(rows, text="banco", status="inativos") == [{"nome": "Banco antigo", "ativo": 0}]
