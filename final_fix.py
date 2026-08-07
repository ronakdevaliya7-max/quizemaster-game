import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question, User

with app.app_context():
    # 1. Update app.py dashboard logic to use 'course' for stream
    app_path = os.path.join(base_dir, "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Fix dashboard query
    old_dash = """    if current_user.education_level == 'School':
        query = query.filter_by(education_level='School', standard=current_user.standard, board=current_user.board)
        if current_user.stream and current_user.stream != 'None' and current_user.stream != 'null':
            query = query.filter_by(stream=current_user.stream)"""
    
    new_dash = """    if current_user.education_level == 'School':
        query = query.filter_by(education_level='School', standard=current_user.standard, board=current_user.board)
        if current_user.stream and current_user.stream != 'None' and current_user.stream != 'null':
            query = query.filter_by(course=current_user.stream)"""
    
    code = code.replace(old_dash, new_dash)
    
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    print("app.py updated to use course for stream.")
    
    # 2. Add specific subjects for Class 11/12
    import random
    
    subjects_to_add = [
        # Commerce
        ("Accountancy", "Class 12 GSEB Commerce", "School", "GSEB", "12", "Commerce"),
        ("Economics", "Class 12 GSEB Commerce", "School", "GSEB", "12", "Commerce"),
        ("Business Administration", "Class 12 GSEB Commerce", "School", "GSEB", "12", "Commerce"),
        ("Statistics", "Class 12 GSEB Commerce", "School", "GSEB", "12", "Commerce"),
        # Arts
        ("History", "Class 12 GSEB Arts", "School", "GSEB", "12", "Arts"),
        ("Geography", "Class 12 GSEB Arts", "School", "GSEB", "12", "Arts"),
        ("Political Science", "Class 12 GSEB Arts", "School", "GSEB", "12", "Arts"),
        ("Psychology", "Class 12 GSEB Arts", "School", "GSEB", "12", "Arts"),
        ("Sociology", "Class 12 GSEB Arts", "School", "GSEB", "12", "Arts"),
    ]
    
    for name, desc, ed_level, board, std, stream in subjects_to_add:
        cat = Category.query.filter_by(name=name, education_level=ed_level, board=board, standard=std, course=stream).first()
        if not cat:
            cat = Category(name=name, description=desc, education_level=ed_level, board=board, standard=std, course=stream)
            db.session.add(cat)
            db.session.commit()
            
            for i in range(50):
                q = Question(
                    category_id=cat.id,
                    text=f"{name} Question {i+1}: What is the correct answer?",
                    option_a=f"{name} Ans A", option_b=f"{name} Ans B", option_c=f"{name} Ans C", option_d=f"{name} Ans D",
                    correct_option=random.choice(["A", "B", "C", "D"]), difficulty=random.choice(["Easy", "Medium", "Hard"]), language="en"
                )
                db.session.add(q)
            db.session.commit()
            print(f"Added {name} for {stream}!")

    print("Complete!")
