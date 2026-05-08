import csv
import io
import os
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, SessionLocal, engine, get_db
from app.models import AdminUser, Agendamento, AuditLog, Barbeiro, Cliente, Produto, Servico
from app.security import (
    SECURITY_HEADERS,
    hash_password,
    is_bcrypt_hash,
    login_bloqueado,
    registrar_falha,
    registrar_sucesso,
    verify_password,
)
from app.seed import seed_if_empty

app = FastAPI(title="Barbearia Invictus", version="2.0.0")

# Chave de sessão lida de variável de ambiente (boa prática para deploy).
# Em dev, cai num default — NUNCA usar em produção.
SECRET_KEY = os.environ.get("INVICTUS_SECRET", "invictus-dev-secret-change-me")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    https_only=False,           # True em produção HTTPS
    same_site="lax",            # mitiga CSRF (cookie não acompanha requests cross-site POST)
    max_age=60 * 60 * 8,        # sessão expira em 8h
)


@app.middleware("http")
async def security_and_cache_headers(request: Request, call_next):
    response = await call_next(request)

    # Headers de segurança (Disciplina 3 — OWASP Secure Headers Project).
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value

    # Cache: estáticos podem ser revalidados; HTML dinâmico nunca cacheia.
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
    else:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "?"


def _audit(db: Session, request: Request, acao: str, detalhe: str | None = None, sucesso: bool = True) -> None:
    """Registra ação no audit log (Disciplina 3 — trilha forense)."""
    try:
        db.add(
            AuditLog(
                usuario=request.session.get("admin"),
                acao=acao,
                detalhe=detalhe,
                ip=_client_ip(request),
                sucesso=sucesso,
            )
        )
        db.commit()
    except Exception:
        db.rollback()

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def startup() -> None:
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


def _parse_time(value: str) -> time:
    try:
        return datetime.strptime(value.strip(), "%H:%M").time()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Hora inválida. Use HH:MM.") from exc


def _parse_date(value: str) -> date:
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail="Data inválida.")


def _is_admin(request: Request) -> bool:
    return bool(request.session.get("admin"))


def _require_admin(request: Request) -> None:
    if not _is_admin(request):
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})


# ---------- Página inicial ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"active": "inicio"},
    )


# ---------- Agendamento (cliente) ----------
@app.get("/agendar", response_class=HTMLResponse)
def agendar_form(request: Request, db: Session = Depends(get_db)):
    barbeiros = db.query(Barbeiro).filter(Barbeiro.ativo == True).order_by(Barbeiro.nome).all()  # noqa: E712
    servicos = db.query(Servico).order_by(Servico.nome).all()
    return templates.TemplateResponse(
        request,
        "agendar.html",
        {
            "active": "agendar",
            "barbeiros": barbeiros,
            "servicos": servicos,
            "hoje_iso": date.today().isoformat(),
            "horarios": ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
        },
    )


@app.post("/agendar", response_class=HTMLResponse)
def agendar_create(
    request: Request,
    nome: str = Form(...),
    barbeiro_id: int = Form(...),
    servico_id: int = Form(...),
    data: str = Form(...),
    hora: str = Form(...),
    telefone: str | None = Form(None),
    email: str | None = Form(None),
    consentimento_lgpd: str | None = Form(None),
    db: Session = Depends(get_db),
):
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise HTTPException(status_code=400, detail="Informe seu nome.")

    # LGPD (Art. 7º, I): coleta de dados pessoais exige consentimento explícito.
    if not consentimento_lgpd:
        raise HTTPException(
            status_code=400,
            detail="É necessário aceitar a Política de Privacidade para agendar.",
        )

    d = _parse_date(data)
    t = _parse_time(hora)

    barbeiro = db.get(Barbeiro, barbeiro_id)
    servico = db.get(Servico, servico_id)
    if not barbeiro or not servico:
        raise HTTPException(status_code=400, detail="Barbeiro ou serviço inválido.")

    conflito = (
        db.query(Agendamento)
        .filter(
            Agendamento.barbeiro_id == barbeiro_id,
            Agendamento.data == d,
            Agendamento.hora == t,
            Agendamento.status != "cancelado",
        )
        .first()
    )
    if conflito:
        raise HTTPException(status_code=400, detail="Horário já reservado para este barbeiro.")

    cliente = Cliente(
        nome=nome_limpo,
        telefone=(telefone or "").strip() or None,
        email=(email or "").strip() or None,
        consentimento_lgpd=True,
        consentimento_em=datetime.utcnow(),
    )
    db.add(cliente)
    db.flush()

    db.add(
        Agendamento(
            data=d,
            hora=t,
            cliente_id=cliente.id,
            barbeiro_id=barbeiro_id,
            servico_id=servico_id,
            status="confirmado",
        )
    )
    db.commit()

    return templates.TemplateResponse(
        request,
        "agendar_ok.html",
        {
            "active": "agendar",
            "cliente": cliente,
            "barbeiro": barbeiro,
            "servico": servico,
            "data": d,
            "hora": t,
        },
    )


# ---------- LGPD: política de privacidade + direitos do titular ----------
@app.get("/privacidade", response_class=HTMLResponse)
def privacidade(request: Request):
    return templates.TemplateResponse(
        request, "privacidade.html", {"active": "privacidade"}
    )


@app.get("/lgpd/meus-dados", response_class=HTMLResponse)
def lgpd_form(request: Request, ok: str | None = None, erro: str | None = None):
    """Tela onde o titular consulta/exclui seus dados (Art. 18 LGPD)."""
    return templates.TemplateResponse(
        request,
        "lgpd_meus_dados.html",
        {"active": "privacidade", "ok": ok, "erro": erro},
    )


@app.post("/lgpd/excluir")
def lgpd_excluir(
    request: Request,
    nome: str = Form(...),
    confirma: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Anonimiza dados do cliente (Art. 18, VI - eliminação).

    Não fazemos hard delete porque agendamentos passados são registros
    legítimos do estabelecimento (base legal: execução de contrato).
    Substituímos os dados pessoais por valores anônimos.
    """
    if not confirma:
        return RedirectResponse(url="/lgpd/meus-dados?erro=confirma", status_code=303)

    clientes = (
        db.query(Cliente)
        .filter(Cliente.nome.ilike(nome.strip()), Cliente.anonimizado == False)  # noqa: E712
        .all()
    )
    if not clientes:
        return RedirectResponse(url="/lgpd/meus-dados?erro=naoencontrado", status_code=303)

    for c in clientes:
        c.nome = f"Cliente Anonimizado #{c.id}"
        c.telefone = None
        c.email = None
        c.anonimizado = True
    db.commit()
    _audit(db, request, "lgpd_anonimizacao", detalhe=f"clientes={[c.id for c in clientes]}")
    return RedirectResponse(url="/lgpd/meus-dados?ok=1", status_code=303)


# ---------- Produtos ----------
@app.get("/produtos", response_class=HTMLResponse)
def produtos(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).order_by(Produto.nome).all()
    return templates.TemplateResponse(
        request,
        "produtos.html",
        {"active": "produtos", "produtos": produtos},
    )


# ---------- Admin (login + painel) ----------
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_form(request: Request, erro: str | None = None, segs: int = 0):
    if _is_admin(request):
        return RedirectResponse(url="/admin", status_code=303)
    return templates.TemplateResponse(
        request,
        "admin_login.html",
        {"active": "admin", "erro": erro, "segs": segs},
    )


@app.post("/admin/login")
def admin_login(
    request: Request,
    usuario: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    chave = f"{_client_ip(request)}::{usuario.strip().lower()}"

    # 1) Lockout temporário (mitiga Brute Force - OWASP A07).
    bloqueio = login_bloqueado(chave)
    if bloqueio:
        _audit(db, request, "login_bloqueado", detalhe=f"usuario={usuario}", sucesso=False)
        return RedirectResponse(url=f"/admin/login?erro=lockout&segs={bloqueio}", status_code=303)

    user = db.query(AdminUser).filter(AdminUser.usuario == usuario.strip()).first()

    # 2) Verificação com bcrypt (constante no tempo, mitiga timing attack).
    senha_ok = False
    if user:
        if is_bcrypt_hash(user.senha):
            senha_ok = verify_password(senha, user.senha)
        else:
            # Migração transparente: usuário ainda com senha em texto puro.
            # Compara, e se acertar, regrava como hash bcrypt.
            if user.senha == senha:
                user.senha = hash_password(senha)
                db.commit()
                senha_ok = True

    if not user or not senha_ok:
        registrar_falha(chave)
        _audit(db, request, "login_falhou", detalhe=f"usuario={usuario}", sucesso=False)
        return RedirectResponse(url="/admin/login?erro=1", status_code=303)

    registrar_sucesso(chave)
    user.ultimo_login = datetime.utcnow()
    db.commit()
    request.session["admin"] = user.usuario
    _audit(db, request, "login_ok", detalhe=f"usuario={usuario}")
    return RedirectResponse(url="/admin", status_code=303)


@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.get("/admin", response_class=HTMLResponse)
def admin_painel(request: Request, db: Session = Depends(get_db), tab: str = "agendamentos"):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)

    hoje = date.today()
    agendamentos = (
        db.query(Agendamento)
        .order_by(Agendamento.data.desc(), Agendamento.hora.desc())
        .limit(200)
        .all()
    )
    barbeiros = db.query(Barbeiro).order_by(Barbeiro.nome).all()
    servicos = db.query(Servico).order_by(Servico.nome).all()
    produtos = db.query(Produto).order_by(Produto.nome).all()
    total_clientes = db.scalar(select(func.count()).select_from(Cliente)) or 0
    total_agendamentos = db.scalar(select(func.count()).select_from(Agendamento)) or 0
    agendamentos_hoje = sum(1 for a in agendamentos if a.data == hoje)

    return templates.TemplateResponse(
        request,
        "admin_painel.html",
        {
            "active": "admin",
            "admin_user": request.session.get("admin"),
            "tab": tab,
            "agendamentos": agendamentos,
            "barbeiros": barbeiros,
            "servicos": servicos,
            "produtos": produtos,
            "total_clientes": total_clientes,
            "total_agendamentos": total_agendamentos,
            "agendamentos_hoje": agendamentos_hoje,
            "hoje": hoje,
            "hoje_iso": hoje.isoformat(),
        },
    )


# ---------- Cadastros administrativos (barbeiros / serviços / produtos) ----------
@app.post("/admin/barbeiros")
def admin_create_barbeiro(
    request: Request,
    nome: str = Form(...),
    especialidade: str | None = Form(None),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    db.add(Barbeiro(nome=nome.strip(), especialidade=(especialidade or "").strip() or None))
    db.commit()
    return RedirectResponse(url="/admin?tab=barbeiros", status_code=303)


@app.post("/admin/servicos")
def admin_create_servico(
    request: Request,
    nome: str = Form(...),
    duracao_minutos: int = Form(...),
    preco: str = Form(...),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    try:
        preco_dec = Decimal(preco.replace(",", "."))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Preço inválido.") from exc
    db.add(Servico(nome=nome.strip(), duracao_minutos=int(duracao_minutos), preco=preco_dec))
    db.commit()
    return RedirectResponse(url="/admin?tab=servicos", status_code=303)


@app.post("/admin/produtos")
def admin_create_produto(
    request: Request,
    nome: str = Form(...),
    preco: str = Form(...),
    estoque: int = Form(0),
    descricao: str | None = Form(None),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    try:
        preco_dec = Decimal(preco.replace(",", "."))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Preço inválido.") from exc
    db.add(
        Produto(
            nome=nome.strip(),
            preco=preco_dec,
            estoque=int(estoque),
            descricao=(descricao or "").strip() or None,
        )
    )
    db.commit()
    return RedirectResponse(url="/admin?tab=produtos", status_code=303)


@app.post("/admin/agendamentos/{agendamento_id}/status")
def admin_update_status(
    request: Request,
    agendamento_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    if status not in {"confirmado", "concluido", "cancelado"}:
        raise HTTPException(status_code=400, detail="Status inválido.")
    ag = db.get(Agendamento, agendamento_id)
    if ag:
        ag.status = status
        db.commit()
    return RedirectResponse(url="/admin?tab=agendamentos", status_code=303)


# ---------- Edição: Agendamentos ----------
@app.get("/admin/agendamentos/{agendamento_id}/edit", response_class=HTMLResponse)
def admin_edit_agendamento_form(request: Request, agendamento_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    ag = db.get(Agendamento, agendamento_id)
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    return templates.TemplateResponse(
        request,
        "admin_edit_agendamento.html",
        {
            "active": "admin",
            "ag": ag,
            "barbeiros": db.query(Barbeiro).order_by(Barbeiro.nome).all(),
            "servicos": db.query(Servico).order_by(Servico.nome).all(),
        },
    )


@app.post("/admin/agendamentos/{agendamento_id}/edit")
def admin_edit_agendamento(
    request: Request,
    agendamento_id: int,
    cliente_nome: str = Form(...),
    barbeiro_id: int = Form(...),
    servico_id: int = Form(...),
    data: str = Form(...),
    hora: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    if status not in {"confirmado", "concluido", "cancelado"}:
        raise HTTPException(status_code=400, detail="Status inválido.")
    ag = db.get(Agendamento, agendamento_id)
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    ag.cliente.nome = cliente_nome.strip()
    ag.barbeiro_id = barbeiro_id
    ag.servico_id = servico_id
    ag.data = _parse_date(data)
    ag.hora = _parse_time(hora)
    ag.status = status
    db.commit()
    return RedirectResponse(url="/admin?tab=agendamentos", status_code=303)


@app.post("/admin/agendamentos/{agendamento_id}/delete")
def admin_delete_agendamento(request: Request, agendamento_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    ag = db.get(Agendamento, agendamento_id)
    if ag:
        db.delete(ag)
        db.commit()
    return RedirectResponse(url="/admin?tab=agendamentos", status_code=303)


# ---------- Edição: Barbeiros ----------
@app.get("/admin/barbeiros/{barbeiro_id}/edit", response_class=HTMLResponse)
def admin_edit_barbeiro_form(request: Request, barbeiro_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    b = db.get(Barbeiro, barbeiro_id)
    if not b:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    return templates.TemplateResponse(
        request, "admin_edit_barbeiro.html", {"active": "admin", "b": b}
    )


@app.post("/admin/barbeiros/{barbeiro_id}/edit")
def admin_edit_barbeiro(
    request: Request,
    barbeiro_id: int,
    nome: str = Form(...),
    especialidade: str | None = Form(None),
    foto: str | None = Form(None),
    ativo: str | None = Form(None),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    b = db.get(Barbeiro, barbeiro_id)
    if not b:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    b.nome = nome.strip()
    b.especialidade = (especialidade or "").strip() or None
    b.foto = (foto or "").strip() or None
    b.ativo = bool(ativo)
    db.commit()
    return RedirectResponse(url="/admin?tab=barbeiros", status_code=303)


@app.post("/admin/barbeiros/{barbeiro_id}/delete")
def admin_delete_barbeiro(request: Request, barbeiro_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    b = db.get(Barbeiro, barbeiro_id)
    if b:
        em_uso = db.query(Agendamento).filter(Agendamento.barbeiro_id == b.id).first()
        if em_uso:
            b.ativo = False
            db.commit()
        else:
            db.delete(b)
            db.commit()
    return RedirectResponse(url="/admin?tab=barbeiros", status_code=303)


# ---------- Edição: Serviços ----------
@app.get("/admin/servicos/{servico_id}/edit", response_class=HTMLResponse)
def admin_edit_servico_form(request: Request, servico_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    s = db.get(Servico, servico_id)
    if not s:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    return templates.TemplateResponse(
        request, "admin_edit_servico.html", {"active": "admin", "s": s}
    )


@app.post("/admin/servicos/{servico_id}/edit")
def admin_edit_servico(
    request: Request,
    servico_id: int,
    nome: str = Form(...),
    duracao_minutos: int = Form(...),
    preco: str = Form(...),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    s = db.get(Servico, servico_id)
    if not s:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    try:
        preco_dec = Decimal(preco.replace(",", "."))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Preço inválido.") from exc
    s.nome = nome.strip()
    s.duracao_minutos = int(duracao_minutos)
    s.preco = preco_dec
    db.commit()
    return RedirectResponse(url="/admin?tab=servicos", status_code=303)


@app.post("/admin/servicos/{servico_id}/delete")
def admin_delete_servico(request: Request, servico_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    s = db.get(Servico, servico_id)
    if s:
        em_uso = db.query(Agendamento).filter(Agendamento.servico_id == s.id).first()
        if em_uso:
            raise HTTPException(status_code=400, detail="Serviço usado em agendamentos. Não pode ser excluído.")
        db.delete(s)
        db.commit()
    return RedirectResponse(url="/admin?tab=servicos", status_code=303)


# ---------- Edição: Produtos ----------
@app.get("/admin/produtos/{produto_id}/edit", response_class=HTMLResponse)
def admin_edit_produto_form(request: Request, produto_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    p = db.get(Produto, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return templates.TemplateResponse(
        request, "admin_edit_produto.html", {"active": "admin", "p": p}
    )


@app.post("/admin/produtos/{produto_id}/edit")
def admin_edit_produto(
    request: Request,
    produto_id: int,
    nome: str = Form(...),
    descricao: str | None = Form(None),
    preco: str = Form(...),
    estoque: int = Form(0),
    imagem: str | None = Form(None),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    p = db.get(Produto, produto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    try:
        preco_dec = Decimal(preco.replace(",", "."))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Preço inválido.") from exc
    p.nome = nome.strip()
    p.descricao = (descricao or "").strip() or None
    p.preco = preco_dec
    p.estoque = int(estoque)
    p.imagem = (imagem or "").strip() or None
    db.commit()
    return RedirectResponse(url="/admin?tab=produtos", status_code=303)


@app.post("/admin/produtos/{produto_id}/delete")
def admin_delete_produto(request: Request, produto_id: int, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    p = db.get(Produto, produto_id)
    if p:
        db.delete(p)
        db.commit()
    return RedirectResponse(url="/admin?tab=produtos", status_code=303)


@app.post("/admin/produtos/{produto_id}/estoque")
def admin_ajustar_estoque(
    request: Request,
    produto_id: int,
    delta: int = Form(...),
    db: Session = Depends(get_db),
):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    p = db.get(Produto, produto_id)
    if p:
        p.estoque = max(0, p.estoque + int(delta))
        db.commit()
    return RedirectResponse(url="/admin?tab=produtos", status_code=303)


# --------------------------------------------------------------------------- #
# Disciplina 2 — Exportação CSV (alimenta os scripts Python de análise)        #
# --------------------------------------------------------------------------- #


def _csv_response(rows: list[list], headers: list[str], filename: str) -> StreamingResponse:
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=";")
    writer.writerow(headers)
    writer.writerows(rows)
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/admin/export/agendamentos.csv")
def export_agendamentos(request: Request, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    ags = db.query(Agendamento).all()
    rows = [
        [
            a.id,
            a.data.isoformat(),
            a.hora.strftime("%H:%M"),
            a.cliente.nome,
            a.barbeiro.nome,
            a.servico.nome,
            float(a.servico.preco),
            a.servico.duracao_minutos,
            a.status,
        ]
        for a in ags
    ]
    return _csv_response(
        rows,
        ["id", "data", "hora", "cliente", "barbeiro", "servico", "preco", "duracao_min", "status"],
        "agendamentos.csv",
    )


@app.get("/admin/export/produtos.csv")
def export_produtos(request: Request, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    rows = [[p.id, p.nome, float(p.preco), p.estoque, p.descricao or ""] for p in db.query(Produto).all()]
    return _csv_response(rows, ["id", "nome", "preco", "estoque", "descricao"], "produtos.csv")


@app.get("/admin/export/servicos.csv")
def export_servicos(request: Request, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    rows = [[s.id, s.nome, s.duracao_minutos, float(s.preco)] for s in db.query(Servico).all()]
    return _csv_response(rows, ["id", "nome", "duracao_min", "preco"], "servicos.csv")


# --------------------------------------------------------------------------- #
# Disciplina 3 — Audit log visível ao admin                                    #
# --------------------------------------------------------------------------- #


@app.get("/admin/auditoria", response_class=HTMLResponse)
def admin_auditoria(request: Request, db: Session = Depends(get_db)):
    if not _is_admin(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    eventos = db.query(AuditLog).order_by(AuditLog.quando.desc()).limit(200).all()
    return templates.TemplateResponse(
        request,
        "admin_auditoria.html",
        {"active": "admin", "eventos": eventos, "admin_user": request.session.get("admin")},
    )
