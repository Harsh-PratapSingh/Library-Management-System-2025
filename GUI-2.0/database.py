from PyQt6.QtSql import QSqlDatabase, QSqlQuery

import random #new import
from datetime import datetime, timedelta #new import

def init_db():
    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("Library-Management-System-2025/Database/library.db")
    # if not db.open():
    #     print("DB error")
    #     return False
    
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

#-------------creating entries--------------#

# Genres list 
genres = ['Fiction', 'Non-Fiction', 'Mystery',
          'Science Fiction', 'Fantasy', 'Romance',
          'Thriller', 'Historical', 'Biography',
          'Children', 'Young Adult', 'Horror',
          'Adventure', 'Classic', 'Graphic Novel',
          'Poetry', 'Self-Help', 'Science',
          'History', 'Travel']

# Real book samples 
sample_books = [
    ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("1984", "George Orwell", 1949),
    ("Pride and Prejudice", "Jane Austen", 1813),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("The Catcher in the Rye", "J.D. Salinger", 1951),
    ("The Lord of the Rings", "J.R.R. Tolkien", 1954),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997),
    ("The Hobbit", "J.R.R. Tolkien", 1937),
    ("The Da Vinci Code", "Dan Brown", 2003),
    ("The Alchemist", "Paulo Coelho", 1988),
    ("The Kite Runner", "Khaled Hosseini", 2003),
    ("The Book Thief", "Markus Zusak", 2005),
    ("Animal Farm", "George Orwell", 1945),
    ("The Little Prince", "Antoine de Saint-Exupéry", 1943),
    ("Fahrenheit 451", "Ray Bradbury", 1953),
    ("Jane Eyre", "Charlotte Brontë", 1847),
    ("The Fault in Our Stars", "John Green", 2012),
    ("The Hunger Games", "Suzanne Collins", 2008),
    ("The Giver", "Lois Lowry", 1993),
    ("Brave New World", "Aldous Huxley", 1932),
    ("The Handmaid's Tale", "Margaret Atwood", 1985),
    ("The Road", "Cormac McCarthy", 2006),
    ("Beloved", "Toni Morrison", 1987),
    ("The Secret Garden", "Frances Hodgson Burnett", 1911),
    ("The Outsiders", "S.E. Hinton", 1967),
    ("Charlotte's Web", "E.B. White", 1952),
    ("Where the Wild Things Are", "Maurice Sendak", 1963),
    ("Goodnight Moon", "Margaret Wise Brown", 1947),
    ("The Very Hungry Caterpillar", "Eric Carle", 1969),
    ("Green Eggs and Ham", "Dr. Seuss", 1960),
    ("The Cat in the Hat", "Dr. Seuss", 1957),
    ("The Giving Tree", "Shel Silverstein", 1964),
    ("Matilda", "Roald Dahl", 1988),
    ("Charlie and the Chocolate Factory", "Roald Dahl", 1964),
    ("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "C.S. Lewis", 1950),
    ("A Wrinkle in Time", "Madeleine L'Engle", 1962),
    ("Percy Jackson and the Olympians: The Lightning Thief", "Rick Riordan", 2005),
    ("The Sisterhood of the Traveling Pants", "Ann Brashares", 2001),
    ("Twilight", "Stephenie Meyer", 2005),
    ("The Bell Jar", "Sylvia Plath", 1963), 
    ("Invisible Man", "Ralph Ellison", 1952),
    ("Slaughterhouse-Five", "Kurt Vonnegut", 1969),
    ("The Color Purple", "Alice Walker", 1982),
    ("Their Eyes Were Watching God", "Zora Neale Hurston", 1937),
    ("The Sun Also Rises", "Ernest Hemingway", 1926),
    ("A Farewell to Arms", "Ernest Hemingway", 1929), ("Of Mice and Men", "John Steinbeck", 1937),
    ("The Grapes of Wrath", "John Steinbeck", 1939),
    ("East of Eden", "John Steinbeck", 1952),
    ("The Old Man and the Sea", "Ernest Hemingway", 1952),
    ("The Name of the Wind", "Patrick Rothfuss", 2007),
    ("The Night Circus", "Erin Morgenstern", 2011),
    ("The Ocean at the End of the Lane", "Neil Gaiman", 2013),
    ("The Shadow of the Wind", "Carlos Ruiz Zafón", 2001),
    ("The Goldfinch", "Donna Tartt", 2013),
    ("Gone Girl", "Gillian Flynn", 2012),
    ("The Girl on the Train", "Paula Hawkins", 2015),
    ("Big Little Lies", "Liane Moriarty", 2014),
    ("The Martian", "Andy Weir", 2011),
    ("Divergent", "Veronica Roth", 2011),
    ("The Maze Runner", "James Dashner", 2009),
    ("Ready Player One", "Ernest Cline", 2011),
    ("The Firm", "John Grisham", 1991),
    ("The Pelican Brief", "John Grisham", 1992), ("A Time to Kill", "John Grisham", 1989),
    ("The Rainmaker", "John Grisham", 1995),
    ("The Runaway Jury", "John Grisham", 1996),
    ("The Testament", "John Grisham", 1999),
    ("The Brethren", "John Grisham", 2000),
    ("The Last Juror", "John Grisham", 2004),
    ("The Appeal", "John Grisham", 2008),
    ("The Confession", "John Grisham", 2010),
    ("The Litigators", "John Grisham", 2011),
    ("Sycamore Row", "John Grisham", 2013),
    ("Gray Mountain", "John Grisham", 2014),
    ("Rogue Lawyer", "John Grisham", 2015),
    ("The Whistler", "John Grisham", 2016),
    ("Camino Island", "John Grisham", 2017),
    ("The Rooster Bar", "John Grisham", 2017),
    ("The Reckoning", "John Grisham", 2018),
    ("The Guardians", "John Grisham", 2019),
    ("Camino Winds", "John Grisham", 2020),
    ("A Time for Mercy", "John Grisham", 2020),
    ("The Judge's List", "John Grisham", 2021),
    ("The Exchange", "John Grisham", 2023),
    ("The Boys from Biloxi", "John Grisham", 2023)
]

# creating random combined genres list from the genre list
def generate_genres(): 
    genre_assignments = []
    for _ in range(84):
        num_genres = random.randint(1, 3)
        selected = random.sample(genres, num_genres)
        selected.sort(key=lambda x: genres.index(x))
        genre_assignments.append(','.join(selected))
    return genre_assignments

# creating books list
def generate_books():
    books = []
    genre_assignments = generate_genres()
    for i in range(0,84):
        title, author, year = sample_books[i]
        isbn = f"{random.randint(10000000, 99999999)}"
        categories = genre_assignments[i]
        total_copies = random.randint(1, 10)
        available_copies = total_copies  # Set to total at creation
        books.append((title, isbn, author, categories, year, total_copies, available_copies))
    return books

# creating users list
def generate_users():
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Anna', 'Michael', 'Mary', 'William', 'Patricia', 'Richard', 'Jennifer', 'Joseph', 'Elizabeth', 'Thomas', 'Susan']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']
    users = []
    for i in range(100):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}@{random.choice(domains)}"
        phone = f"{random.randint(8000000000, 9999999999)}"
        role = 'admin' if i < 50 else 'user'
        password = role
        join_date = (datetime.now() - timedelta(days=random.randint(0, 1825))).strftime('%Y-%m-%d')
        is_active = True if role == 'admin' else random.choice([True, False])
        max_books = 3
        users.append((name, email, phone, password, join_date, max_books, is_active, role))
    users.append(("user", "user@lpu.in", "9999999999", "user", (datetime.now().strftime('%Y-%m-%d')), 3, True, "user"))
    users.append(("admin", "admin@lpu.in", "8888888888", "admin", (datetime.now().strftime('%Y-%m-%d')), 3, True, "admin"))
    return users

# creating random transactions list
def generate_transactions(books_data, users_data):
    transactions = []
    for _ in range(100):
        book_id = random.randint(1, 84)
        user_id = random.randint(51, 95)
        issue_date = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')
        due_date = (datetime.strptime(issue_date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
        if random.random() < 0.8:
            return_date = (datetime.strptime(issue_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')
            status = 'Returned'
            fine = 0.0
        else:
            return_date = None
            status = 'Issued'
            # Random fine for overdue (if due date passed)
            due_dt = datetime.strptime(due_date, '%Y-%m-%d')
            if datetime.now() > due_dt:  # Due date has passed
                overdue_days = (datetime.now() - due_dt).days
                fine = round(overdue_days * 10, 2)  # Rs.10 per day
            else:
                fine = 0.0
        transactions.append((book_id, user_id, issue_date, due_date, return_date, fine, status))
    return transactions

# adding entries to the database using the created lists
def seed_data():
    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("Library-Management-System-2025/Database/library.db")
    # if not db.open():
    #     return False
    query = QSqlQuery()
    
    # Clear existing data (using raw SQL for simplicity)
    query.exec("DELETE FROM Transactions")
    query.exec("DELETE FROM Books")
    query.exec("DELETE FROM Users")
    
    # Insert Books
    books = generate_books()
    for book in books:
        query.prepare("INSERT INTO Books (title, isbn, author, category, published_year, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?, ?)")
        query.addBindValue(book[0])
        query.addBindValue(book[1])
        query.addBindValue(book[2])
        query.addBindValue(book[3])
        query.addBindValue(book[4])
        query.addBindValue(book[5])
        query.addBindValue(book[6])
        query.exec()
    
    # Insert Users
    users = generate_users()
    for user in users:
        query.prepare("INSERT INTO Users (name, email, phone, password, join_date, max_books, is_active, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
        query.addBindValue(user[0])
        query.addBindValue(user[1])
        query.addBindValue(user[2])
        query.addBindValue(user[3])
        query.addBindValue(user[4])
        query.addBindValue(user[5])
        query.addBindValue(1 if user[6] else 0)
        query.addBindValue(user[7])
        if not query.exec():
            print(query.lastError().text())
    
    # Insert Transactions and adjust available_copies
    transactions = generate_transactions(books, users)
    for trans in transactions:
        book_id, user_id, issue_date, due_date, return_date, fine, status = trans

        query.prepare("SELECT available_copies FROM Books WHERE book_id = ?")
        query.addBindValue(book_id)
        query.exec()
        if not query.exec():
            print("Query failed: ", query.lastError().text())
            continue
        if not query.next():
            print("No record found for book_id:", book_id)
            continue
        if query.value(0) == 0:
            continue
        # Insert transaction
        query.prepare("INSERT INTO Transactions (book_id, user_id, issue_date, due_date, return_date, fine, status) VALUES (?, ?, ?, ?, ?, ?, ?)")
        query.addBindValue(book_id)
        query.addBindValue(user_id)
        query.addBindValue(issue_date)
        query.addBindValue(due_date)
        query.addBindValue(return_date)
        query.addBindValue(fine)
        query.addBindValue(status)
        query.exec()
        # Adjust available_copies
        if status == 'Issued':
            query.prepare("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?")
            query.addBindValue(book_id)
            query.exec()
        
    
    return True


# 1. Fiction

# 2. Non-Fiction

# 3. Mystery

# 4. Science Fiction

# 5. Fantasy

# 6. Romance

# 7. Thriller

# 8. Historical

# 9. Biography

# 10. Children

# 11. Young Adult

# 12. Horror

# 13. Adventure

# 14. Classic

# 15. Graphic Novel

# 16. Poetry

# 17. Self-Help

# 18. Science

# 19. History

# 20. Travel
