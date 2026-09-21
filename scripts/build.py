#!/usr/bin/env python3
"""Build static HTML blog for revue-oss-3d into docs/."""

from __future__ import annotations

import html
import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "posts.json"
DOCS = ROOT / "docs"
TAGS_DIR = DOCS / "tags"
POSTS_DIR = DOCS / "posts"

SITE_TITLE = "Revue Open Source Software 3D"
SITE_DESC = "Veille open source 3D, VFX et vidéo — lundi et jeudi."

CSS = """\
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --border: #2d3a4f;
  --text: #e7ecf3;
  --muted: #9aa8bc;
  --accent: #6cb6ff;
  --accent-hover: #9ad0ff;
  --tag-bg: #243044;
  --tag-text: #b8d4f0;
  --radius: 8px;
  --font: system-ui, -apple-system, "Segoe UI", Roboto, Ubuntu, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --max: 720px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-hover); text-decoration: underline; }
.wrap {
  max-width: var(--max);
  margin: 0 auto;
  padding: 1.25rem 1.25rem 3rem;
}
header.site {
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
  padding-bottom: 1.25rem;
}
header.site h1 {
  margin: 0 0 0.35rem;
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
header.site h1 a { color: var(--text); text-decoration: none; }
header.site h1 a:hover { color: var(--accent); }
.tagline { color: var(--muted); margin: 0; font-size: 0.95rem; }
nav.crumbs {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 1.5rem;
}
nav.crumbs a { color: var(--muted); }
nav.crumbs a:hover { color: var(--accent); }
nav.crumbs span.sep { margin: 0 0.35rem; }
.post-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.25rem;
  margin-bottom: 1rem;
}
.post-card h2 {
  margin: 0 0 0.35rem;
  font-size: 1.15rem;
}
.post-card .meta {
  color: var(--muted);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}
.post-card .preview {
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0;
}
.meta { color: var(--muted); font-size: 0.9rem; }
.discovery {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.15rem 1.25rem;
  margin-bottom: 1rem;
}
.discovery h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
}
.discovery h3 a { color: var(--text); }
.discovery h3 a:hover { color: var(--accent); }
.discovery .summary {
  margin: 0 0 0.75rem;
  color: var(--text);
  font-size: 0.95rem;
}
.tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.tag {
  display: inline-block;
  background: var(--tag-bg);
  color: var(--tag-text);
  font-size: 0.75rem;
  font-family: var(--mono);
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  text-decoration: none;
}
.tag:hover {
  background: #2e4058;
  color: var(--accent-hover);
  text-decoration: none;
  border-color: var(--accent);
}
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0 2rem;
  align-items: center;
}
h2.section {
  font-size: 1.25rem;
  margin: 0 0 1rem;
  font-weight: 600;
}
.date-label {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}
footer.site {
  margin-top: 3rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.85rem;
}
.empty { color: var(--muted); }
code { font-family: var(--mono); font-size: 0.9em; }
@media (max-width: 520px) {
  .wrap { padding: 1rem 1rem 2.5rem; }
  header.site h1 { font-size: 1.35rem; }
}
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def format_date_fr(iso: str) -> str:
    dt = datetime.strptime(iso, "%Y-%m-%d")
    months = [
        "", "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre",
    ]
    return f"{dt.day} {months[dt.month]} {dt.year}"


def page(
    title: str,
    body: str,
    *,
    depth: int = 0,
    crumbs: list[tuple[str, str]] | None = None,
) -> str:
    """depth: 0 = docs/, 1 = docs/posts/ or docs/tags/."""
    prefix = "../" * depth
    crumb_html = ""
    if crumbs:
        parts = []
        for i, (label, href) in enumerate(crumbs):
            if i < len(crumbs) - 1 and href:
                parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
            else:
                parts.append(f"<span>{esc(label)}</span>")
        crumb_html = (
            '<nav class="crumbs" aria-label="Fil d’Ariane">'
            + '<span class="sep" aria-hidden="true"> / </span>'.join(parts)
            + "</nav>"
        )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(SITE_DESC)}">
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
  <div class="wrap">
    <header class="site">
      <h1><a href="{prefix}index.html">{esc(SITE_TITLE)}</a></h1>
      <p class="tagline">{esc(SITE_DESC)}</p>
    </header>
    {crumb_html}
    {body}
    <footer class="site">
      <p>Veille open source 3D / VFX / vidéo · lundi &amp; jeudi 9h Europe/Paris</p>
      <p><a href="https://github.com/olanlive/revue-oss-3d">Code source sur GitHub</a>
         · <a href="{prefix}tags/index.html">Tous les tags</a></p>
    </footer>
  </div>
</body>
</html>
"""


def tags_html(tags: list[str], *, tags_base: str) -> str:
    if not tags:
        return ""
    links = [
        f'<a class="tag" href="{tags_base}{esc(t)}.html">#{esc(t)}</a>'
        for t in tags
    ]
    return '<div class="tags">' + "".join(links) + "</div>"


def discovery_html(
    item: dict,
    *,
    tags_base: str,
    show_date: str | None = None,
) -> str:
    date_bit = ""
    if show_date:
        date_bit = (
            f'<p class="date-label"><time datetime="{esc(show_date)}">'
            f"{esc(format_date_fr(show_date))}</time></p>"
        )
    return f"""
<article class="discovery">
  {date_bit}
  <h3><a href="{esc(item['url'])}" rel="noopener" target="_blank">{esc(item['name'])}</a></h3>
  <p class="summary">{esc(item['summary'])}</p>
  {tags_html(item.get('tags', []), tags_base=tags_base)}
</article>
"""


def build() -> None:
    posts = json.loads(DATA.read_text(encoding="utf-8"))
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)

    if DOCS.exists():
        for child in DOCS.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    DOCS.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    TAGS_DIR.mkdir(parents=True, exist_ok=True)

    (DOCS / "style.css").write_text(CSS, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    by_tag: dict[str, list[tuple[str, str, str, dict]]] = defaultdict(list)
    all_tags: set[str] = set()

    for post in posts:
        slug = post["date"]
        for item in post["items"]:
            for tag in item.get("tags", []):
                all_tags.add(tag)
                by_tag[tag].append((post["date"], post["title"], slug, item))

    cards = []
    for post in posts:
        slug = post["date"]
        n = len(post["items"])
        names = ", ".join(i["name"] for i in post["items"][:3])
        if n > 3:
            names += "…"
        cards.append(f"""
<article class="post-card">
  <p class="meta"><time datetime="{esc(post['date'])}">{esc(format_date_fr(post['date']))}</time>
     · {n} découverte{'s' if n != 1 else ''}</p>
  <h2><a href="posts/{esc(slug)}.html">{esc(post['title'])}</a></h2>
  <p class="preview">{esc(names)}</p>
</article>
""")

    tag_links = "".join(
        f'<a class="tag" href="tags/{esc(t)}.html">#{esc(t)}</a>'
        for t in sorted(all_tags)
    )
    home_body = f"""
<section>
  <h2 class="section">Dernières revues</h2>
  {''.join(cards) if cards else '<p class="empty">Aucune revue pour le moment.</p>'}
</section>
<section>
  <h2 class="section">Tags</h2>
  <div class="tag-cloud">{tag_links or '<span class="empty">—</span>'}</div>
</section>
"""
    (DOCS / "index.html").write_text(
        page(SITE_TITLE, home_body, depth=0), encoding="utf-8"
    )

    for post in posts:
        slug = post["date"]
        items_html = "".join(
            discovery_html(item, tags_base="../tags/")
            for item in post["items"]
        )
        body = f"""
<p class="meta"><time datetime="{esc(post['date'])}">{esc(format_date_fr(post['date']))}</time></p>
<h2 class="section">{esc(post['title'])}</h2>
{items_html}
"""
        (POSTS_DIR / f"{slug}.html").write_text(
            page(
                f"{post['title']} · {SITE_TITLE}",
                body,
                depth=1,
                crumbs=[("Accueil", "../index.html"), (post["title"], "")],
            ),
            encoding="utf-8",
        )

    for tag in sorted(all_tags):
        entries = sorted(by_tag[tag], key=lambda e: e[0], reverse=True)
        items_html = "".join(
            discovery_html(item, tags_base="./", show_date=date)
            for date, _title, _slug, item in entries
        )
        body = f"""
<h2 class="section">Tag <code>#{esc(tag)}</code></h2>
<p class="meta">{len(entries)} découverte{'s' if len(entries) != 1 else ''}</p>
{items_html}
"""
        (TAGS_DIR / f"{tag}.html").write_text(
            page(
                f"#{tag} · {SITE_TITLE}",
                body,
                depth=1,
                crumbs=[
                    ("Accueil", "../index.html"),
                    ("Tags", "index.html"),
                    (f"#{tag}", ""),
                ],
            ),
            encoding="utf-8",
        )

    cloud_parts = []
    for t in sorted(all_tags):
        cloud_parts.append(
            f'<a class="tag" href="{esc(t)}.html">#{esc(t)}</a>'
            f'<span class="meta">({len(by_tag[t])})</span>'
        )
    tags_index_body = f"""
<h2 class="section">Tous les tags</h2>
<div class="tag-cloud">{' '.join(cloud_parts) or '<span class="empty">—</span>'}</div>
"""
    (TAGS_DIR / "index.html").write_text(
        page(
            f"Tags · {SITE_TITLE}",
            tags_index_body,
            depth=1,
            crumbs=[("Accueil", "../index.html"), ("Tags", "")],
        ),
        encoding="utf-8",
    )

    print(f"Built {len(posts)} post(s), {len(all_tags)} tag(s) → {DOCS}")


if __name__ == "__main__":
    build()
