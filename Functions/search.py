def search_books_by_title(self, title):
    """
    Search books by title and return results in format compatible with ctkTable.
    Returns a tuple of (column_names, data_rows) or (None, []) if no matches/errors.
    """
    try:
        with sqlite3.connect(self.master.db_path) as conn:
            cursor = conn.cursor()
            
            # Search for books containing the title (case-insensitive)
            cursor.execute(
                """
                SELECT isbn, title, author, genre, available, available_for, check_after
                FROM books 
                WHERE title LIKE ? 
                ORDER BY title
                """,
                (f"%{title}%",)
            )
            results = cursor.fetchall()
            
            if not results:
                return None, []
            
            # Define column names for ctkTable
            column_names = ['ISBN', 'Title', 'Author', 'Genre', 'Available', 'Duration', 'Due Date']
            
            # Format data rows for ctkTable
            data_rows = []
            for row in results:
                isbn = row[0] or ''
                title = row[1] or ''
                author = row[2] or ''
                genre = row[3] or ''
                available = row[4] or ''
                available_for = row[5] or ''
                check_after = row[6] if row[6] else ''
                
                # Format availability status for better display
                if available == 'YES':
                    available_display = 'Yes'
                elif available == 'NO':
                    available_display = 'No'
                else:
                    available_display = available
                
                # Format due date or leave empty
                if check_after and available == 'NO':
                    due_date = check_after
                else:
                    due_date = ''
                
                data_rows.append([
                    isbn,
                    title,
                    author,
                    genre,
                    available_display,
                    available_for,
                    due_date
                ])
            
            return column_names, data_rows
            
    except sqlite3.Error:
        return None, []
    except Exception:
        return None, []

# Example usage:
# column_names, data_rows = self.search_books_by_title("Pride")
# if column_names:
#     # Use with ctkTable
#     table = ctkTable(table_columns=column_names, data=data_rows)
#     print(f"Found {len(data_rows)} books matching 'Pride'")
# else:
#     print("No books found or search error")
