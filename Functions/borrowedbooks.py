import sqlite3
from datetime import datetime, date


def show_borrowed_books(db_path='library.db'):
    """
    Show all currently borrowed books with borrower details and overdue status.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get borrowed books (available='NO') with borrower info
            cursor.execute("""
                SELECT b.id, b.title, b.author, b.genre, b.available_for, b.check_after, u.username
                FROM books b
                LEFT JOIN users u ON b.available_for = u.username
                WHERE b.available = 'NO'
                ORDER BY b.check_after
            """)
            
            borrowed_books = cursor.fetchall()
            
            if not borrowed_books:
                print("✅ No borrowed books currently!")
                return
            
            # Header
            print(f"\n🔒 Borrowed Books ({len(borrowed_books)} books):")
            print("-" * 90)
            print(f"{'ID':<4} {'Title':<30} {'Author':<15} {'Genre':<10} {'Borrower':<15} {'Check After':<12} {'Status':<15}")
            print("-" * 90)
            
            current_date = date.today()  # Use current date dynamically
            
            for book in borrowed_books:
                book_id, title, author, genre, borrower_field, check_after, username = book
                
                # Calculate overdue status
                status = "Borrowed"
                due_str = check_after if check_after else "N/A"
                if check_after:
                    try:
                        due_date = datetime.strptime(check_after, '%Y-%m-%d').date()
                        days_overdue = (current_date - due_date).days
                        if days_overdue > 0:
                            status = f"Overdue ({days_overdue}d)"
                        else:
                            status = f"Due {check_after}"
                    except Exception:
                        pass
                
                borrower = username if username else borrower_field if borrower_field else "Unknown"
                
                print(f"{book_id:<4} {title[:29]:<30} {author[:14]:<15} {genre:<10} {borrower[:14]:<15} {due_str:<12} {status:<15}")
            
            print(f"\n📊 Total borrowed books: {len(borrowed_books)}")
            
    except Exception as e:
        print(f"❌ Error displaying borrowed books: {e}")


if __name__ == "__main__":
    show_borrowed_books()
