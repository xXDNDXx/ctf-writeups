---
title: Home
hide:
  - navigation
  - toc
---

<div class="opfor-mesh" aria-hidden="true"></div>

<div class="opfor-hero" markdown="1">

## :material-sword:{ .prompt } CTF WRITE-UPS<span class="blink">_</span>

**Methodology-first offensive security research** — every machine on Hack The Box & TryHackMe documented like a professional engagement: enumerate → understand → exploit → escalate → **report**.

Entry-level penetration tester, SOC-trained. Every box gets a full write-up; every write-up ships remediation a defender can use.

<div class="opfor-hero__actions" markdown="1">

[ Browse write-ups :material-arrow-right:](#opfor-grid){ .opfor-btn .opfor-btn--accent }
[ My methodology :material-compass:](methodology.md){ .opfor-btn }
[ Template :material-file-document-outline:](TEMPLATE.md){ .opfor-btn }

</div>

Search everything — machines, tools, techniques: press <kbd class="opfor-kbd">/</kbd> or <kbd class="opfor-kbd">Ctrl K</kbd>

</div>

<!-- opfor:ops-grid -->

---

## Telemetry

<div class="opfor-grid--hud" id="opfor-hud">

<div class="opfor-stat opfor-reveal">
  <span class="opfor-stat__label">Machines Rooted</span>
  <span class="opfor-stat__value" data-count="2">2</span>
  <span class="opfor-stat__sub">full kill chain, user + root</span>
</div>

<div class="opfor-stat opfor-reveal">
  <span class="opfor-stat__label">Platforms</span>
  <span class="opfor-stat__value" data-count="2">2</span>
  <span class="opfor-stat__sub">HTB · THM</span>
</div>

<div class="opfor-stat opfor-reveal">
  <span class="opfor-stat__label">Attack Classes</span>
  <span class="opfor-stat__value" data-count="6">6</span>
  <span class="opfor-stat__sub">web · privesc · recon …</span>
</div>

<div class="opfor-stat opfor-reveal">
  <span class="opfor-stat__label">Tools in the Field</span>
  <span class="opfor-stat__value" data-count="15">15</span>
  <span class="opfor-stat__sub">nmap → bloodhound</span>
</div>

</div>

---

## Write-up Grid

<div class="opfor-filters" id="opfor-filters" markdown="1">

**PLATFORM** — <span class="opfor-chip" data-filter="platform" data-value="htb" role="button" tabindex="0" aria-pressed="false">HTB <span class="opfor-chip__count" data-hud="platform-htb">0</span></span> <span class="opfor-chip" data-filter="platform" data-value="thm" role="button" tabindex="0" aria-pressed="false">THM <span class="opfor-chip__count" data-hud="platform-thm">0</span></span>

**DIFFICULTY** — <span class="opfor-chip" data-filter="difficulty" data-value="easy" role="button" tabindex="0" aria-pressed="false">easy <span class="opfor-chip__count" data-hud="difficulty-easy">0</span></span> <span class="opfor-chip" data-filter="difficulty" data-value="medium" role="button" tabindex="0" aria-pressed="false">medium <span class="opfor-chip__count" data-hud="difficulty-medium">0</span></span> <span class="opfor-chip" data-filter="difficulty" data-value="hard" role="button" tabindex="0" aria-pressed="false">hard <span class="opfor-chip__count" data-hud="difficulty-hard">0</span></span> <span class="opfor-chip" data-filter="difficulty" data-value="insane" role="button" tabindex="0" aria-pressed="false">insane <span class="opfor-chip__count" data-hud="difficulty-insane">0</span></span>

**ATTACK VECTOR** — <span class="opfor-chip" data-filter="vector" data-value="web" role="button" tabindex="0" aria-pressed="false">web <span class="opfor-chip__count" data-hud="vector-web">0</span></span> <span class="opfor-chip" data-filter="vector" data-value="privesc" role="button" tabindex="0" aria-pressed="false">privesc <span class="opfor-chip__count" data-hud="vector-privesc">0</span></span> <span class="opfor-chip" data-filter="vector" data-value="ad" role="button" tabindex="0" aria-pressed="false">ad <span class="opfor-chip__count" data-hud="vector-ad">0</span></span> <span class="opfor-chip" data-filter="vector" data-value="recon" role="button" tabindex="0" aria-pressed="false">recon <span class="opfor-chip__count" data-hud="vector-recon">0</span></span>

<small markdown="1">Filters stack across axes — a machine matches when it hits at least one active chip per axis. <span id="opfor-clear" class="opfor-chip" role="button" tabindex="0">clear ×</span></small>

</div>

> [!NOTE]
> Looking for a specific technique? Use search — press <kbd class="opfor-kbd">/</kbd> — or browse by platform: [HTB](HTB/README.md) · [THM](THM/README.md)

---

## The Approach

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

## Methodology in five phases

<div class="opfor-grid" markdown="1">

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">PHASE 01</span>
[Reconnaissance](methodology.md#phase-1-reconnaissance){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">Map the attack surface: full-range nmap, version fingerprinting, every scan saved as evidence. Never trust the first 1000 ports.</span>

</div>

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">PHASE 02</span>
[Enumeration](methodology.md#phase-2-enumeration){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">Work the findings, not the checklist. Every discovered service gets deep enumeration before moving on.</span>

</div>

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">PHASE 03</span>
[Exploitation](methodology.md#phase-3-exploitation){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">Identify the vulnerability class first, verify the PoC, prefer manual before Metasploit. Understand why it works.</span>

</div>

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">PHASE 04</span>
[Privilege Escalation](methodology.md#phase-4-privilege-escalation){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">sudo -l first, SUID, cron, internal services, creds on disk — every hit verified against GTFOBins/LolBAS.</span>

</div>

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">PHASE 05</span>
[Documentation](methodology.md#phase-5-documentation){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">Write during the box, not after. Every command gets its why. Dead ends stay in. Remediation for the blue team.</span>

</div>

<div class="opfor-card opfor-reveal" markdown="1">

<span class="opfor-card__meta">RULES OF ENGAGEMENT</span>
[Rules I don't break](methodology.md#rules-i-dont-break){ .opfor-card__title }
<span class="opfor-card__desc" markdown="1">No flag copying. No active machines. No random attacks — every action maps to a finding or a hypothesis. Ethics are not optional.</span>

</div>

</div>

---

## Contribute

Write-ups follow one professional structure, so every machine reads the same way. Grab [the template](TEMPLATE.md), copy it into the right difficulty folder, and add one line to the navigation.

- [Contributing guide](contributing.md) — policy, folder layout, and how to publish
- [Write-up template](TEMPLATE.md) — the 8-section skeleton

> [!IMPORTANT]
> **Ethics:** all targets are intentionally vulnerable lab environments. Nothing in this repository should be used against systems without explicit written authorization.
