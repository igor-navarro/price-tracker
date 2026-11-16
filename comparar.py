from urllib.parse import urlparse
import historico
import requests

from lojas.jsonld import extrair_preco

PRODUTOS = {
    "Teste": [
        "https://www.kabum.com.br/produto/904345/mouse-gamer-sem-fio-attack-shark-x11-com-base-de-carregamento-magnetico-rgb-tri-mode-22-000-dpi-sensor-optico-paw3311-5-botoes-preto",
        "https://www.terabyteshop.com.br/produto/37777/fonte-asrock-pro-650w-80-plus-bronze-atx-31-pfc-ativo-preto-pro-650b",
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
        historico.salvar(nome, loja, r["preco"], link)

    if resultados:
        preco, loja, link = min(resultados)
        print(f"\nMenor preço: R$ {preco:.2f} na {loja}")
        print(link)