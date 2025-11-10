import sqlite3

def add_book(db_path='library.db'):
    """
    Function to add a new book to the books table.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get input
        print("📚 Add New Book")
        print("-" * 20)
        
        title = input("Book Title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return False
        
        author = input("Author: ").strip()
        if not author:
            print("❌ Author cannot be empty!")
            return False
        
        genre = input("Genre (Fiction/Science/History/etc.): ").strip()
        if not genre:
            print("❌ Genre cannot be empty!")
            return False
        
        isbn = input("ISBN (optional): ").strip()
        if isbn:
            # Check if ISBN already exists
            cursor.execute("SELECT id FROM books WHERE isbn = ?", (isbn,))
            if cursor.fetchone():
                print("❌ ISBN already exists!")
                return False
        
        quantity = input("Quantity (default 1): ").strip()
        quantity = int(quantity) if quantity.isdigit() else 1
        
        # Insert new book
        cursor.execute('''
            INSERT INTO books (title, available, genre, author, isbn, quantity)
            VALUES (?, 'YES', ?, ?, ?, ?)
        ''', (title, genre, author, isbn, quantity))
        
        conn.commit()
        conn.close()
        
        print("✅ Book added successfully!")
        print(f"📖 Title: {title}")
        print(f"✍️  Author: {author}")
        print(f"🎯 Genre: {genre}")
        print(f"📦 Quantity: {quantity}")
        if isbn:
            print(f"🆔 ISBN: {isbn}")
        
        return True
        
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: books.isbn" in str(e):
            print("❌ ISBN already exists!")
        else:
            print("❌ Error: Book title or data conflict!")
    except ValueError:
        print("❌ Invalid quantity! Must be a number.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    add_book()
