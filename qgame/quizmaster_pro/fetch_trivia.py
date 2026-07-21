import urllib.request
import json
import time
import html
import random
from app import app, db
from models import Category, Question

def get_questions(amount, category_id, retries=3):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category_id}&type=multiple"
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            if data['response_code'] == 0:
                return data['results']
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"Rate limited, waiting... (Attempt {i+1}/{retries})")
                time.sleep(6) # Wait out the rate limit
            else:
                print(f"Error fetching: {e}")
        except Exception as e:
            print(f"Error fetching: {e}")
    return []

def populate_real_data():
    category_map = {
        'Python': 18, # Computers
        'Technology': 18,
        'Mathematics': 19,
        'Geography': 22,
        'History': 23,
        'Science': 17, # Science & Nature
        'Sports': 21,
        'Art': 25,
        'Literature': 10, # Books
        'General Knowledge': 9
    }
    
    with app.app_context():
        # Clean existing questions to start fresh with real ones
        Question.query.delete()
        db.session.commit()
        
        categories = Category.query.all()
        
        for cat in categories:
            print(f"Fetching questions for {cat.name}...")
            tdb_id = category_map.get(cat.name, 9)
            
            # Fetch 50 questions
            results = get_questions(50, tdb_id)
            time.sleep(6) # Prevent rate limiting (OpenTDB limits to 1 per 5 seconds)
            
            if not results:
                # Try fallback general knowledge if failed
                results = get_questions(50, 9)
                time.sleep(6)
                
            for res in results:
                question_text = html.unescape(res['question'])
                correct = html.unescape(res['correct_answer'])
                incorrects = [html.unescape(ans) for ans in res['incorrect_answers']]
                
                options = incorrects + [correct]
                random.shuffle(options)
                
                correct_letter = chr(65 + options.index(correct)) # A, B, C, or D
                
                q = Question(
                    category_id=cat.id,
                    text=question_text,
                    option_a=options[0],
                    option_b=options[1],
                    option_c=options[2],
                    option_d=options[3],
                    correct_option=correct_letter,
                    difficulty=res['difficulty'].capitalize()
                )
                db.session.add(q)
            
            db.session.commit()
            print(f"Added {len(results)} questions for {cat.name}")

if __name__ == '__main__':
    populate_real_data()
