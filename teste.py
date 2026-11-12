from lojas.jsonld import extrair_preco

url = input("Cole o link do produto: ").strip()
resultado = extrair_preco(url)

if resultado:
    print(f"\nProduto: {resultado['titulo']}")
    print(f"Preço:   R$ {resultado['preco']:.2f}")
else:
    print("Não consegui achar o preço nessa página.")