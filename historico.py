import sqlite3
from datetime import datetime

DB = "historico.db"


def _conectar():
    con = sqlite3.connect(DB)
    con.execute(
        """CREATE TABLE IF NOT EXISTS precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            loja TEXT,
            preco REAL,
            link TEXT,
            data TEXT
        )"""
    )
    return con


def salvar(produto, loja, preco, link):
    con = _conectar()
    con.execute(
        "INSERT INTO precos (produto, loja, preco, link, data) VALUES (?, ?, ?, ?, ?)",
        (produto, loja, preco, link, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    con.commit()
    con.close()


def listar(produto):
    con = _conectar()
    linhas = con.execute(
        "SELECT data, loja, preco FROM precos WHERE produto = ? ORDER BY data",
        (produto,),
    ).fetchall()
    con.close()
    return linhas