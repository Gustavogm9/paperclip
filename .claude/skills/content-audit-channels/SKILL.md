---
name: content-audit-channels
description: >
  Obriga verificação do que já existe publicado e do que já está programado nos
  canais (LinkedIn pessoal Gustavo, LinkedIn Guilds Page, LinkedIn Guilds Canada,
  Instagram guilds.oficial, Instagram guildsinc) ANTES de produzir peça nova. Evita
  repetição, duplicação, ou conflito com calendário já marcado no PostForMe.
---

# Content Audit Channels — antes de criar, verifique o que já tem

Produzir peça nova sem saber o que está no ar ou já programado causa:
- Duplicação de tema (dois posts sobre case NEOPSICO em 3 dias)
- Tom inconsistente entre peças recentes
- Calendário apertado (3 peças agendadas + peça nova mesmo dia)
- Retrabalho (criar algo que já estava na fila)

Esta skill roda **antes** do Copywriter começar a escrever qualquer peça
destinada a canal público.

## Canais que o time da Guilds opera

### Instagram
- `@guilds.oficial` (ID PostForMe: 26353394497678790) — Instagram Business
- `guildsinc` (ID PostForMe: 17841480002824189) — secundário

### LinkedIn
- `Gustavo Gouveia Macedo` (ID: XMmyBe6t_0) — PESSOAL do CMO, prioridade #1
- `Guilds` (ID: 86433146) — Company Page Brasil
- `Guilds Canada Inc` (ID: 111402137) — Company Page Canadá

### Outros
- Floox Service (ID: 78357607) — legacy, uso eventual

## Processo obrigatório antes de produzir

### Passo 1 — Verificar o que JÁ ESTÁ PUBLICADO (últimos 14 dias)

Consultar via API do Instagram/LinkedIn (ou via Firecrawl/scrape se não houver
API direta) os últimos 10 posts de cada canal-alvo:

- O que foi posted?
- Qual tom/linguagem usada?
- Quais cases já citados?
- Quais keywords já usadas?

Objetivo: peça nova **não repete** tema/case de peça publicada nos últimos 14 dias.

### Passo 2 — Verificar o que JÁ ESTÁ PROGRAMADO no PostForMe

Consultar PostForMe via API (`POSTFORME_API_KEY` no env) para listar posts
agendados (schedule) em cada canal:

- Lista de `scheduled_posts` por canal
- Data + hora de cada post
- Conteúdo resumido
- Status (draft/scheduled/published)

Objetivo: peça nova **não conflita** com calendário já marcado.

### Passo 3 — Verificar memória institucional (Drive/Notion)

Quando estiver plugado (GOV.2):
- Consultar `Drive/Guilds/Ops Agents/01-outputs-internos/approved/YYYY-MM/`
- Ver se peça similar já foi aprovada mas não publicada ainda
- Verificar `memory/decisions/` por decisões que afetem a peça

### Passo 4 — Recomendação ao Content Manager

Antes do Content Manager criar briefing pro Copywriter, ele deve ter:

```yaml
channel_audit:
  canal_alvo: [LinkedIn pessoal Gustavo | LinkedIn Guilds Page | IG | etc]
  ultimos_14d_publicados: [lista resumida dos posts]
  temas_ja_cobertos: [case X, topic Y]
  proximos_agendados: [lista de posts programados com data]
  conflitos: [sim/não, qual]
  recomendacao: [criar nova | adiar | substituir agendado | ajustar tema]
```

Se há conflito/duplicação detectada:
- Content Manager escala ao Head of Marketing
- Ou decide ajustar brief (tema, data, canal)

## Prioridade de canais — 2026-04 (atual)

Decisão do CMO (2026-04-22):

1. **LinkedIn pessoal do Gustavo** (@gustavo-gouveia-macedo) — prioridade #1,
   alavanca personal brand do CMO. Posts com tom pessoal de opinião/experiência.
2. **LinkedIn Guilds Page** — prioridade #2, tom institucional, cases, anúncios.
3. **Instagram @guilds.oficial** — prioridade paralela, carrosséis e reels
   curtos, identidade visual Guilds.
4. **LinkedIn Guilds Canada Inc Page** — prioridade #3 (adaptação em inglês).
5. **Instagram guildsinc** — secundário, decidir conforme evolui.

## Output obrigatório

Quando aplicar esta skill, anexar ao briefing:

```
Content Audit — [data] — canal [alvo]
Últimos 14d publicados: [resumo]
Temas cobertos recentemente: [lista]
Posts agendados próximos: [data + tema]
Conflito detectado: [sim/não]
Recomendação: [criar novo | adiar | substituir | ajustar]
```

Sem esse bloco no briefing, Copywriter devolve para Content Manager revisar.

## Quando pular

Esta skill **NÃO se aplica** a:
- Peças exclusivamente internas (não vão para canal público)
- Rascunhos de exploração (antes de briefing formal)
- Resposta a evento inesperado (ex.: crise, menção de imprensa)

## Integração

Roda antes de qualquer peça destinada a canal público, posicionada entre:
- `icp-validator` (audiência correta) — antes
- `posicionamento-guilds` / `copy-g-forge` (produção) — depois

Content Manager aplica. Resultado entra no briefing que vai pro Copywriter.
