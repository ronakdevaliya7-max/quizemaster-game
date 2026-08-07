import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'quizmaster.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete fake questions
cursor.execute("DELETE FROM question WHERE text LIKE '%What is the correct answer?%'")
deleted_count = cursor.rowcount
conn.commit()

print(f"Removed {deleted_count} fake questions from database.")
conn.close()
