import sqlite3


def show_pending_requests(db_path='library.db'):
    """
    Simple function to show all pending user requests.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get pending users (verified = 'PENDING') - FIXED: correct column name
            cursor.execute("""
                SELECT id, username, email, contact, join_date 
                FROM users 
                WHERE verified = 'PENDING'
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
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    show_pending_requests()


def approve_user(self, username, status):
    """
    Approve or deny user. status: 'YES' or 'NO'
    Returns 1=Success, 2=Error
    """
    try:
        with sqlite3.connect(self.master.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET verified = ? WHERE username = ? AND verified = 'PENDING'",
                (status, username)
            )
            conn.commit()
            return 1 if cursor.rowcount > 0 else 2
    except:
        return 2


def get_pending_users(self):
    """Returns list of pending usernames or empty list"""
    try:
        with sqlite3.connect(self.master.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE verified = 'PENDING'")
            return [row[0] for row in cursor.fetchall()]
    except:
        return []

# Usage:
# approve_user("user25", "YES")  # Approve
# approve_user("user26", "NO")   # Deny
# pending = get_pending_users()  # Get list
