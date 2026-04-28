from datetime import date

from granasimples.core.constants import MEIO_CARTAO, MEIO_CONTA, TIPO_DESPESA, TIPO_RECEITA
from granasimples.models import Lancamento
from granasimples.repositories.cartao_repository import CartaoRepository
from granasimples.repositories.categoria_repository import CategoriaRepository
from granasimples.repositories.conta_repository import ContaRepository
from granasimples.repositories.lancamento_repository import LancamentoRepository
from granasimples.repositories.pessoa_repository import PessoaRepository
from granasimples.repositories.subcategoria_repository import SubcategoriaRepository
from granasimples.services.base_service import parse_int, parse_positive_float


class LancamentoService:
    def __init__(self) -> None:
        self.repository = LancamentoRepository()
        self.categorias = CategoriaRepository()
        self.subcategorias = SubcategoriaRepository()
        self.contas = ContaRepository()
        self.cartoes = CartaoRepository()
        self.pessoas = PessoaRepository()

    def list_all(self, only_active: bool = True) -> list[dict]:
        return self.repository.list_all(only_active)

    def save(
        self,
        tipo: str,
        meio_financeiro: str,
        data_lancamento: str,
        valor: str | float,
        categoria_id: int | str,
        descricao: str | None = None,
        subcategoria_id: int | str | None = None,
        pessoa_id: int | str | None = None,
        conta_id: int | str | None = None,
        cartao_id: int | str | None = None,
        observacoes: str | None = None,
    ) -> int:
        lancamento = self._build_lancamento(
            tipo,
            meio_financeiro,
            data_lancamento,
            valor,
            categoria_id,
            descricao,
            subcategoria_id,
            pessoa_id,
            conta_id,
            cartao_id,
            observacoes,
        )
        item_id = self.repository.create(lancamento)
        self._aplicar_movimento(lancamento)
        return item_id

    def inactivate(self, item_id: int) -> None:
        print(f"[GranaSimples][Service] Inativando lançamento id={item_id}")
        lancamento = self.repository.get_by_id(item_id)
        if not lancamento or not lancamento["ativo"]:
            return
        self._reverter_movimento(lancamento)
        self.repository.inactivate(item_id)

    def remove(self, item_id: int) -> str:
        lancamento = self.repository.get_by_id(item_id)
        if not lancamento:
            return "deleted"
        if lancamento["ativo"]:
            self._reverter_movimento(lancamento)
        self.repository.delete(item_id)
        return "deleted"

    def set_active(self, item_id: int, active: bool) -> None:
        lancamento = self.repository.get_by_id(item_id)
        if not lancamento:
            return
        is_active = bool(lancamento["ativo"])
        if active and not is_active:
            self._aplicar_movimento_dict(lancamento)
            self.repository.activate(item_id)
        elif not active and is_active:
            self._reverter_movimento(lancamento)
            self.repository.inactivate(item_id)

    def totais_mes(self, ano: int, mes: int) -> dict[str, float]:
        return self.repository.totais_mes(ano, mes)

    def _build_lancamento(
        self,
        tipo: str,
        meio_financeiro: str,
        data_lancamento: str,
        valor: str | float,
        categoria_id: int | str,
        descricao: str | None,
        subcategoria_id: int | str | None,
        pessoa_id: int | str | None,
        conta_id: int | str | None,
        cartao_id: int | str | None,
        observacoes: str | None,
    ) -> Lancamento:
        if tipo not in [TIPO_RECEITA, TIPO_DESPESA]:
            raise ValueError("Tipo de lançamento inválido.")
        if tipo == TIPO_RECEITA and meio_financeiro != MEIO_CONTA:
            raise ValueError("Receita deve ser lançada somente em conta.")
        if tipo == TIPO_DESPESA and meio_financeiro not in [MEIO_CONTA, MEIO_CARTAO]:
            raise ValueError("Despesa deve usar conta ou cartão.")

        data_lancamento = self._parse_data(data_lancamento)

        categoria_id_int = parse_int(categoria_id, "Categoria")
        categoria = self.categorias.get_by_id(categoria_id_int)
        if not categoria or not categoria["ativo"]:
            raise ValueError("Categoria não encontrada.")
        if categoria["tipo"] != tipo:
            raise ValueError("Categoria incompatível com o tipo do lançamento.")

        subcategoria_id_int = self._optional_id(subcategoria_id)
        if subcategoria_id_int:
            subcategoria = self.subcategorias.get_by_id(subcategoria_id_int)
            if not subcategoria or subcategoria["categoria_id"] != categoria_id_int:
                raise ValueError("Subcategoria incompatível com a categoria.")

        pessoa_id_int = self._optional_id(pessoa_id)
        if pessoa_id_int and not self.pessoas.get_by_id(pessoa_id_int):
            raise ValueError("Pessoa/Centro de Custo não encontrado.")

        conta_id_int = self._optional_id(conta_id)
        cartao_id_int = self._optional_id(cartao_id)
        if meio_financeiro == MEIO_CONTA:
            if not conta_id_int or not self.contas.get_by_id(conta_id_int):
                raise ValueError("Conta é obrigatória.")
            cartao_id_int = None
        else:
            if not cartao_id_int or not self.cartoes.get_by_id(cartao_id_int):
                raise ValueError("Cartão é obrigatório.")
            conta_id_int = None

        return Lancamento(
            tipo=tipo,
            meio_financeiro=meio_financeiro,
            data=data_lancamento,
            valor=parse_positive_float(valor, "Valor"),
            descricao=(descricao or "").strip() or None,
            categoria_id=categoria_id_int,
            subcategoria_id=subcategoria_id_int,
            pessoa_id=pessoa_id_int,
            conta_id=conta_id_int,
            cartao_id=cartao_id_int,
            observacoes=(observacoes or "").strip() or None,
        )

    def _aplicar_movimento(self, lancamento: Lancamento) -> None:
        if lancamento.meio_financeiro != MEIO_CONTA or not lancamento.conta_id:
            return
        delta = lancamento.valor if lancamento.tipo == TIPO_RECEITA else -lancamento.valor
        self.contas.update_saldo(lancamento.conta_id, delta)

    def _aplicar_movimento_dict(self, lancamento: dict) -> None:
        if lancamento["meio_financeiro"] != MEIO_CONTA or not lancamento["conta_id"]:
            return
        delta = lancamento["valor"] if lancamento["tipo"] == TIPO_RECEITA else -lancamento["valor"]
        self.contas.update_saldo(lancamento["conta_id"], delta)

    def _reverter_movimento(self, lancamento: dict) -> None:
        if lancamento["meio_financeiro"] != MEIO_CONTA or not lancamento["conta_id"]:
            return
        delta = -lancamento["valor"] if lancamento["tipo"] == TIPO_RECEITA else lancamento["valor"]
        self.contas.update_saldo(lancamento["conta_id"], delta)

    def _optional_id(self, value: int | str | None) -> int | None:
        if value in [None, "", "None"]:
            return None
        return parse_int(value, "Identificador")

    def _parse_data(self, value: str | None) -> str:
        data_texto = (value or "").strip()
        if not data_texto:
            return date.today().isoformat()
        if "/" in data_texto:
            try:
                dia, mes, ano = data_texto.split("/")
                return date(int(ano), int(mes), int(dia)).isoformat()
            except ValueError as exc:
                raise ValueError("Data deve estar no formato DD/MM/AAAA.") from exc
        try:
            return date.fromisoformat(data_texto).isoformat()
        except ValueError as exc:
            raise ValueError("Data deve estar no formato DD/MM/AAAA.") from exc
