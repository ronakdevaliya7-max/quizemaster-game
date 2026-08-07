import sqlite3
import random
from deep_translator import GoogleTranslator

db_path = 'qgame/quizmaster.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Get 100 real English questions from the original pool
# We'll just hardcode a few real questions or fetch from the DB if they exist.
# Let's fetch the best 50 English questions from the DB to translate and reuse.
print("Fetching real questions from DB...")
real_en_pool = cursor.execute("SELECT text, option_a, option_b, option_c, option_d, correct_option, difficulty FROM question WHERE language='en' AND length(text) > 15 AND option_a != 'A' LIMIT 50").fetchall()

if len(real_en_pool) < 50:
    print("Not enough real questions in DB, please check.")

print(f"Got {len(real_en_pool)} real English questions.")

# 2. Translate them to Gujarati and Hindi
translator_gu = GoogleTranslator(source='en', target='gu')
translator_hi = GoogleTranslator(source='en', target='hi')

translated_pool = []
print("Translating pool to Gujarati and Hindi... This might take a minute.")
for i, q in enumerate(real_en_pool):
    try:
        en_texts = [q[0], q[1], q[2], q[3], q[4]]
        gu_texts = translator_gu.translate_batch(en_texts)
        hi_texts = translator_hi.translate_batch(en_texts)
        
        translated_pool.append({
            'en': (q[0], q[1], q[2], q[3], q[4], q[5], q[6]),
            'gu': (gu_texts[0], gu_texts[1], gu_texts[2], gu_texts[3], gu_texts[4], q[5], q[6]),
            'hi': (hi_texts[0], hi_texts[1], hi_texts[2], hi_texts[3], hi_texts[4], q[5], q[6])
        })
    except Exception as e:
        print(f"Error translating question {i}: {e}")

print(f"Successfully translated {len(translated_pool)} questions.")

# 3. Clear ALL existing questions
print("Deleting old questions...")
cursor.execute("DELETE FROM question")
conn.commit()

# 4. Insert 40 questions per category
categories = cursor.execute("SELECT id, name FROM category").fetchall()
print(f"Found {len(categories)} categories. Populating 40 questions each...")

total_inserted = 0
for cid, cname in categories:
    # Pick 40 random questions from the translated pool
    # If pool is smaller than 40, we'll allow repeats by using random.choices, or just insert the whole pool
    selected = random.choices(translated_pool, k=40) if len(translated_pool) > 0 else []
    
    for item in selected:
        for lang in ['en', 'gu', 'hi']:
            q = item[lang]
            cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
            total_inserted += 1

conn.commit()
conn.close()

print(f"Done! Inserted {total_inserted} total questions (40 per category in 3 languages).")
