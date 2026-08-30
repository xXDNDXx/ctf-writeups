---
ops:
  machine: <Machine>
  platform: HTB            # HTB | THM
  difficulty: easy         # easy | medium | hard | insane
  os: linux               # linux | windows
  date: YYYY-MM-DD
  vector: web              # web | privesc | ad | recon — primary class
  classes: [web, privesc]  # all classes demonstrated
  tools: [nmap, ffuf, burp]
  summary: "one-line kill chain summary"
description: "<Machine> — <platform> <difficulty> write-up: <summary>"
hide:
  - toc
---

# HTB — <Machine> | Full Walkthrough

<div class="opfor-mesh" aria-hidden="true"></div>

<div class="opfor-metabox">
  <div><span class="meta-label">Platform</span><span class="meta-value"><Platform></span></div>
  <div><span class="meta-label">OS</span><span class="meta-value"><Linux/Windows></span></div>
  <div><span class="meta-label">Difficulty</span><span class="meta-value opfor-tag opfor-tag--<difficulty>"><difficulty></span></div>
  <div><span class="meta-label">Primary Vector</span><span class="meta-value opfor-tag opfor-tag--<vector>"><vector></span></div>
  <div><span class="meta-label">Rooted</span><span class="meta-value">YYYY-MM-DD</span></div>
</div>

> [!TIP]
> **Scope note:** The target IP changes every time the machine spawns.
> Every command below uses `$IP`, set once at the start:
>
> ```bash
> export IP="<machine-ip>"
> ```

---

## 1. Challenge Overview

One paragraph: what the machine is, what the intended path felt like, and the shape of the attack chain in one line.

**Attack chain at a glance:**

```text
nmap → <crack> → <foothold> → <pivot> → <privesc> → root
```

---

## 2. Reconnaissance

**Goal:** map the attack surface before touching anything.

### 2.1 Full Nmap Scan

```bash
sudo nmap -sVC -A -Pn -T3 $IP
```

**Why each switch:** (table or bullets explaining the flags)

| Port | State | Service | Version |
|---|---|---|---|
| 22/tcp | open | ssh | OpenSSH … |
| 80/tcp | open | http | Apache … |

**Screenshot evidence** (drop into the machine's `assets/` folder):

```markdown
![Caption of the screenshot](assets/01-nmap-scan.png)
*Caption.*
```

### 2.2 <Secondary scan — UDP / full-range / scripts>

---

## 3. Enumeration

**Goal:** find the crack in the attack surface. Work the findings, not the checklist.

### 3.1 <Enumeration area — web fuzzing / service enum / AD>

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ -u http://$IP/FUZZ
```

**Key discovery:** e.g. `/admin` login page running X app v1.2

### 3.2 Vulnerability Discovery / Source Review

> [!IMPORTANT]
> State the core bug precisely: what is trusted that shouldn't be, and why
> the check fails.

```php
// relevant source or snippet
```

---

## 4. Exploitation — Initial Foothold

**Vulnerability class:** e.g. SQL injection (auth bypass) · file upload RCE · deserialization

Step-by-step exploitation, with the request/payload and the resulting shell.

```bash
# the command that got you in
```

**Shell stabilization** (if interactive work follows):

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'   # Ctrl+Z
stty raw -echo; fg                                 # on the attacker box
export TERM=xterm; stty rows 40 cols 140
```

??? success "user.txt — click to reveal"

    ```
    <user-flag>
    ```

---

## 5. Privilege Escalation

**Goal:** root. Enumerate systematically — don't guess, verify.

### 5.1 Post-Exploitation Enumeration

```bash
sudo -l                                    # sudo — always first
find / -perm -4000 -type f 2>/dev/null     # SUID binaries
cat /etc/crontab; ls -la /etc/cron*        # scheduled jobs
ss -tlnp                                   # internal services
```

### 5.2 The Vector

Why the misconfiguration matters (GTFOBins / LolBAS reference), then the escalation path:

```bash
# privesc command
```

??? success "root.txt — click to reveal"

    ```
    <root-flag>
    ```

---

## 6. Remediation & Hardening

Client-ready fixes mapped to each finding — this is the section a defender reads.

| # | Vulnerability | Severity | Fix |
|---|---|:---:|---|
| 1 | <finding> | Critical / High / Medium | one concrete fix |
| 2 | <finding> | High | one concrete fix |

---

## 7. Lessons Learned

- **Technique internalized:** <the one concrete takeaway>
- **Do faster next time:** <what you'd do differently>
- **Adding to cheatsheet:** <tool/command/wordlist worth remembering>

---

## 8. Artifacts

| Artifact | Location |
|---|---|
| nmap scans | `assets/` or `nmap/` |
| exploit scripts | `exploits/` |
| loot / evidence | `loot/` |

<div class="opfor-pagefoot">

| | |
|---|---|
| ← Previous | [<Machine>](../<Machine>/README.md) |
| Index | [All write-ups](../../../README.md) · [HTB](../../README.md) · [Easy](../README.md) |
| Next → | *Coming soon* |

</div>
