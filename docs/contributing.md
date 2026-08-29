# Contributing

Thanks for wanting to add a write-up. This page explains the policy, the
folder layout, and the exact steps to get your write-up onto the site.

## Policy

1. **Retired machines only.** HTB forbids public write-ups of active
   machines. Wait until the machine is retired (THM rooms: check the room's
   own disclosure rules).
2. **Spoilers stay behind a toggle.** Wrap flags in a collapsible block so
   people can attempt the machine first (snippet below).
3. **One machine = one folder**, containing the write-up and its evidence:
   `README.md` plus a sibling `assets/` folder.
4. **Explain the why.** Every command should come with a short reason — the
   goal is to teach, not just to paste output.

## Folder layout

Every write-up is self-contained in its own folder — the write-up, its
screenshots, and any scripts travel together:

```
.
├── HTB/
│   └── Easy/
│       └── Base/                 ← one folder per machine
│           ├── README.md         ← the write-up itself
│           ├── assets/           ← numbered screenshots
│           │   ├── 01-nmap-scan.png
│           │   └── 02-foo-bar.png
│           ├── exploits/         ← optional: PoCs & scripts
│           └── nmap/             ← optional: raw scan output
├── THM/
│   └── Medium/
│       └── Support/              ← same structure for rooms
│           ├── README.md
│           └── assets/
└── ...
```

**Naming conventions**

| Item | Convention | Example |
|---|---|---|
| Machine folder | Platform's exact machine name, `PascalCase` | `Base/`, `Support/` |
| Write-up file | always `README.md` (keeps URLs clean: `/HTB/Easy/Base/`) | `README.md` |
| Screenshots | `NN-kebab-case-description.png`, numbered by order of use | `03-login-directory-listing.png` |
| Exploits | `exploit-<name>.py` or platform-suggested names | `exploit-auth-bypass.py` |

## Adding a write-up, step by step

1. Create `HTB/<Difficulty>/<Machine>/README.md` (or `THM/<Difficulty>/<Room>/`)
   from the [`TEMPLATE.md`](TEMPLATE.md) — the 8-section skeleton.
2. Put screenshots in the same folder under `assets/` and reference them
   with relative paths: `![Caption](assets/01-nmap-scan.png)`
3. Add a nav entry in `mkdocs.yml` so the machine appears in the menu:

   ```yaml
   nav:
     - HTB:
         - Easy:
             - HTB/Easy/README.md
             - Base: HTB/Easy/Base/README.md   # ← add yours like this
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

## Optional: regenerate branding assets

The banner, logo, and social preview in `branding/` are generated with
Pillow from `branding/make_assets.py` — adjust the script and rerun it
whenever the identity needs a refresh:

```bash
python branding/make_assets.py   # needs: pip install pillow
```
