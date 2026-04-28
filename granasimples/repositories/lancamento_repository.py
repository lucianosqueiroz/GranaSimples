from typing import Any

from granasimples.models import Lancamento
from granasimples.repositories.base_repository import BaseRepository


class LancamentoRepository(BaseRepository):
    table_name = "lancamentos"

    def create(self, lancamento: Lancamento) -> int:
        return self._execute(
            """
            INSERT INTO lancamentos (
                tipo, meio_financeiro, data, valor, descricao, categoria_id,
                subcategoria_id, pessoa_id, conta_id, cartao_id, observacoes, ativo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lancamento.tipo,
                lancamento.meio_financeiro,
                lancamento.data,
                lancamento.valor,
                lancamento.descricao,
                lancamento.categoria_id,
                lancamento.subcategoria_id,
                lancamento.pessoa_id,
                lancamento.conta_id,
                lancamento.cartao_id,
                lancamento.observacoes,
                int(lancamento.ativo),
            ),
        )

    def list_all(self, only_active: bool = True) -> list[dict[str, Any]]:
        where = "WHERE l.ativo = 1" if only_active else ""
        return self._fetch_all(
            f"""
            SELECT
                l.*,
                c.nome AS categoria_nome,
                s.nome AS subcategoria_nome,
                p.nome AS pessoa_nome,
                co.nome AS conta_nome,
                ca.nome AS cartao_nome
            FROM lancamentos l
            JOIN categorias c ON c.id = l.categoria_id
            LEFT JOIN subcategorias s ON s.id = l.subcategoria_id
            LEFT JOIN pessoas p ON p.id = l.pessoa_id
            LEFT JOIN contas co ON co.id = l.conta_id
            LEFT JOIN cartoes ca ON ca.id = l.cartao_id
            {where}
            ORDER BY l.data DESC, l.id DESC
            """
        )

    def totais_mes(self, ano: int, mes: int) -> dict[str, float]:
        inicio = f"{ano:04d}-{mes:02d}-01"
        fim = f"{ano + 1:04d}-01-01" if mes == 12 else f"{ano:04d}-{mes + 1:02d}-01"
        row = self._fetch_one(
            """
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0) AS receitas,
                COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0) AS despesas
            FROM lancamentos
            WHERE ativo = 1 AND data >= ? AND data < ?
            """,
            (inicio, fim),
        )
        receitas = float(row["receitas"] if row else 0)
        despesas = float(row["despesas"] if row else 0)
        return {"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas}

    def total_cartao_mes(self, ano: int, mes: int) -> float:
        inicio = f"{ano:04d}-{mes:02d}-01"
        fim = f"{ano + 1:04d}-01-01" if mes == 12 else f"{ano:04d}-{mes + 1:02d}-01"
        row = self._fetch_one(
            """
            SELECT COALESCE(SUM(valor), 0) AS total
            FROM lancamentos
            WHERE ativo = 1 AND tipo = 'despesa' AND meio_financeiro = 'cartao'
              AND data >= ? AND data < ?
            """,
            (inicio, fim),
        )
        return float(row["total"] if row else 0)

    def top_categorias_despesa_mes(self, ano: int, mes: int, limit: int = 3) -> list[dict[str, Any]]:
        inicio = f"{ano:04d}-{mes:02d}-01"
        fim = f"{ano + 1:04d}-01-01" if mes == 12 else f"{ano:04d}-{mes + 1:02d}-01"
        return self._fetch_all(
            """
            SELECT c.nome, COALESCE(SUM(l.valor), 0) AS total
            FROM lancamentos l
            JOIN categorias c ON c.id = l.categoria_id
            WHERE l.ativo = 1 AND l.tipo = 'despesa' AND l.data >= ? AND l.data < ?
            GROUP BY c.id, c.nome
            ORDER BY total DESC
            LIMIT ?
            """,
            (inicio, fim, limit),
        )
