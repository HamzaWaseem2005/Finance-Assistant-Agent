import sqlite3

def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            type TEXT,
            description TEXT,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and Table successfully created ")

if __name__ == "__main__":
    init_db()