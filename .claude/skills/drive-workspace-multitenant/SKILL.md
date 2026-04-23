---
name: drive-workspace-multitenant
description: >
  Arquitetura multitenant do Google Drive "Guilds Ops Agents" que todos os agentes
  do time devem seguir. A Guilds Marketing é uma agência — a Guilds Lab é apenas
  o primeiro cliente dela. Esta skill é a referência CANÔNICA de paths para
  leitura e escrita. Use SEMPRE antes de ler/criar arquivos no Drive.
---

# Drive Workspace Multitenant — referência canônica

A Guilds Marketing é uma agência de marketing operada por agentes. Atende
múltiplos clientes. A Guilds Lab é apenas o primeiro cliente. Toda a estrutura
do Drive reflete essa arquitetura.

## Arquitetura (Shared Drive "Guilds Ops Agents")

```
Guilds Ops Agents/                         ← raiz do Shared Drive
├── 00-agency-shared/                      ← conhecimento DA AGÊNCIA
│   ├── metodologia-g-forge/                 (definição G-FORGE, frameworks)
│   ├── skills-runbook/                      (documentação de skills ativas)
│   ├── templates-contratos/                 (contrato padrão, aditivos, NDA)
│   ├── templates-propostas/                 (proposta-modelo, pricing sheet)
│   ├── templates-kickoff/                   (agenda kickoff, baseline sheet)
│   ├── decisoes-estrategicas/               (decisões da agência, não de cliente)
│   └── friction-log/                        (aprendizados gerais da agência)
│
├── 01-clients/                            ← clientes da agência (multitenant)
│   ├── guilds/                              ← cliente: Guilds Lab
│   │   ├── knowledge-base/
│   │   │   ├── posicionamento/
│   │   │   │   ├── aprovados/
│   │   │   │   ├── decisoes/
│   │   │   │   └── evolucoes/
│   │   │   ├── cases-autorizados/
│   │   │   │   ├── neopsico/               (SEM autorização por ora)
│   │   │   │   └── scavaseg/               (SEM autorização por ora)
│   │   │   ├── icp-audiencia/
│   │   │   ├── marca/
│   │   │   │   ├── logos/
│   │   │   │   ├── paleta-cores/
│   │   │   │   └── identidade-visual/
│   │   │   ├── materiais-venda/
│   │   │   │   ├── pitch-decks/
│   │   │   │   ├── one-pagers/
│   │   │   │   ├── propostas-aprovadas/
│   │   │   │   └── casos-uso/
│   │   │   └── pesquisas-mercado/
│   │   │       ├── concorrentes/
│   │   │       └── tendencias/
│   │   ├── outputs/
│   │   │   ├── drafts/
│   │   │   ├── in-review/
│   │   │   ├── approved/
│   │   │   ├── published/
│   │   │   └── rejected/
│   │   ├── reports/
│   │   │   ├── semanais/
│   │   │   ├── mensais/
│   │   │   └── dashboards/
│   │   └── memoria/
│   │       ├── decisoes/
│   │       ├── aprendizados/
│   │       └── friction-log/
│   │
│   └── _template-cliente/                   ← duplicar pra novos clientes
│       └── (estrutura espelho simplificada)
│
└── 99-archive/                            ← arquivo morto
```

## Princípio: isolamento por cliente

- **Agente só acessa 1 cliente ativo por vez** (definido pelo brief / assignment)
- **Nunca misturar dados entre clientes** — um copy produzido para cliente A
  não pode mencionar dados de cliente B por engano
- **00-agency-shared** é a exceção: leitura universal pra todos os agentes
  independente de qual cliente estão servindo
- **99-archive** é leitura sob demanda — histórico geral da agência

## Paths por tipo de operação

Substituir `<cliente>` pelo slug do cliente ativo (hoje: `guilds`).

### Leitura universal (qualquer agente, a qualquer momento)
- `00-agency-shared/metodologia-g-forge/` — entender G-FORGE
- `00-agency-shared/skills-runbook/` — referência de skills
- `00-agency-shared/templates-*/` — templates da agência

### Leitura do cliente ativo
- `01-clients/<cliente>/knowledge-base/posicionamento/aprovados/` — posicionamento atual
- `01-clients/<cliente>/knowledge-base/cases-autorizados/` — cases + autorizações
- `01-clients/<cliente>/knowledge-base/icp-audiencia/` — persona viva
- `01-clients/<cliente>/knowledge-base/marca/` — identidade visual
- `01-clients/<cliente>/knowledge-base/materiais-venda/` — pitch/propostas
- `01-clients/<cliente>/knowledge-base/pesquisas-mercado/` — concorrentes/tendências
- `01-clients/<cliente>/outputs/published/` — histórico de publicados (evitar repetição)
- `01-clients/<cliente>/memoria/decisoes/` — decisões específicas do cliente

### Escrita por tipo de output

| Tipo | Agente escreve | Path |
|---|---|---|
| Draft inicial | Copywriter | `01-clients/<cliente>/outputs/drafts/` |
| Draft em review | Copywriter move | `01-clients/<cliente>/outputs/in-review/` |
| Aprovado (Guardian + humano) | Brand Guardian move | `01-clients/<cliente>/outputs/approved/` |
| Publicado | Social Media Ops move | `01-clients/<cliente>/outputs/published/` |
| Rejeitado | Content Manager move + anota motivo | `01-clients/<cliente>/outputs/rejected/` |
| Relatório semanal | Analyst / Head of Marketing | `01-clients/<cliente>/reports/semanais/` |
| Relatório mensal | Analyst | `01-clients/<cliente>/reports/mensais/` |
| Decisão específica | Head de Marketing | `01-clients/<cliente>/memoria/decisoes/` |
| Aprendizado | Qualquer agente | `01-clients/<cliente>/memoria/aprendizados/` |
| Friction log | Qualquer agente | `01-clients/<cliente>/memoria/friction-log/` |
| Decisão da agência (não do cliente) | Head de Marketing / CEO | `00-agency-shared/decisoes-estrategicas/` |

## Naming convention obrigatória

### Arquivos em `outputs/`
```
YYYY-MM-DD_canal_formato_tema-slug.md

Exemplos:
2026-04-22_linkedin-gustavo_post_case-sst-anonimizado.md
2026-04-25_email_drip-welcome_01-intro.md
2026-05-02_landing_servico-squad-conteudo.md
```

### Arquivos em `reports/`
```
YYYY-WW_resumo-executivo.md       (semanal, WW = semana ISO)
YYYY-MM_relatorio-impacto.md      (mensal)
```

### Arquivos em `memoria/decisoes/`
```
YYYY-MM-DD_tema-decisao-slug.md
```

### Arquivos em `cases-autorizados/<cliente>/`
```
autorizacao-YYYYMMDD.pdf          (documento assinado)
numeros-reais.md                  (metricas autorizadas)
materiais-aprovados/              (subpasta com peças já aprovadas para reuso)
```

## Metadata obrigatória no topo de cada .md

Todo arquivo Markdown criado pelos agentes deve começar com frontmatter YAML:

```yaml
---
cliente: guilds
agente-produtor: copywriter
canal: linkedin-gustavo
formato: post
data-producao: 2026-04-22
status: draft | in-review | approved | published | rejected
skills-aplicadas: [posicionamento-guilds, tom-de-voz-guilds, copy-g-forge, anti-ia-signals, validacao-posicionamento]
issue-paperclip: GUI-14
autorizacao-cliente-usada: nivel-2-anonimizado
---

# [Título da peça]

[conteúdo]

---

## Rodapés de auditoria

[blocos de validacao-posicionamento + anti-ia-signals + client-authorization-check]
```

## Segurança e isolamento

### Bloqueadores absolutos
- ❌ Agente servindo cliente A NÃO lê `01-clients/<cliente-B>/` por default
- ❌ Agente NÃO escreve fora do cliente ativo a não ser que seja output da agência
- ❌ Agente NÃO delete em nenhum path (DELETE é manual, do CMO)
- ❌ `99-archive/` é read-only — nunca escrever lá diretamente

### Quando agente precisa ler outro cliente
- Exemplo: Competitive Intelligence quer saber qual case do cliente A se parece
  com cliente B que está analisando
- Escala ao Head of Marketing, que pode autorizar leitura cruzada específica
- Resultado fica anotado em `01-clients/<cliente-ativo>/memoria/decisoes/`

## Integração com outras skills

### Antes de produzir qualquer peça
1. `icp-validator` — confirma que audiência está dentro do ICP do cliente
2. `client-authorization-check` — confirma autorização de case se vai usar nome
3. `content-audit-channels` — verifica o que já foi publicado/programado

Essas skills agora usam o Drive como fonte:
- `icp-validator` lê `01-clients/<cliente>/knowledge-base/icp-audiencia/`
- `client-authorization-check` lê `01-clients/<cliente>/knowledge-base/cases-autorizados/<case>/autorizacao-*.pdf`
- `content-audit-channels` lê `01-clients/<cliente>/outputs/published/` últimos 14 dias

### Durante produção
4. `posicionamento-guilds` — lê `01-clients/<cliente>/knowledge-base/posicionamento/aprovados/`
5. `tom-de-voz-guilds` — regras gerais (a própria skill é o guia)
6. `copy-g-forge` — fórmulas gerais (a própria skill é o guia)

### Antes de entregar
7. `anti-ia-signals` — filtro final anti-tique
8. `validacao-posicionamento` — checklist 8 perguntas

## Quando for novo cliente

1. Duplicar `01-clients/_template-cliente/` e renomear pro slug (`01-clients/acme-corp/`)
2. Kickoff preenche `knowledge-base/posicionamento/aprovados/` com posicionamento do cliente
3. Audience Research popula `icp-audiencia/`
4. Digital Auditor popula `pesquisas-mercado/`
5. Copywriter começa a produzir em `outputs/drafts/`

## Output obrigatório

Quando aplicar esta skill, anexar ao log do agente:

```
Drive Workspace Check — [data]
Cliente ativo: [slug]
Operação: [leitura-KB | escrita-output | escrita-memoria | ...]
Path-alvo: [path exato]
Permissão verificada: [sim/não]
Veredicto: [prosseguir | escalar | erro]
```
