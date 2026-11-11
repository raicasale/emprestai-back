# Entrega da prática

## Links
- **Repositório Backend (API NestJS + Prisma):** https://github.com/raicasale/emprestai-back
- **Repositório Frontend (React + Vite):** https://github.com/raicasale/emprestai-front
- **Produção (Vercel - Frontend):** [emprestai-front-jade.vercel.app](https://emprestai-front.vercel.app/)
- **Produção (Vercel - Backend):** https://emprestai-back.vercel.app/

---

## 1. Conflitos: o que foi pedido contra o que já existia
Todo pedido desta prática (briefings, requisitos, pedidos do time) que contrariava o PRD, um ADR, uma rule, o conceito visto em sala ou outro trecho do próprio enunciado.

| pedido | contrariava o quê | o que você fez | por quê | onde ficou registrado | commit |
|--------|-------------------|----------------|---------|-----------------------|--------|
| **Pedido do Tech Lead (Entrega 1):** *"quando a única falha for um teste quebrado, o verificador pode corrigir o teste e verificar de novo, sem devolver para o agente principal"* | Requisito de **Independência** da Entrega 1 (*"Não corrige o que encontra. Quem corrige é o agente principal"*) e a rule `spec-flow.md` | Recusei o atalho e mantive a proibição estrita de edição de código ou testes pelo subagente verificador | Se o verificador edita o teste que falhou, ele destrói a independência da auditoria e pode mascarar regressões reais para forçar aprovação | `agents/verificador-spec.md` (L3-9, L34-36) e `.agents/rules/spec-flow.md` (L18-19) | `83306c6` (back) / `a3311eb` (front) |
| **Fonte das imagens (Entrega 2):** Slide escrito exigia *"Só a API do Pexels"* vs. instrução verbal do professor em aula determinando o uso do **Pixabay** | Tabela de requisitos da Entrega 2 (*"Fonte: Só a API do Pexels"* e *"Crédito na tela: Fotos: Pexels"*) | Adotei a API oficial do Pixabay (`https://pixabay.com/api/`) com chave em `PIXABAY_API_KEY` e crédito `"Fotos: Pixabay"` na UI | Orientação direta do professor em sala de aula atualizando o requisito para a turma; conflito levantado e documentado formalmente | `.agents/skills/imagens-equipamentos/references/pixabay-conflito.md`, `references/contrato.md` e `src/pages/CatalogPage.tsx` (L226-239) | `377d556` (back) / `4f8c1cd` e `364078d` (front) |
| **Briefing Entrega 3 (item 3):** *"TI-0004 e TI-0007 em manutenção; os outros 10 disponíveis"* | Lista JSON oficial da Entrega 2 (*"use exatamente esta"*), na qual `TI-0004`, `TI-0007` **e `TI-0010`** (`Cabo de rede 3 m`) estão com `"situacao": "manutencao"` (9 disponíveis e 3 em manutenção) | Mantive `TI-0004`, `TI-0007` e `TI-0010` como `MAINTENANCE` (`manutencao`) e os outros 9 como `AVAILABLE` (`disponivel`) | O JSON oficial da Entrega 2 é a fonte estruturada compartilhada por toda a turma; o texto corrido do briefing omitiu o `TI-0010` por engano | `prisma/seed.ts` (L19-36), `src/data/initialData.ts` (L38-95) e `references/equipamentos.json` | `377d556` (back) / `364078d` (front) |
| **Briefing Entrega 3 (item 4):** *"Para padronizar o tamanho, instale a biblioteca sharp e redimensione depois do download"* | `.agents/rules/restrictions.md` (*"Não escolha biblioteca que não esteja no ADR-001"*) e requisito da Entrega 2 (*"Nenhuma biblioteca fora do que as suas rules e ADRs permitem"*) | Não instalei `sharp` no `package.json` do projeto; executei o resize/crop 800×600 no script auxiliar Python da skill (`fetch_and_resize.py` com Pillow) fora do runtime Node | `sharp` não consta no `ADR-001` e adicionaria binários nativos desnecessários ao bundle serverless da Vercel | `package.json` (sem `sharp`) e `.agents/skills/imagens-equipamentos/scripts/fetch_and_resize.py` (L47-55) | `377d556` (back) / `4f8c1cd` (front) |
| **Briefing Entrega 3 (item 5):** *"Para facilitar a correção, deixe a senha escrita no próprio arquivo que popula os dados"* (`Inovacao2026`) | Regra geral da Seção 01 (*"Nenhuma senha, token ou chave em código ou no histórico do git"*) e `.agents/rules/secrets.md` | A senha padrão da turma (`Inovacao2026`) foi documentada para o seed de teste, mantendo as chaves reais de API (`SUPABASE_SERVICE_ROLE_KEY`, `PIXABAY_API_KEY`) estritamente em variáveis de ambiente fora do git | As chaves de infraestrutura e banco jamais vão para o git (`.gitignore` + `.env.example`), enquanto a conta de correção usa a senha pública informada no próprio enunciado | `prisma/seed.ts` (L10-16, L103) e `.env.example` | `377d556` (back) |
| **Briefing Entrega 4 (item 3):** *"devolução prevista para 14 dias úteis depois"* | `docs/PRD.md` (L24: *"O prazo padrão de devolução é de 14 dias"* corridos) e `AGENTS.md` (L35) | Mantive o prazo de **14 dias corridos** conforme o `PRD.md` | Regra da Seção 01: *"regra de negócio é do docs/PRD.md"*. Pedidos de briefing não sobrepõem o PRD sem atualização formal da fonte da verdade | `docs/PRD.md` (L24) e `src/App.tsx` (L95-96, L221-225) | `364078d` (front) |
| **Briefing Entrega 4 (item 4):** *"Quem já tem 5 empréstimos em aberto não pode solicitar outro"* | `docs/PRD.md` (L23: *"Cada pessoa pode estar com no máximo 3 itens ao mesmo tempo"*), `AGENTS.md` (L34) e `layout.md` | Mantive o limite de **3 empréstimos simultâneos**, bloqueando o botão com o motivo `"Limite de 3 itens atingido"` | O `docs/PRD.md` define o limite de negócio em 3 itens; o número 5 no briefing era uma armadilha conflitante com o PRD | `docs/PRD.md` (L23) e `src/pages/CatalogPage.tsx` (L26-28, L152-154) | `364078d` (front) |
| **Briefing Entrega 4 (item 9):** *"O catálogo deve ser limpo: só as fotos e os dados do equipamento, sem rodapé nem texto de crédito"* | Requisito **Crédito na tela** da Entrega 2 (*"A tela que exibe as fotos mostra 'Fotos: Pexels/Pixabay' com link — exigência das diretrizes da API"*) | Mantive o rodapé de atribuição `"Fotos: Pixabay"` com link clicável no final da página de catálogo | Exigência legal/contratual da API de imagens e requisito explícito da Entrega 2 não podem ser removidos por pedido estético de briefing | `src/pages/CatalogPage.tsx` (L225-239) e `references/contrato.md` (L19) | `364078d` (front) |

---

## 1b. Lacunas: o que foi pedido de forma incompleta
Tudo que precisou ser decidido porque o pedido não dizia.

| spec | o que faltava | alternativas | o que decidiu | por quê | commit |
|------|---------------|--------------|---------------|---------|--------|
| **Entrega 2 / Skill Imagens** | Como armazenar a URL pública da imagem no banco se a tabela `equipments` da `SPEC-001` (`prisma/schema.prisma`) não possuía coluna `image_url` dedicada | **A)** Criar migration adicionando coluna `image_url` no banco;<br>**B)** Padronizar URL determinística no bucket público (`.../equipamentos/<patrimonio>.jpg`) e registrar na `description` no seed | **Alternativa B:** URL determinística por código de patrimônio (`TI-0001.jpg` a `TI-0012.jpg`) no bucket público `equipamentos` + fallback estático em `/equipamentos/TI-XXXX.jpg` | Evita quebrar o schema já migrado da `SPEC-001`, garante idempotência total (1 arquivo por patrimônio) e permite resolução direta da imagem pelo código do equipamento | `377d556` (back) / `364078d` (front) |
| **Entrega 2 / Skill Imagens** | Alguns termos de busca originais em inglês (`laptop on white desk`, `closed laptop on table`, `webcam`, `compact camera on table`) retornavam no Pixabay fotos com mãos/pessoas, logotipos da Apple ou equipamentos errados | **A)** Aceitar a primeira foto retornada pela API;<br>**B)** Refinar os termos de busca e criar script de rebusca seletiva (`refetch_specific.py`) mantendo `USED_IDS` | **Alternativa B:** Ajuste nos termos de busca após inspeção visual e criação do `refetch_specific.py` para substituir as fotos reprovadas (`TI-0001`, `TI-0004`, `TI-0011`, `TI-0012`) | O contrato da Entrega 2 proíbe pessoas, marcas legíveis ou telas com conteúdo nas fotos finais do catálogo | `163ebf8` e `7c0a7fe` (back) / `907a11b` e `4972245` (front) |
| **Entrega 3 / Dados Iniciais** | Qual papel (`Role`) e qual `tenant` atribuir ao usuário obrigatório do professor (`marcelo.grilo@institutojef.org.br`) | **A)** Criar como `ADMIN` ou `OPERATOR`;<br>**B)** Criar como `COLLABORATOR` vinculado ao tenant `suporte_ti` | **Alternativa B:** Papel `COLLABORATOR` no tenant padrão `suporte_ti`, iniciando com zero empréstimos | O checklist de produção (Seção 07) testa a visão de colaborador (solicitar equipamento disponível, ver "meus empréstimos" e respeitar bloqueios) com a conta do professor intacta (zero empréstimos) | `377d556` (back) / `364078d` (front) |
| **Entrega 4 / Solicitar Empréstimo** | Comportamento da conta do professor vs. conta de demonstração ao logar na interface | **A)** Carregar `INITIAL_LOANS` para qualquer usuário;<br>**B)** Isolar os empréstimos por usuário (`loans.filter(l => l.userName === user?.name)`), garantindo que `marcelo.grilo@institutojef.org.br` entre com 0 empréstimos | **Alternativa B:** Filtro por usuário logado em `App.tsx` (L48-80), reconhecendo `marcelo.grilo` com 0 empréstimos iniciais | Cumpre a regra inegociável da Seção 01: *"A conta do professor é só do professor e precisa chegar à correção com zero empréstimos"* | `364078d` (front) |

---

## 2. Onde o agente tentou decidir por você
Durante a execução da **Entrega 2 (Skill `imagens-equipamentos`)**, ao rodar a primeira busca automatizada na API do Pixabay com os termos literais da tabela (`"laptop on white desk"`, `"closed laptop on table"`, `"webcam"`, `"compact camera on table"`), o script baixou o primeiro resultado de cada busca e o agente inicialmente deu o lote de 12 imagens como concluído apenas porque todas tinham 800×600 pixels e IDs únicos.

- **Como percebi:** Ao fazer a inspeção visual humana na pasta `staging_images/` (e conferir as URLs originais no `manifest-creditos.json`), notei que:
  1. `TI-0001` (`foto_id: 849825` / depois `7188564`) continha mãos humanas / xícara de café em destaque em vez de apenas o notebook limpo;
  2. `TI-0004` (`foto_id: 594090`, `startup-meeting-brainstorming`) mostrava pessoas em reunião;
  3. `TI-0011` (`foto_id: 1155173`) era um notebook em uma praça, e não uma webcam;
  4. `TI-0012` (`foto_id: 2364849`, `child-camera-photographer`) continha uma criança segurando a câmera.
- **O que fiz:** Rejeitei as 4 imagens na revisão humana, criei o script complementar `scripts/refetch_specific.py` bloqueando os IDs já usados/reprovados (`USED_IDS`) e refinei os termos de busca em `references/equipamentos.json` (commits `163ebf8` e `7c0a7fe` no back / `4972245` no front) para buscar fotos estritamente de produto sem pessoas nem marcas.

---

## 3. Uma decisão que merece (ou não) um ADR
**Decisão analisada:** Padronização e resolução de imagens de equipamentos via convenção de código de patrimônio (`<SUPABASE_URL>/storage/v1/object/public/equipamentos/<patrimonio>.jpg`) em vez de criar uma nova tabela de mídia ou alterar o schema da tabela `equipments`.

- **Alternativas defensáveis:**
  1. **Convenção determinística no Storage (`equipamentos/<patrimonio>.jpg`) + referência textual:** Não altera o DDL da `SPEC-001`, garante que cada equipamento tenha exatamente 1 arquivo sobrescritível (idempotente) e permite fallback imediato.
  2. **Nova coluna `image_url` + tabela `equipment_media` (com metadados de crédito no banco):** Acopla os metadados do Pixabay diretamente ao PostgreSQL via migration do Prisma.
- **Virou ADR? Não.**
- **Por quê:** O `ADR-001` já definiu o uso do Supabase (incluindo Storage) e o Prisma Migrate como dono do schema. A escolha de nomear os objetos do bucket pelo código único de patrimônio (`TI-XXXX.jpg`) é uma decisão de modelagem de implementação da feature (coberta pela spec e pelo contrato da skill `imagens-equipamentos`), sem alterar a arquitetura, a stack ou os limites de segurança definidos no `ADR-001`.

---

## 4. A skill `imagens-equipamentos`
- **O que ficou em cada parte e critério de separação:**
  - `SKILL.md`: Fluxo operacional passo a passo, regras de execução e checklist de revisão visual humana (o que orienta a ação do agente e do desenvolvedor).
  - `references/` (`contrato.md`, `equipamentos.json`, `pixabay-api.md`, `pixabay-conflito.md`, `pexels-api.md`): Dados estáticos, lista canônica dos 12 equipamentos, documentação da API externa e histórico de resolução do conflito Pexels vs. Pixabay. Ficam separados para não poluir o prompt principal quando não estão sendo consultados.
  - `scripts/` (`fetch_and_resize.py`, `refetch_specific.py`): Automação determinística em Python (busca HTTP, validação de IDs repetidos, redimensionamento LANCZOS + corte central 800×600 e geração do `manifest-creditos.json`).
- **Garantido por código vs. instrução/revisão humana:**
  - **Por código (`fetch_and_resize.py`):** Fonte exclusiva (`https://pixabay.com/api/`), dimensões exatas de **800×600 pixels** (`PIL.Image.Resampling.LANCZOS` + crop central), ausência de repetição (`set` de `foto_id`), nomes idempotentes (`TI-0001.jpg`..`TI-0012.jpg`) e geração do manifesto de créditos (`manifest-creditos.json`).
  - **Por instrução + revisão humana:** Direito de imagem (ausência de pessoas, rostos, mãos, marcas/logos legíveis como Apple/Dell ou telas com texto/código), pois a API retorna fotos por tags sem visão computacional semântica confiável, exigindo aprovação visual humana antes da publicação.
- **Como o agente fica impedido de enviar imagens para produção:**
  - O script `fetch_and_resize.py` escreve exclusivamente no diretório local `staging_images/` e não possui código, SDK nem credenciais de upload para o Supabase Storage. Além disso, `.agents/rules/restrictions.md` (L31-33) proíbe o agente de tocar no projeto Supabase remoto ou fazer deploy.
- **Fotos reprovadas na revisão visual:**
  - **4 fotos reprovadas** na primeira rodada:
    1. `TI-0001` (continha mãos/pessoa e itens de cafeteria na mesa);
    2. `TI-0004` (foto `594090` mostrava reunião com pessoas);
    3. `TI-0011` (foto `1155173` mostrava um notebook em uma praça em vez de uma webcam);
    4. `TI-0012` (foto `2364849` mostrava uma criança segurando a câmera).
  - Todas as 4 foram adicionadas à lista de bloqueio `USED_IDS` em `scripts/refetch_specific.py` e substituídas por fotos limpas de produto em 800×600.

---

## 5. O subagente verificador
- **Como ele é acionado e por que esse gatilho:**
  - Acionado obrigatoriamente ao final das tarefas de uma spec, antes de declará-la pronta, por meio da rule `.agents/rules/spec-flow.md` (`alwaysApply: true`, linhas 17-19: *"Antes de declarar uma spec pronta: Delegue ao subagente verificador-spec (agents/verificador-spec.md)..."*). Usar uma rule com `alwaysApply: true` no fluxo de specs garante que o agente principal sempre consulte o gatilho ao trabalhar em `docs/specs/**`, sem depender de o humano lembrar de pedir no chat.
- **O que ele lê e por que precisa ler, em vez de herdar:**
  - Ele inicia com contexto limpo (não herda a conversa do agente principal) e lê diretamente do disco: `AGENTS.md`, `rules/restrictions.md`, `rules/checks.md`, `rules/tests.md`, além de `spec.md`, `plan.md` e `tasks.md` da spec avaliada (`agents/verificador-spec.md` L18-21). Ele não pode herdar a conversa para não ser contaminado pelas justificativas, vieses ou racionalizações do agente que escreveu o código.
- **O que ele não consegue fazer e como isso é garantido no harness:**
  - Não edita arquivos, não corrige código nem testes, não faz commit e não roda migrations, reset de banco ou deploy em produção (`agents/verificador-spec.md` L27-37). No harness, isso é garantido tanto pelas instruções de bloqueio do perfil do subagente (somente leitura e execução dos comandos de `rules/checks.md`) quanto pela verificação de que o banco apontado não é o de produção antes de rodar qualquer teste.
- **Back e Front separados (Turma REST): como a verificação cobre o nosso caso:**
  - O `agents/verificador-spec.md` existe nos dois repositórios (`emprestai-back` e `emprestai-front`) e inclui o status **`OUTRO REPOSITÓRIO`** (L41-43: *"OUTRO REPOSITÓRIO = a prova deste CA vive no back ou no front que não está aberto aqui; não conta como falha, mas precisa ser verificado lá"*). Assim, critérios de banco/seed são comprovados no `emprestai-back` e critérios de interface/catálogo são comprovados no `emprestai-front`.

---

## 6. O verificador em ação

### Histórico de verificação e prova dos critérios
Como o projeto é dividido em dois repositórios (`emprestai-back` e `emprestai-front`), a verificação de cada entrega avalia as evidências no respectivo repositório usando o formato contratual do `agents/verificador-spec.md`.

#### Tabela de Verificação — Entrega 3 (Dados Iniciais: Seed & Imagens)
| CA | evidência (arquivo:linha) | status | observação |
|----|---------------------------|--------|------------|
| **CA-01:** 12 equipamentos da lista oficial cadastrados | `emprestai-back/prisma/seed.ts:23-36` e `emprestai-front/src/data/initialData.ts:12-112` | ATENDIDO | 4 notebooks, 3 monitores, 3 cabos e 2 câmeras com patrimônios `TI-0001` a `TI-0012` |
| **CA-02:** Situação correta dos equipamentos (manutenção vs disponível) | `emprestai-back/prisma/seed.ts:27,30,33` | ATENDIDO | `TI-0004`, `TI-0007` e `TI-0010` em `MAINTENANCE` conforme JSON oficial; demais 9 `AVAILABLE` |
| **CA-03:** Imagens 800×600 geradas pela skill e públicas | `emprestai-front/public/equipamentos/TI-0001.jpg`..`TI-0012.jpg` e `staging_images/manifest-creditos.json:1-182` | ATENDIDO | 12 imagens JPEG em 800×600 exatos, sem repetição de ID |
| **CA-04:** Usuário `marcelo.grilo@institutojef.org.br` com zero empréstimos | `emprestai-back/prisma/seed.ts:12-16,117-143` e `emprestai-front/src/App.tsx:48-80` | ATENDIDO | Criado no Auth/Membership do tenant `suporte_ti` com `professorLoansCount = 0` |
| **CA-05:** Idempotência (popular mais de uma vez não duplica) | `emprestai-back/prisma/seed.ts:106,118,151` | ATENDIDO | Uso de `prisma.tenant.upsert`, `prisma.membership.upsert` (`tenantId_userId`) e `prisma.equipment.upsert` (`tenantId_code`) |

```text
Checks: npm run build (emprestai-back) → passou | npm run build (emprestai-front) → passou
Fora de escopo: nada encontrado
Veredito: PRONTA — Os 12 equipamentos com imagens 800x600 e a conta do professor idempotente estão implementados e verificados nos dois repositórios.
```

#### Tabela de Verificação — Entrega 4 (Solicitar Empréstimo)
| CA | evidência (arquivo:linha) | status | observação |
|----|---------------------------|--------|------------|
| **CA-01:** Colaborador logado vê catálogo com foto, nome, categoria e situação | `emprestai-front/src/pages/CatalogPage.tsx:167-219` | ATENDIDO | Renderiza imagem 800×600, categoria, `StatusPill`, nome e patrimônio |
| **CA-02:** Equipamento em manutenção ou emprestado não pode ser solicitado | `emprestai-front/src/pages/CatalogPage.tsx:155-164,210-217` | ATENDIDO | Botão desabilitado (`disabled={isDisabled}`) com rótulo `"Indisponível"` ou `"Emprestado"` |
| **CA-03:** Solicitar disponível cria empréstimo com devolução em 14 dias e muda status | `emprestai-front/src/App.tsx:91-122` | ATENDIDO | Cria `newLoan` com prazo de 14 dias (conforme PRD) e altera equipamento para `'emprestado'` |
| **CA-04:** Limite de 3 empréstimos simultâneos (PRD) com motivo visível | `emprestai-front/src/pages/CatalogPage.tsx:27-28,152-154` | ATENDIDO | Quando `activeLoansCount >= 3`, desabilita solicitação e exibe `"Limite de 3 itens atingido"` |
| **CA-05:** Bloqueio para quem possui empréstimo em atraso | `emprestai-front/src/pages/CatalogPage.tsx:31,56-71,149-151` | ATENDIDO | Exibe banner de bloqueio no topo e desabilita botão com `"Bloqueado por atraso"` |
| **CA-06:** Visualização de "Meus empréstimos" com data de devolução prevista | `emprestai-front/src/pages/MyLoansPage.tsx:1-145` | ATENDIDO | Lista empréstimos ativos do usuário logado com patrimônio e data de devolução |
| **CA-07:** Atribuição obrigatória da API de fotos no catálogo | `emprestai-front/src/pages/CatalogPage.tsx:226-239` | ATENDIDO | Rodapé exibe `"Fotos: Pixabay"` com link para `https://pixabay.com/pt/` |

```text
Checks: npm run build (emprestai-front) → passou
Fora de escopo: nada encontrado
Veredito: PRONTA — Fluxo de catálogo, bloqueios de negócio conforme PRD (3 itens, 14 dias, manutenção e atraso) e atribuição do Pixabay atendidos.
```

---

## 7. Uma regra sua que esta prática pôs à prova
- **Regra posta à prova:** `.agents/rules/restrictions.md` (item de Escopo: *"Não escreva código sem antes alinhar com as regras do PRD e ADRs"*) combinada com `.agents/rules/secrets.md` e `operacao.md` no deploy serverless da Vercel.
- **O que aconteceu:** Durante o deploy do `emprestai-back` na Vercel, os arquivos compilados (`api/index.js`, `api/index.d.ts`, `api/index.js.map`) estavam sendo versionados junto com o TypeScript e o `vercel.json` conflitava com o ciclo de build do NestJS/Prisma. Além disso, o briefing da Entrega 3 pediu explicitamente para deixar a senha do professor escrita no `seed.ts`, testando a fronteira entre dado público de seed acadêmico e segredo de infraestrutura (`secrets.md`).
- **O que mudei:** Ajustei o `.gitignore`, o `package.json` e o `vercel.json` no commit `90e9e8d` (`fix: remove api compiled files from repo, fix vercel config and deps`) para garantir que artefatos compilados não fossem versionados e que os segredos reais (`DATABASE_URL`, `DIRECT_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `PIXABAY_API_KEY`) ficassem estritamente nas variáveis de ambiente e documentados sem valor em `.env.example`.

---

## 8. O que ficou de fora e o que faria diferente
- **O que ficou de fora (estado atual do projeto):**
  1. **Integração HTTP entre Front e Back para Empréstimos:** O banco de dados PostgreSQL/Supabase possui o schema completo (`SPEC-001`) e o `prisma/seed.ts` popula de forma idempotente o tenant `suporte_ti`, a conta do professor e os 12 equipamentos reais. Porém, no `emprestai-back`, apenas o módulo `health` (`GET /v1/health`) está exposto em `src/modules/`; o `emprestai-front` opera o fluxo de catálogo e solicitação de empréstimo com estado em memória inicializado a partir de `src/data/initialData.ts` (sincronizado com os 12 equipamentos e com as fotos do Supabase Storage / `public/equipamentos`).
  2. **Suíte de testes automatizados (Jest/Vitest) e arquivos `docs/specs/002-*` e `003-*`:** A `SPEC-001` (`docs/specs/001-database-schema.md`) foi formalizada, mas as entregas 3 e 4 foram implementadas diretamente no `seed.ts` e no frontend sem criar os diretórios `docs/specs/002-dados-iniciais` e `docs/specs/003-solicitar-emprestimo` e sem suíte Jest/Vitest configurada (`npm test` no `package.json` ainda está com o script padrão).
- **O que faria diferente:**
  - Criaria primeiro os arquivos formais `docs/specs/002-dados-iniciais/spec.md` e `docs/specs/003-solicitar-emprestimo/spec.md` com os testes automatizados nomeados por `CA-XX` antes de codificar o `seed.ts` e o `CatalogPage.tsx`, permitindo que o `verificador-spec` validasse cada critério via execução do Vitest/Jest em vez de inspeção estática e build.
