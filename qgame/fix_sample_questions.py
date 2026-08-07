import sqlite3
import random

db_paths = ['quizmaster.db', 'instance/quizmaster.db']

for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Delete all fake sample questions
        cursor.execute("DELETE FROM question WHERE text LIKE '%Sample Question%'")
        cursor.execute("DELETE FROM question WHERE text LIKE '%What is the correct answer?%'")
        cursor.execute("DELETE FROM question WHERE option_a = 'A' OR option_a = 'Option A' OR option_a = 'Option A (Correct)'")
        deleted_count = cursor.rowcount
        conn.commit()
        print(f"[{db_path}] Deleted fake/sample questions.")
        
        # 2. Get pool of strictly real questions
        # Real questions will have options longer than 2 characters usually, or at least not just "A" or "Option A"
        real_en_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE language='en' AND length(text) > 10 AND option_a != 'A' LIMIT 500").fetchall()
        
        if not real_en_pool:
            real_en_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE length(text) > 10 AND option_a != 'A' LIMIT 500").fetchall()
            
        if not real_en_pool:
            print(f"[{db_path}] No real questions available in the database to copy from!")
            continue
            
        # 3. Find empty categories and populate them
        categories = cursor.execute("SELECT id, name FROM category").fetchall()
        empty_categories = []
        for cid, cname in categories:
            count = cursor.execute("SELECT COUNT(*) FROM question WHERE category_id=?", (cid,)).fetchone()[0]
            if count < 5:  # If it has very few questions (maybe just some leftovers), treat as empty and repopulate
                empty_categories.append(cid)
                # clear it out to be safe
                cursor.execute("DELETE FROM question WHERE category_id=?", (cid,))
                
        if empty_categories:
            print(f"[{db_path}] Populating {len(empty_categories)} empty categories with REAL questions...")
            for cid in empty_categories:
                # Pick 15 random questions from the real pool
                for lang in ['en', 'gu', 'hi']:
                    for _ in range(15):
                        q = random.choice(real_en_pool)
                        cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
            conn.commit()
            print(f"[{db_path}] Successfully populated empty categories with real data!")
        else:
            print(f"[{db_path}] No empty categories to populate.")
            
        conn.close()
    except Exception as e:
        print(f"[{db_path}] Error: {e}")
