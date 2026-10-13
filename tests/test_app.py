"""HTTP contracts, preserved content and discoverability; no browser required."""

import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit

from app import ASSET_VERSIONS, LEGACY_PROJECTS, SITE_URL, app
from projects import FEATURED_ORDER, PROJECTS


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_ten_unique_projects_without_duplicate_cards(self):
        html = self.client.get("/").get_data(as_text=True)
        cards = [
            a
            for tag, a in Document(html).elements
            if tag == "article" and "project-card" in a.get("class", "").split()
        ]
        self.assertEqual(len(cards), 10)
        self.assertEqual(len({p["slug"] for p in PROJECTS}), 10)
        for project in PROJECTS:
            self.assertIn(project["repo"], html)

    def test_every_page_has_unique_metadata_and_one_h1(self):
        paths = ["/"] + ["/projetos/" + p["slug"] for p in PROJECTS]
        titles = set()
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path, headers={"Host": "untrusted.example"})
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                doc = Document(html)
                self.assertEqual(sum(tag == "h1" for tag, _ in doc.elements), 1)
                canonical = next(
                    a["href"]
                    for tag, a in doc.elements
                    if tag == "link" and a.get("rel") == "canonical"
                )
                self.assertEqual(canonical, SITE_URL + path)
                titles.add(re.search(r"<title>(.*?)</title>", html).group(1))
                structured = re.search(
                    r'<script type="application/ld\+json">(.*?)</script>', html, re.S
                )
                data = json.loads(structured.group(1))
                self.assertEqual(data["@context"], "https://schema.org")
                self.assertNotIn("untrusted.example", html)
                self.assertTrue(any(a.get("property") == "og:image" for _, a in doc.elements))
                self.assertTrue(any(a.get("name") == "twitter:card" for _, a in doc.elements))
        self.assertEqual(len(titles), len(paths))

    def test_editorial_selection_and_case_navigation(self):
        featured = [p["slug"] for p in PROJECTS if p.get("featured")]
        self.assertEqual(tuple(featured), FEATURED_ORDER)
        self.assertEqual(tuple(p["slug"] for p in PROJECTS[:5]), FEATURED_ORDER)
        for project in PROJECTS:
            html = self.client.get("/projetos/" + project["slug"]).get_data(as_text=True)
            doc = Document(html)
            for anchor in ["contexto", "solucao", "beneficios"]:
                self.assertTrue(any(a.get("href") == "#" + anchor for _, a in doc.elements))
                self.assertTrue(any(a.get("id") == anchor for _, a in doc.elements))

    def test_local_links_and_assets_resolve(self):
        paths = ["/"] + ["/projetos/" + p["slug"] for p in PROJECTS]
        checked = set()
        for path in paths:
            html = self.client.get(path).get_data(as_text=True)
            doc = Document(html)
            ids = {a["id"] for _, a in doc.elements if "id" in a}
            for tag, attrs in doc.elements:
                target = attrs.get("href") or attrs.get("src")
                if not target or tag not in {"a", "link", "script"}:
                    continue
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    continue
                if parsed.fragment and not parsed.path:
                    self.assertIn(parsed.fragment, ids)
                if parsed.path and target not in checked:
                    checked.add(target)
                    with self.client.get(target) as linked:
                        self.assertEqual(linked.status_code, 200, target)

    def test_sitemap_covers_exactly_canonical_pages(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.mimetype, "application/xml")
        urls = [el.text for el in ET.fromstring(response.data).iter() if el.tag.endswith("loc")]
        self.assertEqual(
            set(urls), {SITE_URL + "/"} | {SITE_URL + "/projetos/" + p["slug"] for p in PROJECTS}
        )
        self.assertIn(
            SITE_URL + "/sitemap.xml", self.client.get("/robots.txt").get_data(as_text=True)
        )

    def test_legacy_redirects_preserved(self):
        for slug, repo in LEGACY_PROJECTS.items():
            response = self.client.get("/projetos/" + slug)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, repo)

    def test_not_found_is_useful_and_not_indexable(self):
        for path in ["/missing-page", "/projetos/unknown"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 404)
            self.assertIn("noindex, follow", response.get_data(as_text=True))
            self.assertIn("Explorar projetos", response.get_data(as_text=True))

    def test_asset_cache_only_immutable_for_matching_version(self):
        version = ASSET_VERSIONS["style.css"]
        response = self.client.get("/static/style.css?v=" + version)
        self.assertIn("immutable", response.headers["Cache-Control"])
        response.close()
        for suffix in ["", "?v=wrong"]:
            with self.client.get("/static/style.css" + suffix) as response:
                self.assertNotIn("immutable", response.headers["Cache-Control"])
        with self.client.get("/favicon.ico", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)

    def test_security_headers_and_no_external_render_dependencies(self):
        response = self.client.get("/")
        self.assertIn("script-src 'self'", response.headers["Content-Security-Policy"])
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        doc = Document(response.get_data(as_text=True))
        for tag, attrs in doc.elements:
            if tag == "script" and "src" in attrs:
                self.assertTrue(attrs["src"].startswith("/static/"))
            if tag == "link" and attrs.get("rel") in {"stylesheet", "preload"}:
                self.assertTrue(attrs["href"].startswith("/static/"))


if __name__ == "__main__":
    unittest.main()
