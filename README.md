# Price Tracker

Comparador de preços em Python: lê o preço de páginas de produto (via JSON-LD) em várias lojas e mostra o menor.

## Lojas testadas
- Kabum: funciona
- Terabyte: funciona
- Pichau e Mercado Livre: bloqueiam requisições automáticas

## Como usar
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python comparar.py
```

Edite a lista `PRODUTOS` no `comparar.py` com os links dos produtos.
