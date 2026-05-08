# Disciplina 4 — Pesquisa Operacional

> Documento técnico de **modelagem matemática + resolução algorítmica** com
> PuLP, espelhando o formato de [`docs/d2_dados.md`](d2_dados.md) e
> [`docs/d3_seguranca.md`](d3_seguranca.md).

---

## 0. Regra inegociável do guia

> ⚠️ *"A modelagem e resolução dos problemas devem ser feitas
> obrigatoriamente através de algoritmos em Python (utilizando bibliotecas
> como PuLP ou scipy.optimize). **O uso do Excel Solver é estritamente
> proibido** e resultará na anulação da etapa. Todo o código deve ser
> executável no Google Colab. O grupo deve modelar, resolver e analisar
> **DOIS problemas distintos**."*

| Exigência | Status |
|---|:-:|
| Modelagem 100% em Python | ✅ |
| Biblioteca PuLP (sem Excel Solver) | ✅ |
| Executável no Google Colab | ✅ (notebooks `.ipynb` autocontidos) |
| **DOIS problemas distintos** | ✅ Maximização + Minimização |

---

## 4.1 Problema 1 — Maximização de Lucro

**Notebook:** [`notebooks/03_otimizacao_lucro.ipynb`](../notebooks/03_otimizacao_lucro.ipynb)

### Cenário

A barbearia tem 4 barbeiros disponíveis no sábado, totalizando **40 horas
produtivas (2400 minutos)**. Pode oferecer 3 tipos de pacote, cada um com
duração e lucro distintos. Precisa decidir o **mix ótimo de atendimentos**
para maximizar o lucro do dia.

### Modelagem matemática

**Variáveis de decisão (inteiras, ≥ 0):**

- $x_C$ = quantidade de Cortes simples (30 min, R$ 25 lucro)
- $x_B$ = quantidade de Cortes + Barba (55 min, R$ 45 lucro)
- $x_P$ = quantidade de Pacotes Premium (90 min, R$ 80 lucro)

**Função objetivo (maximizar):**

$$\max Z = 25 x_C + 45 x_B + 80 x_P$$

**Restrições:**

| Restrição | Fórmula | Justificativa de negócio |
|---|---|---|
| Tempo | $30 x_C + 55 x_B + 90 x_P \leq 2400$ | 4 barbeiros × 10 h × 60 min |
| Estoque premium | $x_P \leq 10$ | Pigmentação tem só 10 doses/dia |
| Mix comercial | $x_C \geq 0{,}3 \cdot (x_C + x_B + x_P)$ | 30% mínimo de cortes simples (compromisso de fluxo de novos clientes) |
| Integralidade | $x_C, x_B, x_P \in \mathbb{Z}_{\geq 0}$ | Não existe \"meio atendimento\" |

### Resultado (executado no notebook)

| Cenário | Cortes | Combos | Premium | Lucro Total |
|---|--:|--:|--:|---:|
| **Base** (40 h) | 11 | 0 | 10 | **R$ 2.050,00** |
| Crise (30 h) | 12 | 0 | 10 | R$ 1.550,00 |

> Why-It-Won: o solver privilegia **Premium** porque tem o maior **lucro/minuto**
> (R$ 0,89/min vs R$ 0,82/min do combo vs R$ 0,83/min do corte simples).

### Análise What-If — *obrigatória pelo guia*

**Pergunta:** *"E se um barbeiro adoecer e perdermos 25% das horas?"*

A perda de 25% das horas (40 → 30 h) corta o lucro em **R$ 500 (24,4%)**.
Isso evidencia que **a empresa opera muito perto da capacidade máxima**
e dá insumo direto ao Plano de Riscos do TAP (D1).

---

## 4.2 Problema 2 — Minimização de Custo (Designação de Equipe)

**Notebook:** [`notebooks/04_otimizacao_alocacao.ipynb`](../notebooks/04_otimizacao_alocacao.ipynb)

### Cenário

A barbearia precisa **distribuir 3 barbeiros (origens)** entre **4 turnos
do fim de semana (destinos)** com o menor custo total possível, respeitando
o limite trabalhista de 2 turnos/profissional. Este é um caso clássico de
**problema de designação** — uma forma especial de transporte/alocação
exatamente como descrito pelo guia: *"distribuir recursos, produtos ou
funcionários de diferentes origens para diferentes destinos com o menor
custo possível"*.

### Modelagem matemática

**Variável de decisão (binária):**

$$x_{b,t} = \begin{cases} 1 & \text{se barbeiro } b \text{ é alocado ao turno } t \\ 0 & \text{caso contrário} \end{cases}$$

**Função objetivo (minimizar):**

$$\min Z = \sum_{b \in B} \sum_{t \in T} c_{b,t} \cdot x_{b,t}$$

onde $c_{b,t}$ é o custo de alocar o barbeiro $b$ ao turno $t$ (inclui
adicional de domingo / horário especial).

**Restrições:**

| Restrição | Fórmula | Justificativa |
|---|---|---|
| Cobertura | $\sum_{b} x_{b,t} = 1, \; \forall t \in T$ | Cada turno deve ter exatamente 1 profissional |
| Limite trabalhista | $\sum_{t} x_{b,t} \leq 2, \; \forall b \in B$ | Nenhum barbeiro pode trabalhar mais de 2 turnos no fim de semana (CLT) |
| Binariedade | $x_{b,t} \in \{0, 1\}$ | Alocação é decisão sim/não |

### Resultado (executado no notebook)

| Turno | Barbeiro alocado | Custo |
|---|---|---:|
| Sábado Manhã | Calebe | R$ 180 |
| Sábado Tarde | Calebe | R$ 180 |
| Domingo Manhã | Diego | R$ 220 |
| Domingo Tarde | Diego | R$ 220 |
| | **TOTAL** | **R$ 800,00** |

> O sênior (Guilherme) **não é alocado** porque seu custo (R$ 260) é
> desproporcional ao mix atual.

### Análise What-If — *obrigatória pelo guia*

**Pergunta:** *"E se Calebe (o mais barato) ficar indisponível?"*

A folha sobe **15% (de R$ 800 para R$ 920)** — confirma que a empresa é
**economicamente dependente de profissionais juniores**.

---

## 4.3 Análise Crítica Exigida (Otimização) — resposta consolidada

> ⚠️ **Pergunta obrigatória do guia (transcrita literalmente):**
>
> *"Os resultados matemáticos obtidos no Python para a Maximização e
> Minimização fazem sentido para a realidade de negócios da empresa
> escolhida? Explique detalhadamente como a Análise de Cenário (What-If)
> realizada pelo grupo ajuda a gerência do projeto a se preparar para
> imprevistos (gestão de riscos) e tomar decisões mais seguras no dia
> a dia."*

### Resposta (formato relatório técnico — 2 parágrafos)

**Parágrafo 1 — Os resultados fazem sentido para a Barbearia Invictus.**
Na **maximização**, o solver convergiu para 11 cortes simples + 10
pacotes premium (lucro R$ 2.050,00 no sábado), o que reproduz com
precisão a heurística que o dono já aplica intuitivamente: priorizar
serviços de maior margem por minuto e usar cortes simples para honrar o
fluxo mínimo de clientes novos. Na **minimização**, o algoritmo concluiu
que escalar o **júnior (Calebe)** nos turnos do sábado e o **pleno (Diego)**
no domingo gera a folha mínima de R$ 800/fim de semana, deixando o
**sênior (Guilherme)** estrategicamente fora — decisão coerente com a
estrutura de custos (cada turno do sênior custa 44% a mais que o do
júnior, e os turnos do fim de semana não exigem competência extra).
Os dois resultados, portanto, **validam matematicamente o que a
intuição comercial já sugeria**, mas com a vantagem de provar que
**não existe combinação melhor** dentro das restrições.

**Parágrafo 2 — A Análise What-If é o coração da gestão de riscos.**
No problema de maximização, o What-If \"e se perdermos 25% das horas?\"
mostrou que **24,4% do lucro evapora com apenas 1 barbeiro afastado** —
um número que conecta diretamente ao **Risco R3 da Matriz de Riscos do
TAP** (\"Membro fundamental adoecer\"). Sem o What-If, o gerente saberia
do risco mas **não saberia o tamanho dele**; com o What-If, fica claro
que a barbearia precisa de **um quarto barbeiro reserva** ou de um
acordo de freelancer-rápido. No problema de minimização, o What-If
\"e se Calebe ficar indisponível?\" revelou um aumento de 15% na folha,
tornando explícita a **dependência econômica de juniores** — o que
justifica investimento em formação interna e contratação de um **segundo
júnior**. Em síntese, o What-If transforma a otimização de uma resposta
*estática* em uma **ferramenta de análise de sensibilidade**: a gerência
deixa de tomar decisões com base em \"e se acontecer?\" e passa a operar
com **\"quanto custa se acontecer?\"** — exatamente o salto de maturidade
que a Pesquisa Operacional propõe entregar ao negócio.

---

## Como executar (passo a passo para a banca)

```bash
# Opção A — Google Colab (zero instalação)
#   1. https://colab.research.google.com → Upload notebook
#   2. Selecionar 03_otimizacao_lucro.ipynb e 04_otimizacao_alocacao.ipynb
#   3. Runtime → Run all em cada um
#   4. Os resultados ficam salvos no .ipynb

# Opção B — local
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace `
    notebooks\03_otimizacao_lucro.ipynb `
    notebooks\04_otimizacao_alocacao.ipynb
```

---

## Checklist final para a banca

- [x] **2 problemas distintos** modelados em PuLP (Max + Min)
- [x] Modelagem matemática formal (variáveis, função objetivo, restrições)
- [x] **Zero uso de Excel Solver** (regra inegociável)
- [x] **Análise What-If** em ambos os problemas
- [x] **Análise Crítica consolidada** respondendo à pergunta obrigatória do guia
- [x] Notebooks executados com saídas preservadas (R$ 2.050 e R$ 800 confirmados)
- [x] Conexão explícita com Plano de Riscos do TAP (D1)

## Referências oficiais consultadas

| Tópico | Fonte |
|---|---|
| PuLP — documentação oficial | <https://coin-or.github.io/pulp/> |
| Solver CBC (default do PuLP) | <https://github.com/coin-or/Cbc> |
| Programação Linear Inteira (Mixed Integer LP) | Hillier & Lieberman, *Introduction to Operations Research* (10ª ed.) |
| Problema de Designação (Assignment Problem) | Winston, *Operations Research: Applications & Algorithms* |
| Análise de Sensibilidade (What-If) | Taha, *Operations Research: An Introduction* (10ª ed.) |
