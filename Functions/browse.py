def search_books_by_title(self, title):
    """
    Search books by title and return matching results.
    Returns a list of book details or empty list if no matches.
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
            
            # Format results as list of dictionaries for easy handling
            book_results = []
            for row in results:
                book_results.append({
                    'isbn': row[0],
                    'title': row[1],
                    'author': row[2],
                    'genre': row[3],
                    'available': row[4],
                    'available_for': row[5],
                    'check_after': row[6] if row[6] else None
                })
            
            return book_results
            
    except sqlite3.Error:
        return []
    except Exception:
        return []

# Example usage:
# results = search_books_by_title(self, "Pride")
# This would return all books with "Pride" in the title
