import sqlite3

class TestClass:
    def __init__(self, db_path='library.db'):
        self.master = type('obj', (object,), {'db_path': db_path})()
    
    def show_requested_bookid(self):
        """
        Display requested book IDs in CTkTable format.
        Returns (column_names, data_rows) or (None, [])
        """
        try:
            with sqlite3.connect(self.master.db_path) as conn:
                cursor = conn.cursor()

                # Get users with book requests
                cursor.execute("""
                    SELECT username, requested_bookid, email, contact
                    FROM users
                    WHERE requested_bookid != 'NIL'
                    ORDER BY requested_bookid
                """)
                results = cursor.fetchall()

                if not results:
                    print("No book requests found.")
                    return None, []
                
                # Prepare CTkTable format
                column_names = ['Username', 'Request ID', 'Email', 'Contact']
                
                data_rows = []
                for row in results:
                    username, request_id, email, contact = row
                    
                    data_rows.append([
                        username or '',
                        request_id or '',
                        (email or '')[:30],
                        contact or ''
                    ])
                
                print(f"📊 Found {len(data_rows)} book requests - ready for CTkTable")
                return column_names, data_rows

        except sqlite3.Error:
            print("Database error occurred.")
            return None, []
        except Exception:
            print("An error occurred.")
            return None, []

# Test the function
if __name__ == "__main__":
    print("🚀 Testing Book Requests")
    print("=" * 30)
    
    # Create test instance
    test = TestClass()
    
    # Call the method
    column_names, data_rows = test.show_requested_bookid()
    
    if column_names:
        print(f"\n🎯 Table Data Ready:")
        print(f"Columns: {column_names}")
        print(f"Rows: {len(data_rows)}")
        
        # Show first 3 rows
        print("\nSample rows:")
        for i, row in enumerate(data_rows[:3], 1):
            print(f"  {i}. {row}")
        
        if len(data_rows) > 3:
            print(f"  ... and {len(data_rows)-3} more rows")
    else:
        print("No data available")

import sqlite3




def process_book_request(self, username, action):
    """
    Process book request: accept or deny.
    action: 'YES' = approve, 'NO' = deny
    Returns 1=Success, 2=User not found, 3=Error
    """
    try:
        with sqlite3.connect(self.master.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if user has pending request
            cursor.execute("""
                SELECT username, requested_bookid 
                FROM users 
                WHERE username = ? AND requested_bookid != 'NIL'
            """, (username,))
            user_result = cursor.fetchone()
            
            if not user_result:
                print(f"No pending request found for user '{username}'")
                return 2  # No pending request
            
            # Get book details for the request
            book_id = user_result[1]
            cursor.execute("""
                SELECT title, author FROM books 
                WHERE isbn = ?
            """, (book_id,))
            book_result = cursor.fetchone()
            
            if action == 'YES':
                # Approve: move to borrowed_book_id and add date
                import datetime
                borrow_date = datetime.date.today().strftime('%Y-%m-%d')
                
                cursor.execute("""
                    UPDATE users 
                    SET requested_bookid = 'NIL', 
                        borrowed_book_id = ?, 
                        borrowed_book_date = ?
                    WHERE username = ?
                """, (book_id, borrow_date, username))
                
                # Update book availability
                cursor.execute("""
                    UPDATE books 
                    SET available = 'NO', 
                        available_for = '7 days',
                        check_after = ?
                    WHERE isbn = ?
                """, (borrow_date + datetime.timedelta(days=7), book_id))
                
                print(f"✅ Request APPROVED: {username} borrowed {book_result[0]}")
                print(f"   Borrow date: {borrow_date}, Due date: {borrow_date + datetime.timedelta(days=7)}")
                
            else:  # action == 'NO'
                # Deny: just remove from requested_bookid
                cursor.execute("""
                    UPDATE users 
                    SET requested_bookid = 'NIL'
                    WHERE username = ?
                """, (username,))
                
                print(f"❌ Request DENIED for user: {username}")
                print(f"   Book ID {book_id} removed from requests")
            
            # Commit changes
            if cursor.rowcount > 0:
                conn.commit()
                return 1  # Success
            else:
                return 2  # No update made
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 3
    except Exception as e:
        print(f"Error: {e}")
        return 3

# Test the function
if __name__ == "__main__":
    class DummyMaster:
        db_path = 'library.db'
    
    class TestClass:
        def __init__(self):
            self.master = DummyMaster()
    
    test = TestClass()
    
    print("🚀 Testing Book Request Processing")
    print("=" * 40)
    
    # Test approve
    print("\n1. APPROVE request for user18:")
    result1 = test.process_book_request("user18", "YES")
    print(f"Result: {result1}")
    
    # Test deny
    print("\n2. DENY request for user38:")
    result2 = test.process_book_request("user38", "NO")
    print(f"Result: {result2}")
    
    # Test non-existent user
    print("\n3. PROCESS non-existent user:")
    result3 = test.process_book_request("fakeuser", "YES")
    print(f"Result: {result3}")
    
    # Verify changes
    print("\n4. Check remaining requests:")
    test.show_requested_bookid()

