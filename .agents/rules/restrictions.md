---
description: O que o agente não pode fazer neste projeto
globs: []
alwaysApply: true
---

# O que não fazer
> leitor: agente

## Autoridade

- Não escreva ADR. Se encontrar uma decisão que precisa de um, descreva a decisão e as alternativas, e PARE. Quem decide é o time.
- Não contrarie o que está em docs/adr/. Se precisar contrariar, pare.
- Não responda por conta própria o que o PRD deixou ambíguo. Liste as perguntas e espere.
- Não escolha biblioteca que não esteja no ADR-001. Proponha e espere.

## Escopo

- Não altere arquivo fora do escopo da tarefa atual.
- Não gere scaffold automático de framework sem mostrar antes o que ele vai criar.
- Não escreva código sem antes alinhar com as regras do PRD e ADRs.

## Ritmo

- Não escreva código antes de um plano aprovado. Escreva o plano, mostre e espere.
- "Pode implementar" autoriza a execução da tarefa aprovada. Após implementar, rode os checks e avise o usuário.
- Não relate sucesso parcial. Se um check falhou, a tarefa não terminou.

## Produção

- O usuário é o responsável por criar branches, commits e PRs.
- Não rode deploy nem altere configuração da Vercel.
- Não toque no projeto Supabase remoto: nada de SQL, de alteração de schema ou de dado por lá. Tudo acontece no banco local/testcontainers.

## Precedência

- Se o código e a documentação discordarem sobre comportamento, a documentação está certa até que seja atualizada.
- Se uma regra de procedimento contrariar um ADR, PARE e avise. Não escolha um dos dois por conta própria.