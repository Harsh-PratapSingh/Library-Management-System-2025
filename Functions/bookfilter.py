import sqlite3


def filter_books(db_path='library.db', genre1=None, genre2=None, genre3=None, genre4=None, 
                genre5=None, genre6=None, genre7=None, genre8=None, genre9=None, genre10=None,
                available=None, interactive=False):
    """
    Simple function using parameterized queries for safe SQL filtering.
    Supports both interactive mode and direct parameter calls.
    
    Parameters:
    - 10 genre parameters (genre1 to genre10): 'Y'/'N' or None
    - available: 'Y' (available only) or 'N' (all books)
    - interactive: True for user input mode, False for direct parameter use
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all available genres from database
        cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
        genres = [row[0] for row in cursor.fetchall()]
        
        if interactive:
            print("\n📚 Interactive Book Filter")
            print("-" * 35)
            print("Available Genres:")
            for i, genre in enumerate(genres, 1):
                print(f"  {i}. {genre}")
            
            # Get genre selections interactively
            print("\nEnter genre numbers (e.g., 1,3,5) or press Enter for all:")
            genre_input = input("> ").strip()
            
            # Get availability filter
            print("\nShow only available books? (Y/N):")
            avail_input = input("> ").strip().upper()
            
            # Parse genre input
            genre_numbers = []
            if genre_input:
                for part in genre_input.split(','):
                    part = part.strip()
                    if part.isdigit():
                        genre_numbers.append(int(part))
            
            # Build genre flags
            genre_flags = ['N'] * 10
            for num in genre_numbers:
                if 1 <= num <= min(10, len(genres)):
                    genre_flags[num-1] = 'Y'
            
            show_available = avail_input == 'Y'
            print(f"\n🔍 Filtering: Genres {genre_numbers} | Available only: {show_available}")
        else:
            # Use direct parameters
            genre_inputs = [genre1, genre2, genre3, genre4, genre5, genre6, 
                           genre7, genre8, genre9, genre10]
            
            # Validate parameters
            if any(g not in [None, 'Y', 'N'] for g in genre_inputs):
                print("❌ Genre parameters must be 'Y', 'N', or None!")
                return []
            
            if available not in [None, 'Y', 'N']:
                print("❌ 'available' parameter must be 'Y', 'N', or None!")
                return []
            
            # Map parameters to actual genres (up to 10)
            selected_genres = []
            for i, genre_flag in enumerate(genre_inputs):
                if genre_flag == 'Y' and i < len(genres):
                    selected_genres.append(genres[i])
            
            show_available = available == 'Y'
            genre_numbers = [i+1 for i, flag in enumerate(genre_inputs) if flag == 'Y']
            
            print(f"\n🔍 Direct filter: Genres {genre_numbers} | Available only: {show_available}")
        
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
        base_query = "SELECT id, title, author, genre, available, quantity FROM books"
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        order_clause = " ORDER BY genre, title"
        
        final_query = base_query + where_clause + order_clause
        
        print(f"\n🔍 Executing Query:")
        print(f"   {final_query}")
        print(f"   Params: {query_params}")
        
        # Execute with parameters (SQL injection safe)
        cursor.execute(final_query, query_params)
        books = cursor.fetchall()
        
        # Display results
        if not books:
            print("❌ No books found matching criteria!")
            return []
        
        # Summary
        filter_summary = []
        if selected_genres:
            filter_summary.append(f"Genres: {', '.join(selected_genres)}")
        if show_available:
            filter_summary.append("Available Only")
        
        if not filter_summary:
            filter_summary = ["All Books"]
        
        print(f"\n📖 Results ({len(books)} books): {' | '.join(filter_summary)}")
        print("-" * 75)
        print(f"{'ID':<4} {'Title':<28} {'Author':<15} {'Genre':<10} {'Status':<10} {'Qty':<4}")
        print("-" * 75)
        
        for book in books:
            book_id, title, author, genre, available, quantity = book
            title = title[:27]  # Truncate for display
            author = author[:14]
            status = "🟢 Available" if available == 'YES' else "🔴 Borrowed"
            
            print(f"{book_id:<4} {title:<28} {author:<15} {genre:<10} {status:<10} {quantity:<4}")
        
        print(f"\n📊 Total: {len(books)} books")
        print(f"🎯 Filtered from {len(genres)} total genres in database")
        
        return books  # Return for GUI integration
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_genre_mapping(db_path='library.db'):
    """
    Get the actual genre names from database for reference.
    Useful for GUI dropdowns or parameter mapping.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
            genres = [row[0] for row in cursor.fetchall()]
            return genres
    except Exception as e:
        print(f"❌ Error getting genres: {e}")
        return []


def interactive_filter(db_path='library.db'):
    """
    Interactive version that asks user for genre selections.
    Automatically maps user choices to the 11-parameter format.
    """
    genres = get_genre_mapping(db_path)
    if not genres:
        print("❌ No genres found in database!")
        return
    
    print(f"\n📚 Interactive Book Filter")
    print(f"Found {len(genres)} genres:")
    for i, genre in enumerate(genres, 1):
        print(f"  {i}. {genre}")
    
    # Get genre selections
    genre_input = input("\nEnter genre numbers (e.g., '1,3,5') or Enter for all: ").strip()
    genre_numbers = []
    if genre_input:
        for part in genre_input.split(','):
            part = part.strip()
            if part.isdigit():
                num = int(part)
                if 1 <= num <= len(genres):
                    genre_numbers.append(num)
    
    # Get availability filter
    avail_input = input("\nShow only available books? (Y/N): ").strip().upper()
    show_available = avail_input == 'Y'
    
    # Convert to 11-parameter format
    genre_flags = ['N'] * 10
    for num in genre_numbers:
        if 1 <= num <= 10:
            genre_flags[num-1] = 'Y'
    
    # Unpack parameters
    books = filter_books(
        db_path=db_path,
        genre1=genre_flags[0], genre2=genre_flags[1], genre3=genre_flags[2],
        genre4=genre_flags[3], genre5=genre_flags[4], genre6=genre_flags[5],
        genre7=genre_flags[6], genre8=genre_flags[7], genre9=genre_flags[8],
        genre10=genre_flags[9],
        available='Y' if show_available else 'N'
    )
    
    return books


# Test functions
def test_direct_parameters():
    """Test with direct 11-parameter calls (for GUI integration)."""
    print("\n🧪 Testing Direct Parameter Calls:")
    print("=" * 45)
    
    # Test 1: Fiction (assume 3rd genre) + Available only
    print("\n📝 Test 1: Fiction + Available Only")
    books1 = filter_books(
        genre1='N', genre2='N', genre3='Y',  # Fiction = 3rd genre
        genre4='N', genre5='N', genre6='N', 
        genre7='N', genre8='N', genre9='N', genre10='N',
        available='Y'
    )
    
    # Test 2: Science (assume 8th genre) only
    print("\n📝 Test 2: Science Only (All Availability)")
    books2 = filter_books(
        genre1='N', genre2='N', genre3='N', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='Y',  # Science = 8th genre
        genre9='N', genre10='N',
        available='N'
    )
    
    # Test 3: Multiple genres + Available only
    print("\n📝 Test 3: Fiction + Science + Available Only")
    books3 = filter_books(
        genre1='N', genre2='N', genre3='Y',  # Fiction
        genre4='N', genre5='N', genre6='N', 
        genre7='N', genre8='Y',  # Science
        genre9='N', genre10='N',
        available='Y'
    )
    
    # Test 4: All Available Books (no genre filter)
    print("\n📝 Test 4: All Available Books")
    books4 = filter_books(
        genre1='N', genre2='N', genre3='N', genre4='N', genre5='N',
        genre6='N', genre7='N', genre8='N', genre9='N', genre10='N',
        available='Y'
    )
    
    # Test 5: All Books (no filters)
    print("\n📝 Test 5: All Books (No Filters)")
    books5 = filter_books()  # All parameters default to None
    
    print("\n✅ All tests completed!")
    print(f"📊 Test results: {len(books1)}, {len(books2)}, {len(books3)}, {len(books4)}, {len(books5)} books")


def test_interactive_mode():
    """Test interactive filtering mode."""
    print("\n🧪 Testing Interactive Mode:")
    print("=" * 35)
    interactive_filter()


if __name__ == "__main__":
    print("🚀 Advanced Book Filter System")
    print("=" * 40)
    print("1. Interactive Filter (User Input)")
    print("2. Direct Parameter Tests (GUI Simulation)")
    print("0. Exit")
    
    choice = input("Choose mode: ").strip()
    
    if choice == '1':
        test_interactive_mode()
    elif choice == '2':
        test_direct_parameters()
    elif choice == '0':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")
        # Fallback to interactive
        test_interactive_mode()
