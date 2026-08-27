# Contributing

Thanks for wanting to add a write-up. This page explains the policy, the
folder layout, and the exact steps to get your write-up onto the site.

## Policy

1. **Retired machines only.** HTB forbids public write-ups of active
   machines. Wait until the machine is retired (THM rooms: check the room's
   own disclosure rules).
2. **Spoilers stay behind a toggle.** Wrap flags in a collapsible block so
   people can attempt the machine first (snippet below).
3. **One machine = one Markdown file**, named after the machine, with its
   screenshots in a sibling `assets/` folder.
4. **Explain the why.** Every command should come with a short reason — the
   goal is to teach, not just to paste output.

## Folder layout

```
.
├── HTB/
│   ├── Easy/
│   │   ├── MachineName.md        ← the write-up
│   │   └── assets/
│   │       └── MachineName/      ← its screenshots
│   │           ├── 01-nmap-scan.png
│   │           └── ...
│   ├── Medium/
│   ├── Hard/
│   └── Insane/
├── THM/
│   ├── Easy/ … Medium/ … Hard/ … Insane/
├── README.md                     ← site homepage
└── mkdocs.yml                    ← navigation lives here
```

## Adding a write-up, step by step

1. Copy [`TEMPLATE.md`](TEMPLATE.md) to `HTB/<Difficulty>/<Machine>.md`
   (or `THM/<Difficulty>/<Machine>.md`).
2. Put screenshots in `HTB/<Difficulty>/assets/<Machine>/` and reference
   them with relative paths:
   `![Caption](assets/<Machine>/01-nmap-scan.png)`
3. Add a nav entry in `mkdocs.yml` so the machine appears in the menu:

   ```yaml
   nav:
     - HTB:
         - Easy:
             - HTB/Easy/README.md
             - Base: HTB/Easy/Base.md        # ← add yours like this
   ```

4. Add the machine to the table on the platform's difficulty page
   (e.g. `HTB/Easy/README.md`) and to the index table on the homepage.
5. Preview locally, then open a pull request. Every push to `main` is built
   and published automatically by GitHub Actions.

## Flag spoiler toggle

```markdown
??? success "Flag — click to reveal"

    ```
    5f8ac2473095056a3e4d9a1e0f3c8b02
    ```
```

Renders as a collapsible block on the site.

## Preview the site locally

```bash
pip install -r requirements.txt
mkdocs serve      # live preview at http://127.0.0.1:8000
mkdocs build      # static build into site/
```

## Building blocks you can use

- GitHub-style callouts (`> [!TIP]`, `> [!WARNING]`, `> [!IMPORTANT]`, …) are
  converted automatically to Material admonitions by a build hook — write
  them exactly like in Obsidian/GitHub.
- `!!! note "Title"` / `!!! warning` admonitions also work directly.
- Collapsible `??? details "Title"` blocks for long output or flags.
- Code fences get syntax highlighting and a copy button automatically.
