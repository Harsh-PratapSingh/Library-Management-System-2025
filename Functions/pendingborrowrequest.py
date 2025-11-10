import sqlite3


def show_pending_borrow_requests(db_path='library.db'):
    """
    Show pending borrow requests - users with borrowed books but PENDING approval.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get users who have borrowed books but are still PENDING approval
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.borrowed_book_id, u.borrowed_book_date
                FROM users u
                WHERE u.varified = 'PENDING' AND u.borrowed_book_id != 'NIL'
                ORDER BY u.id
            """)
            
            pending_requests = cursor.fetchall()
            
            if not pending_requests:
                print("✅ No pending borrow requests!")
                print("   (Users with PENDING verification who have borrowed books)")
                return
            
            # Header
            print(f"\n⏳ Pending Borrow Requests ({len(pending_requests)} requests):")
            print("-" * 80)
            print(f"{'User ID':<8} {'Username':<15} {'Email':<25} {'Book ID':<15} {'Borrow Date':<12}")
            print("-" * 80)
            
            for request in pending_requests:
                user_id, username, email, book_id, borrow_date = request
                
                print(f"{user_id:<8} {username:<15} {email[:24]:<25} {book_id[:14]:<15} {borrow_date if borrow_date != 'NIL' else 'N/A':<12}")
            
            print(f"\n📊 Total pending borrow requests: {len(pending_requests)}")
            print("   💡 These users need verification before borrow is fully processed")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    show_pending_borrow_requests()
