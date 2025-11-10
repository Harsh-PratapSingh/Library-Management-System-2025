import sqlite3
from getpass import getpass


def login_function(db_path='library.db'):
    """
    Simple login function that checks credentials in both users and admin_users tables.
    """
    try:
        # Connect to database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Get credentials
            username = input("Enter username: ").strip()
            password = getpass("Enter password: ")

            # Check users table
            cursor.execute(
                "SELECT username FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user_result = cursor.fetchone()

            # Check admin_users table
            cursor.execute(
                "SELECT admin_username FROM admin_users WHERE admin_username = ? AND password = ?",
                (username, password)
            )
            admin_result = cursor.fetchone()

        # Check results
        if user_result or admin_result:
            print("Login successful")
        else:
            print("Invalid credentials")

    except sqlite3.Error:
        print("Invalid credentials")
    except Exception:
        print("Invalid credentials")


# Example usage
if __name__ == "__main__":
    login_function()
