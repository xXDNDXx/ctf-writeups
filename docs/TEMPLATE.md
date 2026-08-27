# HTB — <Machine> | Full Walkthrough

> [!TIP]
> **Scope note:** The target IP changes every time the machine spawns.
> Every command below uses `$IP`, set once at the start:
>
> ```bash
> export IP="<machine-ip>"
> ```

---

## 1. Machine Overview & Metadata

| Field | Value |
|---|---|
| **Machine** | <Machine> |
| **Platform** | Hack The Box (retired) |
| **OS** | Linux / Windows |
| **Difficulty** | Easy / Medium / Hard / Insane |
| **Attack Vector** | Web / SMB / … |
| **Key Vulnerabilities** | Bullet list of the chained bugs |

### Attack Chain at a Glance

```
Nmap (…)
   └─> step one
         └─> step two
               └─> root
```

---

## 2. Reconnaissance & Enumeration

### 2.1 Full Nmap Scan

```bash
sudo nmap -sVC -A -Pn -T3 $IP
```

**Why each switch:** (table or bullets explaining the flags)

| Port | State | Service | Version |
|---|---|---|---|
| 22/tcp | open | ssh | OpenSSH … |
| 80/tcp | open | http | Apache … |

```markdown
![Caption of the screenshot](assets/<Machine>/01-nmap-scan.png)
*Caption.*
```

### 2.2 <Enumeration area>

---

## 3. Vulnerability Discovery / Source Code Review

> [!IMPORTANT]
> State the core bug precisely: what is trusted that shouldn't be, and why
> the check fails.

```<language>
// relevant source or snippet
```

---

## 4. Initial Foothold

Step-by-step exploitation, with the request/payload and the resulting shell.

??? success "user.txt — click to reveal"

    ```
    <user-flag>
    ```

---

## 5. Privilege Escalation

```bash
sudo -l
```

Why the misconfiguration matters, then the escalation path.

??? success "root.txt — click to reveal"

    ```
    <root-flag>
    ```

---

## 6. Remediation & Hardening

For each vulnerability found, one concrete fix.

| Vulnerability | Fix |
|---|---|
| … | … |

---

## 7. Lessons Learned

- What made this machine interesting
- Technique worth remembering (link it to your methodology notes)
