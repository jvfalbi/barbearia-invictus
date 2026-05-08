# Ata de Reunião — Sprint Review 1

| Campo | Valor |
|---|---|
| **Projeto** | Barbearia Invictus |
| **Data** | 03/04/2026 |
| **Horário** | 18h00 às 19h00 |
| **Local / Canal** | Google Meet |
| **Tipo** | Sprint Review — fim da Fase 2 (Sem 5) |

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
| US-01 | Login admin | ✅ Aprovado | Demo com credenciais de teste |
| US-02 | Agendamento online | ✅ Aprovado | Sponsor testou ao vivo |
| US-03 | Consentimento LGPD | ✅ Aprovado | Validado checkbox obrigatório |
| US-04 | Listagem de agendamentos | ✅ Aprovado | Tabela em `/admin` |
| US-05 | CRUD de barbeiros | ✅ Aprovado | Foto + ativo |
| US-06 | CRUD de serviços | ✅ Aprovado | Preço + duração |

## Feedback do Sponsor

- 👍 "Achei o tema visual da barbearia muito bom, combinou."
- 👍 "Gostei do consentimento LGPD aparecer no formulário."
- ⚠️ Pediu: na próxima Sprint, ter o **controle de estoque dos produtos**.

## Próximos passos (Sprint 2 — Fase 3)

| # | Ação | Responsável | Prazo |
|---|---|---|---|
| 1 | Implementar CRUD de produtos com estoque | João Falbi | 19/04/2026 |
| 2 | Hash bcrypt + rate-limiting no login | Diego Lima | 12/04/2026 |
| 3 | Audit log + cabeçalhos HTTP | Diego Lima | 19/04/2026 |
| 4 | Endpoint anonimização LGPD | Diego Lima | 26/04/2026 |
| 5 | Endpoints export CSV | João Falbi | 12/04/2026 |
| 6 | **Preparar artefatos para Sinal Verde** (04/05) | Equipe | 03/05/2026 |

## Riscos atualizados

- R1 (atraso do CSV) **mitigado** — Sponsor enviou no dia 04/04.
- R4 (vulnerabilidade) **monitorando** — Diego rodará bandit ao fim da Sprint 2.

## Assinaturas

| Papel | Nome | Assinatura |
|---|---|---|
| Sponsor | _Dono da Barbearia Invictus_ | __________________________ |
| PM | João Vitor Falbi | __________________________ |
