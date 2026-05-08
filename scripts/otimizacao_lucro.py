"""
Disciplina 4 — Pesquisa Operacional
Problema 1: MAXIMIZAÇÃO DE LUCRO

Cenário (real para a Barbearia Invictus):
  A barbearia tem 4 barbeiros disponíveis no sábado, totalizando 40 horas
  produtivas no dia. Pode aceitar 3 tipos de pacote:
    - Corte simples       (30 min, lucro R$ 25)
    - Corte + Barba       (55 min, lucro R$ 45)
    - Pacote Premium      (90 min, lucro R$ 80)

Restrições:
  - Tempo total de barbeiros: 40h × 60min = 2400 min
  - Demanda máxima de premium: até 10 (limite de produtos como pigmentação)
  - Pelo menos 30% dos slots devem ser do tipo "corte simples"
    (compromisso comercial com fluxo de novos clientes)

Pergunta: quantos atendimentos de cada tipo aceitar para maximizar o lucro?

Inclui Análise de Cenário (What-If):
  E se 1 barbeiro adoecer? (-25% das horas)

Como rodar:
    python scripts/otimizacao_lucro.py
ou colar em célula do Google Colab.
"""

from __future__ import annotations

from pulp import (
    LpInteger,
    LpMaximize,
    LpProblem,
    LpStatus,
    LpVariable,
    PULP_CBC_CMD,
    lpSum,
    value,
)


def resolver(horas_disponiveis: int = 40, max_premium: int = 10) -> dict:
    """Constrói e resolve o modelo de PL inteiro."""

    minutos_total = horas_disponiveis * 60

    model = LpProblem("Max_Lucro_Sabado", LpMaximize)

    # Variáveis de decisão (quantidade de atendimentos por tipo)
    x_corte = LpVariable("Corte_Simples", lowBound=0, cat=LpInteger)
    x_combo = LpVariable("Corte_Barba", lowBound=0, cat=LpInteger)
    x_premium = LpVariable("Premium", lowBound=0, cat=LpInteger)

    # Função objetivo — lucro total
    model += 25 * x_corte + 45 * x_combo + 80 * x_premium, "Lucro_Total"

    # Restrição 1 — tempo total dos barbeiros
    model += 30 * x_corte + 55 * x_combo + 90 * x_premium <= minutos_total, "Restricao_Tempo"

    # Restrição 2 — limite de premium (insumos)
    model += x_premium <= max_premium, "Restricao_Premium"

    # Restrição 3 — pelo menos 30% dos atendimentos são corte simples
    model += x_corte >= 0.3 * (x_corte + x_combo + x_premium), "Restricao_Mix_Corte"

    model.solve(PULP_CBC_CMD(msg=False))

    return {
        "status": LpStatus[model.status],
        "horas_disponiveis": horas_disponiveis,
        "corte_simples": int(value(x_corte) or 0),
        "corte_barba": int(value(x_combo) or 0),
        "premium": int(value(x_premium) or 0),
        "lucro_total": float(value(model.objective) or 0.0),
    }


def imprimir(titulo: str, r: dict) -> None:
    print(f"\n--- {titulo} ---")
    print(f"  Status do solver  : {r['status']}")
    print(f"  Horas disponíveis : {r['horas_disponiveis']}h")
    print(f"  Corte simples     : {r['corte_simples']:3d} atendimentos")
    print(f"  Corte + Barba     : {r['corte_barba']:3d} atendimentos")
    print(f"  Premium           : {r['premium']:3d} atendimentos")
    print(f"  LUCRO TOTAL       : R$ {r['lucro_total']:,.2f}")


def main() -> None:
    print("=" * 70)
    print("Disciplina 4 — PO 1: Maximização de Lucro | Barbearia Invictus")
    print("=" * 70)

    base = resolver(horas_disponiveis=40)
    imprimir("CENÁRIO BASE — 4 barbeiros, dia inteiro", base)

    crise = resolver(horas_disponiveis=30)
    imprimir("WHAT-IF: 1 barbeiro adoeceu (30h disponíveis)", crise)

    perda = base["lucro_total"] - crise["lucro_total"]
    print(
        f"\n>>> IMPACTO DO IMPREVISTO: -R$ {perda:,.2f} de lucro "
        f"({(perda / base['lucro_total']) * 100:.1f}% do potencial)"
    )
    print(
        ">>> DECISÃO ESTRATÉGICA: o modelo recomenda priorizar Combo e Premium\n"
        "    (maior lucro/minuto) e ter 1 barbeiro reserva ou aceitar overbooking\n"
        "    controlado para mitigar o risco mapeado na Matriz GUT."
    )


if __name__ == "__main__":
    main()
