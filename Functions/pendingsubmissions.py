import sqlite3
from datetime import datetime, timedelta

def show_pending_submissions(db_path='library.db'):
    """
    Show books that are overdue (past check_after date) - pending submission.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get overdue books (check_after date passed)
        current_date = datetime(2025, 11, 10)
        cutoff_date = current_date.strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT b.id, b.title, b.author, b.available_for, b.check_after, 
                   u.username, u.email
            FROM books b
            JOIN users u ON b.available_for = u.username
            WHERE b.available = 'NO' AND b.check_after < ?
            ORDER BY b.check_after
        """, (cutoff_date,))
        
        overdue_books = cursor.fetchall()
        
        if not overdue_books:
            print("✅ No pending submissions! All books are on time.")
            return
        
        # Header
        print(f"\n⚠️  Pending Submissions - OVERDUE BOOKS ({len(overdue_books)} books):")
        print("-" * 100)
        print(f"{'Book ID':<8} {'Title':<25} {'Borrower':<15} {'Due Date':<12} {'Days Overdue':<13} {'Contact':<12}")
        print("-" * 100)
        
        current_date_obj = datetime(2025, 11, 10)
        
        for book in overdue_books:
            book_id, title, author, borrower_field, due_date, username, email = book
            
            # Calculate days overdue
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            days_overdue = (current_date_obj - due_date_obj).days
            
            borrower = username if username else borrower_field
            contact = email[:11] if email else "N/A"
            
            print(f"{book_id:<8} {title[:24]:<25} {borrower[:14]:<15} {due_date:<12} {days_overdue:<13} {contact:<12}")
        
        print(f"\n📊 Total overdue books: {len(overdue_books)}")
        print("   ⏰ These books need to be returned or renewed!")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_pending_submissions()
