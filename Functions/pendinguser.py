import sqlite3

def show_pending_requests(db_path='library.db'):
    """
    Simple function to show all pending user requests.
    """
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get pending users (approved = 'PENDING')
        cursor.execute("""
            SELECT id, username, email, contact, join_date 
            FROM users 
            WHERE approved = 'PENDING'
            ORDER BY join_date
        """)
        
        pending_users = cursor.fetchall()
        
        if not pending_users:
            print("✅ No pending user requests!")
            return
        
        # Show header
        print(f"\n📋 Pending User Requests ({len(pending_users)} users):")
        print("-" * 70)
        print(f"{'ID':<4} {'Username':<15} {'Email':<25} {'Contact':<12} {'Joined':<12}")
        print("-" * 70)
        
        # Show each pending user
        for user in pending_users:
            user_id = user[0]
            username = user[1]
            email = user[2]
            contact = user[3]
            join_date = user[4]
            
            print(f"{user_id:<4} {username:<15} {email[:24]:<25} {contact:<12} {join_date:<12}")
        
        print(f"\n📊 Total pending requests: {len(pending_users)}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_pending_requests()
