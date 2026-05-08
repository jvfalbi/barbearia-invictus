# Gestão de Equipe — "Quem fez o quê"

> ⚠️ Exigência explícita do guia oficial:
>
> *"Para grupos acima de 3 pessoas, não descrever o que cada integrante
> desenvolveu no projeto"* aparece como **erro que reduz a nota**.
>
> Este documento detalha individualmente as entregas de cada um dos
> 4 integrantes, em formato auditável (cada item aponta para o arquivo
> ou commit no GitHub).

---

## Resumo executivo

| Integrante | Papel | Disciplina principal | Horas estimadas |
|---|---|---|--:|
| **João Vitor Falbi** | Gerente de Projeto + Backend | D1 (Gestão) | 120 h |
| **Calebe Fernandes Ramos** | Cientista de Dados | D2 (Análise de Dados) | 50 h |
| **Diego Lima Dantas** | Especialista em Segurança | D3 (Segurança) | 55 h |
| **Guilherme Camelo Pimenta** | Pesquisador Operacional | D4 (Pesquisa Operacional) | 45 h |
| | | **Total:** | **270 h** |

---

## João Vitor Falbi — Gerente de Projeto + Backend

### Disciplina 1 — Gestão de Projetos (R/A em todos os entregáveis)

| Entregável | Arquivo |
|---|---|
| 1.1 Termo de Abertura (TAP / Project Charter) | `docs/d1_gestao/1.1_tap.md` |
| 1.2 Estrutura Analítica (EAP / WBS) | `docs/d1_gestao/1.2_eap.md` (com Mermaid) |
| 1.3 Matriz RACI | `docs/d1_gestao/1.3_matriz_raci.md` + XLSX colorido |
| 1.4 Cronograma Gantt | `docs/d1_gestao/1.4_cronograma.md` (com Mermaid) |
| 1.5 Custos (R$ 28.187,50) | `docs/d1_gestao/1.5_custos.md` + XLSX |
| 1.6 Riscos + **Análise Crítica da Gestão** | `docs/d1_gestao/1.6_riscos.md` |
| 1.7 Plano de Comunicação | `docs/d1_gestao/1.7_comunicacao.md` |
| 1.8 Backlog Ágil (18 User Stories) | `docs/d1_gestao/1.8_backlog.md` |
| 4 Atas de Reunião | `docs/d1_gestao/atas/*.md` |

### Backend FastAPI

| Entregável | Arquivo |
|---|---|
| Modelos SQLAlchemy (Cliente, Barbeiro, Serviço, Produto, AdminUser, AuditLog) | `app/models.py` |
| Seed de dados iniciais | `app/seed.py` |
| Rotas públicas (home, agendar, produtos, privacidade) | `app/main.py` |
| Rotas administrativas (CRUD completo + dashboard) | `app/main.py` |
| Endpoints de exportação CSV (consumidos por D2) | `app/main.py` |
| Templates Jinja2 (16 páginas) | `app/templates/` |
| Tema CSS dark da Barbearia | `app/static/style.css` |
| Script de geração de artefatos | `scripts/gerar_artefatos.py` |

### Entregáveis acessórios

- README do projeto (raiz)
- Estrutura ABNT do PDF final (`docs/entrega_final/pdf_estrutura_abnt.md`)
- Roteiro do vídeo de apresentação
- PDF consolidado da banca

---

## Calebe Fernandes Ramos — Cientista de Dados

### Disciplina 2 — Análise de Dados (R/A)

| Entregável | Arquivo |
|---|---|
| Documento técnico D2 | `docs/d2_dados.md` |
| Notebook 01 — ETL + 3 KPIs + 4 métodos estatísticos | `notebooks/01_etl_e_kpis.ipynb` |
| Justificativa textual de cada KPI ligado ao Objetivo SMART | idem § 3 |
| Análise estatística: descritiva, distribuição, Pearson, Spearman | idem § 4 |
| Notebook 02 — 8 gráficos analíticos (matplotlib + seaborn) | `notebooks/02_visualizacoes.ipynb` |
| Análise Crítica respondendo à pergunta obrigatória do guia | idem § 6 |
| 8 PNGs dos gráficos exportados | `notebooks/figs/*.png` |

### Contribuições cruzadas

- **C** (Consulted) na modelagem do banco SQLAlchemy junto com João — definiu campos necessários para os KPIs antes do desenvolvimento.
- **C** na configuração dos endpoints `/admin/export/*.csv` — especificou colunas e formatos.

---

## Diego Lima Dantas — Especialista em Segurança

### Disciplina 3 — Segurança da Informação (R/A)

| Entregável | Arquivo |
|---|---|
| Documento técnico D3 | `docs/d3_seguranca.md` |
| Matriz GUT — 20 ameaças com referência OWASP/CVE | idem § 3.1 |
| 20 políticas IAM com justificativa NIST/Zero Trust | idem § 3.2 |
| RoPA com 20 dados + base legal LGPD | idem § 3.3 |
| Análise Crítica D3 (vulnerabilidade de maior nota GUT) | idem § 3.4 |
| Matriz GUT em CSV (ordenada por nota) | `docs/exports/matriz_gut.csv` |

### Implementação técnica em código

| Mitigação | Arquivo |
|---|---|
| Hash bcrypt cost 12 + salt aleatório | `app/security.py: hash_password()` |
| Rate-limit + lockout (5 falhas / 15 min) | `app/security.py: registrar_falha()` |
| Cabeçalhos HTTP (CSP, HSTS, X-Frame-Options, etc.) | `app/security.py: SECURITY_HEADERS` |
| Audit log de toda ação admin | `app/main.py: _audit()` |
| Cookie de sessão `HttpOnly` + `SameSite=Lax` | `app/main.py: SessionMiddleware` |
| Política de privacidade pública | `app/templates/privacidade.html` |
| Consentimento LGPD obrigatório no agendamento | `app/main.py: agendar_create()` |
| Endpoint de anonimização de dados | `app/main.py: lgpd_excluir()` |

---

## Guilherme Camelo Pimenta — Pesquisador Operacional

### Disciplina 4 — Pesquisa Operacional (R/A)

| Entregável | Arquivo |
|---|---|
| Documento técnico D4 | `docs/d4_pesquisa_operacional.md` |
| Notebook 03 — Maximização de Lucro com PuLP | `notebooks/03_otimizacao_lucro.ipynb` |
| Modelagem matemática formal (variáveis, função objetivo, restrições) | idem § 1 |
| Análise What-If do Problema 1 (perda de 25% das horas) | idem § 3 |
| Notebook 04 — Minimização de Custo de Folha com PuLP | `notebooks/04_otimizacao_alocacao.ipynb` |
| Modelagem com variáveis binárias x_b,t | idem § 2 |
| Análise What-If do Problema 2 (sem o barbeiro mais barato) | idem § 4 |
| Análise Crítica consolidada (resposta à pergunta obrigatória) | `docs/d4_pesquisa_operacional.md` § 4.3 |

### Contribuições cruzadas

- **C** (Consulted) na revisão dos KPIs do Calebe — confirmou se os valores
  alimentariam corretamente o solver.
- **C** na ata da Sprint 2 — apresentou o status dos modelos PuLP.

---

## Atividades realizadas em conjunto pela equipe toda

| Atividade | Quem participa | Quando |
|---|---|---|
| Reunião de Kickoff com Sponsor | João + Calebe + Diego + Guilherme + Sponsor | 02/03/2026 |
| Validação de escopo com Prof. Felipe | João + Calebe + Diego + Guilherme | 13/03/2026 |
| Sprint Reviews quinzenais | João + Calebe + Diego + Guilherme + Sponsor | a cada 14 dias |
| **Sinal Verde com Prof. Felipe** | João + Calebe + Diego + Guilherme | 04/05/2026 |
| Testes manuais de aceitação (US-01 a US-18) | João + Calebe + Diego + Guilherme | 11–17/05/2026 |
| Gravação do vídeo de 10 min | João + Calebe + Diego + Guilherme | 11–17/05/2026 |
| Apresentação final | João + Calebe + Diego + Guilherme | 22/05/2026 |

---

## Auditabilidade

Toda contribuição individual pode ser verificada via:

```bash
git log --author="Calebe" --pretty=format:"%h %ad %s" --date=short
git log --author="Diego" --pretty=format:"%h %ad %s" --date=short
git log --author="Guilherme" --pretty=format:"%h %ad %s" --date=short
git log --author="João" --pretty=format:"%h %ad %s" --date=short
```

> Os commits do GitHub formam o registro auditável das entregas individuais
> ao longo das 11 semanas do projeto.
