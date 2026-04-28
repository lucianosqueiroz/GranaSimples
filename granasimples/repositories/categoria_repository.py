from typing import Any

from granasimples.models import Categoria
from granasimples.repositories.base_repository import BaseRepository


class CategoriaRepository(BaseRepository):
    table_name = "categorias"

    def create(self, categoria: Categoria) -> int:
        return self._execute(
            "INSERT INTO categorias (nome, tipo, ativo) VALUES (?, ?, ?)",
            (categoria.nome, categoria.tipo, int(categoria.ativo)),
        )

    def update(self, item_id: int, categoria: Categoria) -> None:
        self._execute(
            """
            UPDATE categorias
            SET nome = ?, tipo = ?, ativo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (categoria.nome, categoria.tipo, int(categoria.ativo), item_id),
        )

    def has_links(self, item_id: int) -> bool:
        row = self._fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM subcategorias WHERE categoria_id = ?) +
                (SELECT COUNT(*) FROM lancamentos WHERE categoria_id = ?) +
                (SELECT COUNT(*) FROM orcamentos WHERE categoria_id = ?) AS total
            """,
            (item_id, item_id, item_id),
        )
        return bool(row and row["total"])

    def list_by_tipo(self, tipo: str) -> list[dict[str, Any]]:
        return self._fetch_all(
            "SELECT * FROM categorias WHERE tipo = ? AND ativo = 1 ORDER BY nome",
            (tipo,),
        )
