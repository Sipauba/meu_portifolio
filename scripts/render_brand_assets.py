"""Render deterministic brand assets locally; requires the optional Playwright tools."""

import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def render():
    font = base64.b64encode((ROOT / "static/fonts/sora-latin.woff2").read_bytes()).decode()
    svg = (ROOT / "static/favicon.svg").read_text()
    html = """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><style>
    @font-face{font-family:Sora;src:url(data:font/woff2;base64,FONT)}
    *{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#080d15;color:#eff5fb;font-family:Sora,sans-serif;padding:56px 64px}
    header{display:flex;align-items:center;gap:18px;font-size:18px}header svg{width:45px;height:45px}header span{color:#a9b8c9;font-size:13px;margin-left:auto}
    .body{display:flex;align-items:center;justify-content:space-between;margin-top:53px}h1{font-size:56px;font-weight:600;line-height:1.17;letter-spacing:-3px;margin:0}h1 span{color:#72d9dd}
    .diagram{width:350px;height:270px;background:#101824;border:1px solid #33465e;border-radius:16px;padding:24px;display:flex;flex-direction:column;justify-content:center;gap:16px;font-size:14px}
    .node{padding:12px 16px;border:1px solid #435469;border-radius:8px;display:flex;justify-content:space-between}.node span{color:#72d9dd}.node.center{border-color:#72d9dd;background:#193142;margin-left:35px}
    footer{display:flex;justify-content:space-between;margin-top:57px;border-top:1px solid #263344;padding-top:22px;font-size:12px;color:#a9b8c9;letter-spacing:1px}
    </style><header>LOGO<strong>Mateus Sipaúba</strong><span>FORTALEZA, CE · PORTFÓLIO</span></header>
    <div class="body"><h1>Conecto sistemas.<br><span>Simplifico<br>processos.</span></h1><div class="diagram"><div class="node"><span>01</span> Sistemas & dados</div><div class="node center"><span>02</span> n8n + Python + IA</div><div class="node"><span>03</span> Integrações & soluções</div></div></div>
    <footer><span>AUTOMAÇÃO · INTEGRAÇÕES · IA APLICADA</span><span>mateus.sipauba.com.br ↗</span></footer></html>""".replace(
        "FONT", font
    ).replace("LOGO", svg)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        page.set_content(html)
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(ROOT / "static/images/social-card.png"))
        page.set_viewport_size({"width": 180, "height": 180})
        page.set_content(
            "<style>body{margin:0;background:#080d15}svg{width:180px;height:180px}</style>" + svg
        )
        page.screenshot(path=str(ROOT / "static/apple-touch-icon.png"))
        page.set_viewport_size({"width": 32, "height": 32})
        page.set_content("<style>body{margin:0}svg{width:32px;height:32px}</style>" + svg)
        page.screenshot(path="/tmp/portfolio-favicon.png", omit_background=True)
        # ICO supports a PNG payload; this avoids another imaging dependency.
        import struct

        payload = Path("/tmp/portfolio-favicon.png").read_bytes()
        header = struct.pack("<HHH", 0, 1, 1)
        entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(payload), 22)
        (ROOT / "static/favicon.ico").write_bytes(header + entry + payload)
        browser.close()


if __name__ == "__main__":
    render()
