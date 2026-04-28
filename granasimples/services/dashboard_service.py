from datetime import date

from granasimples.repositories.lancamento_repository import LancamentoRepository


class DashboardService:
    def __init__(self) -> None:
        self.lancamentos = LancamentoRepository()

    def resumo_mes_atual(self) -> dict[str, float]:
        hoje = date.today()
        resumo = self.lancamentos.totais_mes(hoje.year, hoje.month)
        resumo["cartoes"] = self.lancamentos.total_cartao_mes(hoje.year, hoje.month)
        return resumo

    def top_categorias_despesa(self) -> list[dict]:
        hoje = date.today()
        return self.lancamentos.top_categorias_despesa_mes(hoje.year, hoje.month)

    def ultimos_lancamentos(self, limit: int = 5) -> list[dict]:
        return self.lancamentos.list_all(True)[:limit]
