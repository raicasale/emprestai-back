# Registro de Conflito: Pedido do Professor em Aula (Pixabay) vs Slide Escrito (Pexels)

## 1. Conflito Identificado
- **Slide Escrito (Entrega 2):** Fixava *"Só a API do Pexels, com a sua chave gratuita. Nenhuma outra origem de imagem."* e *"Fotos: Pexels"*.
- **Instrução Verbal em Aula:** O professor determinou diretamente para a turma que a fonte de busca das imagens dos equipamentos deve ser o **Pixabay** (`https://pixabay.com/pt/`).
- **Diretriz de SDD:** *"O que o briefing não responde, ou responde de forma conflitante, não é decidido pelo agente: é levantado, decidido por você e registrado."*

---

## 2. Tabela de Registro para o ENTREGA.md (Seção 1)

| pedido | contrariava o quê | o que você fez | por quê | onde ficou registrado | commit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Usar a API do Pixabay (`https://pixabay.com/pt/`) para obter as imagens dos 12 equipamentos | Requisito "Fonte" e "Crédito na tela" do slide da Entrega 2, que especificava "Só a API do Pexels" | Adaptou a skill `imagens-equipamentos` e o script `fetch_and_resize.py` para usar a API oficial do Pixabay por padrão, com créditos para o Pixabay | Decisão explícita do professor comunicada em sala de aula, que sobrepõe o slide escrito anterior. O agente alertou sobre o conflito e o desenvolvedor confirmou a orientação verbal | `skills/imagens-equipamentos/references/pixabay-conflito.md`, `references/contrato.md` e `ENTREGA.md` | `<hash-do-commit>` |

---

## 3. Impactos Técnicos e Ajustes Realizados
1. **Endpoint da API:** Alterado para `https://pixabay.com/api/` com autenticação via parâmetro `key`.
2. **Variável de Ambiente:** Utiliza `PIXABAY_API_KEY` (mantendo a regra inegociável de zero chaves em código ou git).
3. **Parâmetros de Filtro:** `image_type=photo` e `orientation=horizontal` para garantir fotografias reais e proporção paisagem.
4. **Dimensões e Desduplicação:** Mantidos 100% rígidos via script Python (corte central em exatamente 800×600 com Pillow e desduplicação por `foto_id`).
5. **Crédito no Frontend:** Atualizado para exibir *"Fotos: Pixabay"* com link para `https://pixabay.com/`.
