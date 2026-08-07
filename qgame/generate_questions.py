import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    # If the app recreated the db, we need to make sure we have a category
    python_cat = Category.query.filter_by(name='Python').first()
    if not python_cat:
        python_cat = Category(name='Python', description='Advanced Python Quiz')
        db.session.add(python_cat)
        db.session.commit()
        
    # Generate 50 questions
    print(f"Generating 50 questions for category: {python_cat.name}...")
    for i in range(1, 51):
        q = Question(
            category_id=python_cat.id,
            text=f'Sample Python Question {i}: What is the output of 2 + {i}?',
            option_a=f'{2 + i}',
            option_b=f'{3 + i}',
            option_c=f'{4 + i}',
            option_d='None of the above',
            correct_option='A',
            explanation='Basic arithmetic',
            difficulty='Medium',
            language='en'
        )
        db.session.add(q)
    db.session.commit()
    print("Successfully added 50 questions!")
