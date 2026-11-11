# Contrato da Skill: imagens-equipamentos (Entrega 2 - Atualizado)

Este documento estabelece os requisitos contratuais inegociáveis para a captura, tratamento, validação e armazenamento das imagens do catálogo do sistema de Empréstimo de Equipamentos Internos (**EMPREST.AI**), incorporando a decisão de sala de aula de utilizar o **Pixabay**.

---

## Tabela de Requisitos Contratuais

| Requisito | O que a skill garante | Divisão de Responsabilidade |
| :--- | :--- | :--- |
| **Fonte** | **API oficial do Pixabay** (`https://pixabay.com/api/`), com chave gratuita obtida no portal. (Decisão verbal do professor que atualizou o slide do Pexels). | **Código (Script)**: Endpoint fixo na API do Pixabay com autenticação via `PIXABAY_API_KEY`. |
| **Direito de imagem** | Nenhuma foto com pessoa, marca ou logo legível, texto ou tela com conteúdo chega ao sistema. | **Revisão Humana Obrigatória**: Inspeção visual em `staging_images/` antes de aprovação. |
| **Mesmo tamanho** | Todas as imagens em exatamente **800×600**. Isso é **garantido**, não apenas pedido. | **Código (Script)**: Resize determinístico proporcional com corte central para 800×600 via Pillow. |
| **Sem repetição** | Uma mesma foto não aparece em dois equipamentos. | **Código (Script)**: Conjunto (`Set`) de identificadores únicos (`foto_id`) para evitar reutilização. |
| **Créditos** | Para cada imagem, fica registrado de onde veio, quem fotografou e sob qual licença. | **Código (Script)**: Geração de arquivo `manifest-creditos.json` contendo autor, URL do perfil no Pixabay, URL original e licença. |
| **Armazenamento** | As imagens ficam identificadas pelo patrimônio (`TI-XXXX.jpg`). Repetir o processo não duplica nada (idempotência). | **Código (Script)**: Nome do arquivo baseado no patrimônio, garantindo substituição limpa. |
| **Produção** | O agente consegue preparar as imagens, mas não consegue enviá-las ao Supabase do deploy. | **Controle de Acesso / Harness**: Bloqueio de envio direto para produção. Upload é executado pelo operador humano. |
| **Segredos e dependências** | Nenhuma chave em código ou no git. Nenhuma biblioteca fora do que as suas rules e ADRs permitem. | **Regras / Script**: Leitura da chave via variável de ambiente (`PIXABAY_API_KEY`). Nenhuma dependência não autorizada nos pacotes de runtime. |
| **Crédito na tela** | A tela que exibe as fotos mostra "Fotos: Pixabay" com link — exigência de atribuição. | **Frontend**: Componente com link de atribuição explícita no catálogo. |

---

## Registro de Decisão
- **Conflito resolvido:** Slide apontava Pexels; professor determinou Pixabay em sala.
- **Resolução:** Pixabay adotado como fonte padrão oficial do projeto, registrado na Seção 1 do `ENTREGA.md`.
