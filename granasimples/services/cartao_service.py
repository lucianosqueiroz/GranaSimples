from granasimples.models import Cartao
from granasimples.repositories.cartao_repository import CartaoRepository
from granasimples.services.base_service import BaseCrudService, parse_int, parse_positive_float, require_text
from granasimples.services.configuracao_service import ConfiguracaoService


class CartaoService(BaseCrudService):
    def __init__(self) -> None:
        self.repository = CartaoRepository()
        self.configuracoes = ConfiguracaoService()

    def save(
        self,
        nome: str,
        ultimos_digitos: str,
        dia_vencimento: str | int,
        dia_fechamento: str | int,
        limite_total: str | float,
        item_id: int | None = None,
    ) -> int | None:
        digitos = require_text(ultimos_digitos, "Últimos dígitos")
        if len(digitos) != 4 or not digitos.isdigit():
            raise ValueError("Informe exatamente os 4 últimos dígitos.")
        vencimento = parse_int(dia_vencimento, "Dia de vencimento")
        fechamento = self.calcular_fechamento(vencimento)
        if not 1 <= vencimento <= 31 or not 1 <= fechamento <= 31:
            raise ValueError("Dias devem estar entre 1 e 31.")
        cartao = Cartao(
            nome=require_text(nome, "Nome"),
            ultimos_digitos=digitos,
            dia_vencimento=vencimento,
            dia_fechamento=fechamento,
            limite_total=parse_positive_float(limite_total, "Limite total"),
        )
        if item_id:
            self.repository.update(item_id, cartao)
            return None
        return self.repository.create(cartao)

    def calcular_fechamento(self, dia_vencimento: str | int) -> int:
        vencimento = parse_int(dia_vencimento, "Dia de vencimento")
        dias = self.configuracoes.get_dias_fechamento_cartao()
        fechamento = vencimento - dias
        if fechamento < 1:
            fechamento += 30
        return fechamento

    def limite_usado(self, cartao_id: int) -> float:
        return self.repository.limite_usado(cartao_id)

    def list_with_limite_usado(self, only_active: bool = True) -> list[dict]:
        cartoes = self.repository.list_all(only_active)
        for cartao in cartoes:
            cartao["limite_usado"] = self.limite_usado(cartao["id"])
        return cartoes
