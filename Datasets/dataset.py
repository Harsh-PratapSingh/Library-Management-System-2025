import sqlite3

print("🔧 Creating Library Database Schema...")

with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()
    
    # Drop existing tables for clean setup
    tables_to_drop = ['admin_users', 'books', 'users']
    for table in tables_to_drop:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
    
    # Create books table (essential for quantity analysis)
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            available TEXT DEFAULT 'YES' CHECK (available IN ('YES', 'NO')),
            check_after TEXT,
            available_for TEXT,
            genre TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER DEFAULT 1
        )
    ''')
    
    # Create other tables (optional but recommended)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            varified TEXT DEFAULT 'PENDING' CHECK (varified IN ('YES', 'NO', 'PENDING')),
            borrowed_book_id TEXT DEFAULT 'NIL',
            borrowed_book_date TEXT DEFAULT 'NIL',
            approved_book TEXT DEFAULT 'PENDING' CHECK (approved_book IN ('YES', 'NO', 'PENDING')),
            requested_bookid TEXT DEFAULT 'NIL',
            contact TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            join_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'ADMIN',
            contact TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    conn.commit()
    print("✅ Schema created successfully!")
    print("Tables created: books, users, admin_users")
