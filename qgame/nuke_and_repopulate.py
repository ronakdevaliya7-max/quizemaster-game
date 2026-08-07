import sqlite3
import random

db_paths = ['quizmaster.db', 'instance/quizmaster.db']

for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Nuke ALL dummy questions across the entire database
        cursor.execute("DELETE FROM question WHERE text LIKE '%Sample Question%'")
        cursor.execute("DELETE FROM question WHERE text LIKE '%Generated Question%'")
        cursor.execute("DELETE FROM question WHERE text LIKE '%What is the correct answer?%'")
        cursor.execute("DELETE FROM question WHERE option_a LIKE 'Option A%'")
        cursor.execute("DELETE FROM question WHERE option_a = 'A'")
        conn.commit()
        
        # 2. Extract the remaining strictly REAL questions (there should be around 896)
        real_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE language='en' AND text NOT LIKE '%Sample Question%' AND text NOT LIKE '%Generated Question%' AND text NOT LIKE '%What is the correct answer?%' AND option_a NOT LIKE 'Option A%' AND option_a != 'A' LIMIT 1000").fetchall()
        
        if not real_pool:
            real_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE text NOT LIKE '%Sample Question%' AND text NOT LIKE '%Generated Question%' AND text NOT LIKE '%What is the correct answer?%' AND option_a NOT LIKE 'Option A%' AND option_a != 'A' LIMIT 1000").fetchall()
            
        if not real_pool:
            print(f"[{db_path}] No real questions available in the database to copy from!")
            continue
            
        print(f"[{db_path}] Found {len(real_pool)} verified REAL questions to use as a pool.")
        
        # 3. Check every single category. If it has fewer than 10 questions, repopulate it!
        categories = cursor.execute("SELECT id, name FROM category").fetchall()
        populated_count = 0
        
        for cid, cname in categories:
            # Delete any remaining stragglers just in case
            count = cursor.execute("SELECT COUNT(*) FROM question WHERE category_id=?", (cid,)).fetchone()[0]
            if count < 10:
                # Clear it completely to be safe
                cursor.execute("DELETE FROM question WHERE category_id=?", (cid,))
                
                # Insert 15 random real questions
                for lang in ['en', 'gu', 'hi']:
                    for _ in range(15):
                        q = random.choice(real_pool)
                        cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
                populated_count += 1
                
        conn.commit()
        print(f"[{db_path}] Successfully repopulated {populated_count} categories with exclusively real data!")
        conn.close()
    except Exception as e:
        print(f"[{db_path}] Error: {e}")
