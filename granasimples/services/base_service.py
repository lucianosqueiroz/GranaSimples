from typing import Any


class BaseCrudService:
    repository: Any

    def list_all(self, only_active: bool = True) -> list[dict[str, Any]]:
        return self.repository.list_all(only_active)

    def get_by_id(self, item_id: int) -> dict[str, Any] | None:
        return self.repository.get_by_id(item_id)

    def remove(self, item_id: int) -> None:
        print(f"[GranaSimples][Service] Solicitação de remoção id={item_id}")
        if self.repository.has_links(item_id):
            print(f"[GranaSimples][Service] Registro id={item_id} tem vínculo. Será inativado.")
            self.repository.inactivate(item_id)
        else:
            print(f"[GranaSimples][Service] Registro id={item_id} sem vínculo. Será excluído fisicamente.")
            self.repository.delete(item_id)

    def set_active(self, item_id: int, active: bool) -> None:
        print(f"[GranaSimples][Service] Alterando status id={item_id} active={active}")
        if active:
            self.repository.activate(item_id)
        else:
            self.repository.inactivate(item_id)


def require_text(value: str | None, field_name: str) -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{field_name} é obrigatório.")
    return text


def parse_positive_float(value: str | float | int, field_name: str) -> float:
    raw_value = str(value).strip()
    if "," in raw_value:
        raw_value = raw_value.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
    else:
        raw_value = raw_value.replace("R$", "").replace(" ", "")
    try:
        number = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{field_name} deve ser numérico.") from exc
    if number <= 0:
        raise ValueError(f"{field_name} deve ser maior que zero.")
    return number


def parse_float(value: str | float | int, field_name: str) -> float:
    raw_value = str(value or "0").strip()
    if "," in raw_value:
        raw_value = raw_value.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
    else:
        raw_value = raw_value.replace("R$", "").replace(" ", "")
    try:
        return float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{field_name} deve ser numérico.") from exc


def parse_int(value: str | int, field_name: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} deve ser um número inteiro.") from exc
