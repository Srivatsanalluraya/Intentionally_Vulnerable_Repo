# medium_vuln.py
import os
import subprocess

def list_user_files(username):
    # Medium: OS command injection possible
    os.system(f"ls -l /home/{username}")

def ping_host(host):
    # Medium: Using subprocess with shell=True
    result = subprocess.run(f"ping -c 2 {host}", shell=True)
    return result.returncode

def store_user_input(data):
    # Medium: Writing unvalidated input to a file
    with open("userdata.txt", "a") as f:
        f.write(data + "\n")

if __name__ == "__main__":
    user = input("Enter username: ")
    host = input("Enter host to ping: ")
    data = input("Enter text to store: ")
    list_user_files(user)
    ping_host(host)
    store_user_input(data)
