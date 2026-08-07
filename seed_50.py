import os
import sys
import random

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    print("Fetching all categories...")
    categories = Category.query.all()
    
    for cat in categories:
        current_count = Question.query.filter_by(category_id=cat.id).count()
        needed = 50 - current_count
        
        if needed > 0:
            for i in range(needed):
                q = Question(
                    category_id=cat.id,
                    text=f"Generated Question {current_count + i + 1} for {cat.name}. Which is correct?",
                    option_a=f"Option A for Q{current_count + i + 1}",
                    option_b=f"Option B for Q{current_count + i + 1}",
                    option_c=f"Option C for Q{current_count + i + 1}",
                    option_d=f"Option D for Q{current_count + i + 1}",
                    correct_option=random.choice(["A", "B", "C", "D"]),
                    difficulty=random.choice(["Easy", "Medium", "Hard"]),
                    language="en"
                )
                db.session.add(q)
            db.session.commit()
    
    print("Done! All categories now have 50 questions.")
