import json
from urllib.parse import urlparse

import requests

import historico
from lojas.jsonld import extrair_preco


def carregar_produtos(caminho="produtos.json"):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def nome_da_loja(url):
    return urlparse(url).netloc.replace("www.", "").split(".")[0].capitalize()


def main():
    produtos = carregar_produtos()

    for nome, dados in produtos.items():
        print(f"\n=== {nome} ===")
        resultados = []

        for link in dados["links"]:
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
            historico.salvar(nome, loja, r["preco"], link)

        if resultados:
            preco, loja, link = min(resultados)
            print(f"\nMenor preço: R$ {preco:.2f} na {loja}")
            print(link)

            alvo = dados.get("alvo")
            if alvo and preco <= alvo:
                print(f"\nALERTA: abaixo do alvo de R$ {alvo:.2f}!")


if __name__ == "__main__":
    main()