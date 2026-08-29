---
hide:
  - toc
---

# >_ My Methodology

> The same discipline on every box — and one day, on every engagement.
> This is the playbook I run from first connection to final report.

---

## The Kill Chain

```text
RECON → ENUMERATE → EXPLOIT → ESCALATE → DOCUMENT
  │        │           │          │          │
  map the   find the    abuse a    abuse a    write it
  surface   crack       bug        misconf   like a pro
```

---

## Phase 1 — Reconnaissance

**Question I'm answering:** *What am I looking at?*

```bash
# 1. Connectivity + OS hint (TTL: 64≈Linux, 128≈Windows)
ping -c 1 $IP

# 2. Full TCP port scan — fast first, then deep
sudo nmap -p- --min-rate 5000 -Pn $IP -oN nmap/all-ports
sudo nmap -sVC -A -Pn -p <found> $IP -oN nmap/deep
```

**Rules:**

- Never skip full-range scanning (`-p-`) — backdoors live on high ports
- Version + script scan (`-sVC`) only against found ports — saves hours
- UDP check (`-sU --top-ports 50`) if TCP gives nothing
- Every scan output is saved to `nmap/` — evidence, like a real engagement

---

## Phase 2 — Enumeration

**Question I'm answering:** *Where's the crack?*

| Surface | First moves |
|---|---|
| **Web (80/443)** | Browse + source review → `ffuf` with SecLists `common.txt` → check `/robots.txt`, headers, cookies, JS files |
| **SMB (445)** | `smbclient -L //noauth` → `NetExec smb $IP --shares` |
| **FTP (21)** | Anonymous login → version-specific exploits |
| **SSH (22)** | Version exploits only if creds leak elsewhere — never brute-force first |
| **AD/88,464** | Users via `kerbrute`/`GetNPUsers` → AS-REP roast → BloodHound |

**Rules:**

- **Work the findings, not the checklist** — every discovered service gets *deep* enumeration before moving on
- Editor artifacts (`.swp`, `.bak`, `~`, `.old`) are findings — always in the wordlist
- Screenshot everything — write-up evidence starts here
- When stuck: re-enumerate with a bigger wordlist, re-check SMB/NFS, re-read the source

---

## Phase 3 — Exploitation

**Question I'm answering:** *How do I turn this crack into access?*

1. **Identify the vulnerability class first** — auth bypass, injection, misconfig, logic flaw — before touching exploits
2. **Prefer manual exploitation first** — Metasploit when it's the right tool, not the default
3. **Verify the PoC** — read the exploit code before running it, adapt it, understand why it works
4. **Catch the callback** — `nc -lvnp 443` (443 sneaks past egress filters), then stabilize:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'   # Ctrl+Z
stty raw -echo; fg                                # attacker side
export TERM=xterm; stty rows 40 cols 140
```

---

## Phase 4 — Privilege Escalation

**Question I'm answering:** *What does this account get away with?*

```bash
sudo -l                                   # 1. sudo — always first
find / -perm -4000 -type f 2>/dev/null    # 2. SUID
cat /etc/crontab; ls -la /etc/cron*       # 3. cron
ss -tlnp; ps auxww                        # 4. services only visible from inside
find / -writable -type d 2>/dev/null      # 5. writable paths
grep -rli 'passw' / --include=*.conf 2>/dev/null   # 6. creds on disk
```

- Every `sudo -l` hit and SUID binary gets checked against **GTFOBins/LolBAS**
- **Verify, don't assume** — test the vector, capture the evidence
- Password reuse is a vector: every found cred goes against SSH and other services

---

## Phase 5 — Documentation

**Question I'm answering:** *Could someone else replay this and learn?*

- Start the write-up **during** the box, not after — notes decay fast
- Follow the [8-section template](TEMPLATE.md) — overview → recon → enum → foothold → privesc → remediation → lessons → artifacts
- Every command gets its **why**
- Dead ends stay in — the path teaches more than the flag
- Remediation written for the blue team — I know what defenders see, they should get fixes they can use

---

## Rules I Don't Break

| # | Rule |
|---|---|
| 1 | **No flag copying.** If I can't explain the step, it doesn't go in the write-up |
| 2 | **No active machines.** Retired only — platform disclosure rules are rules |
| 3 | **No random attacks.** Every action maps to a finding or a hypothesis |
| 4 | **Document as I go.** Screenshots and commands captured in the moment |
| 5 | **Ethics are not optional.** These skills exist to make systems safer, full stop |

---

## Tools I Run

| Phase | Core stack |
|---|---|
| Recon | `nmap` · `ping` · `whatweb` · `dnsrecon` |
| Web enum | `ffuf` · `Burp Suite` · `dirsearch` · `SecLists` · browser DevTools |
| Exploitation | `Metasploit` · `searchsploit` · `Netcat` · custom Python |
| Privesc | `GTFOBins` · `PEAS suite` · `BloodHound` · manual checks |
| Cracking | `Hydra` · `Hashcat` · `CyberChef` |
| Reporting | this MkDocs site · Obsidian for field notes |

---

*[← Back to all write-ups](README.md)*
