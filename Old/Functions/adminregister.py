import sqlite3


def register_admin(db_path='library.db'):
    """
    Register a new admin user. Requires admin code '1111' for successful registration.
    Validates 10-digit contact and ensures uniqueness of username/email.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get admin code first (security check)
        print("🔐 Admin Registration")
        print("-" * 25)
        admin_code = input("Enter admin code (1111): ").strip()
        
        if admin_code != '1111':
            print("❌ Invalid admin code! Access denied.")
            return False
        
        # Get admin details
        username = input("Admin Username: ").strip()
        if not username:
            print("❌ Username cannot be empty!")
            return False
        
        password = input("Password: ").strip()
        if len(password) < 4:
            print("❌ Password must be at least 4 characters!")
            return False
        
        contact = input("10-digit Contact Number: ").strip()
        if not contact.isdigit() or len(contact) != 10:
            print("❌ Contact must be exactly 10 digits!")
            return False
        
        email = input("Email: ").strip()
        if not email or '@' not in email:
            print("❌ Valid email required!")
            return False
        
        # Check if username already exists
        cursor.execute("SELECT id FROM admin_users WHERE admin_username = ?", (username,))
        if cursor.fetchone():
            print("❌ Admin username already exists!")
            return False
        
        # Check if email already exists
        cursor.execute("SELECT id FROM admin_users WHERE email = ?", (email,))
        if cursor.fetchone():
            print("❌ Email already exists!")
            return False
        
        # Check if contact already exists (to avoid duplicates)
        cursor.execute("SELECT id FROM admin_users WHERE contact = ?", (contact,))
        if cursor.fetchone():
            print("❌ Contact number already registered!")
            return False
        
        # Insert new admin user
        cursor.execute('''
            INSERT INTO admin_users (admin_username, password, role, contact, email)
            VALUES (?, ?, 'ADMIN', ?, ?)
        ''', (username, password, contact, email))
        
        conn.commit()
        
        print("\n✅ Admin registered successfully!")
        print(f"👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"📞 Contact: {contact}")
        print(f"🔐 Role: ADMIN")
        print(f"📅 Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("❌ Username or email already exists! Please try different values.")
        else:
            print(f"❌ Database error: {e}")
    except ValueError:
        print("❌ Invalid input! Please check your data.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if conn:
            conn.close()


def view_all_admins(db_path='library.db'):
    """
    Display all existing admin users (for verification).
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, admin_username, role, contact, email, created_date
            FROM admin_users 
            ORDER BY created_date DESC
        """)
        
        admins = cursor.fetchall()
        
        if not admins:
            print("No admin users found.")
            return False
        
        print("\n👨‍💼 Current Admin Users:")
        print("-" * 80)
        print(f"{'ID':<4} {'Username':<15} {'Role':<10} {'Contact':<12} {'Email':<25} {'Created':<12}")
        print("-" * 80)
        
        for admin in admins:
            admin_id, username, role, contact, email, created_date = admin
            print(f"{admin_id:<4} {username:<15} {role:<10} {contact:<12} {email[:24]:<25} {created_date[:10]:<12}")
        
        print(f"\nTotal Admin Users: {len(admins)}")
        return True
        
    except Exception as e:
        print(f"❌ Error displaying admins: {e}")
    finally:
        if conn:
            conn.close()


def main():
    """
    Main function to run admin registration or view existing admins.
    """
    print("🔐 Library Admin Registration System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Register New Admin")
        print("2. View All Admins")
        print("0. Exit")
        
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            if register_admin():
                print("\nYou can now log in with your admin credentials.")
            else:
                print("\nRegistration failed. Try again.")
        
        elif choice == '2':
            view_all_admins()
        
        elif choice == '0':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")
        
        if choice in ['1', '2']:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
