# AGENTS.md — Instruções para Agentes de IA (Backend)

Este repositório contém a API do sistema de Empréstimo de Equipamentos Internos (**EMPREST.AI**).

---

## 1. Documentação de Referência Obrigatória
Antes de propor ou implementar qualquer funcionalidade, consulte:
- `docs/PRD.md`: Regras de negócio, personas e escopo da v1.
- `docs/adr/001-stack.md`: Decisões técnicas de arquitetura, stack, segurança e alternativas descartadas.

---

## 2. Stack e Tecnologias
- **Runtime:** Node.js LTS
- **Framework:** NestJS
- **Adapter HTTP:** Express via `@vendia/serverless-express` (instância cacheada)
- **Organização:** Por domínio (`src/modules/<dominio>/`)
- **Camadas:** Controller → Service → Repository
- **Validação de entrada:** Zod via `nestjs-zod`
- **Contexto de request:** `AsyncLocalStorage` com `tenant_id` e `user_id`
- **Contrato de API:** REST, com OpenAPI gerado dos schemas Zod, prefixo `/v1`, erros em RFC 9457 (Problem Details), paginação por cursor
- **Banco de dados & ORM:** PostgreSQL (Supabase) + Prisma (Prisma Migrate como dono único do schema)
- **Conexões:** Runtime via Supavisor (`porta 6543, ?pgbouncer=true&connection_limit=1`), Migrations via `directUrl` (`porta 5432`)
- **Multi-tenancy:** Discriminado por coluna (`tenant_id` em toda tabela de domínio), vínculo via tabela `memberships (user_id, tenant_id, role)`, tenant extraído do JWT
- **Autenticação & Autorização:** Supabase Auth (JWT validado via JWKS), autorização via Guards do Nest + CASL, RLS ativado em todas as tabelas (defesa em profundidade)
- **Testes:** Jest (unitário), Testcontainers com Postgres real (integração de banco), supertest (API)
- **Logs & Rastreamento:** pino em JSON (com `request_id` e `tenant_id`), Sentry
- **Segurança:** helmet, CSP restritiva, rate limit no Postgres, tabela de auditoria append-only, `service_role` key restrita à API

---

## 3. Regras de Negócio do Domínio (PRD)
- Limite de no máximo 3 itens simultâneos por colaborador.
- Prazo padrão de devolução de 14 dias.
- Usuários com item em atraso não podem solicitar novos empréstimos.
- Equipamento em manutenção não pode aparecer como disponível.
- Visão de empréstimos isolada por colaborador (cada um vê os seus); Operações visualiza todos os empréstimos em aberto e cadastra equipamentos.
- **Fora do escopo da v1:** Reserva com data futura, notificação por e-mail, importação de planilha, WebSockets/tempo real, filas/trabalhos assíncronos e rotinas periódicas/cron.

---

## 4. Diretrizes de Trabalho e Fluxo do Agente
1. **Schema do Prisma:** O agente **não deve aplicar migrations diretamente** nem alterar o schema sem validação prévia. Sempre proponha as alterações de modelo/schema e aguarde a aprovação do usuário antes de rodar migrations.
2. **Autonomia de Código:** O agente deve seguir estritamente as camadas (Controller → Service → Repository), tipagens estritas e validações via Zod.
3. **Validação e Testes:** Ao finalizar alterações/features, o agente **deve executar os testes/lints** e reportar os resultados ao usuário.
4. **Commits e PRs:** O gerenciamento de commits, branches e PRs é feito exclusivamente pelo usuário.
5. **Tecnologias Externas:** Não instalar pacotes ou ferramentas que contrariem as decisões e alternativas descartadas no ADR 001.

