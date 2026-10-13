"""Real-browser responsive, keyboard and progressive-enhancement regression checks."""

import argparse
import json
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def run(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    report = {"viewports": [], "axe": [], "checks": [], "console_errors": [], "failed_requests": []}
    base = args.base_url.rstrip("/")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        if args.baseline_url:
            for width in [1440, 390]:
                page.set_viewport_size({"width": width, "height": 1000 if width > 800 else 844})
                page.goto(args.baseline_url, wait_until="networkidle")
                for offset in range(
                    0, page.locator("body").bounding_box()["height"].__int__(), 600
                ):
                    page.evaluate("(y) => scrollTo(0, y)", offset)
                    page.wait_for_timeout(130)
                page.evaluate("scrollTo(0, 0)")
                page.wait_for_timeout(800)
                page.screenshot(path=str(output / f"before-{width}.png"), full_page=True)
        page.on("pageerror", lambda error: report["console_errors"].append(str(error)))
        page.on(
            "console",
            lambda msg: report["console_errors"].append(msg.text) if msg.type == "error" else None,
        )
        page.on("requestfailed", lambda request: report["failed_requests"].append(request.url))

        def audit(label):
            if not args.axe_script:
                return
            page.evaluate(Path(args.axe_script).read_text())
            result = page.evaluate("""async () => {
                const r = await axe.run(document, {runOnly: {type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}});
                return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})), passes:r.passes.length};
            }""")
            report["axe"].append({"page": label, **result})

        for width in [360, 390, 768, 1024, 1440, 1920]:
            page.set_viewport_size({"width": width, "height": 900 if width > 800 else 844})
            page.goto(base, wait_until="networkidle")
            expect(page.locator(".project-card")).to_have_count(10)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
                f"Overflow at {width}"
            )
            assert page.evaluate(
                "document.fonts.check('600 16px Sora') && document.fonts.check('400 16px Manrope')"
            )
            page.screenshot(path=str(output / f"after-{width}.png"), full_page=True)
            if width in [390, 1440]:
                page.screenshot(path=str(output / f"hero-{width}.png"))
                audit(f"home-{width}")
            if width <= 800:
                toggle = page.locator(".menu-toggle")
                toggle.click()
                expect(toggle).to_have_attribute("aria-expanded", "true")
                page.keyboard.press("Escape")
                expect(toggle).to_be_focused()
                expect(toggle).to_have_attribute("aria-expanded", "false")
                toggle.click()
                page.locator('#primary-nav a[data-section="projetos"]').click()
                expect(toggle).to_have_attribute("aria-expanded", "false")
                expect(page.locator("#projetos")).to_be_focused()
            for label, count in [
                ("IoT", 1),
                ("IA", 4),
                ("GLPI", 6),
                ("RPA", 9),
                ("Integrações", 10),
                ("Todos", 10),
            ]:
                page.locator(f'[data-filter="{label}"]').click()
                expect(page.locator(".project-card:visible")).to_have_count(count)
            search = page.locator("#project-search")
            search.fill("cobranca")
            expect(page.locator(".project-card:visible")).to_have_count(1)
            expect(page.locator(".project-card:visible h3")).to_contain_text("cobrança")
            page.locator('[data-filter="IoT"]').click()
            expect(page.locator(".empty-state")).to_be_visible()
            page.locator("#reset-filters").click()
            expect(search).to_be_focused()
            expect(page.locator(".project-card:visible")).to_have_count(10)
            search.fill("oracle python")
            expect(page.locator(".project-card:visible")).to_have_count(1)
            page.reload(wait_until="networkidle")
            expect(search).to_have_value("oracle python")
            expect(page.locator(".project-card:visible")).to_have_count(1)
            search.fill("")
            expect(page.locator(".project-card:visible")).to_have_count(10)
            trigger = page.locator(".summary-trigger").first
            trigger.click()
            expect(page.locator("#project-dialog")).to_be_visible()
            expect(page.locator(".dialog-close")).to_be_focused()
            assert (
                page.locator("#dialog-github").get_attribute("href")
                == "https://github.com/Sipauba/glados-assitente-ti"
            )
            assert (
                page.locator("#dialog-case")
                .get_attribute("href")
                .endswith("/projetos/glados-assitente-ti")
            )
            for _ in range(8):
                page.keyboard.press("Tab")
                assert page.evaluate(
                    "document.querySelector('#project-dialog').contains(document.activeElement)"
                )
            if width in [390, 1440]:
                page.screenshot(path=str(output / f"dialog-{width}.png"))
                audit(f"dialog-{width}")
            page.keyboard.press("Escape")
            expect(page.locator("#project-dialog")).not_to_be_visible()
            expect(trigger).to_be_focused()
            trigger.click()
            page.locator(".dialog-scroll").evaluate("(el) => el.scrollTop = el.scrollHeight")
            page.locator(".dialog-close").click()
            trigger.click()
            assert page.locator(".dialog-scroll").evaluate("(el) => el.scrollTop") == 0
            page.locator(".dialog-close").click()
            page.locator('[data-map-step="process"]').click()
            expect(page.locator("#map-caption")).to_contain_text("orquestram")
            page.locator('[data-map-step="output"]').click()
            expect(page.locator("#map-caption")).to_contain_text("alertas")
            paths = page.locator(".case-link").evaluate_all("(links) => links.map(l => l.href)")
            for path in paths:
                response = page.goto(path, wait_until="networkidle")
                assert response.status == 200
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
                    f"Overflow {path} {width}"
                )
            page.goto(base + "/projetos/glados-assitente-ti", wait_until="networkidle")
            if width in [390, 1440]:
                page.screenshot(path=str(output / f"case-{width}.png"), full_page=True)
                audit(f"case-{width}")
            report["viewports"].append(
                {
                    "width": width,
                    "home": "pass",
                    "10_case_pages": "pass",
                    "interactions": "pass",
                    "horizontal_overflow": False,
                }
            )
            print(
                f"PASS {width}px: home, 10 cases, filters/search, modal, navigation, map",
                flush=True,
            )

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.goto(base, wait_until="networkidle")
        page.locator(".summary-trigger").first.click()
        page.mouse.click(4, 4)
        expect(page.locator("#project-dialog")).not_to_be_visible()
        page.keyboard.press("Control+Home")
        page.goto(base, wait_until="networkidle")
        page.keyboard.press("Tab")
        expect(page.locator(".skip-link")).to_be_focused()
        page.keyboard.press("Enter")
        expect(page.locator("#conteudo")).to_be_focused()
        page.locator("#tecnologias").scroll_into_view_if_needed()
        expect(page.locator('[data-section="tecnologias"]')).to_have_attribute(
            "aria-current", "location"
        )
        report["checks"].append("backdrop, skip link and active navigation: pass")

        reduced = browser.new_context(
            reduced_motion="reduce", viewport={"width": 390, "height": 844}
        )
        rp = reduced.new_page()
        rp.goto(base, wait_until="networkidle")
        assert rp.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"
        assert rp.locator(".is-entering").count() == 0
        report["checks"].append("reduced motion: pass")
        reduced.close()

        nojs = browser.new_context(
            java_script_enabled=False, viewport={"width": 390, "height": 844}
        )
        np = nojs.new_page()
        np.goto(base, wait_until="networkidle")
        expect(np.locator(".project-card:visible")).to_have_count(10)
        expect(np.locator("#primary-nav")).to_be_visible()
        expect(np.locator(".project-toolbar")).not_to_be_visible()
        np.locator(".case-link").first.click()
        expect(np.locator("h1")).to_contain_text("Glados")
        assert np.evaluate("document.documentElement.scrollWidth <= innerWidth")
        report["checks"].append("no JavaScript: navigation, content, case links: pass")
        nojs.close()
        browser.close()
    (output / "browser-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    assert not report["console_errors"], report["console_errors"]
    assert not report["failed_requests"], report["failed_requests"]
    assert all(not item["violations"] for item in report["axe"]), report["axe"]
    print("All browser checks passed.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument("--output", default="test-results")
    parser.add_argument("--axe-script")
    parser.add_argument("--baseline-url")
    run(parser.parse_args())
