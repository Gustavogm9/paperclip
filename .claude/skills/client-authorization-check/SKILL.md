---
name: client-authorization-check
description: >
  Bloqueia uso de nome real de cliente em peça pública sem autorização escrita
  documentada. Regra absoluta: se a peça cita cliente por nome (NEOPSICO, Scavaseg,
  etc.), precisa ter autorização assinada no caminho references/autorizacoes-cases/
  OU anonimizar. Use SEMPRE antes de produzir peça que mencione case real de cliente.
---

# Client Authorization Check — regra absoluta

Usar nome real de cliente sem autorização escrita é risco legal, reputacional e
contratual. Esta skill é **gate absoluto** — sem passar nela, peça não vai
publicação.

## 3 níveis de referência de case

### Nível 1 — CASE COM AUTORIZAÇÃO ESCRITA
- Cliente assinou documento autorizando uso específico (nome + números + setor)
- Documento está em `references/autorizacoes-cases/<cliente>/autorizacao-YYYYMMDD.pdf`
- Autorização é válida para o tipo de peça (LinkedIn público, email, landing, etc.)
- ✅ Pode usar nome real, números reais, setor real

### Nível 2 — CASE ANONIMIZADO
- Sem autorização escrita OU autorização não cobre tipo de peça
- Obrigatório:
  - Remover nome da empresa
  - Descrever perfil genérico mas reconhecível ("gestora de SST multi-site do
    interior de SP com 80 colaboradores")
  - Arredondar ou substituir números por faixas ("adoção mais que dobrou em
    um mês" em vez de "30% para 90% em 30 dias")
  - Não incluir detalhes que identifiquem (ex.: "primeiro case em SST da
    cidade" — identifica)
- ✅ Pode publicar sem autorização

### Nível 3 — ESTATÍSTICA DE MERCADO
- Não cita case específico
- Usa tendência documentada ou estudo público
- Requer fonte ("Gartner 2024 mostra que...", "estudo da FIA Business School...")
- ✅ Pode publicar com fonte

## Processo obrigatório antes de produzir

1. A peça cita cliente por nome? Se NÃO → continue normal
2. Se SIM → verificar:
   a. Existe `references/autorizacoes-cases/<cliente>/autorizacao-*.pdf`?
   b. Autorização cobre o canal da peça (ex.: "LinkedIn público")?
   c. Autorização cobre o tipo de dado citado (ex.: "números de adoção 2024")?
3. Se TODOS os 3 itens do passo 2 = sim → Nível 1, usar nome real
4. Se qualquer NÃO → Nível 2 (anonimizar) ou escalar ao Head of Marketing

## Bloqueadores absolutos

Independente de autorização, NUNCA publicar:

- ❌ Nome de pessoa física do cliente (CEO, CFO por nome) sem autorização específica
- ❌ Screenshots de tela/sistema do cliente sem autorização específica
- ❌ Números financeiros (receita, lucro, faturamento) do cliente
- ❌ Informações que violem confidencialidade contratual
- ❌ Comparação direta com concorrente do cliente

## Cases atualmente autorizados (quando atualizar, revalidar)

| Cliente | Autorização? | Escopo | Expira |
|---|---|---|---|
| NEOPSICO | ❌ não | — | — |
| Scavaseg | ❌ não | — | — |

**Ação pendente do CMO**: pedir autorização formal para NEOPSICO e Scavaseg, ou
operar exclusivamente com anonimização desses cases até autorização chegar.

## Anonimização — padrões aprovados

### Case NEOPSICO (SST, gestão de risco)
Perfil anonimizado:
- "Gestora de risco ocupacional multi-site do interior paulista, 80+ colaboradores"
- "Operação de SST com ~100 profissionais em campo"
- Números: "adoção mais que dobrou no primeiro mês" (em vez de 30%→90%)
- Mecanismo: "design participativo com equipe de campo antes da primeira linha
  de código"

### Case Scavaseg (corretora de seguros, automação financeira)
Perfil anonimizado:
- "Corretora de seguros PME com operação financeira manual"
- "Operação de seguros com 50+ colaboradores no back-office"
- Números: "fluxo financeiro automatizado em semanas"
- Mecanismo: "implementação acompanhada até conciliação rodar sozinha"

## Output obrigatório

Quando aplicar esta skill, anexar ao rodapé da peça:

```
Client Authorization Check — [data]
Cita cliente por nome? [sim / não]
Se sim, cliente: [nome]
Autorização encontrada? [sim + path | não]
Escopo cobre peça? [sim | não | N-A]
Nível aplicado: [1 autorizado / 2 anonimizado / 3 estatística]
Veredicto: [publicar | reescrever para anonimizar | escalar ao Head]
```

## Integração com outras skills

Roda **antes** de `copy-g-forge` (evita escrever peça inteira pra depois descobrir
que precisa anonimizar). Se Nível 2, Copywriter sabe desde o briefing que
anonimiza.

## Quando escalar ao Head of Marketing

- Cliente pede que paremos de citar mesmo anonimizado
- Autorização está próxima de expirar
- Peça precisa de informação que nenhuma autorização cobre
- Dúvida sobre se anonimização é suficiente (caso borderline)
