from granasimples.models import Conta
from granasimples.repositories.base_repository import BaseRepository


class ContaRepository(BaseRepository):
    table_name = "contas"

    def create(self, conta: Conta) -> int:
        return self._execute(
            "INSERT INTO contas (nome, tipo, saldo_atual, ativo) VALUES (?, ?, ?, ?)",
            (conta.nome, conta.tipo, conta.saldo_atual, int(conta.ativo)),
        )

    def update(self, item_id: int, conta: Conta) -> None:
        self._execute(
            """
            UPDATE contas
            SET nome = ?, tipo = ?, saldo_atual = ?, ativo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (conta.nome, conta.tipo, conta.saldo_atual, int(conta.ativo), item_id),
        )

    def update_saldo(self, item_id: int, delta: float) -> None:
        self._execute(
            """
            UPDATE contas
            SET saldo_atual = saldo_atual + ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (delta, item_id),
        )

    def has_links(self, item_id: int) -> bool:
        row = self._fetch_one(
            "SELECT COUNT(*) AS total FROM lancamentos WHERE conta_id = ?",
            (item_id,),
        )
        return bool(row and row["total"])
