---
description: Fluxo do ciclo de vida de uma spec (SDD) e regras para declarar pronta
globs: ["docs/specs/**"]
alwaysApply: true
---

# Fluxo de Desenvolvimento Guiado por Especificação (Spec-Flow)
> leitor: agente

## Ciclo de Vida da Spec (SDD)
1. **Requisito:** `spec.md` com Critérios de Aceitação (CA) bem definidos e identificados (ex: CA-01, CA-02).
2. **Plano:** `plan.md` estruturado e validado contra ADRs e restrições.
3. **Tarefas:** `tasks.md` dividindo o plano em passos atômicos e ordenados.
4. **Implementação & Testes:** Código implementado com testes que citam explicitamente o ID de cada CA.
5. **Verificação:** Execução dos checks e validação independente.

## Antes de declarar uma spec pronta
- Delegue ao subagente verificador-spec (agents/verificador-spec.md), passando o caminho da spec e o intervalo de commits (ou lista de arquivos/tudo que implementa a spec).
- A spec só é pronta com "Veredito: PRONTA". Qualquer outro resultado volta para as tarefas — quem corrige é o agente principal, nunca o verificador.

