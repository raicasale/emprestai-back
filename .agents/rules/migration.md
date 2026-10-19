---
description: Procedimento para qualquer mudança de schema e migrations
globs: ["prisma/schema.prisma", "prisma/migrations/**"]
alwaysApply: false
---

# Mudança de schema
> leitor: agente

## Quando
Qualquer tarefa que precise criar, alterar ou remover tabela, coluna,
índice, constraint ou política de acesso (RLS) — inclusive quando a mudança
parecer trivial.

## Procedimento
1. Antes de gerar qualquer coisa: escreva a proposta do modelo no `schema.prisma` (e SQL de RLS se aplicável) na resposta e PARE. Eu aprovo ou corrijo.
2. Gere a migration pelo Prisma Migrate: `npx prisma migrate dev --name <nome>`. Uma migration por tarefa.
3. Toda tabela nova nasce com Row Level Security habilitada e pelo menos uma policy explícita via SQL bruto dentro da migration do Prisma. Tabela sem policy não entra no repositório.
4. Se a tabela já tem dado, descreva o que acontece com as linhas existentes. Coluna obrigatória nova precisa de default ou de um passo de preenchimento.
5. Aplique e verifique se o banco e o seed sobem sem falhas (`npx prisma migrate reset` / `npm run test`).

## Verificação
`npx prisma migrate reset` (ou subir banco limpo de teste via Testcontainers) aplica todas as migrations do zero e roda o seed, sem erro e sem nenhum passo manual.

## Não faça
- Não altere schema pelo Studio nem por SQL avulso. O Prisma Migrate é o único dono do schema.
- Não edite migration que já foi para o repositório remoto. Escreva a próxima.
- Não toque no projeto Supabase remoto. Tudo acontece no banco local/testcontainers.