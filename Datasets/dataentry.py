import sqlite3
import datetime

# Connect to the library database
with sqlite3.connect('library.db') as conn:  # Updated path to match dataset.py
    cursor = conn.cursor()
    
    # Insert 10 admin users (Fixed - includes email)
    admin_password = 'adminpass'  # In practice, hash this
    for i in range(1, 11):
        admin_username = f'admin{i}'
        contact = f'98{i}000000{i}'  # Phone number format
        email = f'admin{i}@library.com'  # Added email
        cursor.execute('''
            INSERT OR IGNORE INTO admin_users (admin_username, password, contact, email)
            VALUES (?, ?, ?, ?)
        ''', (admin_username, admin_password, contact, email))
    
    # Insert 50 users (Fixed - includes email)
    user_password = 'userpass'  # In practice, hash this
    for i in range(1, 51):
        username = f'user{i}'
        contact = f'98{i}12345{i}'  # Phone number format
        email = f'user{i}@library.com'  # Added email
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, contact, email)
            VALUES (?, ?, ?, ?)
        ''', (username, user_password, contact, email))
    
    # Define 10 genres and sample book data
    genres = ['Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy', 'Biography', 'Mystery', 'Romance', 'Technology', 'Self-Help']
    
    # Sample books data: list of tuples (title, author, isbn) for each genre
    # Fiction books
    fiction_books = [
        ('Don Quixote', 'Miguel de Cervantes', '978-0-14-044909-1'),
        ('Alice\'s Adventures in Wonderland', 'Lewis Carroll', '978-0-14-143976-1'),
        ('The Adventures of Huckleberry Finn', 'Mark Twain', '978-0-14-243717-9'),
        ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-74-327356-5'),
        ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4'),
        ('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8'),
        ('1984', 'George Orwell', '978-0-45-152493-5'),
        ('The Catcher in the Rye', 'J.D. Salinger', '978-0-31-676948-8'),
        ('Wuthering Heights', 'Emily Brontë', '978-0-14-143955-6'),
        ('Jane Eyre', 'Charlotte Brontë', '978-0-14-144114-7')
    ]
    
    # Non-fiction books (general, e.g., essays, true crime)
    non_fiction_books = [
        ('The Year of Magical Thinking', 'Joan Didion', '978-0-307-27733-6'),
        ('In Cold Blood', 'Truman Capote', '978-0-679-73521-6'),
        ('Outliers: The Story of Success', 'Malcolm Gladwell', '978-0-316-01792-3'),
        ('Quiet: The Power of Introverts', 'Susan Cain', '978-0-307-35215-0'),
        ('The Glass Castle', 'Jeannette Walls', '978-0-7432-4753-5'),
        ('Wild: From Lost to Found on the Pacific Crest Trail', 'Cheryl Strayed', '978-0-307-58845-6'),
        ('Bad Feminist', 'Roxane Gay', '978-0-06-228271-2'),
        ('We Should All Be Feminists', 'Chimamanda Ngozi Adichie', '978-0-00-811528-9'),
        ('The Right Stuff', 'Tom Wolfe', '978-0-312-42759-7'),
        ('Helter Skelter', 'Vincent Bugliosi', '978-0-393-32223-1')
    ]
    
    # Science books (popular science)
    science_books = [
        ('A Brief History of Time', 'Stephen Hawking', '978-0-553-38016-3'),
        ('The Elegant Universe', 'Brian Greene', '978-0-375-70811-7'),
        ('Cosmos', 'Carl Sagan', '978-0-345-90018-8'),
        ('The Selfish Gene', 'Richard Dawkins', '978-0-19-929115-1'),
        ('Surely You\'re Joking, Mr. Feynman!', 'Richard P. Feynman', '978-0-393-35138-7'),
        ('Astrophysics for People in a Hurry', 'Neil deGrasse Tyson', '978-0-393-60879-8'),
        ('Seven Brief Lessons on Physics', 'Carlo Rovelli', '978-0-399-58507-6'),
        ('The Gene: An Intimate History', 'Siddhartha Mukherjee', '978-1-4767-3350-0'),
        ('Hidden Figures', 'Margot Lee Shetterly', '978-0-06-236360-2'),
        ('Lab Girl', 'Hope Jahren', '978-0-385-35267-5')
    ]
    
    # History books
    history_books = [
        ('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', '978-0-06-231609-7'),
        ('Guns, Germs, and Steel', 'Jared Diamond', '978-0-393-31755-8'),
        ('The Guns of August', 'Barbara W. Tuchman', '978-0-345-38423-6'),
        ('A People\'s History of the United States', 'Howard Zinn', '978-0-06-083865-2'),
        ('1491: New Revelations of the Americas Before Columbus', 'Charles C. Mann', '978-1-4000-4006-3'),
        ('The Making of the Atomic Bomb', 'Richard Rhodes', '978-0-684-841178-3'),
        ('Postwar: A History of Europe Since 1945', 'Tony Judt', '978-0-14-303775-0'),
        ('The Rise and Fall of the Third Reich', 'William L. Shirer', '978-0-7432-0671-3'),
        ('Team of Rivals: The Political Genius of Abraham Lincoln', 'Doris Kearns Goodwin', '978-0-7432-7075-8'),
        ('Bury My Heart at Wounded Knee', 'Dee Brown', '978-0-8050-8664-3')
    ]
    
    # Fantasy books
    fantasy_books = [
        ('The Hobbit', 'J.R.R. Tolkien', '978-0-618-26811-1'),
        ('The Name of the Wind', 'Patrick Rothfuss', '978-0-349-13542-3'),
        ('A Game of Thrones', 'George R.R. Martin', '978-0-553-58907-5'),
        ('American Gods', 'Neil Gaiman', '978-0-380-81530-1'),
        ('The Lion, the Witch and the Wardrobe', 'C.S. Lewis', '978-0-06-447104-6'),
        ('Mistborn: The Final Empire', 'Brandon Sanderson', '978-0-7653-8035-2'),
        ('The Lies of Locke Lamora', 'Scott Lynch', '978-0-553-58494-5'),
        ('Jonathan Strange & Mr Norrell', 'Susanna Clarke', '978-0-643-09903-6'),
        ('The Night Circus', 'Erin Morgenstern', '978-0-307-74553-2'),
        ('The Fifth Season', 'N.K. Jemisin', '978-0-316-22929-3')
    ]
    
    # Biography books
    biography_books = [
        ('Steve Jobs', 'Walter Isaacson', '978-1-4516-4853-9'),
        ('Alexander Hamilton', 'Ron Chernow', '978-1-59420-009-0'),
        ('Becoming', 'Michelle Obama', '978-0-525-61978-2'),
        ('The Autobiography of Malcolm X', 'Malcolm X and Alex Haley', '978-0-345-37671-8'),
        ('Educated', 'Tara Westover', '978-0-399-59050-4'),
        ('Long Walk to Freedom', 'Nelson Mandela', '978-0-316-54818-2'),
        ('Born a Crime', 'Trevor Noah', '978-0-7352-1922-1'),
        ('John Adams', 'David McCullough', '978-0-7432-2313-4'),
        ('Frida: A Biography of Frida Kahlo', 'Hayden Herrera', '978-0-374-28158-3'),
        ('Einstein: His Life and Universe', 'Walter Isaacson', '978-0-7432-6475-6')
    ]
    
    # Mystery books
    mystery_books = [
        ('The Hound of the Baskervilles', 'Arthur Conan Doyle', '978-0-14-043786-7'),
        ('The Murder of Roger Ackroyd', 'Agatha Christie', '978-0-06-207347-1'),
        ('The Maltese Falcon', 'Dashiell Hammett', '978-0-679-72616-1'),
        ('Rebecca', 'Daphne du Maurier', '978-0-345-40400-2'),
        ('The Big Sleep', 'Raymond Chandler', '978-0-394-75829-4'),
        ('The Name of the Rose', 'Umberto Eco', '978-0-15-600131-1'),
        ('Gone Girl', 'Gillian Flynn', '978-0-307-58837-1'),
        ('The Girl on the Train', 'Paula Hawkins', '978-0-735-21421-2'),
        ('The Silent Patient', 'Alex Michaelides', '978-1-250-30169-7'),
        ('The Da Vinci Code', 'Dan Brown', '978-0-307-47765-3')
    ]
    
    # Romance books
    romance_books = [
        ('The Love Hypothesis', 'Ali Hazelwood', '978-0-593-33882-0'),
        ('Beach Read', 'Emily Henry', '978-0-198-69130-1'),
        ('Book Lovers', 'Emily Henry', '978-0-593-33383-2'),
        ('Pride and Prejudice', 'Jane Austen', '978-0-553-21310-2'),
        ('Outlander', 'Diana Gabaldon', '978-0-440-21456-3'),
        ('The Notebook', 'Nicholas Sparks', '978-0-446-60934-7'),
        ('Me Before You', 'Jojo Moyes', '978-0-14-312454-2'),
        ('It Ends with Us', 'Colleen Hoover', '978-1-501-11036-8'),
        ('The Kiss Quotient', 'Helen Hoang', '978-0-451-49036-2'),
        ('Red, White & Royal Blue', 'Casey McQuiston', '978-1-250-31377-6')
    ]
    
    # Technology books
    technology_books = [
        ('The Innovators', 'Walter Isaacson', '978-1-4767-0869-0'),
        ('Weapons of Math Destruction', 'Cathy O\'Neil', '978-0-553-34181-4'),
        ('Superintelligence', 'Nick Bostrom', '978-0-19-967811-2'),
        ('Life 3.0', 'Max Tegmark', '978-1-5247-6173-5'),
        ('The Code Book', 'Simon Singh', '978-0-385-49432-5'),
        ('Hackers: Heroes of the Computer Revolution', 'Steven Levy', '978-0-385-48464-9'),
        ('Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '978-0-13-235088-4'),
        ('Artificial Intelligence: A Modern Approach', 'Stuart Russell and Peter Norvig', '978-0-13-461099-3'),
        ('The Soul of a New Machine', 'Tracy Kidder', '978-0-316-49197-6'),
        ('iWoz', 'Steve Wozniak', '978-0-393-33043-4')
    ]
    
    # Self-Help books
    self_help_books = [
        ('Atomic Habits', 'James Clear', '978-0-7352-1129-2'),
        ('How to Win Friends and Influence People', 'Dale Carnegie', '978-0-671-02503-7'),
        ('The 7 Habits of Highly Effective People', 'Stephen R. Covey', '978-0-7432-6951-3'),
        ('Thinking, Fast and Slow', 'Daniel Kahneman', '978-0-374-53355-7'),
        ('Man\'s Search for Meaning', 'Viktor E. Frankl', '978-0-8030-6215-9'),
        ('The Power of Now', 'Eckhart Tolle', '978-1-5773-1480-6'),
        ('Daring Greatly', 'Brené Brown', '978-0-06-902308-8'),
        ('The Subtle Art of Not Giving a F*ck', 'Mark Manson', '978-0-06-245771-4'),
        ('Rich Dad Poor Dad', 'Robert T. Kiyosaki', '978-0-7581-5457-3'),
        ('The Four Agreements', 'Don Miguel Ruiz', '978-1-879-13138-1')
    ]
    
    all_books = [
        ('Fiction', fiction_books),
        ('Non-fiction', non_fiction_books),
        ('Science', science_books),
        ('History', history_books),
        ('Fantasy', fantasy_books),
        ('Biography', biography_books),
        ('Mystery', mystery_books),
        ('Romance', romance_books),
        ('Technology', technology_books),
        ('Self-Help', self_help_books)
    ]
    
    # Insert 10 books for each of the 10 genres, skipping duplicates
    inserted_count = 0
    for genre, book_list in all_books:
        print(f"Inserting books for genre: {genre}")
        for title, author, isbn in book_list:
            try:
                cursor.execute('''
                    INSERT INTO books (title, available, genre, author, isbn, quantity)
                    VALUES (?, 'YES', ?, ?, ?, 1)
                ''', (title, genre, author, isbn))
                inserted_count += 1
            except sqlite3.IntegrityError:
                print(f"Skipped duplicate book: {title} (ISBN: {isbn})")
    
    conn.commit()
    print(f"Data inserted successfully: 10 admins, 50 users, and {inserted_count} books across 10 genres.")

# Optional: Display inserted data counts for verification
with sqlite3.connect('library.db') as conn:  # Updated path to match dataset.py
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    admin_count = cursor.fetchone()[0]
    print(f"Number of admin users: {admin_count}")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Number of users: {user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    print(f"Number of books: {book_count}")
    
    # Show genres distribution
    cursor.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY genre")
    genres_count = cursor.fetchall()
    print("Books per genre:")
    for genre, count in genres_count:
        print(f"  - {genre}: {count}")
    
    # Show sample user data (verify email is included)
    print("\nSample users (first 3):")
    cursor.execute("SELECT username, email, contact, approved FROM users LIMIT 3")
    for row in cursor.fetchall():
        print(f"  - {row[0]} | {row[1]} | {row[2]} | {row[3]}")
    
    # Show sample admin data
    print("\nSample admins (first 2):")
    cursor.execute("SELECT admin_username, email, contact FROM admin_users LIMIT 2")
    for row in cursor.fetchall():
        print(f"  - {row[0]} | {row[1]} | {row[2]}")
