# extreme_vuln.py
"""
THIS FILE IS INTENTIONALLY VULNERABLE.
DO NOT USE THIS CODE IN REAL APPLICATIONS.
"""

import os
import subprocess
import pickle
import sqlite3
import requests
import hashlib
import sys
import random

# 🔥 1. Hardcoded credentials (High severity)
DB_USER = "root"
DB_PASS = "SuperSecret123"
API_KEY = "abcd-1234-xyz"

# 🔥 2. Remote command execution (OS Command Injection)
def dangerous_system_call(user_input):
    # user_input = "anything; rm -rf /"
    os.system(f"ping -c 4 {user_input}")

# 🔥 3. Arbitrary code execution via eval()
def execute_user_code(code):
    return eval(code)  # extremely dangerous

# 🔥 4. Insecure deserialization (Pickle RCE)
def load_untrusted_data(blob):
    return pickle.loads(blob)  # can execute arbitrary code

# 🔥 5. SQL Injection vulnerability
def fetch_user(username):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    # vulnerable string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return cur.execute(query).fetchall()

# 🔥 6. Weak hashing for sensitive data
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is broken

# 🔥 7. Insecure HTTP (MITM risk)
def unsafe_http_download(url):
    return requests.get(url).text  # missing TLS enforcement

# 🔥 8. Subprocess with shell=True (Arbitrary OS Command Injection)
def run_shell_command(cmd):
    subprocess.run(cmd, shell=True)

# 🔥 9. Debug information leak
def leak_sensitive_info():
    print(f"[DEBUG] Internal admin password is {DB_PASS}")

# 🔥 10. Writing unsanitized input to a system file
def write_to_system_file(data):
    with open("/etc/passwd", "a") as f:  # catastrophic privilege escalation
        f.write(data)

# 🔥 Trigger functions for demonstration
if __name__ == "__main__":
    dangerous_system_call("127.0.0.1; rm -rf /")
    execute_user_code("__import__('os').system('echo hacked')")
    print(load_untrusted_data(pickle.dumps({"test": 123})))
    print(fetch_user("admin' OR '1'='1"))
    print(weak_hash("password123"))
    print(unsafe_http_download("http://example.com"))
    run_shell_command("ls; cat /etc/shadow")
    leak_sensitive_info()
    write_to_system_file("InjectedUser:::0:0::/root:/bin/bash\n")
