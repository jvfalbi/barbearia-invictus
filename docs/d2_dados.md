# Disciplina 2 — Análise de Dados

> Documento técnico que **conecta cada exigência do guia oficial** da D2
> aos arquivos do projeto, espelhando o formato de `docs/d3_seguranca.md`.

---

## 0. Aviso obrigatório do guia

> *"Todos os códigos Python desta disciplina **devem ser testados e executados
> no Google Colab ou Jupyter Notebook**. O código funcional e os resultados
> gerados por ele serão avaliados junto com a documentação."*

✅ **Cumprido:** todo código D2 está em formato `.ipynb` na pasta
[`notebooks/`](../notebooks/) — não em scripts soltos.

---

## 2.1 Tratamento de Dados (ETL) e Justificativa dos KPIs

### Pipeline ETL implementado

| Etapa | O que faz | Onde está |
|---|---|---|
| **Extração** | Lê o CSV exportado do sistema (`/admin/export/agendamentos.csv`) | `notebooks/01_etl_e_kpis.ipynb` § 1 |
| **Limpeza** | `dropna` em campos críticos, `to_datetime(errors='coerce')`, normalização de preço (R$, vírgula, milhar) | `notebooks/01_etl_e_kpis.ipynb` § 2 |
| **Carga (features derivadas)** | `mes`, `dia_semana`, `receita`, `foi_cancelado` | `notebooks/01_etl_e_kpis.ipynb` § 2 |

### Os 3 KPIs e sua justificativa em texto

| KPI | Justificativa (resumida) | Objetivo SMART do TAP |
|---|---|---|
| **Receita realizada (R$)** | KPI financeiro principal. Sem ele, o Sponsor não consegue medir sucesso de O3 e O4 do TAP. Também usado como validação para o solver de D4. | **O4** — Aumentar ticket médio em 15% |
| **Taxa de cancelamento (%)** | Mapeia diretamente o problema central identificado no kickoff (overbooking + WhatsApp manual). Justifica todo o escopo IN do TAP (lembrete + confirmação online). | **O1** — Reduzir cancelamentos para < 10% |
| **Ticket médio (R$)** | Mede saúde de precificação. Em queda = perda de margem. Conecta-se à página `/produtos` (venda casada para elevar este número). | **O4** — Aumentar ticket médio em 15% |

> Justificativa textual completa por KPI (1 parágrafo cada) está no
> `notebooks/01_etl_e_kpis.ipynb` § 3.

---

## 2.2 Métodos Estatísticos Essenciais

> O guia exige **pelo menos 3 conceitos estatísticos descritivos**. Aplicamos **4**.

| Conceito | Implementação | Onde |
|---|---|---|
| 1. **Descritiva básica** (média, mediana, desvio padrão, mín, máx) | `pd.describe()` + tabela manual | `01_etl_e_kpis.ipynb` § 4.1 |
| 2. **Distribuição** (assimetria + curtose) | `scipy.stats.skew()` + `kurtosis()` | `01_etl_e_kpis.ipynb` § 4.2 |
| 3. **Correlação Pearson** (linear) | `scipy.stats.pearsonr()` | `01_etl_e_kpis.ipynb` § 4.3 |
| 4. **Correlação Spearman** (monotônica) | `scipy.stats.spearmanr()` | `01_etl_e_kpis.ipynb` § 4.3 |

> Fizemos os **dois métodos de correlação** porque Pearson exige relação
> linear e Spearman é robusto a outliers — comparar os dois é boa prática.

---

## 2.3 Visualização de Dados — 8 dos 10 gráficos do guia

| # | Gráfico | Implementado? | Pergunta de negócio respondida |
|---|---|:-:|---|
| 1 | Barras | ✅ | Quem é o barbeiro mais rentável? |
| 2 | Linhas | ✅ | A demanda está crescendo ou caindo? |
| 3 | Dispersão (scatter) | ✅ | Duração × preço estão correlacionados? |
| 4 | Histograma | ✅ | Onde se concentram os preços? |
| 5 | Boxplot | ✅ | Há atendimentos com preço atípico (outliers)? |
| 6 | Donut (Pizza) | ✅ | Composição de status (concluído/cancelado/confirmado)? |
| 7 | Heatmap | ✅ | Correlações entre métricas numéricas |
| 8 | Pareto (80/20) | ✅ | Quais serviços concentram 80% da receita? |
| 9 | Violino | ❌ não usado | (boxplot + histograma já cobrem distribuição) |
| 10 | Cascata (Waterfall) | ❌ não usado | (não há fluxo financeiro multi-etapa para representar) |

> O guia diz: *"não é necessário usar todos, mas devem escolher os que
> melhor explicam o problema da empresa"*. **8 dos 10** é mais que suficiente
> e cobre toda a paleta analítica (comparação, tendência, correlação,
> distribuição, outliers, composição e concentração).

**Bibliotecas usadas:** `matplotlib` + `seaborn` (ambas exigidas pelo guia).

---

## 2.4 Análise Crítica Exigida (Conexão com a Etapa 1)

> ⚠️ **Pergunta obrigatória do guia (transcrita literalmente):**
>
> *"Baseado nas correlações estatísticas, nos outliers encontrados e no
> principal KPI calculado, qual é o maior gargalo operacional da empresa
> que vocês escolheram? Explique como esses dados numéricos justificam as
> metas e o escopo que o grupo definiu no Termo de Abertura (TAP) na
> Disciplina 1."*

A resposta completa em formato relatório técnico (2 parágrafos) está em:

- `notebooks/01_etl_e_kpis.ipynb` § 6 — Análise Crítica

**Resumo executivo da resposta:**

> O maior gargalo operacional é a **taxa de cancelamento de ~14,7%** (acima da
> meta de 10% do TAP), concentrada no serviço *Corte + Barba* (~60% dos
> cancelamentos identificados via boxplot). Pearson e Spearman entre duração
> e preço deram ≈ 1,0, o que **descarta problema de precificação** e aponta
> para o real gargalo: **falta de mecanismo de confirmação**. Esses números
> justificam o escopo IN do TAP (sistema online com lembrete automático)
> e o escopo OUT (sem mobile/sem gateway, pois o gargalo não está na venda).

---

## Como executar (passo a passo para a banca)

```bash
# 1. Subir o sistema e exportar dados reais
uvicorn app.main:app --reload
# em outro terminal, baixar o CSV (após login admin):
#   http://127.0.0.1:8000/admin/export/agendamentos.csv

# 2. Subir o CSV para o Colab ou rodar local com Jupyter
jupyter notebook notebooks/

# 3. Executar na ordem:
#    01_etl_e_kpis.ipynb  →  gera agendamentos_tratado.csv
#    02_visualizacoes.ipynb  →  consome o CSV tratado
```

> Caso o CSV real ainda não esteja disponível, os notebooks geram amostra
> sintética automaticamente — a banca pode rodar mesmo sem dados.

---

## Checklist final para a entrega

- [x] ETL funcional com pandas (limpeza + tipos + features)
- [x] 3 KPIs com **justificativa em texto** ligada aos Objetivos SMART do TAP
- [x] 4 métodos estatísticos (descritiva, distribuição, Pearson, Spearman)
- [x] 8 gráficos analíticos (matplotlib + seaborn)
- [x] Análise Crítica respondendo à pergunta obrigatória do guia
- [x] Notebooks `.ipynb` (não scripts `.py`)
- [x] **Notebooks executados com saídas preservadas** ✅ rodados via `jupyter nbconvert --execute`
- [x] **8 PNGs dos gráficos** exportados em [`notebooks/figs/`](../notebooks/figs/) ✅
