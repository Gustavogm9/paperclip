---
name: sprint-semanal
description: >
  Como rodar a sprint semanal da Guilds Marketing Company dentro do Paperclip.
  Cobre standup segunda 08h (planejamento), checkin quarta 17h (meio-sprint),
  review sexta 17h (fechamento + resumo pro CMO). Use quando o Head of Marketing
  for iniciar a semana, quando qualquer agente precisar reportar progresso, ou
  quando alguém precisar saber onde está cada entrega da semana. Define os
  formatos dos artefatos (plano da semana, standup, review).
---

# Sprint semanal — Guilds Marketing Company

## Calendário fixo

| Dia | Hora | Evento | Dono | Duração típica |
|---|---|---|---|---|
| Segunda | 08:00 | Standup / Plano da semana | Head of Marketing | 15 min |
| Quarta | 17:00 | Checkin meio-sprint | Head of Marketing | 10 min |
| Sexta | 17:00 | Review + resumo pro CMO | Head of Marketing | 20 min |

Qualquer agente pode ser acionado fora desses horários pra tarefa específica, mas os três eventos acima são ritmo fixo.

## Segunda 08h — Plano da semana

### Input (o que o Head of Marketing lê antes)
1. `PROJECT.md` da company — objetivo da fase atual
2. `TASK.md` — tarefas abertas e bloqueios
3. Resumo da sexta anterior (em `outputs/reports/YYYY-WW_resumo-cmo.md`)
4. Observações do CMO (se houver mensagens novas)

### Output (o que o Head of Marketing escreve)
Arquivo `outputs/briefs/YYYY-WW_plano-semana.md` com:

```markdown
# Plano da semana WW / YYYY (semana DD-MM a DD-MM)

## Objetivo-chave da semana
[1 linha — o que a semana precisa entregar pra mover a fase]

## Entregas (máximo 5)
1. [Entrega] — dono: [agente] — prazo: [dia] — critério pronto: [critério]
2. ...

## Bloqueios conhecidos
- [bloqueio] — quem destrava: [agente/CMO]

## Tarefas atribuídas por agente
- [agente]: [tarefa específica com prazo]
- ...

## Dependências externas do CMO
- [item que precisa de decisão/aprovação dele esta semana]
```

### Ação
Atribuir tarefas pra cada agente via Paperclip (Assignment).

## Quarta 17h — Checkin meio-sprint

### Input
- Progresso de cada agente em suas tarefas de segunda
- Bloqueios novos que surgiram

### Output
Arquivo `outputs/reports/YYYY-WW_checkin.md` com:

```markdown
# Checkin WW — meio-sprint

## Status por entrega
- [Entrega 1]: ✅ concluída / 🟡 em andamento, X% / 🔴 bloqueada — [nota curta]
- ...

## Ações corretivas
- [Se alguma entrega está rubra, o que vai fazer até sexta]

## Escalações pro CMO
- [Se precisa de decisão dele antes de sexta]
```

### Ação
Reatribuir se precisar, escalar bloqueios pro CMO se bloqueiam a semana inteira.

## Sexta 17h — Review + resumo pro CMO

### Input
- Todas as entregas da semana
- Checkin da quarta
- Qualquer input do CMO ao longo da semana

### Output 1: Review interno
Arquivo `outputs/reports/YYYY-WW_review.md` com:
```markdown
# Review WW

## Entregues
- [Entrega] — dono — link pro arquivo em outputs/approved/ ou outputs/content/

## Não entregues
- [Entrega] — dono — razão — plano pra semana seguinte

## Aprendizados
- [3–5 bullets curtos sobre o que funcionou, o que não funcionou, o que testar]

## Métricas da semana
- [Métricas disponíveis — se não tem ainda, escrever "aguardando canais ativos"]
```

### Output 2: Resumo executivo pro CMO
Usar a skill `resumo-executivo`. Arquivo `outputs/reports/YYYY-WW_resumo-cmo.md`.

### Ação
Brand Guardian revisa ambos os outputs antes do resumo ir pro CMO.

## Regra de atomicidade

Uma entrega sempre tem:
- **Artefato físico**: um arquivo em `outputs/` ou um evento externo (post publicado, email enviado)
- **Critério pronto**: definido na segunda, sem ambiguidade
- **Dono único**: um agente, não um grupo

Se uma entrega não tem os três, reescrever antes de atribuir.

## Regra de escopo da semana

Máximo 5 entregas por semana. Se houver mais demanda, priorize por impacto no objetivo-chave e escale o resto pra CMO decidir.

## Como usar esta skill

- **Head of Marketing**: este é seu playbook canônico de ritmo semanal. Siga os templates literalmente nas primeiras 4 semanas — depois pode evoluir com retro.
- **Agentes subordinados**: sabem quando esperar atribuição (segunda 08h), quando reportar (quarta 17h no checkin, sexta 16h preparando review).
- **Brand Guardian**: recebe cada entrega em outputs/ durante a semana, valida até sexta 16h, encaminha pro review.
