#!/usr/bin/env python3
"""
Rebusca de imagens para patrimônios reprovados na revisão visual.

Fluxo em duas etapas (a escolha final é humana):
  1) Candidatos: baixa até N fotos por patrimônio, já em 800x600, para
     staging_images/candidatos/ + candidatos.json (com créditos).
       python refetch_specific.py candidatos
  2) Aprovar: copia o candidato escolhido para staging_images/<PAT>.jpg
     e atualiza manifest-creditos.json.
       python refetch_specific.py aprovar TI-0001=123456 TI-0004=789012

Garantias por código: só Pixabay, 800x600 exatos, nenhum foto_id repetido
(bloqueia os IDs já usados no manifesto e os reprovados), créditos registrados.
Este script NÃO envia nada ao Supabase: o upload é feito por uma pessoa.
"""

import json, os, shutil, sys, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

W, H = 800, 600
N_CANDIDATOS = 6
STAGING = Path("staging_images")
CAND_DIR = STAGING / "candidatos"
MANIFEST = STAGING / "manifest-creditos.json"
CAND_JSON = CAND_DIR / "candidatos.json"

# Patrimônios reprovados na revisão visual e novos termos de busca
REBUSCAR = [
    {"patrimonio": "TI-0001", "nome": "Notebook 14 polegadas", "busca": "laptop isolated white background"},
    {"patrimonio": "TI-0004", "nome": "Notebook 15 polegadas", "busca": "silver laptop white"},
    {"patrimonio": "TI-0011", "nome": "Webcam Full HD", "busca": "web camera"},
    {"patrimonio": "TI-0012", "nome": "Câmera compacta", "busca": "digital camera white background"},
]

# Fotos reprovadas na revisão visual (nunca reutilizar)
REPROVADOS = {
    "849825",   # TI-0001: mãos de pessoa
    "7188564",  # TI-0001: café/cafeteria, não é notebook
    "594090",   # TI-0004: reunião com pessoas
    "1734485",  # TI-0004: logo da Apple legível
    "6105750",  # TI-0004: só teclado, não mostra o notebook
    "1868502",  # TI-0004: notebook pequeno com logo da Apple
    "1155173",  # TI-0011: notebook numa praça, não é webcam
    "2364849",  # TI-0012: criança segurando câmera
    "3545828",  # TI-0012: marca PENTAX e texto legíveis
    "3990861",  # TI-0012: marcas Sony/Zeiss
    "272263",   # TI-0012: marca Samsung
    "3985711",  # TI-0012: marca Lubitel
    "3114729",  # TI-0012: marca Zorki
    "431119",   # TI-0012: marca Nikon
    "3480569",  # TI-0012: várias marcas
    "1362419",  # TI-0012: marca Fujifilm
    "3247925",  # TI-0012: marca Agfa
    "5416893",  # TI-0012: marca Kodak
    "5416894",  # TI-0012: marca Kodak
    "5213430",  # TI-0012: marca Sony
    "6655520",  # TI-0012: é um iPhone, não câmera
    "7169689",  # TI-0012: é um iPhone, não câmera
}


def api_key():
    if os.environ.get("PIXABAY_API_KEY"):
        return os.environ["PIXABAY_API_KEY"]
    for p in [Path.cwd(), Path.cwd() / "emprestai-back"]:
        env = p / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.startswith("PIXABAY_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:  # ignora chave vazia e tenta o próximo .env
                        return val
    return None


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []


def ids_bloqueados(manifest, exceto=()):
    usados = {str(m["foto_id"]) for m in manifest if m["patrimonio"] not in exceto}
    return usados | REPROVADOS


def search(query, key):
    url = ("https://pixabay.com/api/?" + urllib.parse.urlencode({
        "key": key, "q": query, "image_type": "photo", "orientation": "horizontal",
        "safesearch": "true", "per_page": 40, "min_width": W, "min_height": H,
    }))
    req = urllib.request.Request(url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())["hits"]


def resize_crop(img):
    if img.width / img.height > W / H:
        nw, nh = int(img.width * H / img.height), H
    else:
        nw, nh = W, int(img.height * W / img.width)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    l, t = (nw - W) // 2, (nh - H) // 2
    return img.crop((l, t, l + W, t + H))


def baixar(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "EmprestAI-Skill/1.0"})
    tmp = dest.with_suffix(".tmp")
    with urllib.request.urlopen(req, timeout=30) as r, open(tmp, "wb") as f:
        f.write(r.read())
    with Image.open(tmp) as img:
        out = resize_crop(img.convert("RGB"))
        assert out.size == (W, H)
        out.save(dest, "JPEG", quality=90)
    tmp.unlink(missing_ok=True)


def cmd_candidatos(filtro=()):
    key = api_key()
    if not key:
        sys.exit("[ERRO] PIXABAY_API_KEY não encontrada.")
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    alvos = {i["patrimonio"] for i in REBUSCAR}
    bloqueados = ids_bloqueados(manifest, exceto=alvos)
    # mantém candidatos de rodadas anteriores (e bloqueia seus IDs)
    todos = json.loads(CAND_JSON.read_text(encoding="utf-8")) if CAND_JSON.exists() else {}
    for pat, lista in todos.items():
        if not filtro or pat not in filtro:
            bloqueados |= {str(c["foto_id"]) for c in lista}
    for item in REBUSCAR:
        if filtro and item["patrimonio"] not in filtro:
            continue
        pat = item["patrimonio"]
        print(f"\n-> [{pat}] {item['nome']} | busca: '{item['busca']}'")
        lista = []
        for hit in search(item["busca"], key):
            pid = str(hit["id"])
            if pid in bloqueados:
                continue
            dest = CAND_DIR / f"{pat}_{pid}.jpg"
            try:
                baixar(hit.get("largeImageURL") or hit["webformatURL"], dest)
            except Exception as e:
                print(f"   x {pid}: {e}")
                continue
            bloqueados.add(pid)  # evita o mesmo candidato em dois patrimônios
            lista.append({
                "foto_id": hit["id"], "arquivo": dest.name, "tags": hit.get("tags", ""),
                "fotografo": hit["user"],
                "url_fotografo": f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}/",
                "url_original": hit.get("pageURL", ""),
            })
            print(f"   + {dest.name}  [{hit.get('tags', '')}]")
            if len(lista) >= N_CANDIDATOS:
                break
        todos[pat] = lista
    CAND_JSON.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nCandidatos em {CAND_DIR}. Revise visualmente e rode: aprovar TI-XXXX=<foto_id> ...")


def cmd_aprovar(pares):
    cands = json.loads(CAND_JSON.read_text(encoding="utf-8"))
    manifest = load_manifest()
    escolhas = dict(p.split("=", 1) for p in pares)
    alvos = set(escolhas)
    bloqueados = ids_bloqueados(manifest, exceto=alvos)
    if len(set(escolhas.values())) != len(escolhas):
        sys.exit("[ERRO] mesma foto escolhida para dois patrimônios.")
    for pat, pid in escolhas.items():
        if pid in bloqueados:
            sys.exit(f"[ERRO] foto {pid} já usada ou reprovada.")
        c = next((c for c in cands.get(pat, []) if str(c["foto_id"]) == pid), None)
        if not c:
            sys.exit(f"[ERRO] {pid} não é candidato de {pat}.")
        src = CAND_DIR / c["arquivo"]
        with Image.open(src) as img:
            assert img.size == (W, H), f"{src} não é {W}x{H}"
        shutil.copyfile(src, STAGING / f"{pat}.jpg")
        entry = next(m for m in manifest if m["patrimonio"] == pat)
        entry.update({
            "provedor": "Pixabay", "foto_id": c["foto_id"], "fotografo": c["fotografo"],
            "url_fotografo": c["url_fotografo"], "url_original": c["url_original"],
            "licenca": "Pixabay Content License (Livre para uso comercial)",
            "arquivo_local": f"{pat}.jpg", "dimensoes": f"{W}x{H}",
            "status_revisao_visual": "Aprovada na revisão humana (rebusca)",
        })
        print(f"   ✓ {pat} <- foto #{pid} por {c['fotografo']}")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nManifesto atualizado. Envie os arquivos aprovados ao bucket 'equipamentos' MANUALMENTE.")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "candidatos":
        cmd_candidatos(set(sys.argv[2:]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "aprovar":
        cmd_aprovar(sys.argv[2:])
    else:
        print(__doc__)
