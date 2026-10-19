---
description: O que precisa passar antes de declarar uma tarefa pronta
globs: []
alwaysApply: true
---

# Verificação de fim de tarefa (Backend)
> leitor: agente

## Quando
Sempre que você for dizer "pronto", "implementado" ou "funcionando".

## Procedimento
1. Rode os testes (`npm run test` / Jest e testes de integração). Cole a última linha da saída na resposta.
2. Se a tarefa tocou em schema/migration, certifique-se de que o Prisma Migrate rodou perfeitamente e o seed é executado sem erros.
3. Rode o build da aplicação (`npm run build`). Build que quebra na Vercel é o feedback mais lento e mais caro deste projeto.
4. Rode `git status --short`. Só podem aparecer arquivos do escopo da tarefa.
5. Diga qual critério de aceitação ou endpoint esta tarefa atende.

## Verificação
Pronto = os comandos de teste, validação de tipos e build terminaram sem falha E o git status não trouxe surpresa. As duas coisas, não uma.

## Não faça
- Não relate sucesso parcial. Teste vermelho é tarefa não terminada, mesmo que o código "esteja certo".
- Não tente consertar a mesma falha duas vezes seguidas sem me mostrar a saída do erro.
- Não rode teste contra o banco remoto.