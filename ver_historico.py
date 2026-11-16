import historico

produto = input("Nome do produto (igual ao do comparar.py): ").strip()
linhas = historico.listar(produto)

if not linhas:
    print("Sem histórico para esse produto.")
for data, loja, preco in linhas:
    print(f"{data}  {loja:<12} R$ {preco:.2f}")
