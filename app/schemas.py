from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ClienteBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    telefone: str = Field(min_length=8, max_length=32)
    email: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    id: int

    model_config = {"from_attributes": True}


class BarbeiroBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    especialidade: str | None = None


class BarbeiroCreate(BarbeiroBase):
    pass


class BarbeiroRead(BarbeiroBase):
    id: int

    model_config = {"from_attributes": True}


class ServicoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    duracao_minutos: int = Field(ge=5, le=480)
    preco: Decimal = Field(ge=0)


class ServicoCreate(ServicoBase):
    pass


class ServicoRead(ServicoBase):
    id: int

    model_config = {"from_attributes": True}


class AgendamentoCreate(BaseModel):
    data: date
    hora: time
    cliente_id: int = Field(ge=1)
    barbeiro_id: int = Field(ge=1)
    servico_id: int = Field(ge=1)
    status: str = "confirmado"

    @field_validator("status")
    @classmethod
    def status_ok(cls, v: str) -> str:
        allowed = {"confirmado", "concluido", "cancelado"}
        if v not in allowed:
            raise ValueError(f"status deve ser um de: {', '.join(sorted(allowed))}")
        return v


class AgendamentoRead(BaseModel):
    id: int
    data: date
    hora: time
    status: str
    cliente_id: int
    barbeiro_id: int
    servico_id: int
    cliente_nome: str
    barbeiro_nome: str
    servico_nome: str

    model_config = {"from_attributes": True}
