---
name: imagens-equipamentos
description: Busca, trata, valida e credita fotos dos 12 equipamentos do catálogo interno do EMPREST.AI utilizando a API oficial do Pixabay (https://pixabay.com/pt/). Garante dimensões contratuais de exatamente 800x600, desduplicação de fotos, manifesto de créditos e isolamento seguro contra envios automáticos para produção.
---

# Skill: imagens-equipamentos (Provedor Oficial: Pixabay)
> leitor: agente e desenvolvedor

Esta skill é responsável por obter as fotos dos 12 equipamentos do catálogo do **EMPREST.AI**, assegurando conformidade estrita com os critérios técnicos da **Entrega 2** e com a orientação do professor em aula (uso da API do **Pixabay**).

---

## 1. Estrutura da Skill e Critério de Separação

```
skills/imagens-equipamentos/
├── SKILL.md                  ← Regras operacionais, workflow e checklist de inspeção
├── references/               ← Contratos, documentações externas e dados estáticos
│   ├── contrato.md           ← Tabela contratual atualizada (Pixabay como fonte oficial)
│   ├── equipamentos.json     ← Lista oficial dos 12 equipamentos e termos de busca
│   ├── pixabay-api.md        ← Especificação da API oficial do Pixabay (endpoints, params)
│   └── pixabay-conflito.md   ← Registro do conflito (slide Pexels vs orientação verbal em aula)
└── scripts/                  ← Automação determinística e garantias via código
    └── fetch_and_resize.py   ← Busca no Pixabay, corte 800x600, desduplicação e créditos
```

### Critério de Separação
- **`SKILL.md`:** Guarda as regras de fluxo, instruções de trabalho e critérios que necessitam de interpretação do agente e validação do usuário.
- **`references/`:** Guarda contratos imutáveis, especificações externas de API e a lista estática de 12 equipamentos. Não polui a janela de contexto com dados repetitivos a menos que consultados.
- **`scripts/`:** Guarda tudo o que pode e deve ser **garantido matematicamente por código** (dimensões exatas, verificação de duplicidade de ID e formatação do manifesto JSON).

---

## 2. Divisão de Responsabilidade: Código vs Instrução e Revisão Humana

| Requisito Contratual | Como é Garantido | Por que essa divisão? |
| :--- | :--- | :--- |
| **Mesmo tamanho (800×600)** | **Garantido por Código** (`scripts/fetch_and_resize.py`) | Modelos de IA e prompts não redimensionam pixels de forma confiável. O script usa Pillow com corte central (`LANCZOS`) para cravar exatamente 800×600. |
| **Sem repetição** | **Garantido por Código** (`scripts/fetch_and_resize.py`) | O script mantém um conjunto (`Set`) de IDs de fotos do Pixabay, impedindo que a mesma imagem seja reutilizada em dois equipamentos. |
| **Créditos e Metadados** | **Garantido por Código** (`scripts/fetch_and_resize.py`) | Extrai os dados estruturados da resposta da API (autor, perfil, URL da foto, licença) e gera `manifest-creditos.json` de forma determinística. |
| **Fonte Oficial (Pixabay)** | **Garantido por Código** (`scripts/fetch_and_resize.py`) | O endpoint HTTP padrão aponta exclusivamente para `https://pixabay.com/api/` com filtros `image_type=photo` e `orientation=horizontal`. |
| **Direito de Imagem** (sem pessoas, marcas legíveis ou telas com conteúdo) | **Instrução + Revisão Humana Obrigatória** | Algoritmos de busca retornam fotos conceituais que frequentemente incluem modelos humanos ou logotipos de marcas (Apple, Dell, etc.). A checagem visual final é humana. |
| **Segurança em Produção** | **Bloqueio de Harness / Script** | O script gera arquivos apenas em pasta local de staging (`staging_images/`). O upload para o Supabase Storage de produção não é implementado no script automático, exigindo intervenção manual aprovada pelo usuário. |

---

## 3. Gestão do Conflito: Pixabay vs. Slide Pexels

O slide da Entrega 2 indicava *"Só a API do Pexels"*, enquanto o professor instruiu em sala o uso da API do **Pixabay** (`https://pixabay.com/pt/`).
- Conforme as regras de SDD do projeto: toda discrepância é levantada, o usuário decide e a justificativa é documentada no `ENTREGA.md` (Seção 1).
- A decisão tomada é a adoção integral da API do Pixabay como fonte oficial.
- Detalhes e tabela comparativa registrados em `references/pixabay-conflito.md`.

---

## 4. Instruções de Execução

### Passo 1 — Obter e Configurar a Chave da API do Pixabay
1. Crie uma conta gratuita em [https://pixabay.com/pt/](https://pixabay.com/pt/).
2. Acesse a documentação em [https://pixabay.com/api/docs/](https://pixabay.com/api/docs/) e copie a chave em **"API key"**.
3. Configure a variável no seu terminal PowerShell (nunca comitar no git):
```powershell
$env:PIXABAY_API_KEY = "sua_chave_pixabay_aqui"
```

### Passo 2 — Rodar o Script de Download e Resize
```powershell
python skills/imagens-equipamentos/scripts/fetch_and_resize.py --output-dir staging_images
```
*Se a chave não estiver no ambiente, o script roda em modo de simulação/offline gerando as 12 imagens estruturais em 800×600 para teste.*

### Passo 3 — Revisão Visual Humana (Checklist Obrigatório)
Abra o diretório `staging_images/` e inspecione cada arquivo:
- [ ] **Pessoas:** Nenhum rosto, mão em destaque ou pessoa visível.
- [ ] **Marcas:** Nenhum logotipo legível (Dell, Apple, Lenovo, HP, etc.).
- [ ] **Telas:** Nenhuma tela exibindo código, dados, textos legíveis ou interfaces de software.
- [ ] **Qualidade:** Nitidez e resolução de 800×600 confirmadas.

*Caso uma foto seja reprovada na revisão visual, descarte-a e rode o script apontando para o próximo resultado da API para aquele equipamento.*

### Passo 4 — Registro de Créditos e Atribuição no Catálogo
- O manifesto gerado em `staging_images/manifest-creditos.json` é utilizado no seed/banco.
- O catálogo no frontend deve exibir no rodapé da seção de fotos:
  `Fotos: Pixabay (link para https://pixabay.com/)`
