import os
import sys
import random

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question

with app.app_context():
    print("Seeding specific realistic subjects for ALL school classes 1 to 12...")
    
    boards = ["GSEB", "CBSE"] # Let's stick to major ones to avoid blowing up DB too much, or we can just do it for all.
    
    # Classes 1 to 10 subjects
    general_subjects = ["Mathematics", "Science", "English", "Hindi", "Social Studies", "Gujarati"]
    
    # Class 11-12 Science subjects
    science_subjects = ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Computer Science"]
    
    # Class 11-12 Commerce subjects (some already added, but ensure completeness)
    commerce_subjects = ["Accountancy", "Economics", "Business Administration", "Statistics", "English", "Computer Science"]
    
    # Class 11-12 Arts subjects
    arts_subjects = ["History", "Geography", "Political Science", "Psychology", "Sociology", "English"]
    
    def seed_subjects(std_list, stream, subj_list):
        for board in boards:
            for std in std_list:
                for subj in subj_list:
                    if std >= 11:
                        name = f"{subj} ({stream}) - Class {std} {board}"
                    else:
                        name = f"{subj} - Class {std} {board}"
                    # Use course=stream because that's what we modified dashboard to filter by!
                    # For std 1-10, stream is "None" from the frontend, but let's check what register form sends.
                    # It sends "None" or "Science" etc.
                    actual_stream = stream if std >= 11 else "None"
                    
                    cat = Category.query.filter_by(name=name, education_level="School", board=board, standard=str(std), course=actual_stream).first()
                    if not cat:
                        cat = Category(
                            name=name, 
                            description=f"Standard {std} {board} {subj}", 
                            education_level="School", 
                            board=board, 
                            standard=str(std), 
                            course=actual_stream
                        )
                        db.session.add(cat)
                        db.session.commit()
                        
                        # Add 50 questions
                        for i in range(50):
                            q = Question(
                                category_id=cat.id,
                                text=f"{subj} Class {std} Q{i+1}: What is the correct answer?",
                                option_a="A", option_b="B", option_c="C", option_d="D",
                                correct_option=random.choice(["A", "B", "C", "D"]),
                                difficulty=random.choice(["Easy", "Medium", "Hard"]),
                                language="en"
                            )
                            db.session.add(q)
                        db.session.commit()
                        print(f"Added {name}")

    # Seed 1 to 10
    seed_subjects(range(1, 11), "None", general_subjects)
    
    # Seed 11 and 12
    seed_subjects([11, 12], "Science", science_subjects)
    seed_subjects([11, 12], "Commerce", commerce_subjects)
    seed_subjects([11, 12], "Arts", arts_subjects)
    
    print("Done seeding all school subjects!")
