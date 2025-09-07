import json
from pathlib import Path
from getpass import getpass
from passlib.context import CryptContext

USERS_FILE = Path("users.json")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def load_users():
    if not USERS_FILE.exists():
        return []
    return json.loads(USERS_FILE.read_text())

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))

def main():
    users = load_users()
    username = input("Username: ")
    password = getpass("Password: ")
    hashed = pwd_context.hash(password)
    for u in users:
        if u["username"] == username:
            u["hashed_password"] = hashed
            break
    else:
        users.append({"username": username, "hashed_password": hashed})
    save_users(users)
    print("User saved")

if __name__ == "__main__":
    main()