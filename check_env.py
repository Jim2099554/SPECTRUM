import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASS",
    "SECRET_KEY",
    "API_TOKEN",
    "RISK_PHRASES_PATH"
]

print("=== SENTINELA ENVIRONMENT DIAGNOSTIC ===")
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"[OK] {var} = {value}")
    else:
        print(f"[MISSING] {var} is not set!")
