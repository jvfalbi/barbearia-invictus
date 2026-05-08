# Ata de Reunião — Sprint Review 2

| Campo | Valor |
|---|---|
| **Projeto** | Barbearia Invictus |
| **Data** | 24/04/2026 |
| **Horário** | 18h00 às 19h00 |
| **Local / Canal** | Google Meet |
| **Tipo** | Sprint Review — fim da Fase 3 (Sem 8); preparação para Sinal Verde |

## Participantes

| Nome | Papel | Presente? |
|---|---|---|
| Dono da Barbearia Invictus | Sponsor | ✅ |
| João Vitor Falbi | PM + Backend | ✅ |
| Calebe Fernandes Ramos | Dados | ✅ |
| Diego Lima Dantas | Segurança | ✅ |
| Guilherme Camelo Pimenta | Pesq. Operacional | ✅ |

## Entregas demonstradas

| US | Funcionalidade | Status | Observação |
|---|---|---|---|
| US-07 | CRUD de produtos | ✅ Aprovado | Demo na aba Produtos |
| US-08 | Listagem pública de produtos | ✅ Aprovado | Página `/produtos` |
| US-09 | Botões `+`/`-` de estoque | ✅ Aprovado | Sponsor testou em 3 produtos |
| US-10 | Exportação CSV | ✅ Aprovado | 3 endpoints funcionando |
| US-11 | Rate-limiting no login | ✅ Aprovado | 6ª tentativa bloqueia |
| US-12 | Audit log | ✅ Aprovado | Visualizado em `/admin/auditoria` |
| US-13 | Anonimização LGPD | ✅ Aprovado | Demo do fluxo completo |
| US-17 | Política de privacidade | ✅ Aprovado | Página `/privacidade` |
| US-18 | Cabeçalhos HTTP | ✅ Aprovado | Verificado no DevTools |

## Feedback do Sponsor

- 👍 "Adorei poder baixar o CSV, vou usar para fazer o imposto."
- 👍 "O bloqueio depois de 5 erros me deu tranquilidade quanto à segurança."
- 💡 Pediu: na Sprint 3, queria ver **qual é o serviço mais lucrativo**.

## Próximos passos (Fase 4 — Sinal Verde 04/05)

| # | Ação | Responsável | Prazo |
|---|---|---|---|
| 1 | Notebook ETL + KPIs (3 KPIs justificados) | Calebe Ramos | 12/04/2026 |
| 2 | Notebook 8 visualizações | Calebe Ramos | 19/04/2026 |
| 3 | Notebook PuLP — maximização lucro + What-If | Guilherme Pimenta | 19/04/2026 |
| 4 | Notebook PuLP — alocação de equipe + What-If | Guilherme Pimenta | 26/04/2026 |
| 5 | Análise crítica documentada para D2 e D4 | Calebe + Guilherme | 26/04/2026 |
| 6 | **Compilar dossiê para validação com Prof. Felipe** | João Falbi | 03/05/2026 |
| 7 | **Reunião Sinal Verde com Prof. Felipe** | Equipe toda | **04/05/2026** |

## Riscos atualizados

- **R7 (LGPD na banca)** — agora **mitigado**: anonimização funcional + política pública + RoPA documentada em `docs/d3_seguranca.md`.
- **R5 (Solver PuLP)** — monitorando: Guilherme já validou o solver com problema de teste pequeno.

## Assinaturas

| Papel | Nome | Assinatura |
|---|---|---|
| Sponsor | _Dono da Barbearia Invictus_ | __________________________ |
| PM | João Vitor Falbi | __________________________ |
