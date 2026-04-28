from typing import Any

from granasimples.models import Subcategoria
from granasimples.repositories.base_repository import BaseRepository


class SubcategoriaRepository(BaseRepository):
    table_name = "subcategorias"

    def create(self, subcategoria: Subcategoria) -> int:
        return self._execute(
            "INSERT INTO subcategorias (categoria_id, nome, ativo) VALUES (?, ?, ?)",
            (subcategoria.categoria_id, subcategoria.nome, int(subcategoria.ativo)),
        )

    def update(self, item_id: int, subcategoria: Subcategoria) -> None:
        self._execute(
            """
            UPDATE subcategorias
            SET categoria_id = ?, nome = ?, ativo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (subcategoria.categoria_id, subcategoria.nome, int(subcategoria.ativo), item_id),
        )

    def has_links(self, item_id: int) -> bool:
        row = self._fetch_one(
            "SELECT COUNT(*) AS total FROM lancamentos WHERE subcategoria_id = ?",
            (item_id,),
        )
        return bool(row and row["total"])

    def list_by_categoria(self, categoria_id: int) -> list[dict[str, Any]]:
        return self._fetch_all(
            "SELECT * FROM subcategorias WHERE categoria_id = ? AND ativo = 1 ORDER BY nome",
            (categoria_id,),
        )

    def list_with_categoria(self, only_active: bool = True) -> list[dict[str, Any]]:
        where = "WHERE s.ativo = 1" if only_active else ""
        return self._fetch_all(
            f"""
            SELECT s.*, c.nome AS categoria_nome, c.tipo AS categoria_tipo
            FROM subcategorias s
            JOIN categorias c ON c.id = s.categoria_id
            {where}
            ORDER BY c.nome, s.nome
            """
        )
