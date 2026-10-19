# ADR 001 — Definição da Stack Tecnológica

- **Status:** Decidido
- **Data:** 2026-09-03
- **Contexto:** Definição da arquitetura técnica, ferramentas, runtime, persistência e infraestrutura para o sistema de Empréstimo de Equipamentos Internos.

---

## Decisões

| Item | Escolha |
|---|---|
| Repositórios — Estrutura | Dois repositórios: um para o front, um para a API |
| Repositórios — Projetos na Vercel | Dois, um por repositório |
| Repositórios — Compartilhamento de tipos | Nenhum pacote compartilhado; via OpenAPI gerado |
| Frontend — Linguagem | TypeScript em modo `strict` |
| Frontend — Biblioteca de UI | React |
| Frontend — Build e dev server | Vite |
| Frontend — Roteamento | React Router (data APIs) |
| Frontend — Estado de servidor | TanStack Query |
| Frontend — Estado de cliente | Zustand |
| Frontend — Formulários | React Hook Form + `zodResolver` |
| Frontend — Estilização | Tailwind CSS |
| Frontend — Componentes | shadcn/ui |
| Frontend — Cliente da API | Gerado a partir do `openapi.json` com orval |
| Backend — Runtime | Node.js LTS |
| Backend — Framework | NestJS |
| Backend — Adapter HTTP | Express via `@vendia/serverless-express`, com instância cacheada |
| Backend — Organização de pastas | Por domínio (`src/modules/<dominio>/`) |
| Backend — Camadas | Controller → Service → Repository |
| Backend — Validação de entrada | Zod via `nestjs-zod` |
| Backend — Contexto de request | `AsyncLocalStorage` com `tenant_id` e `user_id` |
| Contrato de API — Estilo | REST |
| Contrato de API — Fonte do contrato | OpenAPI gerado dos schemas Zod do Nest |
| Contrato de API — Distribuição | `openapi.json` publicado como artefato do CI da API |
| Contrato de API — Consumo | Front regenera o cliente por script, versionado no repositório |
| Contrato de API — Versionamento | Prefixo de rota `/v1` |
| Contrato de API — Formato de erro | RFC 9457 (Problem Details) |
| Contrato de API — Paginação de listas | Cursor |
| Contrato de API — Tempo real | Fora de escopo — Vercel não suporta WebSocket |
| Dados e persistência — Banco | PostgreSQL gerenciado pelo Supabase |
| Dados e persistência — ORM | Prisma |
| Dados e persistência — Dono do schema | Prisma Migrate (único) |
| Dados e persistência — Objetos não cobertos pelo Prisma | SQL bruto dentro das migrations do Prisma |
| Dados e persistência — Conexão de runtime | Supavisor, porta 6543, `?pgbouncer=true&connection_limit=1` |
| Dados e persistência — Conexão de migration | `directUrl`, porta 5432 |
| Dados e persistência — Seed | `prisma/seed.ts`, idempotente, cria o tenant `suporte_ti` |
| Multi-tenancy — Modelo | Tenant discriminado por coluna, banco único |
| Multi-tenancy — Coluna | `tenant_id` em toda tabela de domínio |
| Multi-tenancy — Vínculo usuário–tenant | Tabela `memberships (user_id, tenant_id, role)` |
| Multi-tenancy — Primeiro tenant | `suporte_ti`, criado no seed |
| Multi-tenancy — Origem do tenant no request | Claim do JWT, resolvido no guard, nunca do body |
| Autenticação e autorização — Provedor de identidade | Supabase Auth, e-mail e senha |
| Autenticação e autorização — Cadastro | Fechado, somente por convite de administrador |
| Autenticação e autorização — Sessão no navegador | Token no header, gerenciado pelo `supabase-js` |
| Autenticação e autorização — Domínio | `*.vercel.app`, um por projeto |
| Autenticação e autorização — Verificação de token na API | Nest valida o JWT via JWKS do Supabase |
| Autenticação e autorização — CORS | Allowlist com a origem do front, `credentials` habilitado |
| Autenticação e autorização — Fonte da verdade de autorização | Guards do Nest + CASL |
| Autenticação e autorização — RLS | Habilitado em todas as tabelas, deny by default |
| Autenticação e autorização — Papel do RLS | Defesa em profundidade, não autorização primária |
| Testes — Unitário no backend | Jest |
| Testes — Unitário no frontend | Vitest |
| Testes — Integração de banco | Testcontainers com Postgres real |
| Testes — Teste de API | supertest sobre a app Nest |
| Testes — E2E de interface | Playwright |
| Testes — Teste obrigatório de isolamento | Um caso por endpoint: tenant A não enxerga dado de tenant B |
| Testes — Verificação de contrato | CI do front falha se o cliente gerado divergir do `openapi.json` publicado |
| Testes — Meta de cobertura | Sem percentual; caminhos críticos obrigatórios |
| Hospedagem e operação — Hospedagem | Vercel (front e API, projetos separados) |
| Hospedagem e operação — Plano | Hobby |
| Hospedagem e operação — Região das functions | Padrão do Hobby (Estados Unidos) |
| Hospedagem e operação — Região do Supabase | `sa-east-1` (São Paulo) |
| Hospedagem e operação — Limite de execução | 60s por request (teto do Hobby) |
| Hospedagem e operação — Fila e trabalho assíncrono | Fora de escopo; tudo roda dentro do request |
| Hospedagem e operação — Agendamento | Fora de escopo; sem cron |
| Hospedagem e operação — Configuração | Variáveis de ambiente validadas com Zod no boot |
| Hospedagem e operação — Log | pino em JSON, com `request_id` e `tenant_id` |
| Hospedagem e operação — Rastreamento de erro | Sentry (API e front) |
| Hospedagem e operação — CI | GitHub Actions, um workflow por repositório |
| Hospedagem e operação — Migration em deploy | `prisma migrate deploy` em job do GitHub Actions, antes do deploy |
| Segurança — Cabeçalhos HTTP | helmet |
| Segurança — CSP | Restritiva, sem `unsafe-inline` |
| Segurança — Rate limit | Por IP e por usuário, com contador no Postgres |
| Segurança — Segredos | Environment variables da Vercel, fora do repositório |
| Segurança — `service_role` key do Supabase | Somente na API, nunca no bundle do front |
| Segurança — Auditoria | Tabela append-only com ator, tenant, ação e recurso |
| Qualidade de código — Lint e formatação | ESLint + Prettier, config replicada nos dois repositórios |
| Qualidade de código — Hook de pré-commit | lint-staged + husky, apenas lint e formatação |
| Qualidade de código — Convenção de commit | Nenhuma automação; mensagem escrita pela pessoa |

---

## Justificativas

### Repositórios
- **Estrutura (dois repositórios)**: Front e API têm ciclo de release e responsáveis diferentes; repositório separado deixa o histórico e as permissões separados também.
- **Projetos na Vercel (dois, um por repositório)**: Front e API rodam como projetos separados na Vercel, acompanhando o ciclo de vida e deploy de cada repositório.
- **Compartilhamento de tipos (sem pacote compartilhado)**: Publicar pacote npm privado e bumpar versão a cada campo alterado é atrito maior do que o ganho; o contrato atravessa via arquivo gerado.

### Frontend
- **Linguagem (TypeScript `strict`)**: Sem `strict` o tipo gerado da API não pega os casos de nulo, que são exatamente os que quebram em produção.
- **Biblioteca de UI (React)**: Já era a decisão; mantida.
- **Build e dev server (Vite)**: O app é uma SPA sem necessidade de renderização no servidor, então não preciso do peso de um framework full-stack.
- **Roteamento (React Router)**: Preciso de rotas aninhadas e proteção de rota por sessão; escrever isso na mão custa mais do que a curva da biblioteca.
- **Estado de servidor (TanStack Query)**: Com REST puro eu teria que reimplementar cache, revalidação, retry e estado de loading em cada tela; isso é a maior fonte de bug repetido em SPA.
- **Estado de cliente (Zustand)**: O estado que sobra depois do TanStack Query é pouco (UI, filtros, wizard), e não justifica uma store grande.
- **Formulários (React Hook Form + `zodResolver`)**: O schema Zod do formulário sai do mesmo OpenAPI, então a regra de validação de formato não é reescrita.
- **Estilização (Tailwind CSS)**: O design vem do Figma e precisa ser reproduzido de perto; biblioteca com visual próprio brigaria com isso.
- **Componentes (shadcn/ui)**: Copia o componente para dentro do repositório em vez de esconder atrás de API de biblioteca, então customizar não vira luta contra a dependência.
- **Cliente da API (gerado com orval)**: Cliente HTTP escrito à mão é onde o tipo da resposta é reescrito errado e ninguém percebe até a tela quebrar.

### Backend
- **Runtime (Node.js LTS)**: O mesmo TypeScript roda nos dois lados e a versão LTS me dá janela de suporte previsível.
- **Framework (NestJS)**: Já era a decisão; mantida. Injeção de dependência é o que torna o service testável sem subir a aplicação inteira.
- **Adapter HTTP (serverless com instância cacheada)**: Na Vercel o Nest não roda como processo; sem guardar a aplicação criada fora do handler, cada request paga o bootstrap do container de DI.
- **Organização de pastas (por domínio)**: Organizar por camada técnica (`controllers/`, `services/`) faz cada feature nova espalhar arquivos em quatro pastas distantes.
- **Camadas (Controller → Service → Repository)**: Substitui "MVC" da lista original: não existe View no servidor, o front é uma SPA separada. O Repository isola o Prisma para o service não depender de ORM.
- **Validação de entrada (Zod via `nestjs-zod`)**: É o que gera o OpenAPI a partir do mesmo schema que valida a entrada; com dois validadores, o documento gerado e a validação real divergem.
- **Contexto de request (`AsyncLocalStorage`)**: Passar `tenant_id` como parâmetro em toda assinatura de método é o tipo de coisa que alguém esquece uma vez e vira vazamento entre tenants.

### Contrato de API
- **Estilo (REST)**: Já era a decisão; mantida. O modelo de recurso casa com o CRUD que domina o app.
- **Fonte do contrato (OpenAPI via schemas Zod)**: ts-rest exige que os dois lados importem o mesmo pacote, o que não existe com repositórios separados. O OpenAPI atravessa a fronteira como arquivo.
- **Distribuição (`openapi.json` via CI)**: Publica o contrato da API como artefato para permitir consumo automatizado sem dependência direta de código.
- **Consumo (cliente gerado versionado no front)**: Deixa a mudança de contrato visível no diff do PR, que é o substituto possível para o build quebrar sozinho.
- **Versionamento (`/v1`)**: Adicionar versionamento depois que existe cliente em produção obriga a manter rota sem versão para sempre.
- **Formato de erro (RFC 9457)**: Sem formato único de erro, cada tela trata a falha de um jeito e o front acaba lendo string de mensagem.
- **Paginação de listas (cursor)**: Offset fica lento e duplica registro quando a lista recebe escrita concorrente.
- **Tempo real (fora de escopo)**: Function serverless não mantém conexão aberta; atualização de tela é polling do TanStack Query.

### Dados e persistência
- **Banco (PostgreSQL no Supabase)**: Já era a decisão; mantida. Traz Auth e Storage sem eu operar servidor de banco.
- **ORM (Prisma)**: Já era a decisão; mantida. Tipagem gerada a partir do schema é o que evita divergência entre modelo e código.
- **Dono do schema (Prisma Migrate como dono único)**: Prisma Migrate e Supabase CLI gerenciando o mesmo banco se sobrescrevem; ter dois donos de schema é como o ambiente diverge de produção sem ninguém notar.
- **Objetos não cobertos pelo Prisma (SQL bruto na migration)**: O Prisma não modela esses objetos, então eles precisam entrar na mesma linha do tempo versionada, não como script solto aplicado à mão.
- **Conexão de runtime (Supavisor)**: `connection_limit=1` é obrigatório em serverless: a Vercel escala instâncias em paralelo e cada uma abrindo pool próprio esgota a conexão do projeto.
- **Conexão de migration (`directUrl`)**: O pooler em transaction mode não suporta os comandos que a migration usa; sem os dois endpoints configurados, `prisma migrate deploy` falha em produção.
- **Seed (`prisma/seed.ts` idempotente)**: Seed que só funciona em banco vazio não serve para ambiente de teste que roda várias vezes.

### Multi-tenancy
- **Modelo (tenant discriminado por coluna, banco único)**: Schema por tenant multiplicaria cada migration pelo número de tenants; para um sistema interno o isolamento lógico basta.
- **Coluna (`tenant_id` em toda tabela)**: Tabela sem a coluna não tem como ser protegida por policy e vira o buraco por onde o dado vaza.
- **Vínculo usuário–tenant (tabela `memberships`)**: A mesma pessoa pode atuar em mais de uma área com papel diferente em cada; papel gravado no usuário não representa isso.
- **Primeiro tenant (`suporte_ti`)**: A estrutura existe desde o primeiro schema mesmo com um único tenant, porque adicionar `tenant_id` depois exige backfill e revisão de toda query que toca a tabela.
- **Origem do tenant no request (claim do JWT)**: Se o cliente manda o tenant no corpo ou na query, trocar o valor é toda a exploração necessária.

### Autenticação e autorização
- **Provedor de identidade (Supabase Auth com e-mail e senha)**: Não há domínio corporativo para federar; SSO fica fora de escopo.
- **Cadastro (fechado por convite)**: Sem domínio de e-mail para filtrar, cadastro aberto deixa qualquer pessoa que descubra a URL criar conta num sistema que guarda inventário de infraestrutura.
- **Sessão no navegador (token no header via `supabase-js`)**: `vercel.app` está na Public Suffix List, então o navegador proíbe cookie no domínio pai; sem domínio próprio, token no header gerenciado pelo SDK é o que resta.
- **Domínio (`*.vercel.app`)**: Um subdomínio por projeto na Vercel atende ao escopo sem custo de domínio customizado.
- **Verificação de token na API (JWKS)**: A API não pode confiar em header enviado pelo cliente; validar assinatura contra a chave pública fecha isso sem consultar o Supabase a cada request.
- **CORS (allowlist com a origem do front)**: Permite requisições apenas da origem autorizada com credentials habilitado.
- **Fonte da verdade de autorização (guards do Nest + CASL)**: As regras são por papel e por tenant ao mesmo tempo; `if (user.role === 'admin')` espalhado por controller não sobrevive à terceira regra.
- **RLS (habilitado em todas as tabelas)**: Se uma credencial vazar ou um endpoint esquecer o guard, a policy é a última barreira entre tenants.
- **Papel do RLS (defesa em profundidade)**: O Prisma conecta com role dono das tabelas e bypassa RLS; forçar RLS como primário exigiria abrir transação com `SET LOCAL` a cada request, onerando o pooler.

### Testes
- **Unitário no backend (Jest)**: Já era a decisão; é o padrão do Nest e o que os schematics geram.
- **Unitário no frontend (Vitest)**: Com Vite, o Jest exige configuração de transform paralela ao build; o Vitest usa o mesmo pipeline e a mesma config.
- **Integração de banco (Testcontainers com Postgres real)**: Mockar o Prisma testa o mock, não o banco. Constraint, cascade, transação e policy de RLS só falham contra Postgres de verdade.
- **Teste de API (supertest)**: Valida o contrato como o cliente vai consumir, incluindo guard, pipe de validação e filtro de exceção.
- **E2E de interface (Playwright)**: Os fluxos que travam a operação (login, abertura de chamado, cadastro de ativo) precisam ser testados no navegador.
- **Teste obrigatório de isolamento**: Vazamento entre tenants é a falha mais cara desse sistema e a mais fácil de introduzir sem perceber; precisa ser verificada por teste, não por revisão.
- **Verificação de contrato (CI do front)**: Com repositórios separados, nada quebra sozinho quando a API muda; essa checagem é o substituto do build compartilhado.
- **Meta de cobertura (sem percentual)**: Meta de cobertura produz teste escrito para subir número; caminho crítico é critério verificável.

### Hospedagem e operação
- **Hospedagem (Vercel)**: Já era a decisão; mantida, e a conta já existe com outros projetos.
- **Plano (Hobby)**: Cobre uso didático não-comercial sem custo; se o sistema for para uso real na empresa, o plano precisa mudar antes.
- **Região das functions (padrão do Hobby / EUA)**: São Paulo só existe no Pro; no Hobby cada query paga a ida e volta transatlântica, o que é aceitável apenas para demonstração.
- **Região do Supabase (`sa-east-1` / São Paulo)**: Mantém os dados no Brasil próximos dos usuários locais.
- **Limite de execução (60s)**: Vira o teto de qualquer operação: importação de planilha, sincronização e relatórios devem ser desenhados em lotes que caibam nesse tempo.
- **Fila e trabalho assíncrono (fora de escopo)**: Não há volume assíncrono conhecido agora; adicionar fila sem caso de uso é custo sem retorno, logo chamadas externas rodam no request.
- **Agendamento (fora de escopo)**: Não há rotinas periódicas ou cron necessárias no escopo atual.
- **Configuração (env validado com Zod)**: Falhar na subida é melhor que `undefined` virando comportamento silencioso em produção.
- **Log (pino em JSON com `tenant_id`)**: Investigar incidente em sistema multi-tenant sem poder filtrar por tenant é procurar no escuro.
- **Rastreamento de erro (Sentry)**: Sem captura de exceção, o erro só é descoberto pelo usuário reclamando.
- **CI (GitHub Actions)**: Um workflow por repositório para desacoplar validação de front e API.
- **Migration em deploy (job no CI)**: Em serverless várias instâncias sobem em paralelo e tentariam migrar ao mesmo tempo; rodar no CI garante execução única.

### Segurança
- **Cabeçalhos HTTP (helmet)**: Cabeçalho de segurança ausente é achado de pentest previsível e barato de evitar.
- **CSP (restritiva, sem `unsafe-inline`)**: Com o token acessível ao JavaScript, a CSP é a principal defesa contra roubo de sessão.
- **Rate limit (no Postgres)**: Throttler em memória não funciona em serverless porque cada instância tem contador próprio e o limite nunca é atingido.
- **Segredos (env vars da Vercel)**: Credenciais ficam fora do repositório e injetadas pela plataforma.
- **`service_role` key do Supabase (somente na API)**: Essa chave ignora RLS; no bundle do front ela daria acesso total ao banco para qualquer visitante.
- **Auditoria (tabela append-only)**: Sistema de TI precisa responder quem mudou o quê; retrofitar log de auditoria depois não recupera o passado.

### Qualidade de código
- **Lint e formatação (ESLint + Prettier)**: Com repositórios separados não há pacote comum; a duplicação é aceita e a divergência é resolvida na revisão.
- **Hook de pré-commit (lint-staged + husky)**: Barra o erro trivial antes do CI sem interferir na mensagem de commit.
- **Convenção de commit (sem automação)**: A mensagem é responsabilidade de quem commita; validação automática seria cerimônia sem changelog gerado para justificar.

---

## Alternativas descartadas

| Alternativa | Motivo do descarte |
|---|---|
| Monorepo com pacote de contrato compartilhado | Contraria a decisão de repositórios separados |
| ts-rest | Exige que os dois lados importem o mesmo pacote, que não existe com repositórios separados |
| Pacote npm privado com os tipos | Bump de versão a cada campo alterado é atrito maior que o ganho |
| RLS como autorização primária | O Prisma conecta com role dono da tabela e bypassa RLS; fazer valer exigiria transação com `SET LOCAL` por request |
| Front falando direto com o Supabase, sem API | Tira o lugar onde regra de negócio e segredo de integração podem viver, e faria a tela driblar a autorização por tenant |
| Cadastro aberto por e-mail | Sem domínio corporativo para filtrar, qualquer pessoa com a URL criaria conta |
| SSO corporativo (OIDC/SAML) | Não há e-mail corporativo para federar |
| Cookie `httpOnly` para a sessão | `vercel.app` está na Public Suffix List; sem domínio próprio o cookie não atravessa do front para a API |
| Domínio próprio com subdomínios | Custo e configuração que o escopo da disciplina não justifica |
| Supabase CLI como dono das migrations | Dois donos de schema no mesmo banco se sobrescrevem |
| BullMQ, pg-boss ou qualquer fila | Sem volume assíncrono conhecido; e worker de vida longa não roda na Vercel |
| Vercel Cron | Sem caso de uso agendado no escopo atual |
| Schema ou banco por tenant | Multiplicaria cada migration pelo número de tenants sem exigência regulatória que justifique |
| `@nestjs/throttler` em memória | Contador por instância não limita nada em ambiente que escala horizontalmente |
| tRPC | Fecha a porta para consumidor não-TypeScript; REST foi decidido antes |
| GraphQL | Custo de schema, resolver e cache não se paga no volume de telas atual |
| Cliente HTTP escrito à mão | Reescrever o tipo da resposta anula o ganho de TypeScript nas duas pontas |
| `class-validator` | Não gera o OpenAPI a partir do mesmo schema que valida a entrada |
| Prisma mockado nos testes de repositório | Testa o mock; constraint, transação e policy não são exercitadas |
| Jest no frontend | Exige pipeline de transform paralelo ao do Vite |
| Redux Toolkit | O estado de cliente restante é pequeno demais para o boilerplate |
| Biblioteca de componentes fechada (MUI, Mantine) | O design vem do Figma e precisaria ser imposto por cima do visual da biblioteca |
| Next.js | Não preciso de SSR; teria dois backends no mesmo projeto |
| VPS ou container (Fly, ECS) para a API | Resolveria região, worker, WebSocket e uso justo, mas contraria a decisão de hospedagem |

---

## Consequências

### O que fica mais fácil
- Permissão, histórico e release do front e da API ficam separados.
- Testar service sem subir a aplicação, e testar repositório contra banco real.
- Auditar autorização: a decisão está em um lugar (CASL), não espalhada em `if`.
- Deploy: push na branch, sem pipeline de container para manter.
- Custo de infraestrutura próximo de zero enquanto o volume for baixo.

### O que fica mais difícil
- Mudança de contrato não quebra o build do front sozinha; depende de regenerar o cliente e da checagem no CI.
- Alterar uma feature que toca os dois lados exige dois PRs coordenados em repositórios diferentes.
- Latência: com as functions nos EUA e o banco em São Paulo, cada query paga a travessia.
- Cold start: a primeira invocação depois de ociosidade paga o bootstrap do Nest.
- Qualquer operação precisa caber em 60s, o que obriga a desenhar importação e relatório em lotes.
- Envio de e-mail e integração externa seguram a resposta do request.
- Manter guards e RLS coerentes exige disciplina — policy desatualizada dá falsa sensação de proteção.
- O token de sessão fica acessível ao JavaScript, então qualquer XSS ou dependência comprometida vira sequestro de sessão; a CSP é a única barreira.
- Config de lint duplicada nos dois repositórios pode divergir sem ninguém notar.

### O que isso nos impede de fazer depois sem custo
- Qualquer funcionalidade com conexão aberta (notificação em tempo real, terminal remoto, streaming de log): a Vercel não suporta WebSocket.
- Processamento longo (importação grande, varredura de rede, relatório pesado): estoura o limite de execução.
- Trabalho agendado ou assíncrono: exige introduzir fila e um lugar para o worker rodar, que não é a Vercel.
- Deixar o front falar direto com o Supabase para uma tela específica: essa tela passa a driblar a autorização por tenant.
- Trocar Prisma por outro ORM: as migrations e o SQL de RLS estão dentro do Prisma Migrate.
- Sair do Supabase: Auth, banco e políticas estão acoplados ao projeto.
- Adicionar `tenant_id` a uma tabela criada sem ele: exige backfill e revisão de toda query que a toca.
- Federar com identidade corporativa depois: exige migrar os usuários já cadastrados por e-mail e senha.
- Trocar para cookie `httpOnly`: exige domínio próprio, mover o login para dentro do Nest e refazer o tratamento de CORS e CSRF.
- Unir os repositórios depois: histórico separado e dependências divergentes tornam a junção um trabalho, não um comando.

> **Contexto de uso:** O plano Hobby só vale enquanto o projeto for didático. Se a empresa passar a usar o sistema, é preciso migrar para Pro antes, porque a conta hospeda outros projetos e a exposição seria de conta, não de projeto.

---

## O que este ADR não decide

- Modelagem de domínio, entidades e relacionamentos.
- Design system, tokens e identidade visual.
- Papéis e matriz de permissão dentro de cada tenant.
- Provisionamento de tenant: quem cria, como se convida usuário.
- Provedor de e-mail transacional e demais integrações.
- Estratégia de backup, retenção e plano de recuperação.
- Ambientes (quantos, como são promovidos) e política de branch.
- Feature flags.
- Observabilidade além de log e erro (métrica, tracing distribuído).
- LGPD: base legal, política de retenção e fluxo de exclusão de dados.
- SLO, meta de latência e orçamento de custo.

