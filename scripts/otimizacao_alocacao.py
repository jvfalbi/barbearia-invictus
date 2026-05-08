"""
Disciplina 4 — Pesquisa Operacional
Problema 2: MINIMIZAÇÃO DE CUSTO (Problema de Transporte/Designação)

Cenário:
  A Barbearia Invictus precisa cobrir 4 turnos no fim de semana:
    - Sábado Manhã, Sábado Tarde, Domingo Manhã, Domingo Tarde
  Tem 3 barbeiros disponíveis (cada um pode trabalhar no máximo 2 turnos).
  Cada barbeiro tem um custo hora diferente (junior/pleno/sênior) e nem
  todos preferem todos os turnos (custo extra de adicional noturno etc.).

Objetivo:
  Atribuir barbeiros aos turnos minimizando o custo total da folha,
  garantindo que cada turno tenha exatamente 1 barbeiro alocado.

Inclui Análise de Cenário (What-If):
  E se o barbeiro mais barato (Calebe) ficar indisponível?

Como rodar:
    python scripts/otimizacao_alocacao.py
"""

from __future__ import annotations

from pulp import (
    LpBinary,
    LpMinimize,
    LpProblem,
    LpStatus,
    LpVariable,
    PULP_CBC_CMD,
    lpSum,
    value,
)

BARBEIROS_BASE = {
    # nome      : (custo_por_turno, turnos_max)
    "Calebe":    (180.0, 2),
    "Diego":     (220.0, 2),
    "Guilherme": (260.0, 2),
}

TURNOS = ["Sab_Manha", "Sab_Tarde", "Dom_Manha", "Dom_Tarde"]

# Adicionais por preferência: barbeiro X turno
ADICIONAL = {
    ("Calebe", "Dom_Tarde"): 40.0,
    ("Diego", "Sab_Manha"): 30.0,
    ("Guilherme", "Dom_Manha"): 50.0,
}


def custo(barbeiro: str, turno: str, base: float) -> float:
    return base + ADICIONAL.get((barbeiro, turno), 0.0)


def resolver(barbeiros: dict[str, tuple[float, int]]) -> dict:
    model = LpProblem("Min_Custo_Folha", LpMinimize)

    # Variável de decisão x_{b,t} ∈ {0,1} — 1 se barbeiro b cobre turno t
    x = {
        (b, t): LpVariable(f"x_{b}_{t}", cat=LpBinary)
        for b in barbeiros
        for t in TURNOS
    }

    # Função objetivo — custo total da folha
    model += lpSum(
        custo(b, t, barbeiros[b][0]) * x[(b, t)]
        for b in barbeiros
        for t in TURNOS
    ), "Custo_Total"

    # Restrição 1 — todo turno deve ter exatamente 1 barbeiro
    for t in TURNOS:
        model += lpSum(x[(b, t)] for b in barbeiros) == 1, f"Cobertura_{t}"

    # Restrição 2 — limite de turnos por barbeiro
    for b, (_, max_turnos) in barbeiros.items():
        model += lpSum(x[(b, t)] for t in TURNOS) <= max_turnos, f"Limite_{b}"

    model.solve(PULP_CBC_CMD(msg=False))

    escala = {
        t: next((b for b in barbeiros if value(x[(b, t)]) > 0.5), "—")
        for t in TURNOS
    }

    return {
        "status": LpStatus[model.status],
        "escala": escala,
        "custo_total": float(value(model.objective) or 0.0),
    }


def imprimir(titulo: str, r: dict) -> None:
    print(f"\n--- {titulo} ---")
    print(f"  Status: {r['status']}")
    for turno, barbeiro in r["escala"].items():
        print(f"    {turno:11s} -> {barbeiro}")
    print(f"  CUSTO TOTAL DA FOLHA: R$ {r['custo_total']:,.2f}")


def main() -> None:
    print("=" * 70)
    print("Disciplina 4 — PO 2: Minimização de Custo | Barbearia Invictus")
    print("=" * 70)

    base = resolver(BARBEIROS_BASE)
    imprimir("CENÁRIO BASE — 3 barbeiros disponíveis", base)

    sem_calebe = {b: v for b, v in BARBEIROS_BASE.items() if b != "Calebe"}
    # Aumenta o limite de turnos dos demais para suprir Calebe
    sem_calebe = {b: (v[0], 3) for b, v in sem_calebe.items()}
    crise = resolver(sem_calebe)
    imprimir("WHAT-IF: Calebe indisponível (somente 2 barbeiros)", crise)

    delta = crise["custo_total"] - base["custo_total"]
    print(
        f"\n>>> IMPACTO: a folha sobe R$ {delta:,.2f} "
        f"({(delta / base['custo_total']) * 100:.1f}%) sem o barbeiro mais barato.\n"
        ">>> DECISÃO ESTRATÉGICA: o modelo justifica manter pelo menos\n"
        "    um barbeiro júnior fixo na escala para reduzir custo de folha,\n"
        "    confirmando o objetivo SMART de gestão de custos do TAP."
    )


if __name__ == "__main__":
    main()
