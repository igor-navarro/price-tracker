import json

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def _achar_produto(dado):
    """Procura o bloco do tipo Product dentro do JSON-LD."""
    if isinstance(dado, list):
        for item in dado:
            achado = _achar_produto(item)
            if achado:
                return achado
    elif isinstance(dado, dict):
        tipo = dado.get("@type")
        tipos = tipo if isinstance(tipo, list) else [tipo]
        if "Product" in tipos:
            return dado
        for valor in dado.values():
            if isinstance(valor, (list, dict)):
                achado = _achar_produto(valor)
                if achado:
                    return achado
    return None


def _para_float(valor):
    texto = str(valor).strip()
    if "," in texto:  # formato brasileiro: 1.299,90
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)


def extrair_preco(url):
    """Devolve {'titulo': ..., 'preco': ..., 'link': ...} ou None."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    sopa = BeautifulSoup(resp.text, "html.parser")
    for bloco in sopa.find_all("script", type="application/ld+json"):
        try:
            dados = json.loads(bloco.string or "")
        except json.JSONDecodeError:
            continue

        produto = _achar_produto(dados)
        if not produto:
            continue

        ofertas = produto.get("offers")
        if isinstance(ofertas, list):
            ofertas = ofertas[0] if ofertas else None
        if not isinstance(ofertas, dict):
            continue

        preco = ofertas.get("price") or ofertas.get("lowPrice")
        if preco is None:
            continue

        return {
            "titulo": produto.get("name", "Sem nome"),
            "preco": _para_float(preco),
            "link": url,
        }
    return None