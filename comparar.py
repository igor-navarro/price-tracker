from urllib.parse import urlparse

import requests

from lojas.jsonld import extrair_preco

PRODUTOS = {
    "Nome do produto": [
        "COLE_AQUI_O_LINK_DA_KABUM",
        "COLE_AQUI_O_LINK_DA_TERABYTE",
    ],
}


def nome_da_loja(url):
    return urlparse(url).netloc.replace("www.", "").split(".")[0].capitalize()


for nome, links in PRODUTOS.items():
    print(f"\n=== {nome} ===")
    resultados = []

    for link in links:
        loja = nome_da_loja(link)
        try:
            r = extrair_preco(link)
        except requests.HTTPError as e:
            print(f"{loja}: bloqueou o acesso ({e.response.status_code})")
            continue
        except requests.RequestException:
            print(f"{loja}: erro de conexão")
            continue

        if r is None:
            print(f"{loja}: preço não encontrado")
            continue

        print(f"{loja}: R$ {r['preco']:.2f}")
        resultados.append((r["preco"], loja, link))

    if resultados:
        preco, loja, link = min(resultados)
        print(f"\nMenor preço: R$ {preco:.2f} na {loja}")
        print(link)