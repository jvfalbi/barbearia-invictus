from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(120))

    # LGPD: registro de consentimento (Art. 7º, I) e data da coleta (Art. 9º).
    consentimento_lgpd: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consentimento_em: Mapped[datetime | None] = mapped_column(DateTime)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    anonimizado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    agendamentos: Mapped[list["Agendamento"]] = relationship(back_populates="cliente")


class Barbeiro(Base):
    __tablename__ = "barbeiros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    especialidade: Mapped[str | None] = mapped_column(String(120))
    foto: Mapped[str | None] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    agendamentos: Mapped[list["Agendamento"]] = relationship(back_populates="barbeiro")


class Servico(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    duracao_minutos: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    agendamentos: Mapped[list["Agendamento"]] = relationship(back_populates="servico")


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    hora: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="confirmado")

    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    barbeiro_id: Mapped[int] = mapped_column(ForeignKey("barbeiros.id"), nullable=False)
    servico_id: Mapped[int] = mapped_column(ForeignKey("servicos.id"), nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="agendamentos")
    barbeiro: Mapped["Barbeiro"] = relationship(back_populates="agendamentos")
    servico: Mapped["Servico"] = relationship(back_populates="agendamentos")


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imagem: Mapped[str | None] = mapped_column(String(255))


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    # Armazena HASH bcrypt — nunca a senha em texto puro (mitiga vazamento de DB).
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    ultimo_login: Mapped[datetime | None] = mapped_column(DateTime)


class AuditLog(Base):
    """Trilha de auditoria — Disciplina 3 (compliance/forense).

    Cada ação relevante do admin (login, criação, edição, exclusão) é registrada
    com timestamp e IP de origem para investigação de incidentes.
    """

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quando: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    usuario: Mapped[str | None] = mapped_column(String(60))
    acao: Mapped[str] = mapped_column(String(80), nullable=False)
    detalhe: Mapped[str | None] = mapped_column(Text)
    ip: Mapped[str | None] = mapped_column(String(45))
    sucesso: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
