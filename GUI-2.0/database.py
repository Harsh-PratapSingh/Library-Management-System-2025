from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("Library-Management-System-2025/Database/library.db")
    if not db.open():
        print("DB error")
        return False
    
    query = QSqlQuery()
    
    # Books table
    query.exec("""
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            published_year INTEGER NOT NULL,
            total_copies INTEGER DEFAULT 1 NOT NULL,
            available_copies INTEGER DEFAULT 1 NOT NULL
        )
    """)
    
    # Users table (with role and password)
    query.exec("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            join_date DATE DEFAULT CURRENT_DATE,
            max_books INTEGER DEFAULT 3 NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            role TEXT DEFAULT 'user' NOT NULL
        )
    """)
    
    # Transactions table
    query.exec("""
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            issue_date DATE DEFAULT CURRENT_DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            fine DECIMAL(5,2) DEFAULT 0.00,
            status TEXT DEFAULT 'Issued' NOT NULL,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    """)
    
    return True
