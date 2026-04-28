from dataclasses import dataclass


@dataclass
class Pessoa:
    nome: str
    tipo: str
    ativo: bool = True
    id: int | None = None
