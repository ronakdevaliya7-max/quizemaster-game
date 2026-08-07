import sqlite3
conn = sqlite3.connect('qgame/quizmaster.db')
c = conn.cursor()
c.execute("SELECT COUNT(DISTINCT text) FROM question WHERE language='gu' AND text NOT LIKE '%?%'")
gu_count = c.fetchone()[0]
print(f"{gu_count}/180")
