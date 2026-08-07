import os
import sys

base_dir = r"d:\project\qgame\qgame"
app_path = os.path.join(base_dir, "app.py")
models_path = os.path.join(base_dir, "models.py")

# 1. Update models.py to add filtering fields to Category
with open(models_path, "r", encoding="utf-8") as f:
    models_code = f.read()

if "education_level = db.Column(db.String" not in models_code.split("class Category(db.Model):")[1]:
    # Need to add fields to Category
    new_cat_fields = """
    education_level = db.Column(db.String(50), nullable=True)
    board = db.Column(db.String(50), nullable=True)
    standard = db.Column(db.String(50), nullable=True)
    course = db.Column(db.String(50), nullable=True)
"""
    models_code = models_code.replace("description = db.Column(db.Text, nullable=True)", "description = db.Column(db.Text, nullable=True)" + new_cat_fields)
    with open(models_path, "w", encoding="utf-8") as f:
        f.write(models_code)

# 2. Update app.py dashboard route
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

import re

def replace_dashboard_function(code):
    lines = code.split('\n')
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if line.startswith("@app.route('/dashboard')"):
            start_idx = i
            break
            
    if start_idx != -1:
        for i in range(start_idx + 2, len(lines)):
            if lines[i].startswith("@app.route"):
                end_idx = i
                break
                
        if end_idx != -1:
            new_dash = '''@app.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    # Dynamic Filtering based on User Profile
    query = Category.query
    if current_user.education_level == 'School':
        query = query.filter_by(education_level='School', standard=current_user.semester)
    elif current_user.education_level in ['Graduation', 'Diploma', 'Post Graduation']:
        query = query.filter_by(education_level=current_user.education_level, course=current_user.department)
    elif current_user.education_level == 'Competitive Exam':
        query = query.filter_by(education_level='Competitive Exam', course=current_user.department)
        
    categories = query.all()
    
    # If no specific categories found for their profile, show generic ones (where education_level is null)
    if not categories:
        categories = Category.query.filter_by(education_level=None).all()
        
    category_counts = {}
    for c in categories:
        category_counts[c.id] = Question.query.filter_by(category_id=c.id, language='en').count()
        
    user_quizzes = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.date.desc()).limit(5).all()
    user_inventory = [inv.store_item_id for inv in current_user.inventory]
    equipped_title = StoreItem.query.get(current_user.active_title_id) if current_user.active_title_id else None
    equipped_border = StoreItem.query.get(current_user.active_border_id) if current_user.active_border_id else None
    
    return render_template('user/dashboard.html', categories=categories, category_counts=category_counts, user_quizzes=user_quizzes, user=current_user, equipped_title=equipped_title, equipped_border=equipped_border)
'''
            new_lines = lines[:start_idx] + new_dash.split('\n') + lines[end_idx:]
            return '\n'.join(new_lines)
    return code

updated_app = replace_dashboard_function(app_code)
with open(app_path, "w", encoding="utf-8") as f:
    f.write(updated_app)

print("Dashboard dynamic filtering added!")
