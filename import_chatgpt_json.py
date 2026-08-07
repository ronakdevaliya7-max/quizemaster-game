import os
import sys
import json

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from qgame.app import app, db
from qgame.models import Question, Category

def import_questions(json_file_path, category_name):
    with app.app_context():
        # Ensure category exists
        cat = Category.query.filter_by(name=category_name).first()
        if not cat:
            print(f"Creating new category: {category_name}")
            cat = Category(name=category_name, description=f"Imported from JSON")
            db.session.add(cat)
            db.session.commit()
            
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            count = 0
            for item in data:
                # Map ChatGPT keys if they used different ones, but we requested specific ones.
                q_text = item.get('question', item.get('text', ''))
                opt_a = item.get('option_a', item.get('A', ''))
                opt_b = item.get('option_b', item.get('B', ''))
                opt_c = item.get('option_c', item.get('C', ''))
                opt_d = item.get('option_d', item.get('D', ''))
                correct = item.get('correct_option', item.get('correct', 'A'))
                diff = item.get('difficulty', 'Medium')
                
                # Basic validation
                if not q_text or not opt_a:
                    continue
                    
                q = Question(
                    category_id=cat.id,
                    text=q_text,
                    option_a=opt_a,
                    option_b=opt_b,
                    option_c=opt_c,
                    option_d=opt_d,
                    correct_option=correct,
                    difficulty=diff,
                    language='en'  # Default, can be adjusted
                )
                db.session.add(q)
                count += 1
                
            db.session.commit()
            print(f"Successfully imported {count} questions into '{category_name}'.")
            
        except Exception as e:
            print(f"Error reading JSON: {e}")

if __name__ == "__main__":
    # Example usage: python import_chatgpt_json.py data.json "GSEB Class 10 Science"
    if len(sys.argv) < 3:
        print("Usage: python import_chatgpt_json.py <path_to_json_file> <category_name>")
    else:
        import_questions(sys.argv[1], sys.argv[2])
