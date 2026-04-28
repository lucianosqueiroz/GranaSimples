from granasimples.models import Subcategoria
from granasimples.repositories.categoria_repository import CategoriaRepository
from granasimples.repositories.subcategoria_repository import SubcategoriaRepository
from granasimples.services.base_service import BaseCrudService, parse_int, require_text


class SubcategoriaService(BaseCrudService):
    def __init__(self) -> None:
        self.repository = SubcategoriaRepository()
        self.categoria_repository = CategoriaRepository()

    def save(self, categoria_id: int | str, nome: str, item_id: int | None = None) -> int | None:
        categoria_id = parse_int(categoria_id, "Categoria")
        if not self.categoria_repository.get_by_id(categoria_id):
            raise ValueError("Categoria não encontrada.")
        subcategoria = Subcategoria(categoria_id=categoria_id, nome=require_text(nome, "Nome"))
        if item_id:
            self.repository.update(item_id, subcategoria)
            return None
        return self.repository.create(subcategoria)

    def list_by_categoria(self, categoria_id: int | str | None) -> list[dict]:
        if not categoria_id:
            return []
        return self.repository.list_by_categoria(parse_int(categoria_id, "Categoria"))

    def list_with_categoria(self, only_active: bool = True) -> list[dict]:
        return self.repository.list_with_categoria(only_active)
