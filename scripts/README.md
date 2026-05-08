# Scripts Auxiliares — Disciplinas 2 e 4

Esta pasta contém os scripts Python que **alimentam o documento final** das
disciplinas 2 (Análise de Dados) e 4 (Pesquisa Operacional) do Projeto de
Extensão UNINOVE.

> **Importante:** os requisitos do projeto exigem que estes scripts sejam
> executados em **Google Colab** ou **Jupyter Notebook**. Os arquivos `.py`
> aqui presentes são autocontidos — basta copiar o conteúdo de cada um
> para uma célula do notebook.

## Conteúdo

| Arquivo | Disciplina | Descrição |
|---|---|---|
| `etl_e_kpis.py` | D2 | ETL com `pandas`, cálculo de 3 KPIs e métodos estatísticos (média/mediana/desvio, distribuição, correlação Pearson). |
| `visualizacoes.py` | D2 | Gera 6 gráficos (barras, linhas, dispersão, histograma, boxplot, mapa de calor) com `matplotlib` + `seaborn`. |
| `otimizacao_lucro.py` | D4 | Maximização de lucro com `pulp` — quantos cortes vs. cortes+barba aceitar dadas as horas disponíveis. Inclui análise *what-if*. |
| `otimizacao_alocacao.py` | D4 | Minimização de custo com `pulp` — alocação de barbeiros aos horários do dia minimizando ociosidade. |

## Como usar

1. **Exporte os dados** do sistema em `/admin/export/agendamentos.csv` (e `produtos.csv`, `servicos.csv`).
2. Coloque os CSVs na pasta `scripts/data/`.
3. Abra o Google Colab → File → Upload notebook OU rode localmente:
   ```bash
   pip install pandas matplotlib seaborn scipy pulp
   python scripts/etl_e_kpis.py
   ```

## Decisões metodológicas

- **Por que pandas + scipy?** Padrão de mercado para análise tabular.
- **Por que PuLP em vez de scipy.optimize?** PuLP gera modelos de PL legíveis
  (variáveis e restrições parecem matemática), facilitando a explicação no
  documento ABNT. Atende à regra "proibido Excel Solver".
- **Por que dois problemas de PO distintos?** O guia da disciplina exige um
  problema de **maximização** (lucro) e um de **minimização** (custo).
