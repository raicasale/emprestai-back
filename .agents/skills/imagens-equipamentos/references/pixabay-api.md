# Referência da API do Pixabay

## 1. Visão Geral
A API do Pixabay fornece acesso a mais de 4,3 milhões de fotos, ilustrações e vetores livres de royalties sob a Licença de Conteúdo Pixabay.
- Documentação oficial: [https://pixabay.com/api/docs/](https://pixabay.com/api/docs/)
- Endpoint de busca: `GET https://pixabay.com/api/`

## 2. Autenticação e Chave
- Parâmetro obrigatório na query string: `key=<PIXABAY_API_KEY>`
- A chave é gratuita e fornecida imediatamente após o cadastro na página de documentação da API.
- **Segurança (Zero Chaves no Git):** A chave NUNCA é colocada no código-fonte nem em commits. É lida via variável de ambiente `PIXABAY_API_KEY` ou `.env` local (ignorado pelo git).

## 3. Parâmetros de Requisição Utilizados
| Parâmetro | Valor | Descrição |
| :--- | :--- | :--- |
| `key` | `string` | Chave de autenticação da API Pixabay |
| `q` | `string` | Termo de busca (ex: `laptop minimal desk`, `webcam`) |
| `image_type` | `photo` | Filtra apenas fotografias reais (elimina ilustrações/vetores) |
| `orientation` | `horizontal` | Fotos na horizontal (ideal para corte em proporção 4:3 / 800×600) |
| `safesearch` | `true` | Garante conteúdo apropriado |
| `per_page` | `15` | Retorna alternativas para desduplicação e revisão visual |

## 4. Estrutura do Objeto de Resposta
```json
{
  "total": 450,
  "totalHits": 450,
  "hits": [
    {
      "id": 123456,
      "pageURL": "https://pixabay.com/pt/photos/laptop-computador-mesa-123456/",
      "type": "photo",
      "tags": "laptop, computador, mesa",
      "previewURL": "https://cdn.pixabay.com/photo/...",
      "webformatURL": "https://pixabay.com/get/...",
      "largeImageURL": "https://pixabay.com/get/...",
      "imageWidth": 4000,
      "imageHeight": 2667,
      "views": 15000,
      "downloads": 8000,
      "likes": 120,
      "user": "NomeDoFotografo",
      "user_id": 987654,
      "userImageURL": "https://cdn.pixabay.com/user/..."
    }
  ]
}
```

## 5. Licença e Atribuição
- Licença Pixabay: Livre para uso comercial e não comercial.
- Atribuição no Projeto: Exibição no frontend de *"Fotos: Pixabay"* com link para `https://pixabay.com/` e registro no `manifest-creditos.json` com nome e link do fotógrafo.
