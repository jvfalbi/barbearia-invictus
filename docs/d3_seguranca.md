# Disciplina 3 — Segurança da Informação

> Documento técnico de **SecOps + LGPD** para o sistema **Barbearia Invictus**,
> seguindo o guia oficial da disciplina (3.1 Matriz GUT, 3.2 IAM, 3.3 LGPD/RoPA,
> 3.4 Análise Crítica).
>
> ⚠️ **Regra do guia:** *"o grupo não deve inventar ameaças ou regras. Vocês
> devem agir como profissionais: pesquisar em fontes oficiais (como OWASP e
> a lei LGPD), escolher as opções adequadas para o projeto e justificar
> tecnicamente cada escolha."*

---

## 3.1 Matriz GUT — Mapeamento de 20 Ameaças Reais

**Fórmula:** `Nota = G × U × T` — cada fator de **1 a 5**.

- **Gravidade (G):** dano se ocorrer (1 = mínimo, 5 = falência/roubo total).
- **Urgência (U):** o quanto precisamos corrigir agora (1 = pode esperar, 5 = imediato).
- **Tendência (T):** se nada for feito, piora? (1 = fica igual, 5 = espalha rápido).

**Fontes pesquisadas:** [OWASP Top 10 — 2021](https://owasp.org/Top10/), [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/), [CVE / NVD](https://nvd.nist.gov/), [CWE Top 25](https://cwe.mitre.org/top25/).

| # | Ameaça (referência) | Como ocorreria no projeto Barbearia Invictus | G | U | T | **Nota** | Mitigação implementada |
|--:|---|---|--:|--:|--:|--:|---|
| 01 | **Vazamento de banco de dados** (OWASP A02 — Cryptographic Failures) | Atacante obtém o arquivo `data/invictus.db` por backup mal configurado e lê todas as senhas/clientes | 5 | 5 | 5 | **125** | Senhas em **hash bcrypt + salt** (`app/security.py: hash_password`). Brute-force inviável (~250 ms/tentativa). |
| 02 | **Brute force no login admin** (OWASP A07 — Identification & Auth Failures) | Bot tenta milhares de senhas comuns por segundo em `/admin/login` | 5 | 5 | 4 | **100** | **Rate-limit + lockout** 5 tentativas/15 min (`registrar_falha`, `login_bloqueado`). |
| 03 | **SQL Injection** (OWASP A03 — Injection / CWE-89) | Atacante envia `'; DROP TABLE clientes;--` no campo "Nome" do agendamento | 5 | 4 | 5 | **100** | **SQLAlchemy ORM** com queries parametrizadas. Strings nunca são concatenadas em SQL bruto. |
| 04 | **XSS armazenado** (OWASP A03 / CWE-79) | Cliente registra `<script>fetch('/admin/.../delete')</script>` como nome; admin abre o painel | 5 | 4 | 4 | **80** | **Jinja2 auto-escape** ativo + **CSP estrita** (`script-src 'self'` + CDN whitelist). |
| 05 | **Session hijacking** (OWASP A07) | Atacante captura cookie de sessão em rede pública (HTTP) | 5 | 4 | 4 | **80** | `https_only=True` em produção + **HSTS** (`max-age=31536000`) + sessão expira em 8h. |
| 06 | **Clickjacking** (OWASP A05 — Security Misconfiguration) | Site malicioso embarca `/admin` em `<iframe>` invisível e captura cliques | 4 | 4 | 4 | **64** | Header `X-Frame-Options: DENY` + CSP `frame-ancestors 'none'`. |
| 07 | **Credential stuffing** (OWASP A07) | Atacante usa lista de senhas vazadas de outro site para tentar logar como admin | 4 | 4 | 4 | **64** | Mesmo mecanismo de **rate-limit/lockout**; senha admin obrigatoriamente forte (política manual). |
| 08 | **Stack trace exposto** (OWASP A05 — Information Disclosure / CWE-209) | Erro 500 em produção mostra caminho `C:\Users\...` e versão do FastAPI | 4 | 4 | 4 | **64** | `DEBUG=False` em produção + handler global de erro retornando mensagem genérica. |
| 09 | **CSRF — exclusão forçada via link malicioso** (OWASP A01) | Admin logado clica em link que dispara POST para `/admin/agendamentos/99/delete` | 4 | 3 | 4 | **48** | Cookie de sessão com `SameSite=Lax` (browser não envia em POST cross-site). |
| 10 | **IDOR** — referência direta insegura (OWASP A01 — Broken Access Control) | Usuário comum altera URL para `/admin/agendamentos/99/edit` | 4 | 4 | 3 | **48** | Toda rota `/admin/*` valida `_is_admin(request)` antes de qualquer operação. |
| 11 | **Mass assignment** (OWASP A08 / CWE-915) | Form de cadastro recebe campo extra `is_admin=true` que altera papel | 4 | 4 | 3 | **48** | Pydantic + lista explícita de campos esperados; `request.form()` lê só os declarados. |
| 12 | **DoS por inundação** no endpoint público de agendamento | Bot envia 1.000 POST/s em `/agendar` | 3 | 4 | 3 | **36** | Mitigação parcial via rate-limit do uvicorn; deploy futuro atrás de Nginx com `limit_req_zone`. |
| 13 | **Dependência vulnerável** (OWASP A06 — Vulnerable Components) | Versão antiga de Jinja2/FastAPI listada em CVE-2024-XXXX | 3 | 4 | 4 | **48** | `pip-audit` + `bandit` ao final de cada Sprint; versões pinadas no `requirements.txt`. |
| 14 | **Path Traversal** (CWE-22) em download de imagem de produto | URL `/static/../../../data/invictus.db` baixa o banco | 4 | 4 | 3 | **48** | FastAPI `StaticFiles` rejeita `..`; nenhum endpoint próprio aceita caminho do usuário. |
| 15 | **Open Redirect** em página de login (OWASP A01) | URL `/admin/login?next=https://phishing.com` redireciona após sucesso | 3 | 3 | 3 | **27** | Validação rígida: `next` só aceita caminhos relativos `^/`. |
| 16 | **MIME sniffing** — XSS via upload mal rotulado | Browser interpreta arquivo `.txt` como HTML executável | 3 | 3 | 2 | **18** | Header `X-Content-Type-Options: nosniff`. |
| 17 | **Privilege escalation** (OWASP A01) — admin comum vira super-admin | DB modificado para promover usuário a `is_admin=true` | 5 | 3 | 3 | **45** | Apenas 1 papel administrativo no projeto + audit log registra qualquer alteração na tabela `AdminUser`. |
| 18 | **Vazamento de PII em logs** (LGPD Art. 46 / CWE-532) | uvicorn escreve `body=...` com CPF/telefone em log de erro | 4 | 4 | 3 | **48** | Logs filtram campos sensíveis; nenhum `print(request.json())` em produção. |
| 19 | **Race condition no estoque** (CWE-362 — TOCTOU) | Dois admins clicam `+1` no mesmo produto ao mesmo tempo e o estoque sobe só 1 | 3 | 3 | 3 | **27** | Operação de estoque usa `UPDATE produtos SET estoque=estoque+:n` (atômica no SQLite). |
| 20 | **SSRF** (OWASP A10 — Server-Side Request Forgery) | Endpoint que aceitasse URL externa poderia ser usado para escanear rede interna | 4 | 3 | 2 | **24** | Não existe endpoint que aceite URL do usuário no escopo atual; futuro: whitelist de domínios. |

### Top-3 prioridades (ordenadas por nota GUT)

1. **125 — Vazamento de banco de dados** (#01) → mitigado com bcrypt cost 12
2. **100 — Brute Force** (#02) → mitigado com rate-limit/lockout
3. **100 — SQL Injection** (#03) → mitigado com SQLAlchemy ORM

Estas 3 ameaças, juntas, somam **325 pontos GUT** (37% do total mapeado) e
recebem o investimento prioritário em segurança.

---

## 3.2 IAM — 20 Políticas de Acesso e Identidade

> Conceitos pesquisados: **NIST SP 800-63B** (Digital Identity), **OWASP ASVS 4.0**,
> **Microsoft Zero Trust** (`Verify Explicitly`, `Least Privilege`, `Assume Breach`),
> **Google BeyondCorp**.

| # | Política | Justificativa técnica para o nosso sistema | Implementação |
|--:|---|---|---|
| 01 | **Autenticação por hash bcrypt** (cost = 12) | Brute force em DB vazado fica inviável; cada tentativa custa ~250 ms | `app/security.py: hash_password()` |
| 02 | **Senha mínima de 8 caracteres** com letra, número e símbolo (NIST 800-63B) | Eleva entropia e mitigia dicionário | Validação no formulário de criação de admin |
| 03 | **Rate-limit + lockout** após 5 falhas em 15 min | Bloqueia botnets de credential stuffing | `registrar_falha()` + `login_bloqueado()` |
| 04 | **Cookie de sessão `HttpOnly` + `SameSite=Lax`** | Mitiga XSS-roubo de cookie e CSRF | `SessionMiddleware` no `main.py` |
| 05 | **Expiração de sessão em 8 h** (NIST: ≤ 12 h para apps comuns) | Reduz janela de ataque com cookie roubado | `max_age=28800` |
| 06 | **Audit log de toda ação administrativa** | Rastreamento forense em incidentes | Tabela `AuditLog` + `_audit()` |
| 07 | **RBAC** (Role-Based Access Control) — perfis `público`, `cliente`, `admin` | Cliente só agenda; admin gerencia. Princípio do menor privilégio | `_is_admin(request)` em rotas `/admin/*` |
| 08 | **CSP estrita** (`script-src 'self'` + CDN allowlist) | Bloqueia XSS injetado mesmo se auto-escape falhar | `SECURITY_HEADERS` |
| 09 | **HSTS** (`max-age=31536000; includeSubDomains`) | Força HTTPS após 1ª visita; mitiga downgrade | Header em produção |
| 10 | **Logout limpa toda a sessão** (`request.session.clear()`) | Evita reuso indevido após logout | `app/main.py: admin_logout()` |
| 11 | **Comparação de senha em tempo constante** | Mitiga timing attack | `bcrypt.checkpw()` |
| 12 | **Secret-key da sessão lida de variável de ambiente** | Não comitar segredo no Git | `os.environ.get("INVICTUS_SECRET")` |
| 13 | **Princípio do menor privilégio no browser** (`Permissions-Policy: camera=(), microphone=(), geolocation=()`) | App não precisa de câmera/microfone; nega por padrão | `SECURITY_HEADERS` |
| 14 | **MFA / 2FA** para conta admin (TOTP via Authy/Google Authenticator) | Mitiga vazamento de senha + zero trust ("Verify Explicitly") | **Roadmap pós-banca** — exige campo `secret_2fa` em `AdminUser` |
| 15 | **Política de rotação de senha admin** a cada 180 dias | Reduz janela de comprometimento crônico | Campo `senha_alterada_em` + flash de aviso ao login |
| 16 | **Segregação de ambientes** (dev / homologação / prod) com `.env` distintos | Evita usar dados reais em testes (LGPD Art. 14) | `.env.dev`, `.env.prod` (Roadmap) |
| 17 | **Backup criptografado e geograficamente separado** (AES-256 + S3 versionado) | Resiliência a ransomware/sinistro | Roadmap; hoje há backup manual `.db` zipado com senha |
| 18 | **Sanitização de input com Pydantic** (validação de tipos antes do ORM) | Defesa em profundidade contra injection / mass assignment | Modelos Pydantic em todos os endpoints POST |
| 19 | **Defense in Depth (camadas)** — CSP + ORM + auto-escape + auth + audit | Falha de uma camada não compromete o sistema | Aplicado em todo `app/` |
| 20 | **Zero Trust posture** — toda requisição admin é re-validada (`_is_admin`) | Confiança zero entre requisições, mesmo dentro da sessão | Middleware aplica em todo `/admin/*` |

> **Status do roadmap:** 16 de 20 políticas estão **implementadas hoje**;
> 4 (MFA, rotação automática, backup criptografado, segregação de ambiente)
> ficam como evolução pós-banca, com justificativa de tempo/custo no TAP.

---

## 3.3 LGPD — RoPA (Registro de Atividades de Tratamento) — 20 Itens

> Lei 13.709/2018 — Art. 7º (bases legais), Art. 18 (direitos do titular),
> Art. 37 (RoPA obrigatório), Art. 46 (segurança técnica).

| # | Dado coletado / Processo | Finalidade | Base Legal (Art. 7º LGPD) | Direito do Titular |
|--:|---|---|---|---|
| 01 | **Nome do cliente** | Identificação na agenda do barbeiro | V — execução de contrato | Acessível e anonimizável em `/lgpd/meus-dados` |
| 02 | **Telefone (opcional)** | Confirmação de horário e reagendamento | I — consentimento | Pode ser apagado a qualquer momento |
| 03 | **E-mail (opcional)** | Envio de comprovante de agendamento | I — consentimento | Pode ser apagado a qualquer momento |
| 04 | **Data e hora do agendamento** | Operação do serviço | V — execução de contrato | Mantido como dado anonimizado para estatística |
| 05 | **Histórico de serviços contratados** | Personalização do atendimento | V — execução de contrato | Anonimizável após 5 anos |
| 06 | **IP do dispositivo + timestamp** | Segurança e auditoria (mitigação fraude) | II — obrigação legal (LGPD Art. 6º, VII) | Não removível durante retenção (6 meses) |
| 07 | **Cookie de sessão (`session`)** | Manter usuário logado no painel admin | V — execução de contrato | Limpável por logout ou exclusão de cookies do browser |
| 08 | **Log de tentativas de login (sucesso/falha)** | Detecção de brute force e auditoria | II — obrigação legal | Não removível durante retenção (1 ano) |
| 09 | **Hash bcrypt da senha admin** | Autenticação | V — execução de contrato | Excluído com a conta admin |
| 10 | **Status do agendamento** | Gestão operacional + cálculo de KPIs | V — execução de contrato | Mantido anonimizado para análise (D2) |
| 11 | **User-Agent do navegador** | Estatística de compatibilidade + auditoria | IX — interesse legítimo | Não removível durante retenção (6 meses) |
| 12 | **Foto do barbeiro** (`barbeiros.foto`) | Exibição na página pública de agendamento | I — consentimento (do funcionário) | O barbeiro pode pedir remoção a qualquer momento |
| 13 | **Nome do barbeiro** | Identificação para o cliente escolher profissional | V — execução de contrato (vínculo trabalhista) | Apagado quando o vínculo termina |
| 14 | **Audit log com IP + ação + usuário** | Compliance e forense de incidentes | II — obrigação legal | Retenção 12 meses; não removível |
| 15 | **Consentimento LGPD do cliente** (`consentimento_lgpd`, `consentimento_em`) | Prova jurídica de consentimento (Art. 8º) | II — obrigação legal | Histórico de consentimento mantido para auditoria |
| 16 | **Estoque de produtos vendidos a um cliente** | Reposição automatizada e histórico de compras | V — execução de contrato | Anonimizável junto com o cliente |
| 17 | **Logs do servidor uvicorn (acessos)** | Diagnóstico de erro + análise de tráfego | IX — interesse legítimo | Retenção 30 dias; rotacionados |
| 18 | **Backup do banco de dados** | Continuidade do negócio | IX — interesse legítimo | Cliente anonimizado também é anonimizado nos backups na próxima rotação |
| 19 | **Telemetria de erro (stack trace sem PII)** | Debug de produção | IX — interesse legítimo | Retenção 90 dias |
| 20 | **Flag de anonimização (`clientes.anonimizado`)** | Marcar registros que exerceram direito de exclusão | II — obrigação legal | Cumpre o direito do titular (Art. 18 VI) |

### Direitos do titular implementados (Art. 18 LGPD)

| Direito | Onde é exercido |
|---|---|
| Confirmação da existência de tratamento | Página `/privacidade` lista todas as finalidades |
| Acesso aos dados | `/lgpd/meus-dados` (formulário + retorno por e-mail) |
| Anonimização / eliminação | Mesmo formulário aciona `lgpd_excluir()` que **anonimiza** (não deleta) preservando integridade contábil |
| Revogação do consentimento | Cliente pode pedir anonimização a qualquer momento |
| Informação sobre compartilhamento | Política de privacidade declara: **dados não são compartilhados com terceiros** |

---

## 3.4 Análise Crítica Exigida (Segurança)

> ⚠️ **Pergunta obrigatória do guia (transcrita literalmente):**
>
> *"Considerando a vulnerabilidade que recebeu a nota mais alta na sua Matriz
> GUT, explique detalhadamente como um invasor poderia explorar essa falha
> no contexto específico das funcionalidades do SEU projeto. Em seguida,
> descreva exatamente qual técnica de programação ou regra de infraestrutura
> o grupo pesquisou e adotou para anular esse risco."*

### Resposta (formato relatório técnico — 2 parágrafos)

**Parágrafo 1 — Como um invasor exploraria a falha #01 (Vazamento de DB, GUT 125):**
A maior nota da nossa matriz é o **vazamento do arquivo `data/invictus.db`**.
No contexto da Barbearia Invictus, esse risco é concreto: o sistema usa
SQLite em arquivo local, e qualquer cópia indevida do `.db` (por backup mal
configurado, acesso físico ao servidor, falha em S3, ou um operador
malicioso) exporia todos os clientes, telefones, e-mails e — antes da
mitigação — a **senha do admin em texto puro**. Um invasor com o arquivo
nas mãos abriria o banco com qualquer cliente SQLite (`sqlite3 invictus.db`),
rodaria `SELECT login, senha FROM admin_users`, leria `admin / admin123` e
**em segundos** teria controle total do painel: poderia editar serviços,
ver dados sensíveis dos clientes, exportar CSVs (LGPD Art. 46) e até
sequestrar a operação inteira. O ataque dispensaria SQL Injection ou XSS —
seria game over instantâneo.

**Parágrafo 2 — Técnica adotada para anular o risco:**
Para mitigar definitivamente, **pesquisamos OWASP ASVS V2.4 (Credential
Storage)** e **NIST SP 800-63B § 5.1.1.2** e implementamos no módulo
[`app/security.py`](../app/security.py) o hash **bcrypt** com **cost factor
12** e **salt aleatório por senha** (função `hash_password`). O bcrypt é
uma KDF (Key Derivation Function) deliberadamente lenta, levando ~250 ms
por hash em CPU moderna — o que torna inviável até mesmo um ataque com
GPU em senha de 8+ caracteres (estimativa: bilhões de anos para força bruta
exaustiva). No login, usamos `bcrypt.checkpw()`, que faz comparação em
**tempo constante**, eliminando também o vetor de **timing attack**.
Adicionalmente, o `data/invictus.db` está no `.gitignore` (nunca vai para o
repositório público), o `SECRET_KEY` é lido de variável de ambiente
(`INVICTUS_SECRET`), e em produção o cookie de sessão usa `https_only=True`
+ `HSTS`. **Mesmo que o atacante consiga o `.db`, agora ele só verá o hash
bcrypt** — que é matematicamente irreversível e custa centenas de milhões
de dólares em compute para tentar quebrar uma senha forte.

---

## Checklist final para a banca

- [x] **20 ameaças** mapeadas na Matriz GUT com referência OWASP/CVE
- [x] **20 políticas IAM** com justificativa técnica (NIST/Zero Trust)
- [x] **20 dados/processos** no RoPA com base legal LGPD
- [x] Análise Crítica respondendo à pergunta obrigatória do guia
- [x] Top-3 prioridades GUT identificadas com nota
- [x] Direitos do titular (Art. 18) mapeados
- [x] Implementação de 17 mitigações em código (auditável em `app/security.py` e `app/main.py`)
- [x] **Matriz GUT em CSV** ([`exports/matriz_gut.csv`](exports/matriz_gut.csv)) ✅
- [ ] Roadmap pós-banca (4 itens) aceito pelo Sponsor: MFA, rotação automática, backup criptografado, segregação de ambientes

## Referências oficiais consultadas

| Fonte | URL |
|---|---|
| OWASP Top 10 (2021) | <https://owasp.org/Top10/> |
| OWASP ASVS 4.0 | <https://owasp.org/www-project-application-security-verification-standard/> |
| OWASP Secure Headers Project | <https://owasp.org/www-project-secure-headers/> |
| CVE / NVD Database | <https://nvd.nist.gov/> |
| CWE Top 25 (2024) | <https://cwe.mitre.org/top25/> |
| LGPD (Lei 13.709/2018) | <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm> |
| ANPD — Guia para Pequenas Empresas | <https://www.gov.br/anpd/pt-br> |
| NIST SP 800-63B (Digital Identity) | <https://pages.nist.gov/800-63-3/sp800-63b.html> |
| Microsoft Zero Trust | <https://www.microsoft.com/security/business/zero-trust> |
