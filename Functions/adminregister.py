import sqlite3

def register_admin(db_path='library.db'):
    """
    Register a new admin user. Requires admin code '1111' for successful registration.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get admin code first
        admin_code = input("Enter admin code: ").strip()
        
        if admin_code != '1111':
            print("Invalid admin code!")
            return False
        
        # Get input
        username = input("Admin Username: ").strip()
        password = input("Password: ").strip()
        contact = input("Contact: ").strip()
        email = input("Email: ").strip()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM admin_users WHERE admin_username = ?", (username,))
        if cursor.fetchone():
            print("Admin username already exists!")
            return False
        
        # Check if email already exists
        cursor.execute("SELECT id FROM admin_users WHERE email = ?", (email,))
        if cursor.fetchone():
            print("Email already exists!")
            return False
        
        # Insert new admin
        cursor.execute('''
            INSERT INTO admin_users (admin_username, password, contact, email)
            VALUES (?, ?, ?, ?)
        ''', (username, password, contact, email))
        
        conn.commit()
        print("Admin registered successfully")
        return True
        
    except sqlite3.IntegrityError as e:
        print("Error: Admin username or email already exists!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    register_admin()
