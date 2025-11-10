import sqlite3

def show_pending_borrow_requests(db_path='library.db'):
    """
    Show pending borrow requests (if you have a requests table).
    For now, shows users who have borrowed books but are pending approval.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get users who borrowed books but are still PENDING approval
        cursor.execute("""
            SELECT u.id, u.username, u.email, b.title, u.borrowed_book_date
            FROM users u
            JOIN books b ON u.borrowed_book_code = b.isbn
            WHERE u.approved = 'PENDING' AND u.borrowed_book_code != 'NIL'
            ORDER BY u.join_date
        """)
        
        pending_requests = cursor.fetchall()
        
        if not pending_requests:
            print("✅ No pending borrow requests!")
            print("   (Users with PENDING status who borrowed books)")
            return
        
        # Header
        print(f"\n⏳ Pending Borrow Requests ({len(pending_requests)} requests):")
        print("-" * 80)
        print(f"{'User ID':<8} {'Username':<15} {'Email':<25} {'Book Title':<25} {'Borrow Date':<12}")
        print("-" * 80)
        
        for request in pending_requests:
            user_id, username, email, book_title, borrow_date = request
            
            print(f"{user_id:<8} {username:<15} {email[:24]:<25} {book_title[:24]:<25} {borrow_date:<12}")
        
        print(f"\n📊 Total pending borrow requests: {len(pending_requests)}")
        print("   💡 These users need approval before their borrow is confirmed")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_pending_borrow_requests()
