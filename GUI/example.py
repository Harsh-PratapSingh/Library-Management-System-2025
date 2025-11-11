import sqlite3
import customtkinter as ctk
from CTkTable import CTkTable

# Connect to or create SQLite database
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create demo table and insert sample data (only run once)
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER
)
''')
cursor.execute("INSERT INTO books (title, author, year) VALUES ('Book A', 'Author A', 2020)")
cursor.execute("INSERT INTO books (title, author, year) VALUES ('Book B', 'Author B', 2021)")
conn.commit()

# Query data
cursor.execute("SELECT id, title, author, year FROM books")
rows = cursor.fetchall()
conn.close()

# Convert sqlite3 tuples to list of lists for CTkTable
table_data = [list(row) for row in rows]

# GUI part
app = ctk.CTk()
app.geometry("600x400")

# Create table with number of rows and columns
table = CTkTable(master=app, row=len(table_data), column=len(table_data[0]), values=table_data)
table.pack(expand=True, fill="both", padx=20, pady=20)

app.mainloop()
