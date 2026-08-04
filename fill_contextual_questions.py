import sqlite3
import random
from deep_translator import GoogleTranslator
import time

# 1. Define contextual pools using real questions
pools = {
    'Science_Tech': [
        ("What is the chemical symbol for water?", "H2O", "O2", "CO2", "HO", "A", "Medium"),
        ("What part of the cell is the powerhouse?", "Nucleus", "Mitochondria", "Ribosome", "Membrane", "B", "Medium"),
        ("What is the speed of light (approx)?", "300,000 km/s", "150,000 km/s", "1,000,000 km/s", "100,000 km/s", "A", "Medium"),
        ("What is the value of Pi (approx)?", "3.14", "3.16", "3.12", "3.18", "A", "Easy"),
        ("What is 7 cubed?", "21", "49", "343", "100", "C", "Hard"),
        ("What does 'def' do in Python?", "Define variable", "Define function", "Define class", "Define loop", "B", "Easy"),
        ("What does HTML stand for?", "Hyper Text Markup Language", "High Text Markup Language", "Hyper Tabular Markup Language", "None", "A", "Easy"),
        ("Which company created the iPhone?", "Samsung", "Google", "Apple", "Microsoft", "C", "Easy"),
        ("What is the brain of the computer?", "RAM", "GPU", "CPU", "Hard Drive", "C", "Easy"),
        ("What force keeps us on the ground?", "Magnetism", "Gravity", "Friction", "Inertia", "B", "Easy"),
        ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "Easy"),
        ("What gas do plants absorb?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "C", "Easy"),
        ("How many bones are in the adult human body?", "206", "208", "210", "212", "A", "Medium"),
        ("Solve for x: 2x = 10", "2", "5", "10", "20", "B", "Easy"),
        ("What is the square root of 144?", "10", "11", "12", "14", "C", "Medium")
    ],
    'Commerce_Business': [
        ("What does ROI stand for?", "Return on Investment", "Rate of Interest", "Return on Income", "Rate of Inflation", "A", "Medium"),
        ("What is the currency of Japan?", "Yuan", "Won", "Yen", "Ringgit", "C", "Easy"),
        ("Which of these is a liability?", "Cash", "Accounts Payable", "Inventory", "Equipment", "B", "Medium"),
        ("What is the main goal of a for-profit business?", "Charity", "Maximize Profit", "Employ people", "Pay taxes", "B", "Easy"),
        ("Who is the co-founder of Microsoft?", "Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Jeff Bezos", "B", "Easy"),
        ("What is GDP?", "Gross Domestic Product", "Gross Domestic Profit", "General Domestic Product", "Gross Daily Profit", "A", "Medium"),
        ("In accounting, Assets = Liabilities + ?", "Revenue", "Expenses", "Equity", "Profit", "C", "Hard"),
        ("Which company is known for its e-commerce platform?", "Ford", "Amazon", "Boeing", "Pfizer", "B", "Easy"),
        ("What is a bull market?", "Market going down", "Market going up", "Market staying flat", "Market closed", "B", "Medium"),
        ("What does B2B stand for?", "Business to Buyer", "Business to Bank", "Business to Business", "Buyer to Buyer", "C", "Easy"),
        ("What is a balance sheet?", "A list of expenses", "A statement of assets, liabilities, and equity", "A tax return", "A budget", "B", "Medium"),
        ("What is inflation?", "Decrease in prices", "Increase in prices", "Stable prices", "No taxes", "B", "Easy"),
        ("What is the primary function of a bank?", "Sell cars", "Accept deposits and make loans", "Build houses", "Farm", "B", "Easy"),
        ("What does CEO stand for?", "Chief Executive Officer", "Chief Engineering Officer", "Chief Export Officer", "Central Executive Officer", "A", "Easy"),
        ("What is a stock dividend?", "A tax", "A penalty", "A portion of company profits paid to shareholders", "A loan", "C", "Medium")
    ],
    'Arts_Humanities': [
        ("Who painted the 'Mona Lisa'?", "Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello", "B", "Easy"),
        ("Who wrote 'Romeo and Juliet'?", "Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain", "B", "Easy"),
        ("Who was the first President of the USA?", "Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams", "B", "Easy"),
        ("In which year did World War II end?", "1940", "1945", "1950", "1918", "B", "Medium"),
        ("Who painted 'The Starry Night'?", "Claude Monet", "Vincent van Gogh", "Edvard Munch", "Gustav Klimt", "B", "Medium"),
        ("What ancient civilization built the pyramids?", "Romans", "Greeks", "Egyptians", "Mayans", "C", "Easy"),
        ("Who wrote the play 'Hamlet'?", "William Shakespeare", "John Milton", "Geoffrey Chaucer", "Arthur Miller", "A", "Easy"),
        ("Which empire was ruled by Julius Caesar?", "Ottoman", "Roman", "British", "Mongol", "B", "Easy"),
        ("Who is the author of 'Pride and Prejudice'?", "Charlotte Bronte", "Jane Austen", "Emily Bronte", "Mary Shelley", "B", "Medium"),
        ("What is the primary setting of 'Dracula' by Bram Stoker?", "London", "Transylvania", "Paris", "Rome", "B", "Medium"),
        ("Who painted the ceiling of the Sistine Chapel?", "Michelangelo", "Leonardo da Vinci", "Raphael", "Sandro Botticelli", "A", "Hard"),
        ("In what year did the Titanic sink?", "1905", "1912", "1920", "1898", "B", "Medium"),
        ("Which artist cut off his own left ear?", "Pablo Picasso", "Vincent van Gogh", "Claude Monet", "Salvador Dali", "B", "Medium"),
        ("Who discovered America in 1492?", "Vasco da Gama", "Ferdinand Magellan", "Christopher Columbus", "James Cook", "C", "Easy"),
        ("What is the title of the first book of the Bible?", "Exodus", "Genesis", "Leviticus", "Numbers", "B", "Hard")
    ],
    'GK_Competitive': [
        ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", "C", "Medium"),
        ("What is the largest ocean on Earth?", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean", "D", "Easy"),
        ("How many continents are there?", "5", "6", "7", "8", "C", "Easy"),
        ("What is the longest river in the world?", "Amazon River", "Nile River", "Yangtze River", "Mississippi River", "B", "Medium"),
        ("Which is the smallest country in the world?", "Monaco", "Vatican City", "San Marino", "Liechtenstein", "B", "Medium"),
        ("Which country won the FIFA World Cup in 2022?", "France", "Argentina", "Brazil", "Croatia", "B", "Easy"),
        ("What is the national game of India?", "Cricket", "Hockey", "Kabaddi", "Football", "B", "Easy"),
        ("Which is the longest river in India?", "Ganges", "Yamuna", "Godavari", "Narmada", "A", "Easy"),
        ("Mount Everest is located in which mountain range?", "Andes", "Rockies", "Alps", "Himalayas", "D", "Easy"),
        ("Which desert is the largest hot desert in the world?", "Gobi", "Sahara", "Kalahari", "Thar", "B", "Easy"),
        ("Who has won the most Olympic gold medals in history?", "Usain Bolt", "Michael Phelps", "Serena Williams", "Roger Federer", "B", "Hard"),
        ("Which country has the longest coastline in the world?", "Australia", "Canada", "Russia", "Indonesia", "B", "Hard"),
        ("Which canal connects the Mediterranean Sea to the Red Sea?", "Panama Canal", "Suez Canal", "Kiel Canal", "Erie Canal", "B", "Medium"),
        ("In cricket, how many wickets must fall to end an innings?", "9", "10", "11", "6", "B", "Easy"),
        ("Which country is also known as the Land of the Rising Sun?", "China", "Japan", "South Korea", "Thailand", "B", "Easy")
    ]
}

db_path = 'qgame/quizmaster.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. Clear ALL existing questions to fix the mess
print("Deleting all old questions...")
cursor.execute("DELETE FROM question")
conn.commit()

# 3. Translate pools with fallback
translator_gu = GoogleTranslator(source='en', target='gu')
translator_hi = GoogleTranslator(source='en', target='hi')

translated_pools = {}
print("Translating category pools... (With fallback to English)")

for pool_name, questions in pools.items():
    translated_pools[pool_name] = []
    print(f"Translating pool: {pool_name} ({len(questions)} questions)")
    for i, q in enumerate(questions):
        gu_texts = [q[0], q[1], q[2], q[3], q[4]]
        hi_texts = [q[0], q[1], q[2], q[3], q[4]]
        try:
            en_texts = [q[0], q[1], q[2], q[3], q[4]]
            gu_texts = translator_gu.translate_batch(en_texts)
            hi_texts = translator_hi.translate_batch(en_texts)
        except Exception as e:
            print(f"Error translating {pool_name} Q{i}: {e}. Falling back to English.")
            
        translated_pools[pool_name].append({
            'en': (q[0], q[1], q[2], q[3], q[4], q[5], q[6]),
            'gu': (gu_texts[0], gu_texts[1], gu_texts[2], gu_texts[3], gu_texts[4], q[5], q[6]),
            'hi': (hi_texts[0], hi_texts[1], hi_texts[2], hi_texts[3], hi_texts[4], q[5], q[6])
        })

# 4. Map categories to pools and insert
categories = cursor.execute("SELECT id, name FROM category").fetchall()
print(f"Found {len(categories)} categories. Matching context and populating...")

total_inserted = 0
for cid, cname in categories:
    lname = cname.lower()
    
    # Context matching logic (using word boundaries to prevent 'it' matching 'competitive')
    import re
    def matches(keywords, text):
        return any(re.search(r'\b' + re.escape(k) + r'\b', text) for k in keywords)

    if matches(['science', 'math', 'tech', 'computer', 'bca', 'mca', 'it', 'biology', 'engineering', 'electrical', 'mechanical', 'b.sc', 'b.tech', 'be'], lname):
        pool = translated_pools['Science_Tech']
    elif matches(['commerce', 'bcom', 'b.com', 'mcom', 'm.com', 'business', 'bba', 'mba', 'account', 'accountancy'], lname):
        pool = translated_pools['Commerce_Business']
    elif matches(['arts', 'history', 'ba', 'b.a', 'ma', 'm.a', 'bed', 'b.ed', 'llb', 'literature'], lname):
        pool = translated_pools['Arts_Humanities']
    else:
        # Default to GK / Competitive / General School subjects
        pool = translated_pools['GK_Competitive']
        
    for item in pool:
        for lang in ['en', 'gu', 'hi']:
            q = item[lang]
            cursor.execute("INSERT INTO question (category_id, text, option_a, option_b, option_c, option_d, correct_option, difficulty, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (cid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], lang))
            total_inserted += 1

conn.commit()
conn.close()

print(f"Done! Inserted {total_inserted} highly contextual questions across all categories.")
