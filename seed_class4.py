

import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    # Make sure we have the required schema updates
    try:
        db.create_all()
    except:
        pass
        
    subjects = [
        ("Mathematics", "Class 4 CBSE Mathematics", "School", "CBSE", "4", None),
        ("Science", "Class 4 CBSE Science", "School", "CBSE", "4", None),
        ("English", "Class 4 CBSE English", "School", "CBSE", "4", None),
        ("Hindi", "Class 4 CBSE Hindi", "School", "CBSE", "4", None),
        ("Social Studies", "Class 4 CBSE Social Studies", "School", "CBSE", "4", None),
        ("Python Programming", "BCA Semester 5 Python", "Graduation", None, None, "BCA"),
        ("Java Programming", "BCA Semester 5 Java", "Graduation", None, None, "BCA"),
    ]
    
    print("Seeding subjects for Class 4 and BCA...")
    for name, desc, ed_level, board, std, course in subjects:
        cat = Category.query.filter_by(name=name, education_level=ed_level).first()
        if not cat:
            cat = Category(name=name, description=desc, education_level=ed_level, board=board, standard=std, course=course)
            db.session.add(cat)
            db.session.commit()
            
            # Add a couple of questions so it doesn't show 0 Qs
            for i in range(5):
                q = Question(
                    category_id=cat.id,
                    text=f"Sample Question {i+1} for {name}",
                    option_a="A", option_b="B", option_c="C", option_d="D",
                    correct_option="A", difficulty="Easy", language="en"
                )
                db.session.add(q)
            db.session.commit()
            print(f"Added {name}!")

print("Seeding complete.")
