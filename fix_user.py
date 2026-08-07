import os

models_path = r"d:\project\qgame\qgame\models.py"
with open(models_path, "r", encoding="utf-8") as f:
    code = f.read()

old_fields = """    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    college = db.Column(db.String(150), nullable=True)"""

new_fields = """    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    college = db.Column(db.String(150), nullable=True)"""

code = code.replace(old_fields, new_fields)

with open(models_path, "w", encoding="utf-8") as f:
    f.write(code)
