import sqlite3
import time
from deep_translator import GoogleTranslator

db_path = 'qgame/quizmaster.db'
conn = sqlite3.connect(db_path, timeout=60)
cursor = conn.cursor()

print("Fetching unique questions to translate...")
cursor.execute("SELECT DISTINCT text, option_a, option_b, option_c, option_d FROM question WHERE language='en'")
unique_questions = cursor.fetchall()

print(f"Found {len(unique_questions)} unique questions. Starting translation process...")

translator_gu = GoogleTranslator(source='en', target='gu')
translator_hi = GoogleTranslator(source='en', target='hi')

success_count = 0

for i, q in enumerate(unique_questions):
    en_text, en_a, en_b, en_c, en_d = q
    
    try:
        # Check if already translated (to skip previously translated ones)
        cursor.execute("SELECT text FROM question WHERE language='gu' AND text != ? LIMIT 1", (en_text,))
        # Actually a better check: check if the 'gu' language row for this specific question text has been translated
        # But our schema doesn't have a link between en and gu except the text.
        # Let's just check if there is a 'gu' row matching the EXACT english text.
        # If there is, it means it hasn't been translated yet (since it's still in english)
        cursor.execute("SELECT 1 FROM question WHERE language='gu' AND text=?", (en_text,))
        if not cursor.fetchone():
            # If no row has the exact english text for 'gu', it means it was ALREADY translated successfully
            continue
            
        en_texts = [en_text, en_a, en_b, en_c, en_d]
        
        time.sleep(1.2)
        gu_texts = translator_gu.translate_batch(en_texts)
        
        time.sleep(1.2)
        hi_texts = translator_hi.translate_batch(en_texts)
        
        cursor.execute("""
            UPDATE question 
            SET text=?, option_a=?, option_b=?, option_c=?, option_d=? 
            WHERE text=? AND language='gu'
        """, (gu_texts[0], gu_texts[1], gu_texts[2], gu_texts[3], gu_texts[4], en_text))
        
        cursor.execute("""
            UPDATE question 
            SET text=?, option_a=?, option_b=?, option_c=?, option_d=? 
            WHERE text=? AND language='hi'
        """, (hi_texts[0], hi_texts[1], hi_texts[2], hi_texts[3], hi_texts[4], en_text))
        
        conn.commit()
        success_count += 1
        
        if success_count % 10 == 0:
            print(f"Progress: Translated {success_count} unique questions so far...")
            
    except Exception as e:
        print(f"Error translating question {i+1}: {e}")
        time.sleep(3)

print(f"Translation complete! Successfully translated and updated {success_count} unique questions across all categories.")
conn.close()
