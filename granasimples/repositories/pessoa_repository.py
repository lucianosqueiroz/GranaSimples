from granasimples.models import Pessoa
from granasimples.repositories.base_repository import BaseRepository


class PessoaRepository(BaseRepository):
    table_name = "pessoas"

    def create(self, pessoa: Pessoa) -> int:
        return self._execute(
            "INSERT INTO pessoas (nome, tipo, ativo) VALUES (?, ?, ?)",
            (pessoa.nome, pessoa.tipo, int(pessoa.ativo)),
        )

    def update(self, item_id: int, pessoa: Pessoa) -> None:
        self._execute(
            """
            UPDATE pessoas
            SET nome = ?, tipo = ?, ativo = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (pessoa.nome, pessoa.tipo, int(pessoa.ativo), item_id),
        )

    def has_links(self, item_id: int) -> bool:
        row = self._fetch_one(
            "SELECT COUNT(*) AS total FROM lancamentos WHERE pessoa_id = ?",
            (item_id,),
        )
        return bool(row and row["total"])
