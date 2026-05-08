"""
Disciplina 2 — Análise de Dados
Script 2/2: Visualizações (matplotlib + seaborn)

Gera 6 gráficos exigidos pela disciplina, salvos como PNG em scripts/figs/:
  1. Barras       — receita por barbeiro
  2. Linhas       — evolução diária de agendamentos
  3. Dispersão    — duração × preço
  4. Histograma   — distribuição de preços
  5. Boxplot      — preço por serviço (identifica outliers)
  6. Mapa de calor — correlações entre métricas numéricas

Pré-requisito: rodar antes `python scripts/etl_e_kpis.py` para gerar
o CSV tratado.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_DIR = Path(__file__).resolve().parent / "data"
FIGS_DIR = Path(__file__).resolve().parent / "figs"
FIGS_DIR.mkdir(exist_ok=True)

PALETTE = ["#dc2626", "#f59e0b", "#16a34a", "#3b82f6", "#9333ea"]
sns.set_theme(style="darkgrid", palette=PALETTE)


def carregar() -> pd.DataFrame:
    csv = DATA_DIR / "agendamentos_tratado.csv"
    if not csv.exists():
        raise SystemExit(
            f"ERRO: rode antes `python scripts/etl_e_kpis.py` para gerar {csv}"
        )
    df = pd.read_csv(csv, sep=";", parse_dates=["data"])
    return df


def fig_barras(df: pd.DataFrame) -> None:
    receita = df.groupby("barbeiro")["receita"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    receita.plot(kind="bar", color=PALETTE, ax=ax)
    ax.set_title("Receita realizada por barbeiro (R$)")
    ax.set_ylabel("R$")
    ax.set_xlabel("")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "01_barras_receita_barbeiro.png", dpi=120)
    plt.close()


def fig_linhas(df: pd.DataFrame) -> None:
    serie = df.groupby(df["data"].dt.date).size()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    serie.plot(ax=ax, color=PALETTE[0])
    ax.set_title("Evolução diária do volume de agendamentos")
    ax.set_ylabel("Agendamentos")
    ax.set_xlabel("Data")
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "02_linhas_volume_diario.png", dpi=120)
    plt.close()


def fig_dispersao(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x="duracao_min", y="preco", hue="servico", s=70, ax=ax)
    ax.set_title("Dispersão: Duração (min) × Preço (R$)")
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "03_dispersao_duracao_preco.png", dpi=120)
    plt.close()


def fig_histograma(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.histplot(df["preco"], bins=15, kde=True, color=PALETTE[0], ax=ax)
    ax.set_title("Distribuição de preços dos serviços")
    ax.set_xlabel("Preço (R$)")
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "04_histograma_precos.png", dpi=120)
    plt.close()


def fig_boxplot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="servico", y="preco", palette=PALETTE, ax=ax)
    ax.set_title("Boxplot: Preço por serviço (outliers em destaque)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "05_boxplot_preco_servico.png", dpi=120)
    plt.close()


def fig_heatmap(df: pd.DataFrame) -> None:
    numericas = df[["preco", "duracao_min", "receita", "foi_cancelado", "mes", "dia_semana"]]
    corr = numericas.corr(method="spearman")
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title("Mapa de calor — correlação de Spearman")
    plt.tight_layout()
    plt.savefig(FIGS_DIR / "06_heatmap_correlacoes.png", dpi=120)
    plt.close()


def main() -> None:
    df = carregar()
    print(f"Gerando 6 gráficos em {FIGS_DIR}/ ...")
    fig_barras(df)
    fig_linhas(df)
    fig_dispersao(df)
    fig_histograma(df)
    fig_boxplot(df)
    fig_heatmap(df)
    print("OK — gráficos salvos.")


if __name__ == "__main__":
    main()
