import sqlite3


def delete_book(db_path='library.db'):
    """
    Simple function to delete book by ID (no confirmation).
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Show books
            cursor.execute("SELECT id, title FROM books ORDER BY id")
            books = cursor.fetchall()
            
            if not books:
                print("No books found!")
                return
            
            print("\nBooks:")
            for book in books:
                print(f"ID: {book[0]} - {book[1]}")
            
            # Get ID
            book_id = input("\nEnter book ID to delete: ").strip()
            
            if not book_id.isdigit():
                print("Invalid ID!")
                return
            
            book_id = int(book_id)
            
            # Check if exists
            cursor.execute("SELECT title FROM books WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            
            if not book:
                print("Book not found!")
                return
            
            # Delete directly (no confirmation)
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            
            print(f"✅ Book '{book[0]}' deleted!")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    delete_book()
