import json
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk
from urllib.parse import urlparse

import requests

import historico
from lojas.jsonld import extrair_preco

links = {}  # guarda o link de cada linha da tabela


def carregar_produtos(caminho="produtos.json"):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def nome_da_loja(url):
    return urlparse(url).netloc.replace("www.", "").split(".")[0].capitalize()


def consultar():
    botao.config(state="disabled")
    status.set("Consultando as lojas...")
    threading.Thread(target=trabalho, daemon=True).start()


def trabalho():
    produtos = carregar_produtos()
    linhas = []  # (produto, loja, preco ou None, situacao, link)

    for nome, dados in produtos.items():
        for link in dados["links"]:
            loja = nome_da_loja(link)
            try:
                r = extrair_preco(link)
            except requests.HTTPError as e:
                linhas.append((nome, loja, None, f"bloqueou ({e.response.status_code})", link))
                continue
            except requests.RequestException:
                linhas.append((nome, loja, None, "erro de conexão", link))
                continue

            if r is None:
                linhas.append((nome, loja, None, "preço não encontrado", link))
                continue

            historico.salvar(nome, loja, r["preco"], link)
            linhas.append((nome, loja, r["preco"], "", link))

    janela.after(0, mostrar, linhas, produtos)


def mostrar(linhas, produtos):
    tabela.delete(*tabela.get_children())
    links.clear()
    alertas = []

    for nome in produtos:
        do_produto = [l for l in linhas if l[0] == nome]
        precos = [l[2] for l in do_produto if l[2] is not None]
        menor = min(precos) if precos else None
        alvo = produtos[nome].get("alvo")

        for _, loja, preco, situacao, link in do_produto:
            if preco is None:
                texto, tag = "-", ""
            else:
                texto = f"R$ {preco:.2f}"
                tag = "menor" if preco == menor else ""
                if preco == menor:
                    situacao = "MENOR PREÇO"
            linha = tabela.insert("", "end", values=(nome, loja, texto, situacao), tags=(tag,))
            links[linha] = link

        if menor is not None and alvo and menor <= alvo:
            alertas.append(f"{nome} (R$ {menor:.2f})")

    if alertas:
        status.set("ALERTA abaixo do alvo: " + ", ".join(alertas))
    else:
        status.set("Pronto. Duplo clique em uma linha abre o produto.")
    botao.config(state="normal")


def abrir_link(_evento):
    selecionado = tabela.focus()
    if selecionado in links:
        webbrowser.open(links[selecionado])


janela = tk.Tk()
janela.title("Comparador de Preços")
janela.geometry("820x420")

botao = tk.Button(janela, text="Consultar preços", command=consultar)
botao.pack(padx=10, pady=10, anchor="w")

tabela = ttk.Treeview(janela, columns=("produto", "loja", "preco", "situacao"), show="headings")
for col, titulo, largura in [
    ("produto", "Produto", 250),
    ("loja", "Loja", 120),
    ("preco", "Preço", 110),
    ("situacao", "Situação", 260),
]:
    tabela.heading(col, text=titulo)
    tabela.column(col, width=largura, stretch=(col == "situacao"))
tabela.tag_configure("menor", background="#1f6f3f", foreground="white")
tabela.pack(fill="both", expand=True, padx=10)
tabela.bind("<Double-1>", abrir_link)

status = tk.StringVar(value="Clique em Consultar preços.")
tk.Label(janela, textvariable=status, anchor="w").pack(fill="x", padx=10, pady=5)

janela.mainloop()