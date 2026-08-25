# [MACHINE NAME] — [Platform] · [Difficulty]

> **OS:** Linux / Windows · **Techniques:** e.g. LFI → SUID privesc
> **Release:** YYYY-MM-DD · **My time:** Xh Ym · **Dnf:** user ✅ / root ✅

---

## 1. Recon

```bash
nmap -sC -sV -oN nmap/initial TARGET_IP
```

**Findings:**

| Port | Service | Version | Notes |
|---|---|---|---|
| 22 | ssh | OpenSSH 8.2 | — |
| 80 | http | nginx 1.18 | <!-- what stood out --> |

<!-- Add secondary scans (UDP, full-range) only if they found something. -->

## 2. Enumeration

<!-- What did you enumerate and WHY? Explain the reasoning, not just commands. -->

```bash
ffuf -u http://TARGET_IP/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fc 404
```

**Key discovery:** <!-- e.g. /admin login page running X app v1.2 -->

## 3. Foothold (User)

<!-- The exploit. State the vulnerability class first, then show it. -->

**Vulnerability:** <!-- e.g. SQL injection in login form (auth bypass) -->

```bash
# the command that got you in
```

```bash
$ cat user.txt
> HTB{...}
```

## 4. Privilege Escalation (Root)

**Enumeration:**

```bash
sudo -l
find / -perm -4000 2>/dev/null
```

**Vector:** <!-- e.g. sudo version vulnerable to CVE-XXXX-XXXX -->

```bash
# privesc command
```

```bash
$ cat /root/root.txt
> HTB{...}
```

## 5. Lessons Learned

- <!-- One concrete takeaway about the technique -->
- <!-- One thing you'd do faster next time -->
- <!-- One tool/command you're adding to your cheatsheet -->

## 6. Artifacts

- [nmap scans](./nmap/) · [exploit scripts](./exploits/) · [loot](./loot/)
