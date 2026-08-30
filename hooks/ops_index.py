"""OPFOR site hook — build-time ops index.

Scans every writeup (docs/HTB|THM/<Difficulty>/<Machine>/README.md) for
`ops:` frontmatter and:
  1. injects a global ops index (JSON) into every page as <script id="opfor-ops">
  2. injects per-card markup on the homepage by replacing a placeholder
     markdown comment — the homepage stays hand-written markdown, the grid
     is generated from frontmatter so it never goes stale.

Frontmatter schema (all optional except machine/difficulty/platform):
    ---
    ops:
      machine: Base
      platform: HTB          # HTB | THM
      difficulty: easy       # easy | medium | hard | insane
      os: linux              # linux | windows
      date: 2026-08-20
      vector: web            # web | privesc | ad | recon (primary class)
      classes: [web, privesc]# multi-tag
      tools: [nmap, ffuf, burp]
      summary: "one-line kill chain"
    ---

This keeps the writeup source of truth in frontmatter; the homepage,
indexes, and client search all derive from it.
"""

import json
import re
from datetime import date

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

PLACEHOLDER = "<!-- opfor:ops-grid -->"

PLATFORM_ICON = {"HTB": ":simple-hackthebox:", "THM": ":simple-tryhackme:"}


def _parse_date(v):
    if isinstance(v, date):
        return v.isoformat()
    return str(v)


def _norm(v):
    return str(v).lower().strip()


def _load_ops(cfg: MkDocsConfig, files: Files):
    """Walk the file tree and collect ops frontmatter per writeup page."""
    index = []
    for f in files:
        if not f.src_path.endswith("README.md"):
            continue
        parts = f.src_path.replace("\\", "/").split("/")
        # HTB/Easy/Base/README.md -> ['HTB','Easy','Base','README.md']
        if len(parts) != 4 or parts[0] not in ("HTB", "THM"):
            continue
        if not f.content_string:
            continue
        text = f.content_string
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if not m:
            continue
        try:
            import yaml

            meta = yaml.safe_load(m.group(1)) or {}
        except Exception:
            continue
        ops = meta.get("ops")
        if not isinstance(ops, dict):
            continue
        platform = parts[0]
        difficulty = parts[1].lower()
        machine = parts[2]
        # Cards render on the homepage, which sits at the site root — so the
        # link is simply the page path relative to root. Works on the
        # github.io/<repo>/ subpath deploy and under mkdocs serve alike.
        url = "/".join(parts[:3])
        entry = {
            "machine": str(ops.get("machine", machine)),
            "platform": _norm(ops.get("platform", platform)),
            "difficulty": _norm(ops.get("difficulty", difficulty)),
            "os": _norm(ops.get("os", "linux")),
            "date": _parse_date(ops.get("date", "")),
            "vector": _norm(ops.get("vector", "web")),
            "classes": [_norm(c) for c in (ops.get("classes") or [ops.get("vector", "web")])],
            "tools": [_norm(t) for t in (ops.get("tools") or [])],
            "summary": str(ops.get("summary", "")),
            "url": url,
            "root": "/".join(parts[1:3]),  # Easy/Base
        }
        index.append(entry)
    index.sort(key=lambda e: (e["date"] or "0000", e["machine"]), reverse=True)
    return index


def _telemetry(index):
    """Aggregate HUD numbers from the index."""
    tools = {}
    for e in index:
        for t in e["tools"]:
            tools[t] = tools.get(t, 0) + 1
    vectors = {}
    for e in index:
        vectors[e["vector"]] = vectors.get(e["vector"], 0) + 1
    return {
        "machines": len(index),
        "platforms": len({e["platform"] for e in index}),
        "tools": tools,
        "vectors": vectors,
        "classes": sorted({c for e in index for c in e["classes"]}),
        "difficulty": {d: sum(1 for e in index if e["difficulty"] == d) for d in ("easy", "medium", "hard", "insane")},
    }


def _card(entry):
    """Render one bento card as HTML."""
    icon = PLATFORM_ICON.get(entry["platform"].upper(), ":material-console:")
    classes = " ".join(entry["classes"])
    tags = []
    for c in entry["classes"][:3]:
        tags.append(f'<span class="opfor-tag opfor-tag--{c}">{c}</span>')
    tag_html = "\n".join(tags)
    tool_html = " · ".join(entry["tools"][:5])
    url = entry["url"].lstrip("/")
    return f"""<article class="opfor-card opfor-reveal" data-platform="{entry['platform']}" data-os="{entry['os']}" data-difficulty="{entry['difficulty']}" data-vector="{entry['vector']}" data-classes="{classes}" data-machine="{entry['machine'].lower()}">
  <div class="opfor-card__meta">
    <span class="material-symbols-outlined" aria-hidden="true">terminal</span>
    <span>{icon} {entry['platform'].upper()}</span>
    <span aria-hidden="true">·</span>
    <span>{entry['difficulty']}</span>
    <span aria-hidden="true">·</span>
    <span>{entry['os']}</span>
  </div>
  <a class="opfor-card__title" href="{entry['url']}/">{entry['machine']}</a>
  <p class="opfor-card__desc">{entry['summary']}</p>
  <div class="opfor-card__tags">
    {tag_html}
  </div>
  <div class="opfor-card__meta" style="margin-top:auto">
    <span class="t-tools">{tool_html}</span>
  </div>
</article>"""


def _grid(index):
    cards = "\n".join(_card(e) for e in index)
    return f'<div class="opfor-grid" id="opfor-grid">\n{cards}\n</div>'


def on_page_markdown(markdown: str, *, page: Page, config: MkDocsConfig, files: Files, **kwargs) -> str:
    """Homepage: replace the placeholder comment with the generated grid."""
    index = getattr(config, "_opfor_index", None)
    if index is None:
        index = _load_ops(config, files)
        try:
            config._opfor_index = index
        except Exception:
            pass
    if page.url == "" or page.url == "index.html":
        if PLACEHOLDER in markdown:
            markdown = markdown.replace(PLACEHOLDER, _grid(index))
    return markdown


def on_page_context(context, *, page: Page, config: MkDocsConfig, **kwargs):
    """Expose telemetry to the homepage template if needed."""
    return context


def on_post_build(config: MkDocsConfig, **kwargs):
    """Write the ops index JSON next to the site assets for the search modal."""
    import os

    index = getattr(config, "_opfor_index", [])
    out = os.path.join(config.site_dir, "opfor-ops.json")
    data = {"ops": index, "telemetry": _telemetry(index)}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[opfor] wrote {len(index)} ops entries -> {out}")
