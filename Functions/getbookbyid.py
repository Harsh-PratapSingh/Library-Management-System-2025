import sqlite3

def get_book_by_id(db_path='library.db'):
    """
    Get detailed information for a specific book by ID.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Quick list of books
        cursor.execute("SELECT id, title FROM books ORDER BY id")
        books = cursor.fetchall()
        
        print("\n📚 Available Books:")
        print("-" * 40)
        for book in books:
            print(f"ID: {book[0]} - {book[1]}")
        print("-" * 40)
        
        # Get book ID
        book_id_input = input("Enter book ID: ").strip()
        
        if not book_id_input.isdigit():
            print("❌ Invalid ID!")
            return
        
        book_id = int(book_id_input)
        
        # Get detailed book info
        cursor.execute("""
            SELECT id, title, author, genre, available, quantity, isbn, check_after, available_for
            FROM books 
            WHERE id = ?
        """, (book_id,))
        
        book = cursor.fetchone()
        
        if not book:
            print(f"❌ Book ID {book_id} not found!")
            return
        
        # Display detailed info
        book_id, title, author, genre, available, quantity, isbn, check_after, borrower = book
        
        print(f"\n📖 Book Details:")
        print("=" * 50)
        print(f"ID:           {book_id}")
        print(f"Title:        {title}")
        print(f"Author:       {author}")
        print(f"Genre:        {genre}")
        print(f"ISBN:         {isbn if isbn else 'N/A'}")
        print(f"Quantity:     {quantity}")
        print(f"Status:       {'Available' if available == 'YES' else 'Borrowed'}")
        
        if available == 'NO':
            if check_after:
                print(f"Check After:  {check_after}")
            if borrower:
                print(f"Borrowed by:  {borrower}")
            else:
                print(f"Borrowed by:  Unknown")
        else:
            print("Check After:  N/A")
            print("Borrowed by:  N/A")
        
        print("=" * 50)
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_book_by_id()
