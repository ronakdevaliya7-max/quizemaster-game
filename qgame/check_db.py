import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import app, db
from models import Question, Category

with app.app_context():
    print("Total Questions:", Question.query.count())
    print("Total Categories:", Category.query.count())
    
    # Check if there is a category ID 252 or 258 or 387
    for cid in [252, 258, 387]:
        c = Category.query.get(cid)
        if c:
            print(f"Category {cid} exists: {c.name}")
        else:
            print(f"Category {cid} does not exist.")
            
    print("All categories:")
    for c in Category.query.all():
        print(c.id, c.name, Question.query.filter_by(category_id=c.id).count())
