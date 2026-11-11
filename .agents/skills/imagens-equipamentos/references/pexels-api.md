# Referência da API do Pexels

## 1. Visão Geral
A API do Pexels oferece busca gratuita de fotos e vídeos em alta resolução sob a Licença Pexels.
- Documentação oficial: [https://www.pexels.com/api/documentation/](https://www.pexels.com/api/documentation/)
- Endpoint de busca: `GET https://api.pexels.com/v1/search`

## 2. Autenticação
- Header obrigatório: `Authorization: <PEXELS_API_KEY>`
- A chave é gratuita e obtida no painel de desenvolvedores do Pexels.
- **Segurança:** A chave NUNCA deve ser commitada no git ou embutida no código. Deve ser injetada via variável de ambiente (`PEXELS_API_KEY`).

## 3. Parâmetros de Requisição Recomendados
- `query`: Termo de busca em inglês (ex: `laptop on white desk`).
- `per_page`: `5` a `15` resultados (permite escolher alternativas caso uma foto seja reprovada na revisão visual).
- `orientation`: `landscape` (horizontal, mais adequado para cards de proporção 4:3 / 800x600).
- `locale`: `pt-BR` ou `en-US`.

## 4. Estrutura do Objeto de Resposta
```json
{
  "total_results": 100,
  "page": 1,
  "per_page": 5,
  "photos": [
    {
      "id": 1234567,
      "width": 4000,
      "height": 3000,
      "url": "https://www.pexels.com/photo/...",
      "photographer": "Nome do Fotógrafo",
      "photographer_url": "https://www.pexels.com/@fotografo",
      "photographer_id": 98765,
      "src": {
        "original": "https://images.pexels.com/photos/...",
        "large2x": "https://images.pexels.com/photos/...",
        "large": "https://images.pexels.com/photos/...",
        "medium": "https://images.pexels.com/photos/..."
      },
      "alt": "Descrição da foto"
    }
  ]
}
```

## 5. Diretrizes da Licença e Atribuição
- O uso é livre para fins comerciais e não comerciais sem custo.
- Modificação permitida.
- **Exigência Contratual:** A tela que exibe as fotos deve creditar o Pexels ("Fotos: Pexels" com link para https://www.pexels.com).
- Para cada foto baixada, salvamos os metadados: autor, perfil do fotógrafo, URL original e ID.
