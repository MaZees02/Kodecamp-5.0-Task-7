import json, os
from passlib.context import CryptContext

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
users_file = os.path.join(BASE_DIR, "app", "users.json")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = input("Enter username: ")
password = input("Enter password: ")

hashed = pwd_context.hash(password)

if os.path.exists(users_file):
    with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = {}

users[username] = {"username": username, "password": hashed}

with open(users_file, "w") as f:
    json.dump(users, f, indent=4)

print(f"User {username} created successfully!")