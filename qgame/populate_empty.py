import sqlite3
import random

db_paths = ['quizmaster.db', 'instance/quizmaster.db']

for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        categories = cursor.execute("SELECT id, name FROM category").fetchall()
        empty_categories = []
        for cid, cname in categories:
            count = cursor.execute("SELECT COUNT(*) FROM question WHERE category_id=?", (cid,)).fetchone()[0]
            if count == 0:
                empty_categories.append((cid, cname))
                
        if empty_categories:
            print(f"[{db_path}] Found {len(empty_categories)} empty categories. Populating...")
            en_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE language='en' LIMIT 100").fetchall()
            
            if not en_pool:
                # If no 'en', just get any questions
                en_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question LIMIT 100").fetchall()
                
            if not en_pool:
                print(f"[{db_path}] No questions in DB to copy from!")
                continue
                
            for cid, cname in empty_categories:
                for lang in ['en', 'gu', 'hi']:
                    for _ in range(15):
                        q = random.choice(en_pool)
                        cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
            conn.commit()
            print(f"[{db_path}] Successfully populated {len(empty_categories)} categories!")
        else:
            print(f"[{db_path}] No empty categories.")
        conn.close()
    except Exception as e:
        print(f"[{db_path}] Error: {e}")
