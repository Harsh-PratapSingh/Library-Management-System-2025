import sqlite3

def filter_books(db_path='library.db', genre1=None, genre2=None, genre3=None, genre4=None, 
                genre5=None, genre6=None, genre7=None, genre8=None, genre9=None, genre10=None,
                available=None):
    """
    Simple function using string building for SQL query.
    11 separate parameters: 10 for genres (Y/N), 1 for availability (Y/N)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all genres
        cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
        genres = []
        for row in cursor.fetchall():
            genres.append(row[0])
        
        # Get genre inputs as list
        genre_inputs = [genre1, genre2, genre3, genre4, genre5, genre6, 
                       genre7, genre8, genre9, genre10]
        
        # Validate inputs
        if len(genre_inputs) != 10:
            print("❌ Need exactly 10 genre parameters!")
            return []
        
        if available not in ['Y', 'N']:
            print("❌ available must be 'Y' or 'N'")
            return []
        
        # Find selected genres (where input is "Y")
        selected_genres = []
        for i, input_val in enumerate(genre_inputs):
            if input_val == 'Y' and i < len(genres):
                selected_genres.append(genres[i])
        
        show_available = available == 'Y'
        
        print(f"\n🔍 Filtering with:")
        if selected_genres:
            print(f"   Genres selected: {', '.join(selected_genres)}")
        print(f"   Available only: {'Yes' if show_available else 'No'}")
        
        # Build SQL query step by step
        base_query = "SELECT id, title, author, genre, available, quantity FROM books"
        
        # Start with WHERE if we have any conditions
        if selected_genres or show_available:
            current_query = base_query + " WHERE "
            conditions = []
        else:
            current_query = base_query
            conditions = []
        
        # Add genre conditions if any
        if selected_genres:
            genre_conditions = []
            for genre in selected_genres:
                genre_conditions.append(f"genre = '{genre}'")
            
            # Join all genre conditions with OR
            all_genre_condition = " OR ".join(genre_conditions)
            conditions.append(f"({all_genre_condition})")
        
        # Add availability condition if requested
        if show_available:
            conditions.append("available = 'YES'")
        
        # Combine all conditions with AND
        if conditions:
            final_where = " AND ".join(conditions)
            current_query += final_where
        
        # Add ORDER BY
        current_query += " ORDER BY genre, title"
        
        print(f"\n🔍 Generated SQL:")
        print(f"   {current_query}")
        
        # Execute the query
        cursor.execute(current_query)
        books = cursor.fetchall()
        
        # Show results
        if not books:
            print("❌ No books found!")
            return []
        
        # Show what was filtered
        filter_info = []
        if selected_genres:
            filter_info.append(f"Genres: {', '.join(selected_genres)}")
        if show_available:
            filter_info.append("Available Only")
        
        if not filter_info:
            filter_info = ["All Books"]
        
        print(f"\n📖 Results ({len(books)} books): {' | '.join(filter_info)}")
        print("-" * 70)
        print(f"ID  | Title                      | Author         | Genre     | Status   | Qty")
        print("-" * 70)
        
        for book in books:
            book_id = book[0]
            title = book[1][:25]
            author = book[2][:12]
            genre = book[3]
            available = book[4]
            quantity = book[5]
            
            status = "Available" if available == 'YES' else "Borrowed"
            
            print(f"{book_id:2}  | {title:<25} | {author:<12} | {genre:<9} | {status:<8} | {quantity}")
        
        print(f"\n📊 Total: {len(books)} books")
        
        conn.close()
        
        return books  # Return books for GUI processing
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# Test function with 11 separate parameters
def test_with_params():
    """
    Test with 11 separate parameters
    """
    print("\n🧪 Testing with 11 separate parameters:")
    print("=" * 50)
    
    # Test 1: Biography (1st genre) + Available Only
    print("\n📝 Test 1: genre1='Y', others='N', available='Y' (Biography + Available)")
    books1 = filter_books(
        genre1='Y', genre2='N', genre3='N', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='N', genre9='N', genre10='N',
        available='Y'
    )
    
    # Test 2: Fiction (3rd genre) only
    print("\n📝 Test 2: genre3='Y', others='N', available='N' (Fiction only)")
    books2 = filter_books(
        genre1='N', genre2='N', genre3='Y', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='N', genre9='N', genre10='N',
        available='N'
    )
    
    # Test 3: Fiction (3rd) + Science (8th) + Available Only
    print("\n📝 Test 3: genre3='Y', genre8='Y', available='Y' (Fiction+Science+Available)")
    books3 = filter_books(
        genre1='N', genre2='N', genre3='Y', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='Y', genre9='N', genre10='N',
        available='Y'
    )
    
    # Test 4: Available Only (all genres N)
    print("\n📝 Test 4: All genres='N', available='Y' (Available Only)")
    books4 = filter_books(
        genre1='N', genre2='N', genre3='N', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='N', genre9='N', genre10='N',
        available='Y'
    )

if __name__ == "__main__":
    print("🚀 Book Filter with 11 Separate Parameters")
    print("=" * 50)
    
    # Interactive test (optional)
    # filter_books()
    
    # Run automated tests with 11 parameters
    test_with_params()
