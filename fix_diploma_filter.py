import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
from qgame.app import app, db
from qgame.models import Category, Question, User

app_path = os.path.join(base_dir, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

old_dash = """    elif current_user.education_level in ['Graduation', 'Diploma', 'Post Graduation']:
        query = query.filter_by(education_level=current_user.education_level, course=current_user.course)"""

new_dash = """    elif current_user.education_level in ['Graduation', 'Diploma', 'Post Graduation']:
        query = query.filter_by(education_level=current_user.education_level, course=current_user.course)
        if current_user.semester and current_user.semester != 'None':
            query = query.filter_by(standard=current_user.semester)"""

code = code.replace(old_dash, new_dash)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Diploma/Grad filter fixed to include semester.")
