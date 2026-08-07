import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'qgame', 'quizmaster.db')

def add_column():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'language' not in columns:
        print("Adding language column to user table...")
        cursor.execute("ALTER TABLE user ADD COLUMN language VARCHAR(10) DEFAULT 'en'")
        conn.commit()
        print("Successfully added language column.")
    else:
        print("Language column already exists.")
        
    conn.close()

if __name__ == '__main__':
    add_column()
