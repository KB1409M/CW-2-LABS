import bcrypt
import os
import re # This import needs to be at the top with the others!

# Step 6. Define the User Data File
USER_DATA_FILE = "users.txt"

# --- CORE SECURITY FUNCTIONS ---

def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt with automatic salt generation.
    """
    # Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    # Hash the password using bcrypt.hashpw()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    hashed_password = hashed_bytes.decode('utf-8')
    return hashed_password

def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a stored bcrypt hash.
    """
    # Encode both the plaintext password and the stored hash to bytes
    plain_text_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Use bcrypt.checkpw() to verify the password
    return bcrypt.checkpw(plain_text_bytes, hashed_bytes)

# --- USER MANAGEMENT FUNCTIONS ---

def user_exists(username):
    """
    Checks if a username already exists in the user database.
    """
    # Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Read the file and check each line for the username
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            # Lines are format: username,hashed_password
            stored_username = line.strip().split(',')[0]
            if stored_username == username:
                return True

    return False

def register_user(username, password):
    """
    Registers a new user by hashing their password and storing credentials.
    """
    # Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    # Hash the password
    hashed_password = hash_password(password)

    # Append the new user to the file (Format: username,hashed_password)
    try:
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{username},{hashed_password}\n")
        print(f"Success: User '{username}' registered successfully!")
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")
        return False

def login_user(username, password):
    """
    Authenticates a user by verifying their username and password.
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users are registered yet.")
        return False

    # Search for the username in the file
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                # Use split(',', 1) in case the hash itself contains commas (though unlikely for bcrypt)
                stored_username, stored_hash = line.split(',', 1)
            except ValueError:
                # Skip malformed lines
                continue

            if stored_username == username:
                # If username matches, verify the password
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # If we reach here, the username was not found
    print("Error: Username not found.")
    return False

# --- INPUT VALIDATION FUNCTIONS ---

def validate_username(username):
    """
    Validates username format.
    Criteria: 3-20 characters, alphanumeric only.
    """
    if not (3 <= len(username) <= 20):
        return False, "Username must be between 3 and 20 characters long."
    if not re.match(r"^\w+$", username):
        return False, "Username can only contain alphanumeric characters and underscores."
    return True, ""

def validate_password(password):
    """
    Validates password strength.
    Criteria: 6-50 characters, requires uppercase, lowercase, and a digit.
    """
    if not (6 <= len(password) <= 50):
        return False, "Password must be between 6 and 50 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    return True, ""

# --- MAIN INTERFACE LOGIC ---

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("(In a real application, you would now access the dashboard/data.)")

            # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    # You can safely remove the TEMPORARY TEST CODE here if you used it earlier.
    main()