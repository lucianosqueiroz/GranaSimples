from granasimples.models import Cartao
from granasimples.repositories.base_repository import BaseRepository


class CartaoRepository(BaseRepository):
    table_name = "cartoes"

    def create(self, cartao: Cartao) -> int:
        return self._execute(
            """
            INSERT INTO cartoes
            (nome, ultimos_digitos, dia_vencimento, dia_fechamento, limite_total, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                cartao.nome,
                cartao.ultimos_digitos,
                cartao.dia_vencimento,
                cartao.dia_fechamento,
                cartao.limite_total,
                int(cartao.ativo),
            ),
        )

    def update(self, item_id: int, cartao: Cartao) -> None:
        self._execute(
            """
            UPDATE cartoes
            SET nome = ?, ultimos_digitos = ?, dia_vencimento = ?, dia_fechamento = ?,
                limite_total = ?, ativo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                cartao.nome,
                cartao.ultimos_digitos,
                cartao.dia_vencimento,
                cartao.dia_fechamento,
                cartao.limite_total,
                int(cartao.ativo),
                item_id,
            ),
        )

    def limite_usado(self, item_id: int) -> float:
        row = self._fetch_one(
            """
            SELECT COALESCE(SUM(valor), 0) AS total
            FROM lancamentos
            WHERE cartao_id = ? AND tipo = 'despesa' AND ativo = 1
            """,
            (item_id,),
        )
        return float(row["total"] if row else 0)

    def has_links(self, item_id: int) -> bool:
        row = self._fetch_one(
            "SELECT COUNT(*) AS total FROM lancamentos WHERE cartao_id = ?",
            (item_id,),
        )
        return bool(row and row["total"])
