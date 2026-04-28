from typing import Any

from granasimples.core.database import db_connection


class BaseRepository:
    table_name: str

    def _fetch_all(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with db_connection() as conn:
            return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def _fetch_one(self, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        with db_connection() as conn:
            row = conn.execute(sql, params).fetchone()
            return dict(row) if row else None

    def _execute(self, sql: str, params: tuple[Any, ...] = ()) -> int:
        with db_connection() as conn:
            cursor = conn.execute(sql, params)
            return int(cursor.lastrowid or 0)

    def list_all(self, only_active: bool = True) -> list[dict[str, Any]]:
        where = "WHERE ativo = 1" if only_active else ""
        return self._fetch_all(f"SELECT * FROM {self.table_name} {where} ORDER BY nome")

    def get_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self._fetch_one(f"SELECT * FROM {self.table_name} WHERE id = ?", (item_id,))

    def inactivate(self, item_id: int) -> None:
        print(f"[GranaSimples][Repository] Inativando {self.table_name} id={item_id}")
        self._execute(
            f"UPDATE {self.table_name} SET ativo = 0, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?",
            (item_id,),
        )

    def activate(self, item_id: int) -> None:
        print(f"[GranaSimples][Repository] Reativando {self.table_name} id={item_id}")
        self._execute(
            f"UPDATE {self.table_name} SET ativo = 1, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?",
            (item_id,),
        )

    def delete(self, item_id: int) -> None:
        print(f"[GranaSimples][Repository] Excluindo {self.table_name} id={item_id}")
        self._execute(f"DELETE FROM {self.table_name} WHERE id = ?", (item_id,))
