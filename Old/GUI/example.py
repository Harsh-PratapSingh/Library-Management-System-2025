import sqlite3

def filter_books(self, genre1=None, genre2=None, genre3=None, genre4=None, 
                genre5=None, genre6=None, genre7=None, genre8=None, genre9=None, genre10=None,
                available=None):
    """
    Advanced book filtering function in class format.
    Returns (column_names, data_rows) tuple or (None, []) on errors.
    
    Parameters:
    - genre1-10: 'Y' to include, 'N' to exclude, None for no filtering
    - available: 'Y' for available only, 'N' for all books
    """
    try:
        with sqlite3.connect(self.master.db_path) as conn:
            cursor = conn.cursor()
            
            # Get all available genres from database
            cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
            genres = [row[0] for row in cursor.fetchall()]
            
            if not genres:
                return None, []
            
            # Validate parameters
            genre_inputs = [genre1, genre2, genre3, genre4, genre5, genre6, 
                           genre7, genre8, genre9, genre10]
            
            if any(g not in [None, 'Y', 'N'] for g in genre_inputs):
                return None, []
            
            if available not in [None, 'Y', 'N']:
                return None, []
            
            # Map parameters to actual genres (up to 10)
            selected_genres = []
            for i, genre_flag in enumerate(genre_inputs):
                if genre_flag == 'Y' and i < len(genres):
                    selected_genres.append(genres[i])
            
            show_available = available == 'Y'
            
            # Build safe parameterized query
            query_params = []
            conditions = []
            
            # Genre conditions
            if selected_genres:
                genre_placeholders = ','.join(['?' for _ in selected_genres])
                conditions.append(f"(genre IN ({genre_placeholders}))")
                query_params.extend(selected_genres)
            
            # Availability condition
            if show_available:
                conditions.append("available = 'YES'")
            
            # Build final query
            base_query = """
                SELECT isbn, title, author, genre, available, available_for, check_after, quantity 
                FROM books
            """
            where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
            order_clause = " ORDER BY genre, title"
            
            final_query = base_query + where_clause + order_clause
            
            # Execute with parameters (SQL injection safe)
            cursor.execute(final_query, query_params)
            books = cursor.fetchall()
            
            if not books:
                return None, []
            
            # Prepare output format
            column_names = ['ISBN', 'Title', 'Author', 'Genre', 'Available', 'Duration', 'Due Date', 'Quantity']
            
            # Format data rows for text output
            data_rows = []
            for book in books:
                isbn, title, author, genre, available, available_for, check_after, quantity = book
                
                # Format each column for display
                isbn_display = isbn or ''
                title_display = (title or '')[:50]  # Truncate long titles
                author_display = (author or '')[:30]  # Truncate long authors
                genre_display = genre or ''
                
                # Format availability status
                if available == 'YES':
                    available_display = 'Yes'
                elif available == 'NO':
                    available_display = 'No'
                else:
                    available_display = available or ''
                
                # Duration is always '7 days' for all books
                duration_display = '7 days'  # Fixed as per requirement
                
                # Due date only for borrowed books
                if check_after and available == 'NO':
                    due_date_display = check_after
                else:
                    due_date_display = ''
                
                quantity_display = str(quantity or 0)
                
                data_rows.append([
                    isbn_display,
                    title_display,
                    author_display,
                    genre_display,
                    available_display,
                    duration_display,
                    due_date_display,
                    quantity_display
                ])
            
            print(f"Found {len(data_rows)} books matching criteria")
            print(f"Filter: Genres {selected_genres if selected_genres else 'All'} | Available only: {show_available}")
            print("-" * 100)
            
            # Print table header
            header = f"{'ISBN':<15} {'Title':<35} {'Author':<25} {'Genre':<12} {'Available':<10} {'Duration':<10} {'Due Date':<12} {'Qty'}"
            print(header)
            print("-" * 100)
            
            # Print data rows
            for row in data_rows:
                print(f"{row[0]:<15} {row[1]:<35} {row[2]:<25} {row[3]:<12} {row[4]:<10} {row[5]:<10} {row[6]:<12} {row[7]}")
            
            print("-" * 100)
            print(f"Total: {len(data_rows)} books")
            
            return column_names, data_rows
            
    except sqlite3.Error:
        print("Database error occurred.")
        return None, []
    except Exception:
        print("An error occurred.")
        return None, []

# Example usage in your class:
# self.filter_books(
#     genre1='N', genre2='N', genre3='Y',  # Fiction = 3rd genre
#     genre4='N', genre5='N', genre6='N', 
#     genre7='N', genre8='N', genre9='N', genre10='N',
#     available='Y'  # Available only
# )