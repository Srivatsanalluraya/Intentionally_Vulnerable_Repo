# high_vuln.py
import pickle
import sqlite3
 
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

if __name__ == "__main__":
    user = input("Enter username: ")
    pwd = input("Enter password: ")
    if authenticate(user, pwd):
        print(get_user_data(user))
    else:
        print("Invalid credentials.")
    
    malicious = input("Enter serialized data: ")
    unsafe_deserialization(malicious.encode())
