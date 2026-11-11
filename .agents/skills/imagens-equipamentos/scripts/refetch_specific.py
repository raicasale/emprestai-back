#!/usr/bin/env python3
"""
Script auxiliar: rebusca imagens apenas para os patrimônios problemáticos.
Usa os mesmos critérios contratuais do fetch_and_resize.py (800x600, Pixabay, sem repetição).
"""

import os, sys, json, urllib.request, urllib.parse
from pathlib import Path
from PIL import Image

TARGET_WIDTH, TARGET_HEIGHT = 800, 600

# Patrimônios a rebuscar com novos termos
REBUSCAR = [
    {"patrimonio": "TI-0001", "nome": "Notebook 14 polegadas", "busca": "laptop macbook desk minimal"},
]

USED_IDS = {
    "1853259", "886462", "4532323", "1868496", "6801334",
    "2202226", "4875319", "494649",
    "849825",   # TI-0001 anterior (pessoa com mãos)
    "1219748", "2562361", "272263",
    "594090", "593341", "2364849", "7188564", "1155173",
    "849822", "84626",
}

def get_api_key():
    val = os.environ.get("PIXABAY_API_KEY")
    if val:
        return val
    for p in [Path.cwd(), Path.cwd() / "emprestai-back"]:
        env_file = p / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("PIXABAY_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def search_pixabay(query, api_key, per_page=20):
    url = (f"https://pixabay.com/api/?key={api_key}"
           f"&q={urllib.parse.quote(query)}"
           f"&image_type=photo&orientation=horizontal&safesearch=true&per_page={per_page}")
    req = urllib.request.Request(url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())["hits"]

def resize_crop(img, w=TARGET_WIDTH, h=TARGET_HEIGHT):
    r = img.width / img.height
    if r > w / h:
        nw = int(img.width * (h / img.height)); nh = h
    else:
        nw = w; nh = int(img.height * (w / img.width))
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2; top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))

def main():
    api_key = get_api_key()
    if not api_key:
        print("[ERRO] PIXABAY_API_KEY não encontrada. Use: $env:PIXABAY_API_KEY='sua_chave'")
        sys.exit(1)

    out_dir = Path("staging_images")
    out_dir.mkdir(exist_ok=True)

    used_ids = set(USED_IDS)
    results = []

    for item in REBUSCAR:
        pat = item["patrimonio"]
        busca = item["busca"]
        print(f"\n-> [{pat}] {item['nome']} | busca: '{busca}'")
        
        hits = search_pixabay(busca, api_key)
        selected = None
        for hit in hits:
            pid = str(hit["id"])
            if pid not in used_ids:
                used_ids.add(pid)
                selected = hit
                break
        
        if not selected:
            print(f"   [AVISO] Nenhuma foto nova encontrada para '{busca}'")
            continue

        img_url = selected.get("largeImageURL") or selected.get("webformatURL")
        dest = out_dir / f"{pat}.jpg"
        temp = out_dir / f"temp_{pat}.jpg"
        
        try:
            req = urllib.request.Request(img_url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r, open(temp, "wb") as f:
                f.write(r.read())
            with Image.open(temp) as img:
                processed = resize_crop(img.convert("RGB"))
                processed.save(dest, "JPEG", quality=90)
            temp.unlink(missing_ok=True)
            print(f"   ✓ {selected['user']} | {selected.get('pageURL','')}")
            print(f"     Salvo em: {dest}")
            results.append({"patrimonio": pat, "foto_id": selected["id"],
                            "fotografo": selected["user"], "url": selected.get("pageURL","")})
        except Exception as e:
            print(f"   ✗ Erro: {e}")

    print("\n=== CONCLUÍDO ===")
    for r in results:
        print(f"  {r['patrimonio']}: foto #{r['foto_id']} por {r['fotografo']}")
    print("\nAgora: substitua os 4 arquivos no Supabase Storage e recarregue a página.")

if __name__ == "__main__":
    main()
