import sqlite3


def add_new_user(db_path='library.db'):
    """
    Simple function to add a new user.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get input
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            contact = input("Contact: ").strip()
            email = input("Email: ").strip()
            
            # Insert user with all required fields + defaults for other columns
            cursor.execute('''
                INSERT INTO users (username, password, varified, borrowed_book_id, borrowed_book_date,
                                   approved_book, requested_bookid, contact, email, join_date)
                VALUES (?, ?, 'PENDING', 'NIL', 'NIL', 'PENDING', 'NIL', ?, ?, datetime('now'))
            ''', (username, password, contact, email))
            
            conn.commit()
            print("User added successfully")
        
    except sqlite3.IntegrityError as e:
        print(f"User or email already exists: {e}")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    add_new_user()
