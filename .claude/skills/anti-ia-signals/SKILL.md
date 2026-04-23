---
name: anti-ia-signals
description: >
  Remove sinais óbvios de texto gerado por LLM antes de qualquer peça ser entregue.
  LLMs têm tiques de escrita (travessão longo, "não apenas X mas também Y", frases
  paralelas simétricas demais, clichês de copy genérico) que leitor treinado
  identifica em segundos. Use SEMPRE antes de marcar peça como pronta. Complementa
  tom-de-voz-guilds e copy-g-forge.
---

# Anti-IA Signals — Guilds

Leitor sofisticado do ICP Guilds (Diretor Ops, CEO, CFO de PME) reconhece texto
de IA em 5 segundos. Quando reconhece, o crédito da peça cai. Esta skill é o
filtro anti-tique.

## Tiques de LLM — REMOVA TODOS

### 1. Travessão longo em excesso (—)

Esse é o tique #1 do Claude e do GPT. Use com parcimônia extrema.

❌ **Proibido**: mais de **1 travessão longo por parágrafo**. Mais de **3 em peça de 150 palavras**.
❌ **Proibido**: travessão longo como pausa dramática padrão ("Fizemos X — e o resultado foi Y").
✅ **Permitido**: usar vírgula, ponto, ou dois-pontos no lugar.

**Antes (IA)**:
> "A NEOPSICO tinha 30% de adoção — e subiu para 90% em um mês — graças ao G-FORGE™ — uma metodologia que combina ciência comportamental — design participativo — e acompanhamento pós-implantação."

**Depois (humano)**:
> "A NEOPSICO tinha 30% de adoção. Em um mês, subiu para 90%. Como? G-FORGE™: ciência comportamental aplicada, design feito com a equipe de campo, acompanhamento até o último colaborador estar usando."

### 2. "Não apenas X, mas também Y"

Giveaway clássico. Use no máximo 1x por peça de 300+ palavras. Zero em peças curtas.

❌ "Não apenas implementamos, mas também acompanhamos."
✅ "Implementamos. E acompanhamos."
✅ "Implementação não é o fim, é metade do trabalho."

### 3. Paralelismo artificial

LLMs amam estruturas paralelas simétricas. O leitor humano usa variação.

❌ "Nós desenhamos sistemas. Nós implementamos processos. Nós acompanhamos adoção."
✅ "Desenhamos o sistema com a equipe, implementamos em semanas, e ficamos até todo mundo estar usando."

### 4. Clichês de copy genérico

Esses estão **proibidos** em peças Guilds:

- "Em um mercado cada vez mais competitivo..."
- "No cenário atual..."
- "Em última análise..."
- "No fim das contas..."
- "Vale ressaltar que..."
- "Cabe destacar..."
- "É importante salientar..."
- "Imagine por um momento..."
- "E se eu te dissesse que...?"
- "Você já parou para pensar...?"
- "A chave para o sucesso é..."
- "O segredo está em..."
- "Transforme sua [empresa/negócio/vida]..."
- "Destrave o potencial..."
- "Desmistificando..."
- "Desbloqueie..."
- "Potencialize..."
- "Alavanque..."

### 5. Abertura-pergunta retórica

Tique LinkedIn clássico. Proibido.

❌ "Você sabia que 70% dos projetos digitais falham por falta de adoção?"
❌ "E se eu te dissesse que dobrar a adoção é possível?"
✅ "70% dos projetos digitais morrem por falta de adoção. A NEOPSICO inverteu isso."

### 6. Emoji em posição de âncora (LinkedIn)

LLMs usam emoji no início de bullets ou para estruturar seções. Guilds NÃO usa.

❌
```
⚡ Rápido: entrega em semanas
🔧 Prático: metodologia aplicada
📊 Mensurável: ROI em 90 dias
```

✅ Texto corrido. Se usar bullet, sem emoji.

### 7. Estruturas listinha-de-três

"Três coisas mudaram: A, B, e C." Quando é real, ok. Quando é força de lista, remove.

❌ "Três pilares fazem adoção acontecer: cultura, sistema e acompanhamento."
✅ "Adoção acontece quando o sistema nasce junto com a equipe que vai usar."

### 8. Frase de fechamento tipo sermão

❌ "No final, adoção não é sobre tecnologia, é sobre pessoas."
❌ "Porque no fundo, todo projeto digital é um projeto humano."
✅ Encerra com ação concreta: "Agende 30 min, sai com diagnóstico do seu projeto parado."

### 9. Explicação tautológica

LLM repete a mesma ideia em palavras diferentes achando que está enriquecendo.

❌ "A metodologia G-FORGE garante adoção. Ela é um método que assegura que as pessoas usem o sistema. Com G-FORGE, você tem certeza que a equipe vai adotar a ferramenta."
✅ "G-FORGE garante adoção por método, não por sorte."

### 10. Uso excessivo de "real"/"verdadeiro"/"genuíno"

"Adoção real", "resultado verdadeiro", "impacto genuíno" — LLM usa pra dar peso. Humano confia na palavra base.

❌ "Entregamos resultado real, com impacto verdadeiro e adoção genuína."
✅ "Entregamos adoção. Com número medido antes e depois."

## Checklist antes de marcar peça como pronta

- [ ] Contei travessões longos — ≤ 1 por parágrafo, ≤ 3 em peça de 150 palavras?
- [ ] Removi "não apenas X mas também Y"?
- [ ] Variei estrutura das frases (não tem 3+ frases seguidas com mesmo padrão)?
- [ ] Nenhum clichê da lista (#4) aparece?
- [ ] Nenhuma pergunta retórica de abertura?
- [ ] Zero emoji em posição de âncora/bullet?
- [ ] Zero estrutura listinha-de-três forçada?
- [ ] Fechamento tem ação concreta, não sermão?
- [ ] Removi frases redundantes que só repintam a mesma ideia?
- [ ] Frequência de "real/verdadeiro/genuíno" ≤ 1x por peça?

Se qualquer [ ] está vazio, **reescreva antes de marcar como pronta**.

## Teste rápido (30 segundos)

Leia em voz alta. Se soar como:
- LinkedIn coach profissional → reescreve
- Artigo de blog genérico → reescreve
- "Guru" motivando equipe → reescreve
- Gestor experiente explicando pro colega → OK

## Integração com outras skills

Esta skill roda **depois** de `copy-g-forge` e **antes** de `validacao-posicionamento`.

Ordem de aplicação no Copywriter:
1. `posicionamento-guilds` — substância
2. `tom-de-voz-guilds` — voz
3. `copy-g-forge` — estrutura/fórmulas
4. `anti-ia-signals` — filtro anti-tique ← ESTA SKILL
5. `validacao-posicionamento` — checklist final

## Output obrigatório

Quando aplicar esta skill, anexar ao rodapé da peça:

```
Anti-IA Audit — [data]
Travessões longos: [contagem]
Clichês removidos: [sim/não, se sim, lista]
Perguntas retóricas: [0 / N]
Emoji em bullet: [0 / N]
Voz: [leitura em voz alta aprovada?]
Veredicto: [aprovado / reescrever]
```
