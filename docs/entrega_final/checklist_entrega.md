# Checklist da Entrega Final — 22/05/2026

> Lista única para garantir nota ≥ 6,0 (aprovação) e mirar nota 8,0+
> (Bom Desempenho).

---

## 🚦 Bloqueadores (sem isso = REPROVAÇÃO automática)

- [ ] **PDF final** entregue até 22/05/2026 (formato ABNT)
- [ ] **Vídeo de 10 minutos** com link dentro do PDF, em "leitor"/"público"
- [ ] **Sinal Verde do Prof. Felipe** (ata em `docs/d1_gestao/atas/ata_sinal_verde.md`)
- [ ] **Repositório GitHub público** com permissão de leitor para o professor
- [ ] **Códigos Python rodando** — notebooks executados com saídas preservadas

---

## 📐 Formatação (ABNT) — para nota 8,0+

- [ ] Capa nas normas (instituição, autores, título, cidade, ano)
- [ ] Folha de rosto (autores + RAs + orientador)
- [ ] Sumário automático (gerado pelo Word/Docs)
- [ ] Margens: 3 cm sup/esq, 2 cm inf/dir
- [ ] Fonte Times/Arial 12 pt, espaçamento 1,5
- [ ] Numeração de páginas a partir da introdução
- [ ] Referências no padrão **ABNT NBR 6023:2018**
- [ ] Apêndices (atas escaneadas, prints do board, links)

---

## 📋 Disciplina 1 — Gestão de Projetos

- [x] TAP com Objetivos SMART + Escopo IN/OUT + Stakeholders
- [x] EAP até nível 3 (texto + diagrama Mermaid)
- [x] Backlog Ágil — 18 User Stories no formato "Como [usuário], quero..."
- [x] Matriz RACI — 33 linhas com R/A/C/I + planilha XLSX colorida
- [x] Cronograma Gantt com dependências e caminho crítico
- [x] Custos com contingência (R$ 28.187,50)
- [x] Plano de Comunicação + Matriz de 10 Riscos
- [x] **4 Atas de Reunião** (Kickoff + Sprint 1 + Sprint 2 + Sinal Verde)
- [ ] **Imprimir TAP e Atas e coletar assinatura física do Sponsor**
- [ ] **Print do e-mail real com pauta** enviado antes de cada Sprint Review

## 📊 Disciplina 2 — Análise de Dados

- [x] ETL pandas (limpeza, conversão, features derivadas)
- [x] **3 KPIs justificados em texto** ligados aos Objetivos SMART
- [x] 4 métodos estatísticos (descritiva, distribuição, Pearson, Spearman)
- [x] **8 gráficos** matplotlib + seaborn (de 10 opções do guia)
- [x] Análise Crítica (pergunta obrigatória respondida)
- [x] Notebooks `.ipynb` executados com saídas preservadas
- [x] 8 PNGs em `notebooks/figs/` para anexar ao PDF

## 🔒 Disciplina 3 — Segurança da Informação

- [x] **20 ameaças** mapeadas com nota GUT + referência OWASP/CVE
- [x] **20 políticas IAM** justificadas com NIST/Zero Trust
- [x] **20 dados** mapeados em RoPA + base legal LGPD
- [x] Direitos do Titular (Art. 18) implementados
- [x] Análise Crítica (vulnerabilidade de maior nota explicada)
- [x] 17 mitigações implementadas em código (`app/security.py`)
- [x] Audit log funcional em `/admin/auditoria`
- [x] Endpoint de anonimização funcional em `/lgpd/meus-dados`
- [x] Política de privacidade pública em `/privacidade`

## 🧮 Disciplina 4 — Pesquisa Operacional

- [x] **2 problemas distintos** modelados com PuLP
- [x] Modelagem matemática formal (variáveis, função objetivo, restrições)
- [x] **Excel Solver não foi usado** (regra inegociável cumprida)
- [x] **Análise What-If** em ambos os problemas
- [x] Análise Crítica conjunta (Max + Min) na pergunta obrigatória
- [x] Notebooks executados com saídas (R$ 2.050 lucro, R$ 800 folha)

## 👥 Gestão de Equipe (exigida para grupos > 3)

- [x] Documento "quem fez o quê" em `docs/entrega_final/gestao_equipe.md`
- [x] Histórico de commits do Git auditável por autor

## 🎬 Vídeo de Apresentação (10 min)

- [x] Roteiro pronto em `docs/entrega_final/roteiro_video.md`
- [ ] Equipe ensaiou pelo menos 1 vez antes da gravação
- [ ] Gravação em **1080p** com boa iluminação
- [ ] Áudio sem ruído (headset)
- [ ] Tela compartilhada com **fonte aumentada** (sistema + notebooks)
- [ ] Duração entre **9:30 e 10:30**
- [ ] Subido como **YouTube unlisted** ou **Drive público**
- [ ] **Link testado em janela anônima** antes de submeter

## 🔗 Acesso aos arquivos (cuidado fatal)

- [ ] Repositório GitHub está **público**
- [ ] Pasta no Google Drive (se houver) está com link de **leitor para qualquer um**
- [ ] Vídeo está com permissão de **público/não listado**
- [ ] Todos os links no PDF foram **testados em janela anônima**

---

## 📦 Pacote final a entregar

```
Barbearia_Invictus_Entrega_Final_2026/
├── Barbearia_Invictus_Entrega_Final_2026.pdf       ← documento principal ABNT
├── apendices/
│   ├── A_atas_assinadas.pdf                        ← 4 atas escaneadas
│   ├── B_print_github_repo.png
│   ├── C_notebooks_executados/
│   │   ├── 01_etl_e_kpis.pdf
│   │   ├── 02_visualizacoes.pdf
│   │   ├── 03_otimizacao_lucro.pdf
│   │   └── 04_otimizacao_alocacao.pdf
│   ├── D_link_video.txt
│   ├── E_board_kanban.png
│   └── F_planilhas_RACI_e_custos.xlsx
└── README.txt   ← sumário do que tem em cada pasta
```

---

## 🎯 Definição de "PRONTO PARA ENTREGAR"

Você só pode submeter quando **TODOS** estes 5 itens forem ✅:

1. ✅ PDF ABNT gerado e revisado
2. ✅ Vídeo gravado e link público funcionando
3. ✅ Sinal Verde do Prof. Felipe documentado
4. ✅ Repositório GitHub público acessível
5. ✅ Janela anônima abriu PDF + vídeo + repositório sem problema
