import os
import re

base_dir = r"d:\project\qgame\qgame"
models_path = os.path.join(base_dir, "models.py")
app_path = os.path.join(base_dir, "app.py")
register_path = os.path.join(base_dir, "templates", "register.html")

# 1. Update models.py
with open(models_path, "r", encoding="utf-8") as f:
    models_content = f.read()

# Add new models at the end
new_models = """

# --- NEW EDUCATION HIERARCHY ---
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Standard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=True)

class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    total_semesters = db.Column(db.Integer, nullable=False, default=1)

class CompetitiveExam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=True)
    standard_id = db.Column(db.Integer, db.ForeignKey('standard.id'), nullable=True)
    stream_id = db.Column(db.Integer, db.ForeignKey('stream.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('competitive_exam.id'), nullable=True)
    
    topics = db.relationship('Topic', backref='subject', lazy=True, cascade="all, delete-orphan")

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), default='Medium')
    
    questions = db.relationship('Question', backref='topic', lazy=True, cascade="all, delete-orphan")
"""

if "class Board" not in models_content:
    models_content += new_models

# Add new fields to User
if "education_level = db.Column" not in models_content:
    user_fields = """
    # Education Profile
    education_level = db.Column(db.String(50), nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=True)
    standard_id = db.Column(db.Integer, db.ForeignKey('standard.id'), nullable=True)
    stream_id = db.Column(db.Integer, db.ForeignKey('stream.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    semester_num = db.Column(db.Integer, nullable=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('competitive_exam.id'), nullable=True)
"""
    models_content = models_content.replace("semester = db.Column(db.String(50), nullable=True)", "semester = db.Column(db.String(50), nullable=True)\n" + user_fields)

# Update Question model to use topic_id instead of category_id
models_content = models_content.replace("category_id = db.Column(db.Integer, db.ForeignKey('category.id')", "topic_id = db.Column(db.Integer, db.ForeignKey('topic.id')")
models_content = models_content.replace("def __init__(self, category_id, text,", "def __init__(self, topic_id, text,")
models_content = models_content.replace("self.category_id = category_id", "self.topic_id = topic_id")

with open(models_path, "w", encoding="utf-8") as f:
    f.write(models_content)


print("Features injected!")
