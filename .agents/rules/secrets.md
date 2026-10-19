---
description: Onde cada variável de ambiente vive e qual chave usar
globs: ["**/.env*", "src/config/**", "prisma/**"]
alwaysApply: false
---

# Variáveis de ambiente e chaves (Backend)
> leitor: agente

## Quando
Ao criar ou usar qualquer variável de ambiente, ao instanciar clientes de banco/serviços, ou ao escrever código que lê configuração (`src/config/`).

## Procedimento
1. **Chave pública / JWKS:** O Nest valida tokens JWT do Supabase Auth via JWKS.
2. **Chave de serviço (`service_role`):** Ignora todas as políticas (RLS). Vive exclusivamente no backend/API, **nunca** no bundle do frontend.
3. **Strings de Conexão do Banco:**
   - Runtime: Supavisor (`porta 6543, ?pgbouncer=true&connection_limit=1`) via `DATABASE_URL`.
   - Migration: Conexão direta (`porta 5432`) via `DIRECT_URL`.
4. **Variável nova existe em TRÊS lugares ou em nenhum:**
   - `.env.local` / `.env` (desenvolvimento local)
   - `.env.example` (versionado, sem valores reais)
   - Painel da Vercel / Environment Variables (preview e production).
5. Ao criar uma variável, valide-a obrigatoriamente no boot da aplicação com schema **Zod** e avise na resposta o que precisa ser configurado no painel da Vercel.

## Verificação
- `.env.example` contém todas as chaves que o projeto usa, sem nenhum valor sensível.
- A validação Zod no boot falha imediatamente caso alguma variável obrigatória esteja ausente.

## Não faça
- Não escreva valores reais de segredos ou chaves em respostas, commits, logs ou comentários.
- Não crie variável apenas no ambiente local.
- Não faça bypass de validações ou permissões sem usar o fluxo oficial.

