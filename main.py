import sqlite3
from datetime import datetime, timedelta  # For date handling in due dates

# Create or connect to the library database
with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()
    
    # Drop existing tables if they exist for clean creation (comment out for additive runs)
    cursor.execute('DROP TABLE IF EXISTS admin_users')
    cursor.execute('DROP TABLE IF EXISTS books')
    cursor.execute('DROP TABLE IF EXISTS users')
    
    # 1. Users table (as previously defined)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            approved TEXT DEFAULT 'PENDING' CHECK (approved IN ('YES', 'NO', 'PENDING')),
            borrowed_book_code TEXT DEFAULT 'NIL',
            member_id TEXT UNIQUE,
            contact TEXT,
            join_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    # 2. Books table (as previously defined)
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            available TEXT DEFAULT 'YES' CHECK (available IN ('YES', 'NO')),
            check_after TEXT,
            genre TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER DEFAULT 1
        )
    ''')
    
    # 3. Admin users table (as previously defined)
    cursor.execute('''
        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'ADMIN',
            last_login TEXT,
            created_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    # Insert sample admin users (simple credentials; hash in production)
    admin_data = [
        ('admin1', 'adminpass123', 'ADMIN', None),
        ('library_manager', 'libmgr456', 'MANAGER', '2025-11-07 10:30:00')
    ]
    cursor.executemany('''
        INSERT INTO admin_users (admin_username, password, role, last_login) 
        VALUES (?, ?, ?, ?)
    ''', admin_data)
    
    # Insert sample books (mix of genres, availability; some borrowed with due dates)
    books_data = [
        ('BK001', 'Python Crash Course', 'YES', None, 'Programming', 'Eric Matthes', '9781593279288', 2),
        ('BK002', 'Clean Code', 'NO', '2025-11-15', 'Programming', 'Robert C. Martin', '9780132350884', 1),
        ('BK003', 'To Kill a Mockingbird', 'YES', None, 'Fiction', 'Harper Lee', '9780446310789', 3),
        ('BK004', '1984', 'NO', '2025-11-12', 'Fiction', 'George Orwell', '9780451524935', 1),
        ('BK005', 'The Great Gatsby', 'YES', None, 'Fiction', 'F. Scott Fitzgerald', '9780743273565', 2),
        ('BK006', 'Data Structures and Algorithms', 'YES', None, 'Programming', 'Michael T. Goodrich', '9781118771334', 1),
        ('BK007', 'Pride and Prejudice', 'NO', '2025-11-18', 'Romance', 'Jane Austen', '9780141439518', 1),
        ('BK008', 'The C Programming Language', 'YES', None, 'Programming', 'Brian W. Kernighan', '9780131103627', 2),
        ('BK009', 'Brave New World', 'YES', None, 'Fiction', 'Aldous Huxley', '9780060850524', 3),
        ('BK010', 'Fluent Python', 'NO', '2025-11-20', 'Programming', 'Luciano Ramalho', '9781492056348', 1)
    ]
    cursor.executemany('''
        INSERT INTO books (book_code, title, available, check_after, genre, author, isbn, quantity) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', books_data)
    
    # Insert sample users (mixed statuses; link some to borrowed books)
    users_data = [
        ('john_doe', 'password123', 'YES', 'NIL', 'MEM001', 'john@example.com', '2025-10-01 14:20:00'),
        ('alice_smith', 'pass456', 'YES', 'BK002', 'MEM002', 'alice@library.org', '2025-09-15 09:15:00'),
        ('bob_wilson', 'secret789', 'PENDING', 'NIL', 'MEM003', None, '2025-11-05 16:45:00'),
        ('emma_brown', 'emma2023', 'NO', 'NIL', 'MEM004', 'emma@email.com', '2025-10-20 11:30:00'),
        ('mike_johnson', 'mike456', 'YES', 'BK004', 'MEM005', 'mike@tech.com', '2025-08-12 13:00:00'),
        ('sarah_davis', 'sarah789', 'PENDING', 'NIL', None, 'sarah@books.com', '2025-11-03 08:20:00'),
        ('david_wilson', 'david101', 'YES', 'BK007', 'MEM007', None, '2025-09-28 15:10:00'),
        ('lisa_miller', 'lisa2024', 'YES', 'NIL', 'MEM008', 'lisa@readingclub.org', '2025-10-10 12:45:00')
    ]
    cursor.executemany('''
        INSERT INTO users (username, password, approved, borrowed_book_code, member_id, contact, join_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    conn.commit()

# Display the inserted data
print("\n=== SAMPLE DATA ADDED TO LIBRARY DATABASE ===\n")

with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()
    
    # Display Admin Users
    print("1. ADMIN USERS:")
    cursor.execute("SELECT admin_username, password, role, last_login FROM admin_users")
    admins = cursor.fetchall()
    for admin in admins:
        status = "Active" if admin[3] else "New"
        print(f"   - Username: {admin[0]}, Password: {admin[1]}, Role: {admin[2]}, Status: {status}")
    
    print("\n2. BOOKS:")
    cursor.execute("""
        SELECT book_code, title, available, check_after, genre, author 
        FROM books 
        ORDER BY genre, title
    """)
    books = cursor.fetchall()
    for book in books:
        status_icon = "✅" if book[2] == 'YES' else "❌"
        due = f" (Due: {book[3]})" if book[3] else ""
        print(f"   {status_icon} [{book[0]}] {book[1]} by {book[5]} - Genre: {book[4]}{due}")
    
    print("\n3. USERS:")
    cursor.execute("""
        SELECT username, approved, borrowed_book_code, member_id, contact 
        FROM users 
        ORDER BY approved, username
    """)
    users = cursor.fetchall()
    for user in users:
        approved_status = {"YES": "✅", "NO": "❌", "PENDING": "⏳"}.get(user[1], user[1])
        borrowed = f"Book: {user[2]}" if user[2] != 'NIL' else "No book borrowed"
        print(f"   {approved_status} {user[0]} (ID: {user[3] if user[3] else 'N/A'}) - {borrowed}")
        if user[4]:
            print(f"      Contact: {user[4]}")

print(f"\nDatabase 'library.db' created with {len(books_data)} books, {len(users_data)} users, and {len(admin_data)} admin accounts.")
