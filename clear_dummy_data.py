import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from qgame.app import app, db
from qgame.models import Question, Category

with app.app_context():
    print("Deleting all dummy questions...")
    num_questions = Question.query.delete()
    print(f"Deleted {num_questions} questions.")
    
    print("Deleting all dummy categories...")
    num_categories = Category.query.delete()
    print(f"Deleted {num_categories} categories.")
    
    db.session.commit()
    print("Database successfully cleared!")
