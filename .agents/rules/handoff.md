---
description: Procedimento de encerramento e transição de contexto entre sessões
globs: []
alwaysApply: true
---

# Handoff entre sessões
> leitor: agente

## Quando
Ao encerrar uma sessão de trabalho longa, ao atingir o limite de contexto ou quando o operador solicitar transição de sessão.

## Procedimento
1. Resuma o que foi feito na sessão atual (arquivos modificados, funcionalidades entregues).
2. Indique o estado atual dos testes e checks (`npm run test`, `npm run build`, `git status`).
3. Liste pendências imediatas ou próximos passos para a próxima sessão.
4. Garanta que nenhum arquivo temporário ou incompleto quebre o build.
