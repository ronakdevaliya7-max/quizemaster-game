import sqlite3
import random
import os

db_paths = [
    'instance/quizmaster.db',
    'qgame/instance/quizmaster.db',
    'qgame/quizmaster.db',
    'quizmaster.db'
]

for db_path in db_paths:
    if not os.path.exists(db_path):
        continue
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Delete all fake questions
    patterns = [
        '%Sample Python Question%',
        '%Sample Question%',
        '%Generated Question%',
        '%What is the correct answer?%',
        'Q% for %'
    ]
    
    total_deleted = 0
    for p in patterns:
        cursor.execute('DELETE FROM question WHERE text LIKE ?', (p,))
        total_deleted += cursor.rowcount
        
    cursor.execute("DELETE FROM question WHERE option_a = 'A' OR option_a = 'Option A'")
    total_deleted += cursor.rowcount
    
    conn.commit()
    print(f'[{db_path}] Deleted {total_deleted} dummy questions.')
    
    # 2. Get real questions
    real_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE language='en' AND length(text) > 15 LIMIT 1000").fetchall()
    
    if not real_pool:
        print(f'[{db_path}] No real pool found in English. Searching all languages...')
        real_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE length(text) > 15 LIMIT 1000").fetchall()

    print(f'[{db_path}] Found {len(real_pool)} real questions for pool.')
    
    if real_pool:
        categories = cursor.execute('SELECT id FROM category').fetchall()
        populated_count = 0
        for (cid,) in categories:
            count = cursor.execute('SELECT COUNT(*) FROM question WHERE category_id=?', (cid,)).fetchone()[0]
            if count == 0:
                for lang in ['en', 'gu', 'hi']:
                    for _ in range(10):
                        q = random.choice(real_pool)
                        cursor.execute('INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                       (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
                populated_count += 1
        
        conn.commit()
        print(f'[{db_path}] Populated {populated_count} categories with real questions.')
        
    conn.close()
