from dataclasses import dataclass


@dataclass
class Cartao:
    nome: str
    ultimos_digitos: str
    dia_vencimento: int
    dia_fechamento: int
    limite_total: float
    ativo: bool = True
    id: int | None = None
