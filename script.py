#!/usr/bin/env python3
import subprocess

def run(cmd):
    return subprocess.getoutput(cmd)

print("\n" + "="*65)
print("   Linux Privilege Escalation Automation Toolkit")
print("="*65 + "\n")

# ---------- SUID ----------
print("[1] Checking SUID files...\n")
suid_files = run("find / -perm -4000 2>/dev/null").split("\n")

interesting = ["find","awk","perl","python","ruby","vim","less","more",
               "nmap","bash","sh","cp","mv","tar","zip","env"]

for f in suid_files:
    if any(i in f for i in interesting):
        print("[HIGH RISK] " + f)
    else:
        print(f)

# ---------- WRITABLE ----------
print("\n[2] Writable files :\n")
print(run("find / -writable -type f 2>/dev/null | head -10"))

# ---------- FILE PERMISSIONS ----------
print("\n[3] Important file permissions:\n")
print("passwd -> " + run("ls -l /etc/passwd"))
print("shadow -> " + run("ls -l /etc/shadow"))

# ---------- CRON ----------
print("\n[4] Cron jobs:\n")
print(run("cat /etc/crontab 2>/dev/null"))

# ---------- SUDO ----------
print("\n[5] Sudo permissions:\n")
sudo = run("sudo -n -l 2>/dev/null")

if sudo:
    print(sudo)
    if "NOPASSWD" in sudo:
        print("\n[!!!] NOPASSWD FOUND -> EASY ROOT")
else:
    print("No sudo access")

# ---------- SERVICES ----------
print("\n[6] Running services:\n")
print(run("systemctl list-units --type=service --state=running | head -10"))

# ---------- KERNEL ----------
print("\n[7] Kernel version:\n")
kernel = run("uname -r")
print(kernel)

if kernel.startswith(("3.", "4.")):
    print("[WARNING] Old kernel -> possible exploits")

print("\n========== DONE ==========\n")
