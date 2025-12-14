from app.data.db import connect_database
import bcrypt
from pathlib import Path

# Path to users.txt for migration
DATA_DIR = Path(__file__).resolve().parents[2] / "DATA"
USERS_FILE = DATA_DIR / "users.txt"

# --- Database CRUD helpers ---
def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()


# --- Service functions used by main.py ---
def register_user(username, password, role='user'):
    """Register new user with hashed password."""
    if get_user_by_username(username):
        return False, f"Username '{username}' already exists."

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Welcome, {username}!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath=USERS_FILE):
    """Migrate users from text file to database."""
    if not filepath.exists():
        print(f" File not found: {filepath}. No users to migrate.")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Expected format: username,password_hash,role(optional)
            parts = line.split(',', 2)
            username = parts[0]
            password_hash = parts[1] if len(parts) > 1 else "placeholder"
            role = parts[2] if len(parts) > 2 else "user"
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                if cursor.rowcount > 0:
                    migrated_count += 1
            except Exception as e:
                print(f"Error migrating user {username}: {e}")

    conn.commit()
    conn.close()
    print(f" Migrated {migrated_count} users from {filepath.name}")
    return migrated_count

