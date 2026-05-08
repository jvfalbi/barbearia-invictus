"""
Módulo de segurança da Barbearia Invictus.

Implementa as práticas de IAM (Identity and Access Management) exigidas pela
Disciplina 3 (Segurança da Informação) do projeto:

- Hashing de senhas com bcrypt + salt (mitiga vazamento de banco - OWASP A02)
- Rate limiting + lockout temporário após N tentativas (mitiga Brute Force - OWASP A07)
- Cabeçalhos HTTP de segurança (mitiga Clickjacking, XSS, MIME sniffing - OWASP A05)
- Validação de hash em tempo constante (mitiga Timing Attacks)

Justificativas técnicas detalhadas em docs/seguranca.md.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque

import bcrypt


# --------------------------------------------------------------------------- #
# 1. Hashing de senhas (bcrypt com salt automático)                           #
# --------------------------------------------------------------------------- #

# Custo 12: ~250ms por hash em CPU moderna. Alto o suficiente para tornar
# brute force inviável, baixo o suficiente para não travar o servidor.
BCRYPT_ROUNDS = 12


def hash_password(plain: str) -> str:
    """Gera hash bcrypt da senha em texto puro."""
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Compara senha em texto puro com o hash armazenado.

    Usa comparação em tempo constante internamente (mitiga timing attack).
    """
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def is_bcrypt_hash(value: str) -> bool:
    """Detecta se o valor armazenado já é hash bcrypt (começa com $2b$)."""
    return bool(value) and value.startswith(("$2a$", "$2b$", "$2y$"))


# --------------------------------------------------------------------------- #
# 2. Rate limiting / lockout do login (em memória — basta para o MVP)         #
# --------------------------------------------------------------------------- #

MAX_TENTATIVAS = 5            # Bloqueia após 5 falhas
JANELA_SEGUNDOS = 15 * 60     # ...em 15 minutos
LOCKOUT_SEGUNDOS = 15 * 60    # Bloqueio dura 15 minutos

_falhas: dict[str, Deque[float]] = defaultdict(deque)
_bloqueios: dict[str, float] = {}


def login_bloqueado(chave: str) -> int:
    """Retorna segundos restantes de bloqueio (0 se liberado)."""
    expira = _bloqueios.get(chave)
    if not expira:
        return 0
    restante = int(expira - time.time())
    if restante <= 0:
        _bloqueios.pop(chave, None)
        return 0
    return restante


def registrar_falha(chave: str) -> int:
    """Registra uma tentativa de login falha. Retorna nº de falhas na janela."""
    agora = time.time()
    fila = _falhas[chave]
    fila.append(agora)
    while fila and (agora - fila[0]) > JANELA_SEGUNDOS:
        fila.popleft()
    if len(fila) >= MAX_TENTATIVAS:
        _bloqueios[chave] = agora + LOCKOUT_SEGUNDOS
        fila.clear()
    return len(fila)


def registrar_sucesso(chave: str) -> None:
    """Limpa o histórico após login bem-sucedido."""
    _falhas.pop(chave, None)
    _bloqueios.pop(chave, None)


# --------------------------------------------------------------------------- #
# 3. Cabeçalhos HTTP de segurança                                             #
# --------------------------------------------------------------------------- #

SECURITY_HEADERS = {
    # Mitiga Clickjacking — proíbe a página ser embarcada em iframes externos
    "X-Frame-Options": "DENY",
    # Impede o navegador de "adivinhar" o MIME type (mitiga drive-by downloads)
    "X-Content-Type-Options": "nosniff",
    # Não envia URL completa no Referer ao sair do site (privacidade)
    "Referrer-Policy": "strict-origin-when-cross-origin",
    # Bloqueia uso de APIs sensíveis (câmera, mic, geolocalização)
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    # Em produção (HTTPS) força conexões seguras por 1 ano
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    # Restringe origens de scripts/estilos/imagens
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    ),
}
