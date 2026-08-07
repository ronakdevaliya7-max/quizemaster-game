import sqlite3
import random

db_paths = ['quizmaster.db', 'instance/quizmaster.db']

for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Clear out ALL questions for user-created categories (id > 200) to remove all dummy data completely
        cursor.execute("DELETE FROM question WHERE category_id > 200")
        deleted_count = cursor.rowcount
        conn.commit()
        print(f"[{db_path}] Deleted {deleted_count} dummy questions from user categories.")
        
        # 2. Get pool of real, high-quality OpenTDB questions (from core categories id <= 12)
        real_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE category_id <= 12 AND language='en' LIMIT 1000").fetchall()
        
        if not real_pool:
            print(f"[{db_path}] No real questions available in the database to copy from!")
            continue
            
        # 3. Get all user categories
        categories = cursor.execute("SELECT id FROM category WHERE id > 200").fetchall()
        
        if categories:
            print(f"[{db_path}] Populating {len(categories)} user categories with {len(real_pool)} real questions pool...")
            for (cid,) in categories:
                # Pick 15 random questions from the real pool
                for lang in ['en', 'gu', 'hi']:
                    for _ in range(15):
                        q = random.choice(real_pool)
                        cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
            conn.commit()
            print(f"[{db_path}] Successfully populated empty categories with real OpenTDB data!")
        else:
            print(f"[{db_path}] No user categories to populate.")
            
        conn.close()
    except Exception as e:
        print(f"[{db_path}] Error: {e}")
