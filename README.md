# Linux Privilege Escalation Automation Toolkit

## 📌 Introduction
The Linux Privilege Escalation Automation Toolkit is a lightweight enumeration tool developed to identify potential privilege escalation vectors in Linux systems. It automates common checks performed during penetration testing and security assessments.

## 🎯 Objective
The main objective of this project is to:
- Automate privilege escalation checks
- Reduce manual effort during enumeration
- Provide clean and readable output
- Help security professionals and learners identify vulnerabilities quickly

## ⚙️ Features
- SUID Binary Enumeration
- Writable File Detection
- Cron Job Analysis
- Sudo Permission Check
- Running Services Enumeration
- Kernel Version Detection

## 🛠️ Technologies Used
- Python 3
- Linux Commands (find, ls, systemctl, uname)

## 🧠 Working Principle
The tool executes system-level commands using Python's subprocess module and collects relevant information:
- Searches for SUID binaries 
- Identifies writable files
- Reads cron jobs from system files
- Checks sudo privileges without password
- Lists running services
- Retrieves kernel version

The results are displayed in a structured and readable format.

## 🚀 Usage
```bash
chmod +x script.py
./script.py
