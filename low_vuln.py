# low_vuln.py
import random
import os

# Low: Using random for security (not cryptographically safe)
def generate_temp_password():
    password = "".join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"Generated temp password: {password}")  # Debug statement
    return password

# Low: Hardcoded API key (developer mistake)
API_KEY = "12345-ABCDE"

# Low: Using eval unsafely but on trusted input (mild risk)
def calculate_expression(expr: str):
    # Suppose input is from internal user
    return eval(expr)

if __name__ == "__main__":
    generate_temp_password()
    print(calculate_expression("2 + 3 * 5"))
