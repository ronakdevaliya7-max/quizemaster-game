import os

models_path = r"d:\project\qgame\qgame\models.py"
with open(models_path, "r", encoding="utf-8") as f:
    code = f.read()

old_init = """    def __init__(self, name, description=None, image_filename=None):
        self.name = name
        self.description = description
        self.image_filename = image_filename"""

new_init = """    def __init__(self, name, description=None, image_filename=None, education_level=None, board=None, standard=None, course=None):
        self.name = name
        self.description = description
        self.image_filename = image_filename
        self.education_level = education_level
        self.board = board
        self.standard = standard
        self.course = course"""

code = code.replace(old_init, new_init)

with open(models_path, "w", encoding="utf-8") as f:
    f.write(code)
