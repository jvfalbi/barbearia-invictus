# Estrutura do PDF Final (Normas ABNT)

> **Como usar:** copie o conteúdo abaixo para um **Google Docs** ou
> **Microsoft Word**, aplique as fontes/espaçamentos da ABNT (descritos
> ao final) e exporte como PDF.

---

## Estrutura obrigatória da ABNT

| Ordem | Elemento | Obrigatório? |
|:-:|---|:-:|
| 1 | **Capa** | ✅ Sim |
| 2 | Folha de rosto | ✅ Sim |
| 3 | Sumário | ✅ Sim |
| 4 | Resumo + palavras-chave | Recomendado |
| 5 | **1. Introdução** | ✅ Sim |
| 6 | 2. Disciplina 1 — Gestão de Projetos | ✅ Sim |
| 7 | 3. Disciplina 2 — Análise de Dados | ✅ Sim |
| 8 | 4. Disciplina 3 — Segurança da Informação | ✅ Sim |
| 9 | 5. Disciplina 4 — Pesquisa Operacional | ✅ Sim |
| 10 | 6. Conclusão | ✅ Sim |
| 11 | **Referências** (ABNT NBR 6023) | ✅ Sim |
| 12 | Apêndices (códigos, atas, prints) | Recomendado |

---

## Modelo da Capa (copiar tal qual)

```
                        UNIVERSIDADE NOVE DE JULHO — UNINOVE
                        ESCOLA DE TECNOLOGIA E INOVAÇÃO

                              Calebe Fernandes Ramos
                              Diego Lima Dantas
                              Guilherme Camelo Pimenta
                              João Vitor Falbi


                       BARBEARIA INVICTUS — PLATAFORMA DE
                       AGENDAMENTO, ESTOQUE E INTELIGÊNCIA
                                  DE NEGÓCIO

                Projeto Prático em Desenvolvimento de Software
                  (Disciplinas Integradas: Gestão de Projetos,
                  Análise de Dados, Segurança da Informação e
                              Pesquisa Operacional)



                                  São Paulo
                                     2026
```

---

## Modelo da Folha de Rosto

```
                              Calebe Fernandes Ramos    — RA: ______
                              Diego Lima Dantas         — RA: ______
                              Guilherme Camelo Pimenta  — RA: ______
                              João Vitor Falbi          — RA: ______


                   BARBEARIA INVICTUS — PLATAFORMA DE
                   AGENDAMENTO, ESTOQUE E INTELIGÊNCIA
                              DE NEGÓCIO


                    Trabalho apresentado ao Prof. Felipe ____,
                    do curso de _____________ da Universidade
                    Nove de Julho, como requisito parcial para
                    aprovação no Projeto Integrador 2026.

                    Orientador: Prof. Felipe _____________


                                 São Paulo
                                    2026
```

---

## Sumário (modelo)

```
1  INTRODUÇÃO ............................................... 5
1.1   A Empresa ............................................. 5
1.2   O Problema ............................................ 5
1.3   Objetivos do Projeto .................................. 6

2  DISCIPLINA 1 — GESTÃO DE PROJETOS ........................ 7
2.1   Termo de Abertura (Project Charter / TAP) ............. 7
2.2   Estrutura Analítica do Projeto (EAP / WBS) ............ 9
2.3   Matriz RACI .......................................... 11
2.4   Cronograma (Gantt) ................................... 13
2.5   Gestão de Custos ..................................... 15
2.6   Gestão de Riscos ..................................... 16
2.7   Plano de Comunicação ................................. 17
2.8   Backlog do Produto Ágil (User Stories) ............... 18
2.9   ⚠️ Análise Crítica Exigida (Gestão) .................. 20
2.10  Atas de Reunião ...................................... 21

3  DISCIPLINA 2 — ANÁLISE DE DADOS .......................... 23
3.1   Tratamento de Dados (ETL) ............................ 23
3.2   Justificativa dos 3 KPIs ............................. 24
3.3   Métodos Estatísticos ................................. 25
3.4   Visualizações (8 gráficos) ........................... 27
3.5   ⚠️ Análise Crítica Exigida (Dados) ................... 30

4  DISCIPLINA 3 — SEGURANÇA DA INFORMAÇÃO ................... 31
4.1   Matriz GUT (20 ameaças) .............................. 31
4.2   Políticas de IAM (20) ................................ 34
4.3   Adequação à LGPD — RoPA (20 dados) ................... 36
4.4   ⚠️ Análise Crítica Exigida (Segurança) ............... 38

5  DISCIPLINA 4 — PESQUISA OPERACIONAL ...................... 39
5.1   Problema 1 — Maximização de Lucro .................... 39
5.2   Problema 2 — Minimização de Custo .................... 41
5.3   Análise What-If ...................................... 43
5.4   ⚠️ Análise Crítica Exigida (Otimização) .............. 44

6  CONCLUSÃO ................................................ 43
6.1   Considerações finais ................................. 43
6.2   Lições aprendidas .................................... 43
6.3   Trabalhos futuros .................................... 43

   REFERÊNCIAS ............................................. 44
   APÊNDICES ............................................... 46
A   Atas de reunião (Kickoff, Sprints, Sinal Verde) ........ 46
B   Código-fonte do sistema (link GitHub) .................. 50
C   Notebooks Jupyter executados ........................... 50
D   Vídeo de apresentação (link) ........................... 51
```

---

## 1. INTRODUÇÃO (texto-modelo, ~1 página)

### 1.1 A Empresa

A **Barbearia Invictus** é uma microempresa do ramo de estética masculina,
localizada em São Paulo / SP, especializada em corte, barba e cuidados
capilares. Opera no formato presencial com agendamento digital e venda
complementar de produtos (pomadas, óleos, ceras).

### 1.2 O Problema

Antes deste projeto, todo o agendamento era feito por **WhatsApp e caderno
físico**, gerando: (a) conflitos de horário, (b) ausência de histórico
de clientes, (c) falta de controle de estoque e (d) impossibilidade de
medir desempenho (faturamento, taxa de cancelamento, ticket médio).
O dono perdia em média **2 h/dia** apenas em organização manual.

### 1.3 Objetivos

Construir um sistema web em FastAPI + SQLite + Jupyter Notebooks que:
1. Reduza a taxa de cancelamento para abaixo de 10%
2. Elimine conflitos de horário
3. Calcule KPIs operacionais
4. Atenda LGPD (consentimento + anonimização)
5. Otimize matematicamente a alocação de recursos (PuLP)

---

## 2 a 5 — Disciplinas (importar dos arquivos `docs/`)

> Cole o conteúdo dos arquivos abaixo na ordem (já formatados em Markdown,
> basta usar o Google Docs com a opção "**Importar Markdown**" ou copiar/colar):

| Capítulo | Origem |
|---|---|
| 2.1 | `docs/d1_gestao/1.1_tap.md` |
| 2.2 | `docs/d1_gestao/1.2_eap.md` |
| 2.3 | `docs/d1_gestao/1.3_matriz_raci.md` |
| 2.4 | `docs/d1_gestao/1.4_cronograma.md` |
| 2.5 | `docs/d1_gestao/1.5_custos.md` |
| 2.6 | `docs/d1_gestao/1.6_riscos.md` (matriz + caixa amarela) |
| 2.7 | `docs/d1_gestao/1.7_comunicacao.md` |
| 2.8 | `docs/d1_gestao/1.8_backlog.md` |
| 2.9 | seção "Análise Crítica Exigida" do `1.6_riscos.md` |
| 2.10 | `docs/d1_gestao/atas/*.md` (4 atas) |
| 3   | `docs/d2_dados.md` + notebooks `01_etl_e_kpis.ipynb` e `02_visualizacoes.ipynb` |
| 4   | `docs/d3_seguranca.md` |
| 5   | `docs/d4_pesquisa_operacional.md` + notebooks `03_otimizacao_lucro.ipynb` e `04_otimizacao_alocacao.ipynb` |

---

## ⚠️ As 4 Caixas Amarelas Obrigatórias (Análise Crítica Exigida)

> O template oficial do projeto exige **uma caixa amarela em cada disciplina**
> com uma pergunta analítica que precisa ser respondida no PDF final.
> **No Word/Docs, formate cada uma em quadro com fundo amarelo claro
> (`#FFF8DC`) e borda laranja (`#FFA500`) — exatamente como no exemplo
> oficial "TechBridge ERP".**

### Caixa 1 — Análise Crítica Exigida (Gestão) — Cap. 2.9

> **Pergunta:** *"Os custos alocados são realistas para suportar os riscos
> identificados? Explique como a adoção do framework ágil (Backlog) ajuda
> a mitigar o 'Risco 1' citado acima."*
>
> **Resposta:** copiar do final de [`docs/d1_gestao/1.6_riscos.md`](../d1_gestao/1.6_riscos.md)
> (seção "Análise Crítica Exigida (Gestão)").

### Caixa 2 — Análise Crítica Exigida (Dados) — Cap. 3.5

> **Pergunta:** *"Baseado nos gráficos acima e na Taxa de Cancelamento
> calculada, qual é o principal gargalo operacional da Barbearia Invictus?
> Como esses dados justificam a necessidade do 'Termo de Abertura' criado
> na Etapa 1?"*
>
> **Resposta:** copiar da seção final do notebook
> [`notebooks/01_etl_e_kpis.ipynb`](../../notebooks/01_etl_e_kpis.ipynb)
> ou de [`docs/d2_dados.md`](../d2_dados.md).

### Caixa 3 — Análise Crítica Exigida (Segurança) — Cap. 4.4

> **Pergunta:** *"Explique tecnicamente como a vulnerabilidade priorizada
> na Matriz GUT pode ser explorada no contexto específico do SEU projeto
> e quais medidas exatas de código ou infraestrutura mitigam esse risco."*
>
> **Resposta:** copiar da seção "Análise Crítica" de
> [`docs/d3_seguranca.md`](../d3_seguranca.md) (foco em Quebra de
> Autenticação / SQL Injection no `app/main.py`).

### Caixa 4 — Análise Crítica Exigida (Otimização) — Cap. 5.4

> **Pergunta:** *"Os resultados matemáticos obtidos no Python fazem sentido
> para a realidade de negócios da empresa? Explique como a Análise de Cenário
> (What-If) ajuda a gerência a se preparar para imprevistos e tomar decisões
> mais seguras."*
>
> **Resposta:** copiar da seção "Análise Crítica Consolidada" de
> [`docs/d4_pesquisa_operacional.md`](../d4_pesquisa_operacional.md).

---

## 6. CONCLUSÃO (texto-modelo)

O projeto Barbearia Invictus integrou as 4 disciplinas em uma solução
real, partindo de um problema operacional concreto e chegando a uma
plataforma funcional. A **Gestão de Projetos** garantiu que escopo,
prazo e custo fossem controlados; a **Análise de Dados** transformou
dados brutos em 3 KPIs que justificam decisões; a **Segurança da
Informação** mapeou 20 ameaças, definiu 20 políticas IAM e adequou
o sistema à LGPD; a **Pesquisa Operacional** modelou matematicamente
dois problemas (max lucro, min custo de folha) com o solver PuLP,
provando que a alocação ótima difere da intuição em ~24% no pior cenário
(análise What-If).

A maior lição do projeto foi perceber que **nenhuma disciplina, sozinha,
resolveria o problema da empresa**. Apenas a integração — backend seguro
+ KPIs confiáveis + otimização matemática + plano de projeto — gerou
valor mensurável: redução estimada de 14,7% para < 10% de cancelamentos
e potencial de R$ 500/mês recuperados.

---

## REFERÊNCIAS (ABNT NBR 6023:2018)

```
ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. NBR 14724: Informação e documentação
— Trabalhos acadêmicos — Apresentação. Rio de Janeiro: ABNT, 2011.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados
Pessoais (LGPD). Diário Oficial da União, Brasília, DF, 15 ago. 2018.
Disponível em: <http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>.
Acesso em: 22 maio 2026.

HILLIER, Frederick S.; LIEBERMAN, Gerald J. Introduction to Operations
Research. 10. ed. New York: McGraw-Hill, 2015.

NIST. Special Publication 800-63B: Digital Identity Guidelines. Gaithersburg:
National Institute of Standards and Technology, 2017. Disponível em:
<https://pages.nist.gov/800-63-3/sp800-63b.html>. Acesso em: 22 maio 2026.

OWASP FOUNDATION. OWASP Top 10 — 2021. Maryland: OWASP, 2021. Disponível em:
<https://owasp.org/Top10/>. Acesso em: 22 maio 2026.

PMI — PROJECT MANAGEMENT INSTITUTE. PMBOK Guide: A Guide to the Project
Management Body of Knowledge. 7. ed. Newtown Square: PMI, 2021.

PuLP — Optimization with Python. Documentation. Disponível em:
<https://coin-or.github.io/pulp/>. Acesso em: 22 maio 2026.

WINSTON, Wayne L. Operations Research: Applications and Algorithms.
4. ed. Belmont: Thomson Brooks/Cole, 2004.

McKINNEY, Wes. Python for Data Analysis: Data Wrangling with Pandas, NumPy,
and IPython. 3. ed. Sebastopol: O'Reilly Media, 2022.
```

---

## Configuração ABNT no Word/Docs

| Item | Valor |
|---|---|
| **Fonte do corpo** | Times New Roman ou Arial — **12 pt** |
| **Espaçamento entre linhas** | **1,5** |
| **Espaçamento de citações longas** | **1,0** (recuo 4 cm) |
| **Margens** | Superior 3 cm · Inferior 2 cm · Esquerda 3 cm · Direita 2 cm |
| **Papel** | A4 (210 × 297 mm) |
| **Numeração de páginas** | Canto superior direito a partir da introdução |
| **Títulos de capítulo** | Negrito, caixa alta, fonte 12 pt |
| **Subtítulos** | Negrito, sentence case, fonte 12 pt |
| **Alinhamento do corpo** | Justificado |
| **Recuo de parágrafo** | 1,25 cm na primeira linha |

---

## Apêndices (anexar)

| Apêndice | Conteúdo |
|---|---|
| **A** | 4 Atas de Reunião (Kickoff + Sprint 1 + Sprint 2 + Sinal Verde) — escaneadas com assinatura |
| **B** | Print/QR Code do repositório GitHub público |
| **C** | Notebooks `.ipynb` exportados como PDF (4 arquivos) |
| **D** | Link do vídeo de apresentação no YouTube/Drive (com permissão pública) |
| **E** | Print do board GitHub Projects (`docs/d1_gestao/exports/board_kanban.png`) |
| **F** | Planilhas RACI e Custos (`docs/d1_gestao/exports/*.xlsx`) |

---

## Como gerar o PDF final em 5 passos

1. **Abrir** Google Docs novo (ou Word)
2. **Aplicar** configuração ABNT acima (margens, fonte, espaçamento)
3. **Importar Markdown** dos arquivos listados na seção "2 a 5 — Disciplinas"
4. **Inserir** capa, folha de rosto, sumário automático e referências
5. **Exportar como PDF** → renomear para `Barbearia_Invictus_Entrega_Final_2026.pdf`

> Dica: o Google Docs tem "Inserir → Sumário" que gera automaticamente
> o sumário se você usar os estilos "Título 1", "Título 2", etc.
