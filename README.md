# Barbearia Invictus — Projeto Integrador UNINOVE 2026

> Sistema de gestão de barbearia desenvolvido como **Projeto Prático em
> Desenvolvimento de Software** (UNINOVE 2026 — Disciplinas Integradas: Gestão de
> Projetos, Análise de Dados, Segurança da Informação e Pesquisa Operacional).
>
> 🚩 **Data limite oficial de entrega: 22/05/2026** (Fase 5 do guia oficial)
>
> 🟢 **Validação Sinal Verde com Prof. Felipe: 04/05/2026** (Fase 4 — obrigatória)

---

## 📌 Integrantes

| Nome | RA |
|---|---|
| João Vitor Falbi | _adicionar_ |
| _Outros integrantes_ | _adicionar_ |

> ⚠️ Atualizar com os RAs reais antes da entrega.

## 🏪 A Empresa

- **Nome:** Barbearia Invictus
- **Ramo:** Estética masculina — corte, barba e cuidados capilares
- **Localização:** São Paulo / SP
- **Modelo:** Atendimento presencial com agendamento digital + venda de produtos

## 🎯 O Problema

A Barbearia Invictus realizava todo o agendamento por WhatsApp e caderno físico,
gerando: (a) horários conflitantes para o mesmo barbeiro, (b) ausência de
histórico de clientes, (c) falta de controle de estoque dos produtos vendidos
e (d) impossibilidade de medir desempenho (faturamento, taxa de cancelamento,
serviço mais lucrativo). O projeto entrega um sistema web completo que resolve
essas quatro dores e ainda fornece dados para análise estatística e otimização.

## 📅 As 5 Fases oficiais do Projeto (guia do Prof. Felipe)

| Fase | Período | Entregas |
|:-:|---|---|
| **F1** Setup | 02/mar — 15/mar/2026 | Repositório GitHub + README inicial + validação de escopo |
| **F2** Planejamento + Paralelo | 16/mar — 05/abr/2026 | TAP, EAP, RACI, Gantt + início de D2/D3/D4 em paralelo |
| **F3** Execução / Mão na Massa | 06/abr — 26/abr/2026 | Custos, Riscos, KPIs, GUT, Modelos PuLP completos |
| **F4** ⚠️ Validação **"Sinal Verde"** | 27/abr — 10/mai/2026 | Reunião com Prof. Felipe + ajustes solicitados |
| **F5** 🚩 Entrega Final | 11/mai — **22/mai/2026** | PDF ABNT + vídeo 10 min + repositório público |

> Detalhes do cronograma com dependências e caminho crítico em [`docs/d1_gestao/1.4_cronograma.md`](docs/d1_gestao/1.4_cronograma.md).
>
> **Pacote da entrega final** (PDF, vídeo, checklist) em [`docs/entrega_final/`](docs/entrega_final/).

## 🧩 Cobertura das 4 Disciplinas

| Disciplina | Documentação principal | Artefatos prontos para a banca |
|---|---|---|
| **D1 — Gestão de Projetos** | [`docs/d1_gestao/`](docs/d1_gestao/) — TAP, EAP, RACI, Gantt, Custos, Riscos+**Análise Crítica**, Comunicação, Backlog Ágil + 4 Atas | [`matriz_raci.xlsx`](docs/d1_gestao/exports/matriz_raci.xlsx) · [`custos.xlsx`](docs/d1_gestao/exports/custos.xlsx) · [`board_kanban.png`](docs/d1_gestao/exports/board_kanban.png) · diagramas Mermaid (EAP+Gantt) |
| **D2 — Análise de Dados** | [`docs/d2_dados.md`](docs/d2_dados.md) + 2 notebooks Jupyter | [`notebooks/figs/`](notebooks/figs/) com **8 PNGs** dos gráficos · notebooks executados com saídas preservadas |
| **D3 — Segurança da Informação** | [`docs/d3_seguranca.md`](docs/d3_seguranca.md) — 20 GUT + 20 IAM + 20 RoPA + Análise Crítica | `app/security.py` · audit log em `/admin/auditoria` · [`matriz_gut.csv`](docs/exports/matriz_gut.csv) |
| **D4 — Pesquisa Operacional** | [`docs/d4_pesquisa_operacional.md`](docs/d4_pesquisa_operacional.md) + 2 notebooks Jupyter (PuLP, sem Excel Solver) | [`03_otimizacao_lucro.ipynb`](notebooks/03_otimizacao_lucro.ipynb) · [`04_otimizacao_alocacao.ipynb`](notebooks/04_otimizacao_alocacao.ipynb) com What-If executado |

### Cobertura ponto-a-ponto dos guias oficiais

| Item exigido pelo guia | Status | Onde |
|---|:-:|---|
| 1.1 TAP com Objetivos SMART + Escopo IN/OUT + Stakeholders | ✅ | `docs/d1_gestao/1.1_tap.md` |
| 1.2 EAP até Nível 3 (texto + diagrama Mermaid) | ✅ | `docs/d1_gestao/1.2_eap.md` |
| 1.3 Matriz RACI com R/A/C/I | ✅ | 33 linhas em `1.3_matriz_raci.md` + XLSX colorido |
| 1.4 Cronograma Gantt com dependências + caminho crítico | ✅ | Mermaid em `1.4_cronograma.md` |
| 1.5 Custos com contingência (10%) | ✅ | R$ 28.187,50 em `1.5_custos.md` + XLSX |
| 1.6 Matriz de Riscos + ⚠️ **Análise Crítica da Gestão** (caixa amarela) | ✅ | 10 riscos em `1.6_riscos.md` |
| 1.7 Plano de Comunicação | ✅ | `1.7_comunicacao.md` |
| 1.8 Backlog do Produto Ágil (User Stories) | ✅ | 18 stories em `1.8_backlog.md` |
| Atas de Reunião (Kickoff + Sprints + Sinal Verde) | ✅ | 4 atas em `atas/` |
| ETL pandas + 3 KPIs **justificados** ligados ao SMART | ✅ | `notebooks/01_etl_e_kpis.ipynb` |
| 3+ métodos estatísticos | ✅ | 4 métodos: descritiva + skew/curtose + Pearson + Spearman |
| Visualizações matplotlib/seaborn | ✅ | **8 de 10** gráficos do guia |
| Análise Crítica D2 (pergunta obrigatória) | ✅ | `notebooks/01_etl_e_kpis.ipynb` § 6 |
| Matriz GUT — 20 ameaças OWASP/CVE | ✅ | `docs/d3_seguranca.md` § 3.1 |
| 20 políticas IAM (NIST/Zero Trust) | ✅ | `docs/d3_seguranca.md` § 3.2 |
| RoPA com 20 dados + base legal LGPD | ✅ | `docs/d3_seguranca.md` § 3.3 |
| Análise Crítica D3 (pergunta obrigatória sobre maior GUT) | ✅ | `docs/d3_seguranca.md` § 3.4 |
| Otimização linear PuLP — maximização lucro + What-If | ✅ | `notebooks/03_otimizacao_lucro.ipynb` |
| Otimização linear PuLP — minimização custo + What-If | ✅ | `notebooks/04_otimizacao_alocacao.ipynb` |
| **Notebooks executados com saídas preservadas** (exigência Colab/Jupyter) | ✅ | Todos rodados via `jupyter nbconvert --execute` |
| Proibição de Excel Solver | ✅ | Apenas PuLP é usado em todo o projeto |

## 🚀 Como rodar

```bash
# 1. Criar ambiente virtual
python -m venv .venv
.\.venv\Scripts\activate         # Windows
# source .venv/bin/activate      # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Subir o servidor
uvicorn app.main:app --reload
```

Acessar em <http://127.0.0.1:8000>.

**Acesso administrativo:** `admin` / `admin123` (senha armazenada como hash bcrypt).

## 🗂️ Estrutura

```
barbearia-invictus/
├── app/
│   ├── main.py             # rotas FastAPI (público + admin + LGPD + export)
│   ├── models.py           # SQLAlchemy: Cliente, Barbeiro, Servico, Produto, AdminUser, AuditLog
│   ├── security.py         # bcrypt, rate-limit, security headers (D3)
│   ├── seed.py             # dados iniciais (admin, barbeiros, serviços, produtos)
│   ├── database.py         # SQLite local
│   ├── templates/          # Jinja2 (index, agendar, produtos, admin/*, privacidade, lgpd)
│   └── static/style.css
├── notebooks/                    # ★ formato Jupyter/Colab (exigência do guia)
│   ├── 01_etl_e_kpis.ipynb       # D2: ETL + 3 KPIs + estatística
│   ├── 02_visualizacoes.ipynb    # D2: 6 gráficos (matplotlib + seaborn)
│   ├── 03_otimizacao_lucro.ipynb # D4: PL maximização (PuLP)
│   └── 04_otimizacao_alocacao.ipynb # D4: PL minimização (PuLP)
├── scripts/                      # versão .py equivalente (mesma lógica)
├── docs/
│   └── d3_seguranca.md     # Matriz GUT, IAM, RoPA-LGPD
├── requirements.txt
└── README.md
```

## 🔐 Compliance & Segurança

- Senha armazenada como **hash bcrypt** (custo 12, com salt automático).
- **Rate-limiting** no login (5 tentativas / 15 min, lockout 15 min).
- **Cabeçalhos HTTP de segurança**: CSP, X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy, Permissions-Policy.
- **SameSite cookies** (mitigação CSRF).
- **Audit log** de todas as ações administrativas com IP e timestamp.
- **LGPD**: consentimento explícito no agendamento, política de privacidade pública, endpoint de anonimização (`/lgpd/meus-dados`).
- **ORM SQLAlchemy** com queries parametrizadas (mitiga SQL Injection).

Detalhes técnicos completos em `docs/d3_seguranca.md`.

## 📊 Como usar os notebooks (D2 e D4)

O guia oficial da disciplina **exige execução em Jupyter Notebook ou Google
Colab** — por isso a entrega oficial está em `notebooks/`.

### Opção A — Google Colab (recomendado para a entrega)

1. Acesse <https://colab.research.google.com>
2. Faça **Upload notebook** e selecione cada `.ipynb` da pasta `notebooks/`
3. (Opcional) Faça upload do CSV exportado em `/admin/export/agendamentos.csv`
   para o ambiente do Colab — se não enviar, o notebook gera amostra sintética
4. Rode as células de cima para baixo (`Runtime → Run all`)

### Opção B — Jupyter local

```bash
pip install jupyter
jupyter notebook notebooks/
```

### Ordem de execução

| # | Notebook | Disciplina |
|---|---|---|
| 1 | `01_etl_e_kpis.ipynb` | D2 — ETL + KPIs + estatística |
| 2 | `02_visualizacoes.ipynb` | D2 — 8 gráficos analíticos |
| 3 | `03_otimizacao_lucro.ipynb` | D4 — Maximização de lucro (PuLP) |
| 4 | `04_otimizacao_alocacao.ipynb` | D4 — Minimização de custo (PuLP) |

> Para gerar dados reais antes: faça login em `/admin/login` e baixe os CSVs em
> `/admin/export/agendamentos.csv`, `produtos.csv`, `servicos.csv`.

## 🛠️ Regenerar todos os artefatos (1 comando)

Para reproduzir os PNGs dos gráficos, planilhas Excel/CSV e o board Kanban:

```bash
.\.venv\Scripts\python.exe scripts\gerar_artefatos.py
```

O script gera:
- `notebooks/figs/*.png` — 8 gráficos da D2
- `docs/d1_gestao/exports/matriz_raci.{csv,xlsx}` — Matriz RACI colorida
- `docs/d1_gestao/exports/custos.{csv,xlsx}` — Orçamento total R$ 28.187,50
- `docs/d1_gestao/exports/board_kanban.png` — Board Kanban (snapshot Sprint 3)
- `docs/exports/matriz_gut.csv` — Matriz GUT ordenada por nota

Para re-executar os notebooks com as saídas preservadas (importante para a banca):

```bash
cd notebooks
..\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace 01_etl_e_kpis.ipynb 02_visualizacoes.ipynb 03_otimizacao_lucro.ipynb 04_otimizacao_alocacao.ipynb
```

## ✅ Status final da entrega

Tudo o que pode ser automatizado pelo agente está pronto. **O que ainda
depende de ação humana:**

| O que falta | Responsável | Prazo |
|---|---|---|
| Imprimir TAP + 4 atas e coletar **assinatura física do Sponsor** | João Falbi | até a banca |
| Tirar **print do e-mail real** com pauta antes de cada Sprint Review | João Falbi | a cada sprint |
| **Reunião Sinal Verde com Prof. Felipe** + preencher `ata_sinal_verde.md` | Equipe | 04/05/2026 |
| **Aplicar ajustes** solicitados pelo Prof. Felipe | Equipe | até 10/05/2026 |
| **Compilar PDF em ABNT** seguindo `docs/entrega_final/pdf_estrutura_abnt.md` | João Falbi | até 17/05/2026 |
| **Gravar vídeo de 10 min** seguindo `docs/entrega_final/roteiro_video.md` | Equipe toda | até 17/05/2026 |
| **Testar links em janela anônima** (PDF + vídeo + repo) | João Falbi | até 21/05/2026 |
| 🚩 **Submeter PDF + vídeo** ao Prof. Felipe | João Falbi | **22/05/2026** |

> Checklist completo da entrega: [`docs/entrega_final/checklist_entrega.md`](docs/entrega_final/checklist_entrega.md)
