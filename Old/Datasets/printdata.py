import sqlite3
from datetime import date, datetime

DB = 'library.db'

def print_admin_users():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, admin_username, role, contact, email, created_date FROM admin_users ORDER BY id")
        rows = cur.fetchall()
        print("\n👨‍💼 ADMIN USERS")
        if not rows:
            print("  (none)")
            return
        print(f"{'ID':<4} {'Username':<15} {'Role':<10} {'Contact':<12} {'Email':<28} {'Created':<10}")
        print("-" * 85)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<15} {r[2]:<10} {r[3]:<12} {r[4][:27]:<28} {str(r[5])[:10]:<10}")

def print_users():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, verified, approved_book, contact, email,
                   borrowed_book_id, borrowed_book_date, requested_bookid, join_date
            FROM users ORDER BY id
        """)
        rows = cur.fetchall()
        print("\n👥 USERS")
        if not rows:
            print("  (none)")
            return
        print(f"{'ID':<4} {'Username':<15} {'verified':<9} {'Approved':<9} {'Contact':<12} {'Email':<28} {'BorrowID':<14} {'BorrowDate':<12} {'ReqID':<8} {'Joined':<10}")
        print("-" * 130)
        v_yes = v_no = v_pend = 0
        with_borrow = with_req = 0
        for r in rows:
            v = r[2]
            if v == 'YES': v_yes += 1
            elif v == 'NO': v_no += 1
            else: v_pend += 1
            if r[6] != 'NIL': with_borrow += 1
            if r[8] != 'NIL': with_req += 1
            print(f"{r[0]:<4} {r[1]:<15} {r[2]:<9} {r[3]:<9} {r[4]:<12} {r[5][:27]:<28} {r[6][:13]:<14} {r[7]:<12} {r[8]:<8} {str(r[9])[:10]:<10}")
        print(f"\n   Totals -> Users: {len(rows)} | Verified YES: {v_yes} | Pending: {v_pend} | Rejected: {v_no} | Borrowers: {with_borrow} | Requests: {with_req}")

def print_books():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, author, genre, available, quantity, isbn, available_for, check_after
            FROM books ORDER BY genre, title
        """)
        rows = cur.fetchall()
        print("\n📚 BOOKS")
        if not rows:
            print("  (none)")
            return
        print(f"{'ID':<4} {'Title':<30} {'Author':<18} {'Genre':<12} {'Avail':<6} {'Qty':<3} {'ISBN':<14} {'Borrower':<14} {'Due/Status':<16}")
        print("-" * 135)
        by_genre = {}
        avail_yes = overdue = borrowed = 0
        today = date.today()
        for r in rows:
            by_genre[r[3]] = by_genre.get(r[3], 0) + 1
            if r[4] == 'YES':
                avail_yes += 1
                due_status = "N/A"
            else:
                borrowed += 1
                if r[8]:
                    due = datetime.strptime(r[8], '%Y-%m-%d').date()
                    if due < today:
                        overdue += 1
                        due_status = f"OVERDUE {(today-due).days}d"
                    else:
                        due_status = r[8]
                else:
                    due_status = "N/A"
            isbn_short = (r[6] or "N/A")
            if len(isbn_short) > 13:
                isbn_short = isbn_short[:13] + "…"
            borrower = r[7] or "None"
            print(f"{r[0]:<4} {r[1][:29]:<30} {r[2][:17]:<18} {r[3][:11]:<12} {r[4]:<6} {r[5]:<3} {isbn_short:<14} {borrower[:13]:<14} {due_status:<16}")
        print("\n   By Genre:")
        for g, c in sorted(by_genre.items()):
            print(f"     {g}: {c}")
        print(f"\n   Totals -> Books: {len(rows)} | Available: {avail_yes} | Borrowed: {borrowed} | Overdue: {overdue}")

def print_borrow_links():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT b.id, b.title, b.isbn, b.check_after, b.available_for,
                   u.username, u.verified, u.email
            FROM books b
            LEFT JOIN users u ON u.username = b.available_for
            WHERE b.available = 'NO'
            ORDER BY b.check_after
        """)
        rows = cur.fetchall()
        print("\n🔗 ACTIVE BORROWS (Book → User)")
        if not rows:
            print("  (none)")
            return
        print(f"{'BookID':<6} {'Title':<28} {'ISBN':<14} {'Due':<12} {'Borrower':<14} {'verified':<9} {'Email':<28}")
        print("-" * 120)
        today = date.today()
        overdue = 0
        for r in rows:
            due = r[3] or 'N/A'
            if r[3]:
                d = datetime.strptime(r[3], '%Y-%m-%d').date()
                if d < today:
                    due = f"{r[3]} (OVERDUE { (today-d).days }d)"
                    overdue += 1
            borrower = r[4] or 'Unknown'
            print(f"{r[0]:<6} {r[1][:27]:<28} { (r[2] or 'N/A')[:13]:<14} {due:<12} {borrower[:13]:<14} { (r[6] or 'N/A'):<9} { (r[7] or 'N/A')[:27]:<28}")
        print(f"\n   Totals -> Active borrows: {len(rows)} | Overdue: {overdue}")

def main():
    print_admin_users()
    print_users()
    print_books()
    print_borrow_links()
    print("\n✅ Finished printing all data.")

if __name__ == "__main__":
    main()
