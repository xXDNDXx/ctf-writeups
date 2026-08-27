"""Convert GitHub-style callouts ("> [!NOTE]" etc.) into Material for MkDocs
admonitions ("!!! note"), so writeups written for Obsidian/GitHub render
correctly on the site without editing the source files.
"""

import re

_TYPES = {
    "note": "note",
    "abstract": "abstract",
    "summary": "abstract",
    "info": "info",
    "todo": "todo",
    "tip": "tip",
    "hint": "tip",
    "important": "important",
    "success": "success",
    "check": "success",
    "question": "question",
    "help": "question",
    "faq": "question",
    "warning": "warning",
    "caution": "warning",
    "attention": "warning",
    "failure": "failure",
    "fail": "failure",
    "missing": "failure",
    "danger": "danger",
    "error": "danger",
    "bug": "bug",
    "example": "example",
}

# "> [!TIP]" / "> [!NOTE]-" / "> [!TIP] Optional title"
_CALLOUT = re.compile(r"^>\s*\[!([A-Za-z]+)\]([+-])?(?:[ \t]+(.*?))?[ \t]*$")
# Continuation line of the same blockquote: "> anything" or ">"
_QUOTE = re.compile(r"^>(?:[ \t]?(.*))$")
_FENCE = re.compile(r"^[ \t]*(?:```|~~~)")


def _convert(source: str) -> str:
    lines = source.splitlines()
    out = []
    i = 0
    in_fence = False
    fence_marker = ""
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            if not in_fence:
                in_fence = True
                fence_marker = stripped[:3]
            elif stripped.startswith(fence_marker):
                in_fence = False
            out.append(line)
            i += 1
            continue

        if not in_fence:
            m = _CALLOUT.match(line)
            if m:
                kind = _TYPES.get(m.group(1).lower(), "note")
                collapsible, title = m.group(2), m.group(3)
                if collapsible:
                    marker = "???" if collapsible == "+" else "???+"
                else:
                    marker = "!!!"
                if title:
                    out.append(f'{marker} {kind} "{title}"')
                else:
                    out.append(f"{marker} {kind}")
                i += 1
                while i < len(lines):
                    q = _QUOTE.match(lines[i])
                    if not q:
                        break
                    content = q.group(1) or ""
                    out.append(("    " + content) if content.strip() else "")
                    i += 1
                continue

        out.append(line)
        i += 1
    return "\n".join(out) + ("\n" if source.endswith("\n") else "")


def on_page_markdown(markdown, *, page, files, **kwargs):
    if "[!" not in markdown:
        return markdown
    return _convert(markdown)
