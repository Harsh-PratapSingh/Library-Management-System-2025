import sqlite3
import datetime
import random

print("🚀 Library Management System - Data Entry (7-day loan, unique ISBNs)")
print("=" * 70)

with sqlite3.connect('library.db') as conn:
    cursor = conn.cursor()

    # 1) Admin users (10 rows) — contacts exactly 10 digits
    print("\n👨‍💼 Inserting 10 admin users...")
    admin_password = 'adminpass'
    admin_contacts = [
        '9812345678', '9823456789', '9834567890', '9845678901', '9856789012',
        '9867890123', '9878901234', '9889012345', '9890123456', '9810234567'
    ]
    for i in range(10):
        admin_username = f'admin{i+1}'
        email = f'admin{i+1}@library.edu'
        cursor.execute(
            "INSERT OR REPLACE INTO admin_users (admin_username, password, contact, email) VALUES (?,?,?,?)",
            (admin_username, admin_password, admin_contacts[i], email)
        )

    # 2) Users (50 rows) — contacts exactly 10 digits, mix varified and approved_book, some borrowed, some requested
    print("\n👥 Inserting 50 users (varified: YES/NO/PENDING) with 10-digit contacts...")
    user_password = 'userpass'

    # build 50 unique 10-digit numbers starting with 7/8/9
    user_contacts = set()
    while len(user_contacts) < 50:
        contact = str(random.randint(7000000000, 9999999999))
        user_contacts.add(contact)
    user_contacts = list(user_contacts)

    users = []
    for i in range(1, 51):
        username = f'user{i}'
        email = f'user{i}@library.edu'
        contact = user_contacts[i-1]

        # varified distribution: 20 PENDING, 20 YES, 10 NO
        if i <= 20:
            varified = 'PENDING'
        elif i <= 40:
            varified = 'YES'
        else:
            varified = 'NO'

        # approved_book distribution: first 25 PENDING, next 20 YES, last 5 NO
        if i <= 25:
            approved_book = 'PENDING'
        elif i <= 45:
            approved_book = 'YES'
        else:
            approved_book = 'NO'

        # requested_bookid: ~30% have requests
        requested_bookid = 'NIL'
        if random.random() < 0.30:
            requested_bookid = f'REQ{random.randint(100, 999):03d}'

        # placeholders for borrows; will be updated after books are inserted
        borrowed_book_id = 'NIL'
        borrowed_book_date = 'NIL'

        users.append((username, user_password, varified, borrowed_book_id, borrowed_book_date,
                      approved_book, requested_bookid, contact, email))

    cursor.executemany("""
        INSERT OR REPLACE INTO users
        (username, password, varified, borrowed_book_id, borrowed_book_date,
         approved_book, requested_bookid, contact, email)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, users)

    # 3) Books (100 rows) — 10 per genre, unique ISBNs, 7-day loan period for borrowed
    print("\n📚 Inserting 100 books (10 per genre) with unique ISBNs...")
    genres = ['Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy',
              'Biography', 'Mystery', 'Romance', 'Technology', 'Self-Help']

    book_data = {
        'Fiction': [
            ('Don Quixote', 'Miguel de Cervantes'),
            ('Pride and Prejudice', 'Jane Austen'),
            ('1984', 'George Orwell'),
            ('The Great Gatsby', 'F. Scott Fitzgerald'),
            ('To Kill a Mockingbird', 'Harper Lee'),
            ('Jane Eyre', 'Charlotte Brontë'),
            ('Wuthering Heights', 'Emily Brontë'),
            ('The Catcher in the Rye', 'J.D. Salinger'),
            ('Brave New World', 'Aldous Huxley'),
            ("The Handmaid's Tale", 'Margaret Atwood')
        ],
        'Non-fiction': [
            ('Sapiens', 'Yuval Noah Harari'),
            ('The Glass Castle', 'Jeannette Walls'),
            ('Educated', 'Tara Westover'),
            ('Becoming', 'Michelle Obama'),
            ('The Year of Magical Thinking', 'Joan Didion'),
            ('Quiet', 'Susan Cain'),
            ('Outliers', 'Malcolm Gladwell'),
            ('Thinking, Fast and Slow', 'Daniel Kahneman'),
            ('The Immortal Life of Henrietta Lacks', 'Rebecca Skloot'),
            ('Into the Wild', 'Jon Krakauer')
        ],
        'Science': [
            ('A Brief History of Time', 'Stephen Hawking'),
            ('The Elegant Universe', 'Brian Greene'),
            ('Cosmos', 'Carl Sagan'),
            ('The Selfish Gene', 'Richard Dawkins'),
            ('Guns, Germs, and Steel', 'Jared Diamond'),
            ('The Gene', 'Siddhartha Mukherjee'),
            ('Lab Girl', 'Hope Jahren'),
            ('Hidden Figures', 'Margot Lee Shetterly'),
            ('The Double Helix', 'James D. Watson'),
            ('The Structure of Scientific Revolutions', 'Thomas S. Kuhn')
        ],
        'History': [
            ('1491', 'Charles C. Mann'),
            ('Bury My Heart at Wounded Knee', 'Dee Brown'),
            ('The Guns of August', 'Barbara W. Tuchman'),
            ('Team of Rivals', 'Doris Kearns Goodwin'),
            ('The Rise and Fall of the Third Reich', 'William L. Shirer'),
            ("A People's History of the United States", 'Howard Zinn'),
            ('Postwar', 'Tony Judt'),
            ('The Making of the Atomic Bomb', 'Richard Rhodes'),
            ('Empire of the Summer Moon', 'S.C. Gwynne'),
            ('Blood and Thunder', 'Hampton Sides')
        ],
        'Fantasy': [
            ('The Hobbit', 'J.R.R. Tolkien'),
            ('A Game of Thrones', 'George R.R. Martin'),
            ('The Name of the Wind', 'Patrick Rothfuss'),
            ('Mistborn: The Final Empire', 'Brandon Sanderson'),
            ('American Gods', 'Neil Gaiman'),
            ('The Lies of Locke Lamora', 'Scott Lynch'),
            ('The Night Circus', 'Erin Morgenstern'),
            ('Jonathan Strange & Mr Norrell', 'Susanna Clarke'),
            ('The Fifth Season', 'N.K. Jemisin'),
            ('The Magicians', 'Lev Grossman')
        ],
        'Biography': [
            ('Steve Jobs', 'Walter Isaacson'),
            ('Alexander Hamilton', 'Ron Chernow'),
            ('Becoming', 'Michelle Obama'),
            ('Educated', 'Tara Westover'),
            ('The Autobiography of Malcolm X', 'Malcolm X'),
            ('Long Walk to Freedom', 'Nelson Mandela'),
            ('Born a Crime', 'Trevor Noah'),
            ('John Adams', 'David McCullough'),
            ('Einstein: His Life and Universe', 'Walter Isaacson'),
            ('Titan: The Life of John D. Rockefeller', 'Ron Chernow')
        ],
        'Mystery': [
            ('The Hound of the Baskervilles', 'Arthur Conan Doyle'),
            ('The Murder of Roger Ackroyd', 'Agatha Christie'),
            ('The Maltese Falcon', 'Dashiell Hammett'),
            ('Rebecca', 'Daphne du Maurier'),
            ('The Big Sleep', 'Raymond Chandler'),
            ('Gone Girl', 'Gillian Flynn'),
            ('The Girl on the Train', 'Paula Hawkins'),
            ('The Silent Patient', 'Alex Michaelides'),
            ('The Da Vinci Code', 'Dan Brown'),
            ('And Then There Were None', 'Agatha Christie')
        ],
        'Romance': [
            ('Pride and Prejudice', 'Jane Austen'),
            ('Outlander', 'Diana Gabaldon'),
            ('The Notebook', 'Nicholas Sparks'),
            ('Me Before You', 'Jojo Moyes'),
            ('It Ends with Us', 'Colleen Hoover'),
            ('The Love Hypothesis', 'Ali Hazelwood'),
            ('Beach Read', 'Emily Henry'),
            ('The Kiss Quotient', 'Helen Hoang'),
            ('Red, White & Royal Blue', 'Casey McQuiston'),
            ('Book Lovers', 'Emily Henry')
        ],
        'Technology': [
            ('The Innovators', 'Walter Isaacson'),
            ('Clean Code', 'Robert C. Martin'),
            ('Weapons of Math Destruction', 'Cathy O’Neil'),
            ('Superintelligence', 'Nick Bostrom'),
            ('Life 3.0', 'Max Tegmark'),
            ('The Code Book', 'Simon Singh'),
            ('iWoz', 'Steve Wozniak'),
            ('The Soul of a New Machine', 'Tracy Kidder'),
            ('Hatching Twitter', 'Nick Bilton'),
            ('The Everything Store', 'Brad Stone')
        ],
        'Self-Help': [
            ('Atomic Habits', 'James Clear'),
            ('How to Win Friends and Influence People', 'Dale Carnegie'),
            ('The 7 Habits of Highly Effective People', 'Stephen R. Covey'),
            ('The Power of Habit', 'Charles Duhigg'),
            ('Daring Greatly', 'Brené Brown'),
            ('Mindset', 'Carol S. Dweck'),
            ('The Subtle Art of Not Giving a F*ck', 'Mark Manson'),
            ('You Are a Badass', 'Jen Sincero'),
            ('The Four Agreements', 'Don Miguel Ruiz'),
            ('Big Magic', 'Elizabeth Gilbert')
        ],
    }

    # pre-generate 100 unique ISBN-13 strings (simple random format)
    isbn_set = set()
    unique_isbns = []
    while len(unique_isbns) < 100:
        core = f"{random.randint(1000000000000, 9999999999999)}"  # 13 digits
        if core not in isbn_set:
            isbn_set.add(core)
            unique_isbns.append(core)

    books_inserted = 0
    isbn_idx = 0

    # choose borrowers only from varified YES users to keep logic clean
    cursor.execute("SELECT username FROM users WHERE varified = 'YES'")
    verified_usernames = [r[0] for r in cursor.fetchall()]

    for g in genres:
        for title, author in book_data[g]:
            isbn = unique_isbns[isbn_idx]
            isbn_idx += 1

            # 20% borrowed, 80% available
            if random.random() < 0.20 and verified_usernames:
                available = 'NO'
                borrower = random.choice(verified_usernames)
                # borrow date in past 1–30 days, fixed 7-day loan => check_after = borrow_date + 7
                borrow_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))
                check_after = (borrow_date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
                available_for = borrower
            else:
                available = 'YES'
                available_for = None
                check_after = None

            cursor.execute("""
                INSERT INTO books (title, available, check_after, available_for, genre, author, isbn, quantity)
                VALUES (?,?,?,?,?,?,?,?)
            """, (title, available, check_after, available_for, g, author, isbn, 1))
            books_inserted += 1

    # sync users.borrowed_book_id and borrowed_book_date from books where borrowed
    cursor.execute("""
        SELECT isbn, available_for, check_after
        FROM books
        WHERE available = 'NO' AND available_for IS NOT NULL AND check_after IS NOT NULL
    """)
    borrowed = cursor.fetchall()
    links_updated = 0
    for isbn, borrower, check_after in borrowed:
        # borrow_date = check_after - 7 days (fixed loan period)
        due = datetime.datetime.strptime(check_after, '%Y-%m-%d').date()
        borrow_date = (due - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("""
            UPDATE users
            SET borrowed_book_id = ?, borrowed_book_date = ?
            WHERE username = ?
        """, (isbn, borrow_date, borrower))
        links_updated += 1

    conn.commit()

    # Stats
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    admin_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT varified, COUNT(*) FROM users GROUP BY varified")
    var_map = dict(cursor.fetchall())
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT genre) FROM books")
    genre_count = cursor.fetchone()[0]
    cursor.execute("SELECT available, COUNT(*) FROM books GROUP BY available")
    availability = dict(cursor.fetchall())

print("\n🎉 Data entry complete!")
print(f"👨‍💼 Admins: {admin_count}")
print(f"👥 Users: {user_count} (YES={var_map.get('YES',0)}, NO={var_map.get('NO',0)}, PENDING={var_map.get('PENDING',0)})")
print(f"📚 Books: {book_count} across {genre_count} genres")
print(f"📦 Available: {availability.get('YES',0)} | 🔒 Borrowed: {availability.get('NO',0)}")
print(f"🔗 Borrow links updated from books → users: {links_updated}")
