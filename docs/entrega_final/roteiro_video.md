# Roteiro do Vídeo de Apresentação (10 minutos)

> Roteiro alinhado ao **"Guia para o Vídeo de Apresentação"** do Prof. Felipe.
> O vídeo é entregável obrigatório; **link deve estar dentro do PDF final**
> com permissão de "leitor"/"público" (YouTube unlisted, Drive ou Vimeo).

---

## Distribuição de tempo (10 min totais)

| Bloco | Duração | Quem fala | Conteúdo |
|---|--:|---|---|
| 1. Abertura e contexto | **1:00** | João (PM) | Empresa, problema, equipe |
| 2. Gestão de Projetos | **1:30** | João | Pasta, cronograma, RACI |
| 3. **Prática (mais importante)** | **4:00** | Calebe + Guilherme | Scripts Python rodando + resultados |
| 4. Segurança da Informação | **2:00** | Diego | Vulnerabilidades GUT + LGPD |
| 5. Fechamento | **1:30** | Equipe toda | Considerações finais + aprendizado |
| **TOTAL** | **10:00** | | |

---

## Bloco 1 — Abertura e Contexto (1:00) — *João*

**[Tela: capa do projeto + foto da equipe]**

> "Olá Prof. Felipe, somos o Grupo 4. Eu sou o **João Falbi**, gerente
> de projeto, e aqui comigo estão **Calebe** (Análise de Dados),
> **Diego** (Segurança da Informação) e **Guilherme** (Pesquisa Operacional).
>
> Nosso projeto é a **Barbearia Invictus**, uma microempresa de São
> Paulo. O problema que escolhemos resolver é claro: a barbearia perdia
> ~14% de receita por **cancelamentos não notificados** e o dono gastava
> 2 horas por dia organizando agenda manualmente no WhatsApp.
>
> Nossa solução: uma plataforma web em FastAPI que **agenda online,
> controla estoque, mede KPIs em tempo real e otimiza matematicamente**
> a alocação dos barbeiros."

**[Transição: tela do README do GitHub]**

---

## Bloco 2 — Gestão de Projetos (1:30) — *João*

**[Tela: estrutura de pastas + Gantt em Mermaid]**

> "Começamos pela **Gestão**, porque sem isso nada flui. Aqui está nossa
> estrutura — repositório GitHub público, pasta `docs/d1_gestao/` com
> os 7 entregáveis (TAP assinado pelo Sponsor, EAP, RACI, Gantt,
> Custos, Riscos, e Atas).
>
> O **TAP** definiu 5 Objetivos SMART, todos mensuráveis. A **EAP**
> decompõe o projeto até nível 3, mostrando que separamos backend,
> análise de dados, segurança, otimização e homologação.
>
> Aqui está nosso **Gantt** — 11 semanas, com a entrega final fixada
> para hoje, **22 de maio**. O caminho crítico passou pela validação
> com você no dia 4 de maio (Sinal Verde) e está cumprido.
>
> A **Matriz RACI** divide responsabilidades — cada disciplina tem um
> R/A principal, e todos somos C ou I nas demais. Isso evitou
> sobrecarga de uma pessoa só."

**[Transição: passar a palavra para o Calebe]**

---

## Bloco 3 — Prática (4:00) — *Calebe + Guilherme*

> ⚠️ **Este é o bloco mais importante segundo o guia.** Tela compartilhada
> com Jupyter rodando ao vivo.

### 3.1 Análise de Dados (2:00) — *Calebe*

**[Tela: Notebook 01 rodando]**

> "No notebook `01_etl_e_kpis.ipynb`, fazemos o **ETL com pandas**: lemos
> o CSV exportado pelo sistema FastAPI, removemos nulos, normalizamos
> preços com vírgula brasileira, e geramos features como `mes`,
> `dia_semana`, `receita`.
>
> A partir do dataset tratado, calculamos os **3 KPIs justificados**:
> - **Receita Realizada** (R$ 7.040 no mês simulado)
> - **Taxa de Cancelamento** (14,7%) — acima da meta SMART de 10%
> - **Ticket Médio** (R$ 39,71)
>
> Aplicamos **4 métodos estatísticos**: descritiva, distribuição
> (assimetria), Pearson e Spearman. A correlação Pearson entre
> duração e preço deu 1,0, provando que precificação está coerente —
> o problema não é o preço, é o cancelamento."

**[Tela: Notebook 02 rodando — mostrar 3 dos 8 gráficos]**

> "No notebook `02_visualizacoes.ipynb`, geramos **8 gráficos**:
> barras, linhas, dispersão, histograma, boxplot, heatmap, donut e
> Pareto. O **Pareto** mostra que ~70% da receita vem de 50% dos
> serviços — concentração clássica que justifica investir mais nos
> combos de maior margem."

### 3.2 Pesquisa Operacional (2:00) — *Guilherme*

**[Tela: Notebook 03 rodando]**

> "No notebook `03_otimizacao_lucro.ipynb`, modelamos o **Problema 1 —
> Maximização de Lucro** com **PuLP** — sem Excel Solver, conforme
> regra inegociável.
>
> Variáveis de decisão inteiras: cortes simples, combos, premiums.
> Restrições: tempo disponível (2400 min), estoque de pigmentação (10),
> e mix mínimo de 30% de cortes simples. O solver convergiu para
> 11 cortes + 10 premiums, lucro de **R$ 2.050**.
>
> O **What-If** mostrou: se perdermos 25% das horas (1 barbeiro fora),
> o lucro cai 24,4%. Isso conecta direto ao Risco R3 do TAP."

**[Tela: Notebook 04 rodando]**

> "No notebook `04_otimizacao_alocacao.ipynb`, é o **Problema 2 —
> Minimização de Custo de Folha**. Variáveis binárias x_b,t (barbeiro
> b no turno t). O solver atribui Calebe ao sábado e Diego ao domingo,
> custo total **R$ 800**. O What-If mostra que sem o júnior, a folha
> sobe 15%. Decisão estratégica: contratar segundo júnior."

**[Transição: passar para o Diego]**

---

## Bloco 4 — Segurança da Informação (2:00) — *Diego*

**[Tela: docs/d3_seguranca.md aberto]**

> "Em **Segurança da Informação**, mapeamos **20 ameaças** com fórmula
> GUT (Gravidade × Urgência × Tendência), todas referenciadas no
> OWASP Top 10 ou CVE.
>
> A vulnerabilidade de maior nota foi **125 — Vazamento de banco de
> dados**. Antes da nossa mitigação, a senha do admin estava em texto
> puro. Um invasor que copiasse o `.db` lia a senha em segundos.
>
> Mitigamos com **bcrypt cost 12 + salt aleatório** — pesquisamos
> OWASP ASVS V2.4 e NIST SP 800-63B. Cada tentativa de força bruta
> custa 250 ms. Brute force vira inviável."

**[Tela: /admin/login mostrando rate-limit]**

> "Demonstro: faço 5 logins errados e o sistema bloqueia por 15
> minutos. Esse é o `registrar_falha` do `app/security.py`."

**[Tela: /admin/auditoria com logs]**

> "Aqui está o **audit log** registrando IP, ação e usuário de toda
> operação administrativa — ferramenta forense para incidentes."

**[Tela: /lgpd/meus-dados]**

> "**LGPD**: 20 dados mapeados em RoPA com base legal por item.
> Implementamos os 5 direitos do titular do Art. 18 — esta página
> permite ao cliente solicitar a anonimização dos próprios dados,
> que **mantém integridade contábil** mas remove a PII."

**[Transição: passar para a equipe]**

---

## Bloco 5 — Fechamento (1:30) — *Equipe toda*

**[Tela: dashboard final com KPIs e link do GitHub]**

> **João:** "Em resumo, o projeto entregou **17 de 20 mitigações** em
> código rodando, **20 ameaças GUT mapeadas**, **20 políticas IAM**,
> **20 itens RoPA**, **2 problemas PuLP modelados** e **8 gráficos
> analíticos**. O dono da barbearia já tem a ferramenta para reduzir
> cancelamentos abaixo de 10%."
>
> **Calebe:** "A maior lição da Análise de Dados foi: o número não
> mente, mas precisa ser *justificado* — cada KPI tem que estar
> ligado a um Objetivo SMART do TAP. Senão, vira ruído."
>
> **Diego:** "Em Segurança, aprendi que **defesa em profundidade**
> não é jargão: é colocar bcrypt, depois CSP, depois ORM, depois
> audit log. Se uma camada falhar, as outras seguram."
>
> **Guilherme:** "Pesquisa Operacional me mostrou que a intuição do
> dono estava ~95% certa, mas o solver confirmou matematicamente —
> e a What-If revelou os outros 5% que ele não enxergava."
>
> **João:** "Obrigado pela orientação ao longo das 5 fases, Prof.
> Felipe. Todos os links e códigos estão no PDF e no repositório
> GitHub público. Estamos abertos a perguntas."

**[Tela final: agradecimento + URL do repositório]**

---

## Checklist de gravação

- [ ] Câmera ligada para todos os apresentadores (mostrar o rosto inicial)
- [ ] Microfone com qualidade — testar 5 min antes
- [ ] Tela compartilhada em **fullscreen** (não usar ALT-TAB durante demo)
- [ ] Aumentar zoom/fonte do terminal e do navegador para a banca enxergar
- [ ] **Sistema rodando antes de gravar** (`.\.venv\Scripts\uvicorn.exe app.main:app`)
- [ ] **Notebooks abertos em abas separadas** já executados
- [ ] Cronometrar: vídeo entre **9:30 e 10:30** (margem de 30s)
- [ ] Editar com **legenda em momentos críticos** (números do KPI, nota GUT)
- [ ] Exportar em **MP4 1080p**
- [ ] Subir no **YouTube como "não listado"** ou **Google Drive público**
- [ ] **Testar o link em janela anônima** antes de colar no PDF

## Cuidados que reduzem nota (do guia)

| Erro | Como evitar |
|---|---|
| Vídeo onde não dá para ver o que está rodando | Aumentar fonte, gravar 1080p |
| Links não funcionam | Testar em janela anônima |
| Pessoas falando sem mostrar a tela | Sempre compartilhar tela durante demo |
| Áudio ruim | Headset com microfone, ambiente silencioso |
| Mais de 10 minutos | Cortar na edição (foco no Bloco 3 — Prática) |

## Software de gravação recomendado (gratuito)

- **OBS Studio** (Windows/Mac/Linux) — <https://obsproject.com>
- **Loom** (Chrome) — <https://www.loom.com>
- **Google Meet** com função "Gravar reunião" (versão paga ou estudante)
- **Microsoft Teams** com gravação local
