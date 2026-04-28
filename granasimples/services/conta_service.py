from granasimples.models import Conta
from granasimples.repositories.conta_repository import ContaRepository
from granasimples.services.base_service import BaseCrudService, parse_float, require_text


class ContaService(BaseCrudService):
    def __init__(self) -> None:
        self.repository = ContaRepository()

    def save(
        self,
        nome: str,
        tipo: str,
        saldo_atual: str | float = 0,
        item_id: int | None = None,
    ) -> int | None:
        saldo = parse_float(saldo_atual, "Saldo atual")
        conta = Conta(
            nome=require_text(nome, "Nome"),
            tipo=require_text(tipo, "Tipo"),
            saldo_atual=saldo,
        )
        if item_id:
            self.repository.update(item_id, conta)
            return None
        return self.repository.create(conta)

    def ajustar_saldo(self, conta_id: int, delta: float) -> None:
        self.repository.update_saldo(conta_id, delta)
