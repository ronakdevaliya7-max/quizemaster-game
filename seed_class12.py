import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    subjects = [
        ("Physics", "Class 12 GSEB Physics", "School", "GSEB", "12", "Science"),
        ("Chemistry", "Class 12 GSEB Chemistry", "School", "GSEB", "12", "Science"),
        ("Mathematics", "Class 12 GSEB Mathematics", "School", "GSEB", "12", "Science"),
        ("Biology", "Class 12 GSEB Biology", "School", "GSEB", "12", "Science"),
        ("Accountancy", "Class 12 GSEB Accountancy", "School", "GSEB", "12", "Commerce"),
        ("Economics", "Class 12 GSEB Economics", "School", "GSEB", "12", "Commerce"),
        ("Business Studies", "Class 12 GSEB BA", "School", "GSEB", "12", "Commerce"),
    ]
    
    print("Seeding subjects for Class 12 GSEB...")
    for name, desc, ed_level, board, std, stream in subjects:
        cat = Category.query.filter_by(name=name, education_level=ed_level, board=board, standard=std).first()
        if not cat:
            cat = Category(name=name, description=desc, education_level=ed_level, board=board, standard=std, course=None)
            db.session.add(cat)
            db.session.commit()
            
            for i in range(5):
                q = Question(
                    category_id=cat.id,
                    text=f"Sample Question {i+1} for Class 12 {name}",
                    option_a="A", option_b="B", option_c="C", option_d="D",
                    correct_option="A", difficulty="Easy", language="en"
                )
                db.session.add(q)
            db.session.commit()
            print(f"Added {name}!")

print("Seeding complete for Class 12.")
