from granasimples.core.constants import TIPO_CENTRO_CUSTO, TIPO_PESSOA
from granasimples.models import Pessoa
from granasimples.repositories.pessoa_repository import PessoaRepository
from granasimples.services.base_service import BaseCrudService, require_text


class PessoaService(BaseCrudService):
    def __init__(self) -> None:
        self.repository = PessoaRepository()

    def save(self, nome: str, tipo: str, item_id: int | None = None) -> int | None:
        if tipo not in [TIPO_PESSOA, TIPO_CENTRO_CUSTO]:
            raise ValueError("Tipo inválido.")
        pessoa = Pessoa(nome=require_text(nome, "Nome"), tipo=tipo)
        if item_id:
            self.repository.update(item_id, pessoa)
            return None
        return self.repository.create(pessoa)
