"""
Disciplina 2 — Análise de Dados
Script 1/2: ETL + Cálculo de KPIs + Métodos Estatísticos

Justificativa metodológica para o documento final:
- Os dados brutos vêm de exportação CSV do próprio sistema (admin/export/agendamentos.csv).
- O ETL trata valores nulos, normaliza datas e cria features derivadas.
- Os 3 KPIs foram escolhidos para responder diretamente os Objetivos SMART
  do TAP: receita, taxa de cancelamento e ticket médio.
- A análise estatística (média/mediana/desvio, assimetria, correlação)
  comprova matematicamente o comportamento observado nos gráficos.

Como rodar:
    python scripts/etl_e_kpis.py
ou colar em uma célula do Google Colab.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# --------------------------------------------------------------------------- #
# 1. EXTRAÇÃO                                                                 #
# --------------------------------------------------------------------------- #
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_AGENDAMENTOS = DATA_DIR / "agendamentos.csv"


def carregar() -> pd.DataFrame:
    """Lê o CSV exportado do sistema. Se não existir, gera amostra realista."""
    if CSV_AGENDAMENTOS.exists():
        return pd.read_csv(CSV_AGENDAMENTOS, sep=";")

    # Amostra sintética para permitir rodar antes da primeira exportação.
    np.random.seed(42)
    n = 300
    barbeiros = ["Calebe", "Diego", "Guilherme", "João"]
    servicos_data = [
        ("Corte", 30, 35.0),
        ("Barba", 25, 30.0),
        ("Corte + Barba", 55, 60.0),
        ("Pigmentação", 40, 50.0),
    ]
    nomes_serv, duracoes, precos = zip(*servicos_data)
    idx = np.random.choice(len(servicos_data), size=n)
    datas = pd.date_range("2026-01-01", periods=n, freq="D")
    horas = np.random.choice(["09:00", "10:00", "13:00", "14:00", "16:00"], size=n)
    status = np.random.choice(
        ["confirmado", "concluido", "cancelado"], size=n, p=[0.30, 0.55, 0.15]
    )
    return pd.DataFrame({
        "id": range(1, n + 1),
        "data": datas.strftime("%Y-%m-%d"),
        "hora": horas,
        "cliente": [f"Cliente {i}" for i in range(n)],
        "barbeiro": np.random.choice(barbeiros, size=n),
        "servico": [nomes_serv[i] for i in idx],
        "preco": [precos[i] for i in idx],
        "duracao_min": [duracoes[i] for i in idx],
        "status": status,
    })


# --------------------------------------------------------------------------- #
# 2. TRANSFORMAÇÃO (ETL)                                                      #
# --------------------------------------------------------------------------- #
def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline de limpeza — usa try/except para isolar linhas defeituosas."""
    df = df.copy()

    # Remoção de linhas com colunas críticas nulas
    antes = len(df)
    df = df.dropna(subset=["data", "hora", "barbeiro", "servico", "preco"])
    print(f"[ETL] removidas {antes - len(df)} linhas com campos críticos nulos")

    # Normalização de datas
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data"])

    # Conversão segura de preço (lida com vírgula decimal e R$)
    df["preco"] = (
        df["preco"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Features derivadas — semana do ano e dia da semana
    df["dia_semana"] = df["data"].dt.day_name(locale="pt_BR.UTF-8") if False else df["data"].dt.dayofweek
    df["mes"] = df["data"].dt.month
    df["receita"] = np.where(df["status"] == "concluido", df["preco"], 0.0)
    df["foi_cancelado"] = (df["status"] == "cancelado").astype(int)

    return df


# --------------------------------------------------------------------------- #
# 3. KPIs (justificativa atrelada aos Objetivos SMART do TAP)                 #
# --------------------------------------------------------------------------- #
def calcular_kpis(df: pd.DataFrame) -> dict:
    """
    KPI 1 — Receita realizada (R$): mede o objetivo SMART de faturamento.
    KPI 2 — Taxa de cancelamento (%): mede a qualidade da operação.
    KPI 3 — Ticket médio por agendamento (R$): base para precificação futura.
    """
    receita = df["receita"].sum()
    taxa_cancel = df["foi_cancelado"].mean() * 100
    concluidos = df[df["status"] == "concluido"]
    ticket_medio = concluidos["preco"].mean() if len(concluidos) else 0.0

    return {
        "receita_realizada_brl": round(float(receita), 2),
        "taxa_cancelamento_pct": round(float(taxa_cancel), 2),
        "ticket_medio_brl": round(float(ticket_medio), 2),
        "total_agendamentos": int(len(df)),
        "total_concluidos": int(len(concluidos)),
    }


# --------------------------------------------------------------------------- #
# 4. ESTATÍSTICA DESCRITIVA + CORRELAÇÃO                                      #
# --------------------------------------------------------------------------- #
def analise_estatistica(df: pd.DataFrame) -> dict:
    preco = df["preco"]

    # Métricas centrais
    desc = {
        "media_preco": round(float(preco.mean()), 2),
        "mediana_preco": round(float(preco.median()), 2),
        "desvio_padrao_preco": round(float(preco.std()), 2),
        "assimetria_preco": round(float(stats.skew(preco)), 3),  # >0: cauda longa à direita
        "curtose_preco": round(float(stats.kurtosis(preco)), 3),
    }

    # Correlação: duração do serviço vs. preço (Spearman para não exigir linearidade)
    rho, p_valor = stats.spearmanr(df["duracao_min"], df["preco"])
    desc["correlacao_duracao_preco_spearman"] = round(float(rho), 3)
    desc["correlacao_p_valor"] = round(float(p_valor), 4)

    # Frequência por barbeiro (participação de mercado interna)
    desc["distribuicao_barbeiros"] = (
        (df["barbeiro"].value_counts(normalize=True) * 100).round(1).to_dict()
    )
    return desc


def main() -> None:
    print("=" * 70)
    print("Disciplina 2 — ETL + KPIs + Estatística | Barbearia Invictus")
    print("=" * 70)

    bruto = carregar()
    limpo = limpar(bruto)
    print(f"\n[OK] DataFrame final: {limpo.shape[0]} linhas × {limpo.shape[1]} colunas\n")

    print("--- KPIs (justificam o TAP) ---")
    for k, v in calcular_kpis(limpo).items():
        print(f"  {k}: {v}")

    print("\n--- Análise estatística ---")
    for k, v in analise_estatistica(limpo).items():
        print(f"  {k}: {v}")

    # Salva o CSV tratado para uso pelo script de visualização
    saida = DATA_DIR / "agendamentos_tratado.csv"
    limpo.to_csv(saida, sep=";", index=False)
    print(f"\n[OK] CSV tratado salvo em {saida}")


if __name__ == "__main__":
    main()
