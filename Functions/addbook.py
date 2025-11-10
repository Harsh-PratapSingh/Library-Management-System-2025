import sqlite3


def add_book(db_path='library.db'):
    """
    Function to add a new book to the books table.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # User inputs
        print("📚 Add New Book")
        print("-" * 30)

        title = input("Book Title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return False

        author = input("Author: ").strip()
        if not author:
            print("❌ Author cannot be empty!")
            return False

        genre = input("Genre (e.g. Fiction/Science/History): ").strip()
        if not genre:
            print("❌ Genre cannot be empty!")
            return False

        isbn = input("ISBN (optional, unique): ").strip()
        if isbn:
            cursor.execute("SELECT id FROM books WHERE isbn = ?", (isbn,))
            if cursor.fetchone():
                print("❌ ISBN already exists!")
                return False
        else:
            isbn = None  # store NULL if no ISBN provided

        quantity_input = input("Quantity (default 1): ").strip()
        quantity = int(quantity_input) if quantity_input.isdigit() and int(quantity_input) > 0 else 1

        # Insert new book
        cursor.execute('''
            INSERT INTO books (title, available, genre, author, isbn, quantity)
            VALUES (?, 'YES', ?, ?, ?, ?)
        ''', (title, genre, author, isbn, quantity))

        conn.commit()

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
            print(f"❌ IntegrityError: {e}")
    except ValueError:
        print("❌ Invalid quantity! Must be a positive integer.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    add_book()
