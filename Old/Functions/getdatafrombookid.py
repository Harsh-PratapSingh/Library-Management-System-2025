import sqlite3
from datetime import datetime


def get_data_by_book_id(db_path='library.db'):
    """
    Get complete details for a book by ID - FIXED TABLE NAME.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Show book list - FIXED: 'books' table (plural)
            cursor.execute("SELECT id, title FROM books ORDER BY id LIMIT 10")
            books = cursor.fetchall()
            
            print("\n📚 Recent Books:")
            for book in books:
                print(f"ID: {book[0]} - {book[1]}")
            
            book_id = int(input("\nEnter book ID: "))
            
            # Get complete book details - FIXED: 'books' table (plural)
            cursor.execute("""
                SELECT b.id, b.title, b.author, b.genre, b.available, b.quantity, b.isbn,
                       b.check_after, b.available_for
                FROM books b                    -- FIXED: 'books' table (plural)
                WHERE b.id = ?
            """, (book_id,))
            
            book = cursor.fetchone()
            
            if not book:
                print(f"❌ Book ID {book_id} not found!")
                return
            
            # Parse results
            book_id, title, author, genre, available, quantity, isbn, check_after, borrower = book
            
            # Display comprehensive info
            print(f"\n📖 Complete Book Information:")
            print("=" * 60)
            print(f"🆔 Book ID:      {book_id}")
            print(f"📘 Title:        {title}")
            print(f"✍️  Author:      {author}")
            print(f"🎯 Genre:        {genre}")
            print(f"📍 ISBN:         {isbn if isbn else 'Not specified'}")
            print(f"📦 Quantity:     {quantity}")
            print(f"📊 Status:       {'🟢 Available' if available == 'YES' else '🔴 Borrowed'}")
            
            if available == 'NO':
                print(f"👤 Current Borrower: {borrower}")
                if check_after:
                    current_date = datetime(2025, 11, 10)
                    due_date = datetime.strptime(check_after, '%Y-%m-%d')
                    days_diff = (current_date - due_date).days
                    status = f"{'⚠️  Overdue' if days_diff > 0 else '⏰ Due Soon'} ({days_diff} days)"
                    print(f"⏰ Status:        {status}")
                else:
                    print(f"⏰ Check After:     Not set")
            else:
                print(f"👤 Current Borrower: None")
                print(f"⏰ Check After:     N/A")
            
            # Show activity
            print(f"\n📈 Recent Activity:")
            print(f"   Last queried: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("=" * 60)
        
    except ValueError:
        print("❌ Please enter a valid book ID number!")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    get_data_by_book_id()
