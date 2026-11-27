"""Gera uma versão estática (GitHub Pages) das páginas públicas do app.

Uso: python scripts/gerar_site_estatico.py <pasta-do-repo> <pasta-de-saida>
"""
import re, shutil, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo))
from fastapi.testclient import TestClient
from app.main import app

PAGES = {"/": "index.html", "/agendar": "agendar.html", "/produtos": "produtos.html",
         "/privacidade": "privacidade.html", "/lgpd/meus-dados": "lgpd.html", "/admin/login": "admin.html"}
LINKS = dict(PAGES); LINKS["/admin"] = "admin.html"

AVISO = """
<div class="demo-banner" style="background:#b45309;color:#fff;text-align:center;padding:8px 12px;font:500 14px Inter,sans-serif">
  Versão de demonstração (GitHub Pages) — agendamentos e login funcionam apenas no sistema completo rodando com o servidor Python.
</div>
<script>
document.addEventListener('submit', function (e) {
  e.preventDefault();
  alert('Esta é a versão de demonstração no GitHub Pages.\\nPara agendar ou acessar o painel, rode o sistema completo (veja o README).');
}, true);
</script>
"""

def rewrite(html: str) -> str:
    html = re.sub(r'(href|src)="/static/([^"?]*)(\?[^"]*)?"', r'\1="static/\2"', html)
    def fix(m):
        attr, path = m.group(1), m.group(2)
        base = path.split("?")[0].split("#")[0]
        if base in LINKS: return f'{attr}="{LINKS[base]}"'
        if base.startswith("/admin"): return f'{attr}="admin.html"'
        return m.group(0)
    html = re.sub(r'(href|action)="(/[^"]*)"', fix, html)
    return html

with TestClient(app) as c:
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    for route, fname in PAGES.items():
        r = c.get(route); r.raise_for_status()
        html = rewrite(r.text)
        html = re.sub(r'(<body[^>]*>)', r'\1' + AVISO.replace('\\', '\\\\'), html, count=1)
        (out / fname).write_text(html, encoding="utf-8")
        print("ok", route, "->", fname, len(html))
shutil.copytree(repo / "app" / "static", out / "static")
(out / ".nojekyll").write_text("")
