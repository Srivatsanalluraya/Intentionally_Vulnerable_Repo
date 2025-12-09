# ultra_extreme_vuln.py
# This file intentionally contains *severe, high-impact vulnerabilities* for testing security scanners.

import os
import pickle
import subprocess
import sqlite3
import requests

# 1️⃣ Hardcoded credentials + API keys
DB_USER = "admin"
DB_PASSWORD = "supersecret123"
API_KEY = "12345-ABCDE-SECRETKEY"

# 2️⃣ WORLD-WRITABLE temp file (Privilege escalation)
open("/tmp/extreme.log", "w").write("This is insecure!")

# 3️⃣ Remote Code Execution via eval()
def execute_user_code(code):
    return eval(code)  # MASSIVE RCE vulnerability

# 4️⃣ Arbitrary Command Execution
def run_system_command(cmd):
    return os.system(cmd)  # Extremely dangerous

# 5️⃣ Subprocess with shell=True — immediate injection vector
def ping_host(host):
    return subprocess.run(f"ping -c 2 {host}", shell=True)

# 6️⃣ Insecure deserialization (Pickle RCE)
def load_data(data):
    return pickle.loads(data)

# 7️⃣ SQL Injection
def login(username):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(name TEXT, pass TEXT)")
    query = f"SELECT * FROM users WHERE name = '{username}'"  # SQLi vulnerability
    return cur.execute(query).fetchall()

# 8️⃣ Unsafe request to HTTP — no SSL, no timeout
def fetch_data(url):
    return requests.get(url).text  # insecure HTTP + no timeout

# 9️⃣ Insecure temporary directory creation
os.makedirs("/tmp/appdata", exist_ok=True)

# 🔟 Weak cryptography
import hashlib
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is cryptographically broken

# 1️⃣1️⃣ Global exception swallow (hides security failures)
try:
    risky = 1 / 0
except:
    pass

# 1️⃣2️⃣ Exposed debug backdoor
def backdoor():
    password = input("Enter backdoor password: ")
    if password == "root123":
        os.system("/bin/bash")
