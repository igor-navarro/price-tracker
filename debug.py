import re

import requests
from bs4 import BeautifulSoup

from lojas.jsonld import HEADERS

url = input("Cole o link do produto: ").strip()
resp = requests.get(url, headers=HEADERS, timeout=15)
sopa = BeautifulSoup(resp.text, "html.parser")

print("\nStatus:", resp.status_code)
print("URL final:", resp.url)
print("Título da página:", sopa.title.string if sopa.title else None)
print("Tamanho do HTML:", len(resp.text))
print("Blocos JSON-LD:", len(sopa.find_all("script", type="application/ld+json")))

metas = sopa.find_all("meta", attrs={"property": re.compile("price", re.I)})
print("Metas com 'price':", [(m.get("property"), m.get("content")) for m in metas])

achados = re.findall(r'"price"\s*:\s*"?([\d.,]+)', resp.text)
print("Ocorrências de \"price\" no HTML:", achados[:5])

with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(resp.text)
print("\nHTML salvo em pagina.html")