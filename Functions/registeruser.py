import sqlite3
db_path='library.db'

def add_new_user(username, password, contact, email):
    """
    Simple function to add a new user.
    Takes username, password, contact, email as string parameters.
    Returns '1' for successful, '2' for unsuccessful.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Insert user with all required fields + defaults for other columns
            cursor.execute('''
                INSERT INTO users (username, password, varified, borrowed_book_id, borrowed_book_date,
                                   approved_book, requested_bookid, contact, email, join_date)
                VALUES (?, ?, 'PENDING', 'NIL', 'NIL', 'PENDING', 'NIL', ?, ?, datetime('now'))
            ''', (username, password, contact, email))
            
            conn.commit()
            print(f"User '{username}' added successfully")
            return "1"  # Login successful
        
    except sqlite3.IntegrityError as e:
        print(f"User or email already exists: {e}")
        return "2"  # Login unsuccessful
    except Exception as e:
        print(f"Error: {e}")
        return "2"  # Login unsuccessful


# Example usage
if __name__ == "__main__":
    # Test with parameters instead of input
    result = add_new_user("testuser", "testpass", "9876543210", "test@example.com")
    print(f"Result: {result}")
