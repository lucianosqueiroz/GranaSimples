from dataclasses import dataclass


@dataclass
class Categoria:
    nome: str
    tipo: str
    ativo: bool = True
    id: int | None = None
