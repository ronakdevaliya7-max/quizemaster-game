import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    print("Starting massive database seed for ALL combinations...")
    
    # 1. School
    boards = ["GSEB", "CBSE", "ICSE", "IB", "NIOS"]
    for board in boards:
        for std in range(1, 13):
            streams = ["None"] if std < 11 else ["Science", "Commerce", "Arts"]
            for stream in streams:
                subj_name = f"{board} Class {std} " + (stream if stream != "None" else "General") + " Subject"
                cat = Category.query.filter_by(name=subj_name).first()
                if not cat:
                    cat = Category(
                        name=subj_name, 
                        description=f"Automated quizzes for {subj_name}",
                        education_level="School",
                        board=board,
                        standard=str(std),
                        course=None
                    )
                    db.session.add(cat)
                    db.session.commit()
                    
                    # Add 5 questions
                    for i in range(5):
                        q = Question(
                            category_id=cat.id,
                            text=f"Question {i+1} for {subj_name}: What is the correct answer?",
                            option_a="Correct Option", option_b="Wrong Option 1", option_c="Wrong Option 2", option_d="Wrong Option 3",
                            correct_option="A", difficulty="Medium", language="en"
                        )
                        db.session.add(q)
                    db.session.commit()

    # 2. Diploma
    branches = ["Computer Engineering", "Mechanical", "Civil", "Electrical", "Automobile", "IT", "Electronics"]
    for branch in branches:
        for sem in range(1, 7):
            subj_name = f"Diploma {branch} Sem {sem}"
            cat = Category.query.filter_by(name=subj_name).first()
            if not cat:
                cat = Category(
                    name=subj_name, 
                    description=f"Automated quizzes for {subj_name}",
                    education_level="Diploma",
                    board=None,
                    standard=str(sem),
                    course=branch
                )
                db.session.add(cat)
                db.session.commit()
                for i in range(5):
                    q = Question(category_id=cat.id, text=f"Q{i+1} for {subj_name}", option_a="A", option_b="B", option_c="C", option_d="D", correct_option="A")
                    db.session.add(q)
                db.session.commit()

    # 3. Graduation
    courses = ["BCA", "BBA", "B.Com", "BA", "B.Sc", "B.Tech", "BE", "B.Ed", "LLB"]
    for course in courses:
        for sem in range(1, 9):
            subj_name = f"Graduation {course} Sem {sem}"
            cat = Category.query.filter_by(name=subj_name).first()
            if not cat:
                cat = Category(
                    name=subj_name, description=f"Automated quizzes for {subj_name}",
                    education_level="Graduation", course=course, standard=str(sem)
                )
                db.session.add(cat)
                db.session.commit()
                for i in range(5):
                    db.session.add(Question(category_id=cat.id, text=f"Q{i+1} for {subj_name}", option_a="A", option_b="B", option_c="C", option_d="D", correct_option="A"))
                db.session.commit()

    # 4. Post Graduation
    pg_courses = ["MCA", "MBA", "M.Com", "M.Sc", "MA", "ME", "M.Tech"]
    for course in pg_courses:
        for sem in range(1, 5):
            subj_name = f"PG {course} Sem {sem}"
            cat = Category.query.filter_by(name=subj_name).first()
            if not cat:
                cat = Category(name=subj_name, education_level="Post Graduation", course=course, standard=str(sem))
                db.session.add(cat)
                db.session.commit()
                for i in range(5):
                    db.session.add(Question(category_id=cat.id, text=f"Q{i+1} for {subj_name}", option_a="A", option_b="B", option_c="C", option_d="D", correct_option="A"))
                db.session.commit()

    # 5. Competitive Exams
    exams = ["UPSC", "GPSC", "SSC", "RRB", "Banking", "Police", "Forest", "Army", "Air Force", "Navy", "NEET", "JEE", "GUJCET", "CAT", "CLAT", "GATE", "Other"]
    for exam in exams:
        subj_name = f"{exam} Mock Test"
        cat = Category.query.filter_by(name=subj_name).first()
        if not cat:
            cat = Category(name=subj_name, education_level="Competitive Exam", course=exam)
            db.session.add(cat)
            db.session.commit()
            for i in range(5):
                db.session.add(Question(category_id=cat.id, text=f"Q{i+1} for {subj_name}", option_a="A", option_b="B", option_c="C", option_d="D", correct_option="A"))
            db.session.commit()

    print("Successfully seeded thousands of categories and questions for all possible form combinations!")
