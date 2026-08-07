import os
import re

base_dir = r"d:\project\qgame\qgame"
models_path = os.path.join(base_dir, "models.py")
app_path = os.path.join(base_dir, "app.py")

# ==========================================
# 1. FIX MODELS.PY
# ==========================================
with open(models_path, "r", encoding="utf-8") as f:
    models_code = f.read()

# Make sure all education fields are on User
user_fields_to_add = """
    board = db.Column(db.String(50), nullable=True)
    standard = db.Column(db.String(50), nullable=True)
    stream = db.Column(db.String(50), nullable=True)
    course = db.Column(db.String(100), nullable=True)
    exam = db.Column(db.String(100), nullable=True)
"""
if "board = db.Column" not in models_code:
    models_code = models_code.replace("education_level = db.Column(db.String(50), nullable=True)", 
                                      "education_level = db.Column(db.String(50), nullable=True)" + user_fields_to_add)

with open(models_path, "w", encoding="utf-8") as f:
    f.write(models_code)

# ==========================================
# 2. FIX APP.PY (Register & Dashboard)
# ==========================================
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Fix Register
def fix_register(code):
    start_idx = -1
    end_idx = -1
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("@app.route('/register'"):
            start_idx = i
            break
    if start_idx != -1:
        for i in range(start_idx + 2, len(lines)):
            if lines[i].startswith("@app.route"):
                end_idx = i
                break
        if end_idx != -1:
            new_reg = '''@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password, name=name, role='user')
        
        try:
            new_user.email = request.form.get('email')
            new_user.mobile = request.form.get('mobile')
            new_user.gender = request.form.get('gender')
            new_user.dob = request.form.get('dob')
            new_user.country = request.form.get('country')
            new_user.state = request.form.get('state')
            new_user.city = request.form.get('city')
            
            # Education Details
            ed_level = request.form.get('education_level')
            new_user.education_level = ed_level
            
            if ed_level == 'School':
                new_user.board = request.form.get('board')
                new_user.standard = request.form.get('standard')
                new_user.stream = request.form.get('stream')
            elif ed_level == 'Diploma':
                new_user.course = request.form.get('diploma_branch')
                new_user.semester = request.form.get('diploma_semester')
            elif ed_level == 'Graduation':
                new_user.college = request.form.get('university')
                new_user.course = request.form.get('grad_course')
                new_user.semester = request.form.get('grad_semester')
            elif ed_level == 'Post Graduation':
                new_user.course = request.form.get('pg_course')
                new_user.semester = request.form.get('pg_semester')
            elif ed_level == 'Competitive Exam':
                new_user.exam = request.form.get('exam')
                
        except Exception as e:
            print("DB field missing:", e)
            pass
            
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')
'''
            return '\n'.join(lines[:start_idx] + new_reg.split('\n') + lines[end_idx:])
    return code

# Fix Dashboard
def fix_dashboard(code):
    start_idx = -1
    end_idx = -1
    lines = code.split('\n')
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
        
    query = Category.query
    if current_user.education_level == 'School':
        query = query.filter_by(education_level='School', standard=current_user.standard, board=current_user.board)
    elif current_user.education_level in ['Graduation', 'Diploma', 'Post Graduation']:
        query = query.filter_by(education_level=current_user.education_level, course=current_user.course)
    elif current_user.education_level == 'Competitive Exam':
        query = query.filter_by(education_level='Competitive Exam', course=current_user.exam)
        
    categories = query.all()
    
    # If no subjects are specifically matched, don't show random ones! 
    # Just show empty list so they know their specific profile has no subjects yet.
    # We will seed the DB to ensure there ARE subjects.
        
    category_counts = {}
    for c in categories:
        category_counts[c.id] = Question.query.filter_by(category_id=c.id).count()
        
    user_quizzes = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.date.desc()).limit(5).all()
    user_inventory = [inv.store_item_id for inv in current_user.inventory]
    equipped_title = StoreItem.query.get(current_user.active_title_id) if current_user.active_title_id else None
    equipped_border = StoreItem.query.get(current_user.active_border_id) if current_user.active_border_id else None
    
    return render_template('user/dashboard.html', categories=categories, category_counts=category_counts, user_quizzes=user_quizzes, user=current_user, equipped_title=equipped_title, equipped_border=equipped_border)
'''
            return '\n'.join(lines[:start_idx] + new_dash.split('\n') + lines[end_idx:])
    return code

app_code = fix_register(app_code)
app_code = fix_dashboard(app_code)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)

print("Models, Register and Dashboard fixed perfectly!")
