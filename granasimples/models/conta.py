from dataclasses import dataclass


@dataclass
class Conta:
    nome: str
    tipo: str
    saldo_atual: float = 0
    ativo: bool = True
    id: int | None = None
