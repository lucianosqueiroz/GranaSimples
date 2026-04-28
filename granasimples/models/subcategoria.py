from dataclasses import dataclass


@dataclass
class Subcategoria:
    categoria_id: int
    nome: str
    ativo: bool = True
    id: int | None = None
