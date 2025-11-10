import sqlite3

def print_all_data(db_path='library.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # ... all your SELECTs and prints here ...
        # no need to call conn.close(); 'with' will close automatically

if __name__ == "__main__":
    print_all_data()
