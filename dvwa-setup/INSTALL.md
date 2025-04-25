# 🛠️ Installing DVWA on Kali Linux (VM)

This guide will walk you through the step-by-step installation of DVWA (Damn Vulnerable Web Application) on Kali Linux.

---

## 🔽 1. Download and Place DVWA

```bash
cd /var/www/html
sudo git clone https://github.com/digininja/DVWA.git dvwa
sudo chmod -R 755 /var/www/html/dvwa
```

---

## ⚙️ 2. Configure DVWA

```bash
cd /var/www/html/dvwa/config
sudo mv config.inc.php.dist config.inc.php
sudo nano config.inc.php
```

Make sure your file contains something like:

```php
<?php
$_DVWA[ 'db_user' ] = 'dvwa';
$_DVWA[ 'db_password' ] = 'p@ssw0rd';
$_DVWA[ 'db_database' ] = 'dvwa';
?>
```

---

## 🛢️ 3. Configure MySQL

### ➤ Start MySQL

```bash
sudo service mysql start
```

### ➤ Create DVWA Database and user

```bash
sudo mysql -u root -p
```

Then in MySQL console :

```sql
CREATE DATABASE dvwa;
CREATE USER 'dvwa'@'127.0.0.1' IDENTIFIED BY 'p@ssw0rd';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'127.0.0.1';
FLUSH PRIVILEGES;
exit;
```

---

## 🔧 4. Configure PHP and Apache

```bash
cd /etc/php/8.2/apache2/
sudo nano php.ini
```

### Modify the folowwing setting :

```ini
allow_url_include = On
```

Save (CTRL + O), then exit (CTRL + X).

---

## 🔁 5. Restart Apache

```bash
sudo service apache2 start
```

---

## ✅ 6. Check PHP Version (Optional)

Create a test file :

```bash
sudo nano /var/www/html/phpinfo.php
```

Add :

```php
<?php
phpinfo();
?>
```

Go to :  
http://127.0.0.1/phpinfo.php

---

## 🚀 7. Start DVWA

In the browser :  
http://127.0.0.1/dvwa/setup.php

Click **"Create / Reset Database"**

### Default Credentials :

- **Username:** `admin`  
- **Password:** `password`

---


