import sqlite3
from datetime import datetime

def submit_book(db_path='library.db'):
    """
    Function to submit (return) a borrowed book.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Show borrowed books
        cursor.execute("""
            SELECT b.id, b.title, b.author, b.available_for, u.username
            FROM books b
            JOIN users u ON b.available_for = u.username
            WHERE b.available = 'NO'
            ORDER BY b.check_after
        """)
        
        borrowed_books = cursor.fetchall()
        
        if not borrowed_books:
            print("✅ No borrowed books to return!")
            return
        
        print("\n📚 Borrowed Books (Available for Return):")
        print("-" * 60)
        print(f"{'ID':<4} {'Title':<25} {'Author':<15} {'Borrower':<15}")
        print("-" * 60)
        
        for book in borrowed_books:
            book_id, title, author, borrower_field, username = book
            borrower = username if username else borrower_field
            print(f"{book_id:<4} {title[:24]:<25} {author[:14]:<15} {borrower[:14]:<15}")
        
        # Get book ID to return
        book_id_input = input("\nEnter book ID to return: ").strip()
        
        if not book_id_input.isdigit():
            print("❌ Invalid ID!")
            return
        
        book_id = int(book_id_input)
        
        # Check if book is borrowed
        cursor.execute("""
            SELECT b.title, b.available_for, u.username, b.check_after
            FROM books b
            LEFT JOIN users u ON b.available_for = u.username
            WHERE b.id = ? AND b.available = 'NO'
        """, (book_id,))
        
        book_info = cursor.fetchone()
        
        if not book_info:
            print(f"❌ Book ID {book_id} is not currently borrowed!")
            return
        
        title, borrower_field, username, check_after = book_info
        borrower = username if username else borrower_field
        
        # Return the book
        cursor.execute("""
            UPDATE books 
            SET available = 'YES', 
                check_after = NULL, 
                available_for = NULL
            WHERE id = ?
        """, (book_id,))
        
        # Clear user's borrowed book info
        cursor.execute("""
            UPDATE users 
            SET borrowed_book_code = 'NIL',
                borrowed_book_date = 'NIL'
            WHERE username = ? OR username = ?
        """, (borrower, borrower_field))
        
        conn.commit()
        
        print(f"\n✅ Book '{title}' returned successfully!")
        print(f"   📖 Book ID: {book_id}")
        print(f"   👤 Returned by: {borrower}")
        if check_after:
            due_date = datetime.strptime(check_after, '%Y-%m-%d')
            current_date = datetime(2025, 11, 10)
            days_late = (current_date - due_date).days
            print(f"   ⏰ Was {'overdue' if days_late > 0 else 'on time'} ({days_late} days)")
        else:
            print(f"   ⏰ Check after date: {check_after}")
        
        # Update book count
        cursor.execute("SELECT COUNT(*) FROM books WHERE available = 'YES'")
        available_count = cursor.fetchone()[0]
        print(f"   📚 Total available books now: {available_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    submit_book()
