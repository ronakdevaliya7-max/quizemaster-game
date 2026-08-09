import os
import sys
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'qgame'))
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from qgame.app import app, db
from qgame.models import Question, Category

topics = [
    ("Ramayana", ['ramayana.json', 'ramayana_part2.json', 'ramayana_part3.json'], "Test your knowledge of the Ramayana epic, its characters, events, and teachings."),
    ("Mahabharata", ['mahabharata.json', 'mahabharata_part2.json', 'mahabharata_part3.json'], "Test your knowledge of the Mahabharata epic."),
    ("Hindu Gods", ['hindu_gods.json', 'hindu_gods_part2.json', 'hindu_gods_part3.json'], "Test your knowledge about Hindu Gods and Deities."),
    ("Indian History", ['indian_history.json', 'indian_history_part2.json', 'indian_history_part3.json'], "Test your knowledge of Indian History."),
    ("Indian Culture", ['indian_culture.json', 'indian_culture_part2.json', 'indian_culture_part3.json'], "Test your knowledge of Indian Culture and traditions.")
]

with app.app_context():
    total_added = 0
    for cat_name, file_names, desc in topics:
        questions = []
        for fn in file_names:
            data_file = os.path.join(base_dir, 'data', fn)
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    questions.extend(json.load(f))
                    
        if not questions:
            print(f"No questions found for {cat_name}.")
            continue
            
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, description=desc)
            db.session.add(cat)
            db.session.commit()
            print(f"Created category {cat_name}")
            
        added_count = 0
        for q_data in questions:
            # check if it has en/hi/gu keys
            if 'en' in q_data:
                existing = Question.query.filter_by(category_id=cat.id, text=q_data['en']['text']).first()
                if not existing:
                    for lang in ['en', 'hi', 'gu']:
                        if lang in q_data:
                            q = Question(
                                category_id=cat.id,
                                text=q_data[lang]['text'],
                                option_a=q_data[lang]['opt_a'],
                                option_b=q_data[lang]['opt_b'],
                                option_c=q_data[lang]['opt_c'],
                                option_d=q_data[lang]['opt_d'],
                                correct_option=q_data['correct_option'],
                                difficulty=q_data['difficulty'],
                                language=lang
                            )
                            db.session.add(q)
                    added_count += 3
            else:
                # maybe flat format
                q_text = q_data.get('question', q_data.get('text', ''))
                existing = Question.query.filter_by(category_id=cat.id, text=q_text).first()
                if not existing and q_text:
                    q = Question(
                        category_id=cat.id,
                        text=q_text,
                        option_a=q_data.get('option_a', q_data.get('A', '')),
                        option_b=q_data.get('option_b', q_data.get('B', '')),
                        option_c=q_data.get('option_c', q_data.get('C', '')),
                        option_d=q_data.get('option_d', q_data.get('D', '')),
                        correct_option=q_data.get('correct_option', q_data.get('correct', 'A')),
                        difficulty=q_data.get('difficulty', 'Medium'),
                        language='en'
                    )
                    db.session.add(q)
                    added_count += 1
        
        db.session.commit()
        print(f"Imported {added_count} questions for {cat_name}.")
        total_added += added_count
        
    print(f"Done! Total questions imported: {total_added}")
