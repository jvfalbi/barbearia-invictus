from datetime import date, time
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import AdminUser, Agendamento, Barbeiro, Cliente, Produto, Servico
from app.security import hash_password


def seed_if_empty(db: Session) -> None:
    if not db.query(AdminUser).first():
        # Senha "admin123" — armazenada como hash bcrypt (Disciplina 3 - IAM).
        # Em produção, exigir reset no primeiro login.
        db.add(AdminUser(usuario="admin", senha=hash_password("admin123")))
        db.commit()

    if db.query(Barbeiro).first():
        return

    barbeiros = [
        Barbeiro(nome="Calebe", especialidade="Corte clássico", foto="calebe.jpg"),
        Barbeiro(nome="Diego", especialidade="Degradê e barba", foto="diego.jpg"),
        Barbeiro(nome="Guilherme", especialidade="Corte + barba completo", foto="guilherme.jpg"),
        Barbeiro(nome="João", especialidade="Pigmentação e acabamento", foto="joao.jpg"),
    ]

    servicos = [
        Servico(nome="Corte", duracao_minutos=30, preco=Decimal("35.00")),
        Servico(nome="Barba", duracao_minutos=25, preco=Decimal("30.00")),
        Servico(nome="Corte + Barba", duracao_minutos=55, preco=Decimal("60.00")),
        Servico(nome="Pigmentação", duracao_minutos=40, preco=Decimal("50.00")),
    ]

    produtos = [
        Produto(
            nome="Cera Fosca",
            descricao="Acabamento fosco com duração prolongada.",
            preco=Decimal("34.90"),
            estoque=15,
            imagem="cera-fosca.jpg",
        ),
        Produto(
            nome="Gel Fixador Forte",
            descricao="Fixação máxima sem ressecar os fios.",
            preco=Decimal("22.90"),
            estoque=20,
            imagem="gel-fixador.jpg",
        ),
        Produto(
            nome="Máquina de Corte Premium",
            descricao="Alto desempenho e durabilidade.",
            preco=Decimal("249.90"),
            estoque=5,
            imagem="maquina-corte.jpg",
        ),
        Produto(
            nome="Pomada Modeladora",
            descricao="Controle e fixação com estilo.",
            preco=Decimal("29.90"),
            estoque=12,
            imagem="pomada.jpg",
        ),
        Produto(
            nome="Shampoo Antirresíduos",
            descricao="Limpeza profunda para cabelo e barba.",
            preco=Decimal("29.90"),
            estoque=8,
            imagem="shampoo.jpg",
        ),
        Produto(
            nome="Pós Barba Premium",
            descricao="Hidrata e acalma a pele após o barbear.",
            preco=Decimal("19.90"),
            estoque=18,
            imagem="pos-barba.jpg",
        ),
    ]

    for row in barbeiros + servicos + produtos:
        db.add(row)
    db.commit()

    cliente = Cliente(nome="Cliente Demonstração", telefone="(11) 90000-0000")
    db.add(cliente)
    db.commit()

    b1 = db.query(Barbeiro).first()
    s1 = db.query(Servico).first()
    if cliente and b1 and s1:
        db.add(
            Agendamento(
                data=date.today(),
                hora=time(14, 30),
                status="confirmado",
                cliente_id=cliente.id,
                barbeiro_id=b1.id,
                servico_id=s1.id,
            )
        )
        db.commit()
