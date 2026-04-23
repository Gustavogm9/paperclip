---
name: resumo-executivo
description: >
  Como escrever o resumo executivo semanal pro CMO Gustavo. Formato máximo 1
  página, leitura em 90 segundos, zero rodeio. Use toda sexta 17h após a review
  da sprint semanal — ou sempre que o CMO pedir status. Define estrutura,
  tom, o que incluir, o que cortar. O CMO tem tempo como restrição #1; resumo
  longo não é lido.
---

# Resumo executivo semanal — para o CMO Gustavo

## Princípio

Gustavo é fundador de múltiplas iniciativas simultâneas. Tempo é a restrição #1 dele. Se o resumo não couber em 90 segundos de leitura, ele não lê — e a semana seguinte começa sem input dele.

Regra: **1 página no máximo, 250–400 palavras, estrutura fixa.**

## Estrutura obrigatória

```markdown
# Resumo semana WW / YYYY (DD-MM a DD-MM)

## O que andou
[2–4 bullets. Cada bullet começa com verbo no passado. Cada um tem um número
ou evento concreto — nunca abstrato.]

## O que não andou
[1–3 bullets. Mesma regra. Explicar razão em 1 linha, não 5.]

## Decisões que preciso de você esta semana
[0–3 bullets. Cada bullet tem: pergunta específica + opções + recomendação
do Head of Marketing + prazo pra decidir.]

## Métricas da semana
[Se houver canais ativos: métrica + delta vs semana anterior. Se não houver,
escrever "sem canais ativos, próxima semana começamos medir X".]

## Próxima semana
[3 bullets. Entregas-chave da semana que vem. Sem detalhe tático.]
```

## Regras de estilo

- Sem adjetivos. "Bom", "ótimo", "excelente", "difícil" — cortar. Use números.
- Sem "acredito", "penso", "sinto". Use "recomendo", "proponho", "decidi".
- Sem jargão. Gustavo tem background em engenharia mecânica e gestão em enfermagem — fala português claro.
- Sem introdução. Primeiro caractere do documento já é informação útil.
- Sem encerramento. Último caractere é o último bullet.

## O que SEMPRE incluir

- Números concretos (entregas feitas, não feitas, dias)
- Nome do dono de cada entrega/bloqueio
- Decisões pendentes com prazo explícito
- Referência a artefatos (link ou path) quando relevante

## O que NUNCA incluir

- Processo interno ("reunimos os agentes", "alinhamos os outputs")
- Desculpas ou justificativas longas
- Roadmap futuro detalhado (Gustavo tem o roadmap de 90 dias, não precisa rever toda sexta)
- Agradecimentos ou fechamento amistoso
- Sumário do posicionamento, da fase, ou do projeto — ele conhece

## Exemplo de resumo bom

```
# Resumo semana 16 / 2026 (13/04 a 17/04)

## O que andou
- Publicado posicionamento aprovado — 1ª revisão do Brand Guardian, 100% conformidade
- Pauta Instagram semana 17: 4 posts aprovados, 1 em revisão
- Primeiro heartbeat do Head of Marketing rodou sexta 08h sem erro

## O que não andou
- LinkedIn Pessoal do CMO: sem post esta semana — aguardando autorização PostForMe
- Análise NEOPSICO case: bloqueada na coleta de números com a diretoria deles

## Decisões que preciso de você esta semana
1. LinkedIn Pessoal — autorizar PostForMe até ter? Recomendação: sim,
   publicação começa segunda. Prazo: responder até domingo 18/04 20h.
2. Brevo vs Mailerlite: recomendação Brevo (R$ 0 até 300 contatos, API simples).
   Prazo: segunda-feira.

## Métricas da semana
- Sem canais ativos. Segunda 20/04 começamos medir: impressões LinkedIn CMO,
  clicks no site, leads capturados via CTA Calendly.

## Próxima semana
- Lançar LinkedIn CMO (3 posts segunda, quarta, sexta)
- Fechar conta Brevo + importar 47 contatos do CRM atual
- Publicar primeiro case NEOPSICO se números liberarem
```

## Exemplo de resumo ruim (NÃO imitar)

```
# Resumo Semanal — Equipe de Marketing Guilds — 17 de Abril de 2026

Olá Gustavo! Espero que você esteja bem. Foi uma semana super produtiva pra
nossa equipe e gostaríamos de compartilhar com você tudo que aconteceu...

Primeiramente, quero agradecer o envolvimento de todos os agentes que se
dedicaram incansavelmente...

[continua por 3 páginas]
```

Erros: introdução vazia, agradecimento, "super produtiva" (adjetivo), promessa de "tudo que aconteceu" (nem tudo importa), comprimento.

## Como usar esta skill

1. Abra o review da sexta (já escrito pela skill sprint-semanal)
2. Extraia só o que cabe nas 5 seções
3. Passe pelo Brand Guardian pra sanity check
4. Salve em `outputs/reports/YYYY-WW_resumo-cmo.md`
5. Envie pro CMO via canal acordado (inicialmente: Slack/WhatsApp direto — quando houver MCPs, via Slack DM)
