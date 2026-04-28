from granasimples.core.database import db_connection
from granasimples.services.base_service import parse_int


DEFAULT_DIAS_FECHAMENTO_CARTAO = 9
DEFAULT_PERCENTUAL_ALERTA_ORCAMENTO = 80


class ConfiguracaoService:
    def get_dias_fechamento_cartao(self) -> int:
        return self._get_int("dias_fechamento_cartao", DEFAULT_DIAS_FECHAMENTO_CARTAO)

    def get_percentual_alerta_orcamento(self) -> int:
        return self._get_int("percentual_alerta_orcamento", DEFAULT_PERCENTUAL_ALERTA_ORCAMENTO)

    def save(self, dias_fechamento_cartao: str | int, percentual_alerta_orcamento: str | int) -> None:
        dias = parse_int(dias_fechamento_cartao, "Dias de fechamento")
        alerta = parse_int(percentual_alerta_orcamento, "Percentual de alerta")
        if not 1 <= dias <= 30:
            raise ValueError("Dias de fechamento deve estar entre 1 e 30.")
        if not 1 <= alerta <= 100:
            raise ValueError("Percentual de alerta deve estar entre 1 e 100.")
        self._set("dias_fechamento_cartao", str(dias))
        self._set("percentual_alerta_orcamento", str(alerta))

    def _get_int(self, chave: str, default: int) -> int:
        with db_connection() as conn:
            row = conn.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,)).fetchone()
        return int(row["valor"]) if row else default

    def _set(self, chave: str, valor: str) -> None:
        with db_connection() as conn:
            conn.execute(
                """
                INSERT INTO configuracoes (chave, valor, atualizado_em)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chave) DO UPDATE SET
                    valor = excluded.valor,
                    atualizado_em = CURRENT_TIMESTAMP
                """,
                (chave, valor),
            )
