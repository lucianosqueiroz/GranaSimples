from granasimples.core.constants import TIPOS_LANCAMENTO
from granasimples.models import Categoria
from granasimples.repositories.categoria_repository import CategoriaRepository
from granasimples.services.base_service import BaseCrudService, require_text


class CategoriaService(BaseCrudService):
    def __init__(self) -> None:
        self.repository = CategoriaRepository()

    def save(self, nome: str, tipo: str, item_id: int | None = None) -> int | None:
        nome = require_text(nome, "Nome")
        if tipo not in TIPOS_LANCAMENTO:
            raise ValueError("Tipo de categoria inválido.")
        categoria = Categoria(nome=nome, tipo=tipo)
        if item_id:
            self.repository.update(item_id, categoria)
            return None
        return self.repository.create(categoria)

    def list_by_tipo(self, tipo: str) -> list[dict]:
        return self.repository.list_by_tipo(tipo)
