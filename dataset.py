import sqlite3

# Create or connect to the library database
with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()
    
    # Drop existing tables if they exist for clean creation (remove these lines for persistent runs)
    cursor.execute('DROP TABLE IF EXISTS admin_users')
    cursor.execute('DROP TABLE IF EXISTS books')
    cursor.execute('DROP TABLE IF EXISTS users')
    
    # 1. Users table: username, password, approved (YES/NO/PENDING), borrowed_book_code (or NIL), and additional useful columns
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,  -- Store hashed passwords in practice
            approved TEXT DEFAULT 'PENDING' CHECK (approved IN ('YES', 'NO', 'PENDING')),
            borrowed_book_code TEXT DEFAULT 'NIL',  -- Book code if borrowed, else NIL
            contact TEXT,
            join_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    # 2. Books table: book_code, title, available (YES/NO), check_after (due date), genre, and additional columns
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            available TEXT DEFAULT 'YES' CHECK (available IN ('YES', 'NO')),
            check_after TEXT,  -- Due date for borrowed books
            available_for TEXT, 
            genre TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER DEFAULT 1
        )
    ''')
    
    # 3. Admin users table: admin_username, password, and basic additional columns
    cursor.execute('''
        CREATE TABLE admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,  -- Store hashed passwords in practice
            role TEXT DEFAULT 'ADMIN',
            contact TEXT,
            created_date TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    conn.commit()

# Display created tables and schemas for verification
with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Created tables:")
    for table in tables:
        if table[0] != 'sqlite_sequence':  # Skip internal table
            print(f"- {table[0]}")
    #hello
    # Display schema for each table
    user_tables = ['users', 'books', 'admin_users']
    for table_name in user_tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        print(f"\nSchema for {table_name}:")
        for col in schema:
            not_null = "YES" if col[3] else "NO"
            pk = "YES" if col[5] else "NO"
            default = col[4] if col[4] else "None"
            print(f"  - {col[1]} ({col[2]}) - Not Null: {not_null}, Default: {default}, PK: {pk}")
