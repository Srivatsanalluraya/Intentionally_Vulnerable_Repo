# high_vuln.py (modified for testing - intentionally vulnerable patterns inside safe guards)

import pickle
import sqlite3
import subprocess
import os
import requests
import tempfile
import stat

# High: Hardcoded credentials
DB_USER = "admin"
DB_PASS = "password123"

def authenticate(user, password):
    if user == DB_USER and password == DB_PASS:
        return True
    return False

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # High: SQL Injection risk!
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    return cur.fetchall()

def unsafe_deserialization(data):
    # High: Dangerous pickle.load
    return pickle.loads(data)

# -------------------------
# Extra intentionally insecure patterns for scanner detection
# (wrapped in `if False:` so they are not executed at runtime)
# -------------------------

if False:
    # 1) unsafe eval/exec (Semgrep/Bandit should flag)
    user_expr = "2 + 2"
    result_eval = eval(user_expr)          # flagged: eval usage
    exec("print('exec called')")          # flagged: exec usage

if False:
    # 2) subprocess with shell=True and unsanitized concatenation
    user_input = "some_input"
    cmd = "ls -la " + user_input
    subprocess.call(cmd, shell=True)      # flagged: shell=True

if False:
    # 3) os.system call with user input
    os.system("rm -rf /tmp/" + user_input)  # flagged: os.system usage (dangerous)

if False:
    # 4) requests with verify=False (insecure TLS)
    r = requests.get("https://example.com", verify=False)  # flagged: insecure SSL verification

if False:
    # 5) insecure temporary file handling (bad permissions)
    tmp_dir = tempfile.mkdtemp()
    bad_path = os.path.join(tmp_dir, "secret.txt")
    with open(bad_path, "w") as fh:
        fh.write("sensitive")
    # set world-readable permissions (insecure)
    os.chmod(bad_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

# -------------------------
# Keep existing main interactive behavior (unchanged)
# -------------------------
if __name__ == "__main__":
    # Simple interactive demo — remains functional but won't trigger the if False blocks
    user = input("Enter username: ")
    pwd = input("Enter password: ")
    if authenticate(user, pwd):
        print(get_user_data(user))
    else:
        print("Invalid credentials.")
    
    malicious = input("Enter serialized data: ")
    try:
        unsafe_deserialization(malicious.encode())
    except Exception as e:
        print("Deserialization failed (as expected in test):", e)
