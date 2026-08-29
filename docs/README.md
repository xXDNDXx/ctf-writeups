---
title: Home
hide:
  - navigation
  - toc
---

# >_ CTF WRITE-UPS

**Methodology-first offensive security write-ups** for **Hack The Box** and **TryHackMe** — every machine documented like a professional engagement: enumerate → understand → exploit → escalate → **report**.

I'm **Daniel Dayan**, an entry-level penetration tester with a SOC/blue-team foundation (650-hour Cisco & Fortinet program) — which means every write-up here also ships with remediation a defender can actually use.

[**:simple-hackthebox: Hack The Box**](HTB/README.md) · [**:simple-tryhackme: TryHackMe**](THM/README.md) · [**:material-compass: My Methodology**](methodology.md) · Retired machines only · Web · Linux · Windows · PrivEsc

---

## :material-sword: The Approach

Every write-up in this collection follows the same professional discipline:

- **Full kill chain** — first nmap scan to root shell, nothing skipped
- **The "why" for every command** — methodology over answer-pasting
- **Dead ends documented** — the path to the flag is the lesson
- **Remediation for the blue team** — I know what defenders see; my fixes reflect that
- **Flags behind spoiler toggles** — attempt the machine first, compare notes after

!!! warning "Spoilers below"

    Every write-up contains full commands, source code, and flags.
    Attempt the machine on your own first — then come back to compare notes
    or get unstuck.

!!! note "Publication policy"

    Only write-ups for **retired** Hack The Box machines are published here,
    in line with HTB's disclosure rules. No active machines, ever.

---

## Machine Index

:simple-hackthebox: **Hack The Box**

| Machine | Difficulty | OS | Kill chain | Status |
|---|:---:|:---:|---|---|
| [**Base**](HTB/Easy/Base/README.md) | :green-circle: Easy | Linux | `strcmp` type-juggling auth bypass → file upload RCE → password reuse → `sudo find` privesc | Retired |

:fontawesome-regular-window-restore: **TryHackMe**

| Room | Difficulty | Kill chain | Status |
|---|:---:|---|---|
| [**Support**](THM/Medium/Support/README.md) | :yellow_circle: Medium | hydra brute-force → forged `isITUser` role cookie → BOLA API abuse → skin LFI → hard-coded password → command injection | Premium room |

---

## Skills & Tools on Display

The write-ups here demonstrate hands-on use of the professional pentest stack:

**Recon & Enumeration** — nmap · ffuf · gobuster · SecLists · dnsrecon
**Web attacks** — Burp Suite · OWASP ZAP · SQLMap · auth bypasses · LFI · injection
**Exploitation** — Metasploit · searchsploit · Netcat · PoC adaptation · shell stabilization
**PrivEsc** — sudo/SUID abuse (GTFOBins) · cron · service misuse · credential reuse
**Cracking** — Hydra · Hashcat · CyberChef
**Scripting** — Python · Bash · PowerShell

Full roadmap — certifications, current study focus, and the playbook behind every write-up — on [**My Methodology**](methodology.md).

---

## Contribute

Write-ups follow one professional structure, so every machine reads the same way. Grab [the template](TEMPLATE.md), copy it into the right difficulty folder, and add one line to the navigation.

- [Contributing guide](contributing.md) — policy, folder layout, and how to publish
- [Write-up template](TEMPLATE.md) — the 8-section skeleton

---

> [!IMPORTANT]
> **Ethics:** all targets are intentionally vulnerable lab environments. Nothing in this repository should be used against systems without explicit written authorization.
