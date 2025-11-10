import sqlite3

def add_new_user(db_path='library.db'):
    """
    Simple function to add a new user.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get input
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        contact = input("Contact: ").strip()
        email = input("Email: ").strip()
        
        # Insert user with all required fields
        cursor.execute('''
            INSERT INTO users (username, password, contact, email)
            VALUES (?, ?, ?, ?)
        ''', (username, password, contact, email))
        
        conn.commit()
        conn.close()
        
        print("User added successfully")
        
    except:
        print("Invalid credentials")

# Example usage
if __name__ == "__main__":
    add_new_user()
