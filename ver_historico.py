import json

import historico


def main():
    with open("produtos.json", encoding="utf-8") as f:
        produtos = list(json.load(f).keys())

    print("Produtos:")
    for i, nome in enumerate(produtos, start=1):
        print(f"  {i}. {nome}")

    escolha = input("\nNúmero do produto: ").strip()
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(produtos):
        print("Opção inválida.")
        return

    produto = produtos[int(escolha) - 1]
    linhas = historico.listar(produto)

    if not linhas:
        print("Sem histórico para esse produto.")
        return

    print(f"\n=== {produto} ===")
    for data, loja, preco in linhas:
        print(f"{data}  {loja:<12} R$ {preco:.2f}")

    menor = min(linhas, key=lambda l: l[2])
    print(f"\nMenor preço registrado: R$ {menor[2]:.2f} na {menor[1]} ({menor[0]})")


if __name__ == "__main__":
    main()