from dataclasses import dataclass


@dataclass
class Lancamento:
    tipo: str
    meio_financeiro: str
    data: str
    valor: float
    categoria_id: int
    descricao: str | None = None
    subcategoria_id: int | None = None
    pessoa_id: int | None = None
    conta_id: int | None = None
    cartao_id: int | None = None
    observacoes: str | None = None
    ativo: bool = True
    id: int | None = None
