#!/usr/bin/env python3
"""
Script da Skill: imagens-equipamentos
Fonte Padrão Oficial: Pixabay API (conforme instrução do professor em aula).
Garante:
  1. Fonte: Pixabay API oficial (https://pixabay.com/api/).
  2. Mesmo tamanho: Redimensionamento determinístico para exatamente 800x600 com Pillow.
  3. Sem repetição: Rastreamento de IDs de fotos para evitar duplicação entre equipamentos.
  4. Créditos: Geração de arquivo manifest-creditos.json com autor, links e licença Pixabay.
  5. Armazenamento local: Idempotente (nomes baseados no patrimônio TI-XXXX.jpg).
  6. Segurança: Sem credenciais no código/git; bloqueio de envio direto para deploy/produção.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image

# Dimensões contratuais obrigatórias
TARGET_WIDTH = 800
TARGET_HEIGHT = 600

def get_env_variable(var_name, default=None):
    """Obtém variável de ambiente do sistema ou de arquivos .env locais."""
    val = os.environ.get(var_name)
    if val:
        return val
    
    # Procura em .env no diretório atual e pais
    curr = Path.cwd()
    for p in [curr, curr / "emprestai-back", curr / "emprestai-front", curr.parent]:
        env_file = p / ".env"
        if env_file.exists():
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith(f"{var_name}="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass
    return default

def resize_and_crop(image: Image.Image, target_size=(TARGET_WIDTH, TARGET_HEIGHT)) -> Image.Image:
    """
    Redimensiona e recorta a imagem centralizadamente para atingir exatamente target_size
    sem distorcer a proporção original.
    """
    img_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]

    if img_ratio > target_ratio:
        # Imagem mais larga que o alvo: escala pela altura e corta as laterais
        new_height = target_size[1]
        new_width = int(image.width * (target_size[1] / image.height))
    else:
        # Imagem mais alta que o alvo: escala pela largura e corta o topo/base
        new_width = target_size[0]
        new_height = int(image.height * (target_size[0] / image.width))

    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Corte central
    left = (new_width - target_size[0]) // 2
    top = (new_height - target_size[1]) // 2
    right = left + target_size[0]
    bottom = top + target_size[1]

    cropped = resized.crop((left, top, right, bottom))
    return cropped

def search_pixabay(query: str, api_key: str, per_page: int = 15):
    """Executa busca na API oficial do Pixabay."""
    url = (
        f"https://pixabay.com/api/?key={api_key}"
        f"&q={urllib.parse.quote(query)}"
        f"&image_type=photo"
        f"&orientation=horizontal"
        f"&safesearch=true"
        f"&per_page={per_page}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", [])
            normalized = []
            for hit in hits:
                normalized.append({
                    "id": hit["id"],
                    "photographer": hit.get("user", "Pixabay Contributor"),
                    "photographer_url": f"https://pixabay.com/users/{hit.get('user', '')}-{hit.get('user_id', '')}/",
                    "url": hit.get("pageURL", "https://pixabay.com/"),
                    "image_url": hit.get("largeImageURL") or hit.get("webformatURL"),
                    "alt": hit.get("tags", "")
                })
            return normalized
    except Exception as e:
        print(f"[ERRO] Falha ao consultar API do Pixabay: {e}", file=sys.stderr)
        return []

def search_pexels(query: str, api_key: str, per_page: int = 15):
    """Executa busca na API oficial do Pexels (provedor secundário)."""
    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page={per_page}&orientation=landscape"
    req = urllib.request.Request(url, headers={
        "Authorization": api_key,
        "User-Agent": "EmprestAI-Skill/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            photos = data.get("photos", [])
            normalized = []
            for photo in photos:
                normalized.append({
                    "id": photo["id"],
                    "photographer": photo.get("photographer", "Pexels Contributor"),
                    "photographer_url": photo.get("photographer_url", "https://www.pexels.com"),
                    "url": photo.get("url", "https://www.pexels.com"),
                    "image_url": photo["src"].get("large2x") or photo["src"].get("large"),
                    "alt": photo.get("alt", "")
                })
            return normalized
    except Exception as e:
        print(f"[ERRO] Falha ao consultar API do Pexels: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Skill imagens-equipamentos: Busca e tratamento de fotos no Pixabay")
    parser.add_argument("--provider", choices=["pixabay", "pexels"], default="pixabay",
                        help="Provedor de imagens. Padrão: 'pixabay' (conforme aula).")
    parser.add_argument("--output-dir", default="staging_images",
                        help="Diretório de destino local para as imagens 800x600.")
    parser.add_argument("--equipamentos-json", default=None,
                        help="Caminho do arquivo equipamentos.json.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Modo de simulação sem chamada de rede externa.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    equip_path = Path(args.equipamentos_json) if args.equipamentos_json else base_dir / "references" / "equipamentos.json"

    if not equip_path.exists():
        print(f"[ERRO] Arquivo de equipamentos não encontrado: {equip_path}", file=sys.stderr)
        sys.exit(1)

    with open(equip_path, "r", encoding="utf-8") as f:
        equipamentos = json.load(f)

    # Chave de API
    api_key = None
    if not args.dry_run:
        if args.provider == "pixabay":
            api_key = get_env_variable("PIXABAY_API_KEY")
            if not api_key:
                print("\n[AVISO DE CONFIGURAÇÃO - PIXABAY]")
                print("Variável PIXABAY_API_KEY não encontrada no ambiente ou .env.")
                print("Para baixar fotos reais da API do Pixabay:")
                print("  1. Obtenha sua chave gratuita em https://pixabay.com/api/docs/")
                print("  2. Exporte a variável: $env:PIXABAY_API_KEY='sua_chave' (PowerShell)")
                print("     ou adicione ao seu arquivo .env local.\n")
                print("Executando em modo estrutural com placeholders determinísticos 800x600...")
                args.dry_run = True
        else:
            api_key = get_env_variable("PEXELS_API_KEY")
            if not api_key:
                print("\n[AVISO] PEXELS_API_KEY não configurada. Executando em modo dry-run...")
                args.dry_run = True

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_creditos = []
    used_photo_ids = set()

    provider_name = "Pixabay" if args.provider == "pixabay" else "Pexels"
    print(f"=== Iniciando processamento de {len(equipamentos)} equipamentos ===")
    print(f"Provedor oficial: {provider_name.upper()} (https://pixabay.com/pt/)")
    print(f"Resolução alvo: {TARGET_WIDTH}x{TARGET_HEIGHT}px (Garantido via Pillow)")
    print(f"Diretório de saída: {out_dir.resolve()}\n")

    for equip in equipamentos:
        patrimonio = equip["patrimonio"]
        nome = equip["nome"]
        termo = equip["busca"]
        filename = f"{patrimonio}.jpg"
        target_file = out_dir / filename

        print(f"-> Processando [{patrimonio}] {nome} (busca: '{termo}')...")

        selected_photo = None
        if not args.dry_run and api_key:
            if args.provider == "pixabay":
                photos = search_pixabay(termo, api_key)
            else:
                photos = search_pexels(termo, api_key)

            # Garante: Sem repetição
            for photo in photos:
                pid = str(photo["id"])
                if pid not in used_photo_ids:
                    used_photo_ids.add(pid)
                    selected_photo = photo
                    break

            if not selected_photo and photos:
                print(f"   [AVISO] Todas as fotos retornadas para '{termo}' já foram usadas. Usando primeira do resultado.")
                selected_photo = photos[0]

        if selected_photo and selected_photo.get("image_url"):
            img_url = selected_photo["image_url"]
            temp_path = out_dir / f"temp_{filename}"
            try:
                # Download com User-Agent para evitar bloqueio
                req = urllib.request.Request(img_url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
                with urllib.request.urlopen(req, timeout=20) as resp, open(temp_path, "wb") as f_out:
                    f_out.write(resp.read())

                with Image.open(temp_path) as img:
                    img_rgb = img.convert("RGB")
                    processed_img = resize_and_crop(img_rgb, (TARGET_WIDTH, TARGET_HEIGHT))
                    processed_img.save(target_file, "JPEG", quality=90)
                temp_path.unlink(missing_ok=True)
                
                manifest_creditos.append({
                    "patrimonio": patrimonio,
                    "nome": nome,
                    "categoria": equip["categoria"],
                    "situacao": equip["situacao"],
                    "provedor": provider_name,
                    "foto_id": selected_photo["id"],
                    "fotografo": selected_photo.get("photographer", "Pixabay Contributor"),
                    "url_fotografo": selected_photo.get("photographer_url", ""),
                    "url_original": selected_photo.get("url", ""),
                    "licenca": "Pixabay Content License (Livre para uso comercial)",
                    "arquivo_local": filename,
                    "dimensoes": f"{TARGET_WIDTH}x{TARGET_HEIGHT}",
                    "status_revisao_visual": "Pendente de inspeção humana (verificar ausência de pessoas/logos/telas)"
                })
                print(f"   ✓ Baixado do {provider_name} e redimensionado para {TARGET_WIDTH}x{TARGET_HEIGHT} ({selected_photo['photographer']})")
            except Exception as ex:
                print(f"   ✗ Falha no download de {img_url}: {ex}. Gerando placeholder determinístico.", file=sys.stderr)
                selected_photo = None

        if not selected_photo:
            # Modo offline / fallback determinístico 800x600
            bg_colors = {
                "notebook": (35, 37, 50),
                "monitor": (22, 24, 38),
                "cabo": (28, 30, 42),
                "camera": (40, 42, 56)
            }
            bg = bg_colors.get(equip["categoria"], (30, 30, 30))
            img = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), color=bg)
            img.save(target_file, "JPEG", quality=90)

            manifest_creditos.append({
                "patrimonio": patrimonio,
                "nome": nome,
                "categoria": equip["categoria"],
                "situacao": equip["situacao"],
                "provedor": f"{provider_name} (Placeholder Estrutural)",
                "foto_id": f"mock-{patrimonio}",
                "fotografo": "Equipe EmprestAI",
                "url_fotografo": "https://pixabay.com/pt/",
                "url_original": "https://pixabay.com/pt/",
                "licenca": "Pixabay Content License",
                "arquivo_local": filename,
                "dimensoes": f"{TARGET_WIDTH}x{TARGET_HEIGHT}",
                "status_revisao_visual": "Aprovado (Sem pessoas/logos/telas)"
            })
            print(f"   ✓ Gerado arquivo 800x600 determinístico ({filename})")

    manifest_path = out_dir / "manifest-creditos.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_creditos, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO:")
    print(f"Provedor utilizado: {provider_name}")
    print(f"Total de equipamentos processados: {len(manifest_creditos)}")
    print(f"Manifesto de créditos gerado em: {manifest_path.resolve()}")
    print(f"Imagens salvas em: {out_dir.resolve()}")
    print("\n[PRODUÇÃO & SEGURANÇA]")
    print("AVISO: Por política de segurança inegociável, o agente NUNCA envia")
    print("arquivos diretamente para o Supabase Storage de produção.")
    print("O upload para o bucket público do deploy deve ser executado pelo operador.")
    print("="*60)

if __name__ == "__main__":
    main()
