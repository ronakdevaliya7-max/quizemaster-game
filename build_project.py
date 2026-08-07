import os

base_dir = r"d:\project\qgame\qgame"
templates_dir = os.path.join(base_dir, "templates")
user_templates = os.path.join(templates_dir, "user")
auth_templates = templates_dir
static_css = os.path.join(base_dir, "static", "css")

os.makedirs(user_templates, exist_ok=True)
os.makedirs(static_css, exist_ok=True)

# 1. NEW APP.PY
app_py_content = """import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from qgame.models import db, User, Board, Standard, Stream, Course, CompetitiveExam, Subject, Topic, Question, QuizAttempt, Certificate, Badge, UserBadge
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart_edu_quiz_secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quizmaster.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        education_level = request.form.get('education_level')
        
        # In a real app we'd validate and check existing
        user = User(
            username=username,
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            education_level=education_level
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def user_dashboard():
    # Dynamic Subjects based on user profile
    query = Subject.query
    if current_user.education_level == 'School':
        query = query.filter_by(board_id=current_user.board_id, standard_id=current_user.standard_id)
    elif current_user.education_level == 'Graduation':
        query = query.filter_by(course_id=current_user.course_id, semester=current_user.semester)
        
    subjects = query.all()
    # Fallback to all if empty for testing
    if not subjects:
        subjects = Subject.query.all()
        
    return render_template('user/dashboard.html', subjects=subjects, user=current_user)

@app.route('/subject/<int:subject_id>')
@login_required
def subject_view(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    topics = Topic.query.filter_by(subject_id=subject.id).all()
    return render_template('user/subject.html', subject=subject, topics=topics)

@app.route('/topic/<int:topic_id>')
@login_required
def topic_view(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    questions_count = Question.query.filter_by(topic_id=topic.id).count()
    return render_template('user/topic.html', topic=topic, questions_count=questions_count)

@app.route('/quiz/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if request.method == 'POST':
        # Submit Quiz
        score = 0
        total = 0
        questions = Question.query.filter_by(topic_id=topic.id).all()
        for q in questions:
            total += 1
            if request.form.get(f'q_{q.id}') == q.correct_option:
                score += 1
                
        attempt = QuizAttempt(user_id=current_user.id, topic_id=topic.id, score=score, total_questions=total, time_taken=0)
        db.session.add(attempt)
        db.session.commit()
        return redirect(url_for('quiz_result', attempt_id=attempt.id))
        
    questions = Question.query.filter_by(topic_id=topic.id).all()
    return render_template('user/quiz.html', topic=topic, questions=questions)

@app.route('/result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    return render_template('user/result.html', attempt=attempt)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    return render_template('admin/dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
"""

with open(os.path.join(base_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_py_content)

# 2. SEED DATA SCRIPT
seed_py_content = """import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from qgame.app import app, db
from qgame.models import User, Subject, Topic, Question, Board, Standard
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create Admin
    admin = User(username='admin', name='Admin', email='admin@edu.com', password_hash=generate_password_hash('admin123'), role='admin')
    db.session.add(admin)
    
    # Create User
    student = User(username='student1', name='John Doe', email='stu@edu.com', password_hash=generate_password_hash('password'), education_level='School')
    db.session.add(student)
    
    # Create Board and Standard
    gseb = Board(name='GSEB')
    cbse = Board(name='CBSE')
    db.session.add_all([gseb, cbse])
    db.session.commit()
    
    std10 = Standard(name='10', board_id=gseb.id)
    db.session.add(std10)
    db.session.commit()
    
    student.board_id = gseb.id
    student.standard_id = std10.id
    
    # Create Subjects
    maths = Subject(name='Mathematics', description='Advanced Math', board_id=gseb.id, standard_id=std10.id)
    science = Subject(name='Science', description='Physics, Chemistry, Bio', board_id=gseb.id, standard_id=std10.id)
    db.session.add_all([maths, science])
    db.session.commit()
    
    # Create Topics
    algebra = Topic(subject_id=maths.id, name='Algebra', difficulty='Medium')
    physics = Topic(subject_id=science.id, name='Physics', difficulty='Hard')
    db.session.add_all([algebra, physics])
    db.session.commit()
    
    # Create Questions
    q1 = Question(topic_id=algebra.id, text='What is 2+2?', option_a='3', option_b='4', option_c='5', option_d='6', correct_option='B')
    q2 = Question(topic_id=physics.id, text='What is speed of light?', option_a='3x10^8', option_b='2x10^8', option_c='4x10^8', option_d='None', correct_option='A')
    db.session.add_all([q1, q2])
    db.session.commit()
    
    print("Database Seeded Successfully!")
"""
with open(os.path.join(base_dir, "seed_new.py"), "w", encoding="utf-8") as f:
    f.write(seed_py_content)

# 3. BASE HTML TEMPLATE
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Education Quiz Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #FFD700; --secondary: #FFC107; --bg-light: #f8f9fa; }
        body { background-color: var(--bg-light); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; transition: background 0.3s; }
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .glass-card:hover { transform: translateY(-5px); }
        .btn-premium { background-color: var(--primary); color: #000; font-weight: bold; border-radius: 25px; padding: 10px 25px; border: none; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4); }
        .btn-premium:hover { background-color: var(--secondary); color: #000; }
        .navbar-custom { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light navbar-custom sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/"><i class="fas fa-graduation-cap text-warning"></i> SmartEdu</a>
            <div class="d-flex">
                {% if current_user.is_authenticated %}
                    <span class="navbar-text me-3 fw-bold">Level {{ current_user.level }} | <i class="fas fa-coins text-warning"></i> {{ current_user.coins }}</span>
                    <a href="/logout" class="btn btn-outline-danger btn-sm rounded-pill">Logout</a>
                {% else %}
                    <a href="/login" class="btn btn-outline-dark btn-sm rounded-pill me-2">Login</a>
                    <a href="/register" class="btn btn-premium btn-sm">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info alert-dismissible fade show rounded-3" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open(os.path.join(templates_dir, "base.html"), "w", encoding="utf-8") as f:
    f.write(base_html)

# 4. DASHBOARD HTML
dashboard_html = """{% extends 'base.html' %}
{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <h2 class="fw-bold">Welcome back, {{ user.name }}! 👋</h2>
        <p class="text-muted">Education Profile: {{ user.education_level }}</p>
    </div>
</div>
<div class="row">
    <div class="col-12 mb-3"><h4 class="fw-bold"><i class="fas fa-book text-primary"></i> Your Subjects</h4></div>
    {% for subject in subjects %}
    <div class="col-md-4 mb-4">
        <div class="card glass-card h-100 p-3">
            <div class="card-body text-center">
                <i class="fas fa-laptop-code fa-3x text-warning mb-3"></i>
                <h4 class="card-title fw-bold">{{ subject.name }}</h4>
                <p class="text-muted">{{ subject.description }}</p>
                <div class="progress mb-3" style="height: 10px; border-radius: 5px;">
                    <div class="progress-bar bg-warning" style="width: 30%"></div>
                </div>
                <a href="/subject/{{ subject.id }}" class="btn btn-premium w-100">Start Learning</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
with open(os.path.join(user_templates, "dashboard.html"), "w", encoding="utf-8") as f:
    f.write(dashboard_html)

# 5. SUBJECT & TOPIC & QUIZ HTML
subject_html = """{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">{{ subject.name }} Topics</h2>
<div class="row">
    {% for topic in topics %}
    <div class="col-md-6 mb-4">
        <div class="card glass-card p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="fw-bold mb-1">{{ topic.name }}</h5>
                    <span class="badge bg-{{ 'success' if topic.difficulty == 'Easy' else 'warning' if topic.difficulty == 'Medium' else 'danger' }}">{{ topic.difficulty }}</span>
                </div>
                <a href="/topic/{{ topic.id }}" class="btn btn-outline-dark rounded-pill">View Topic</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""
with open(os.path.join(user_templates, "subject.html"), "w", encoding="utf-8") as f:
    f.write(subject_html)

topic_html = """{% extends 'base.html' %}
{% block content %}
<div class="card glass-card p-5 text-center">
    <h2 class="fw-bold">{{ topic.name }}</h2>
    <p class="text-muted mb-4">Difficulty: {{ topic.difficulty }} | Questions: {{ questions_count }}</p>
    <a href="/quiz/{{ topic.id }}" class="btn btn-premium btn-lg"><i class="fas fa-play"></i> Start Quiz</a>
</div>
{% endblock %}
"""
with open(os.path.join(user_templates, "topic.html"), "w", encoding="utf-8") as f:
    f.write(topic_html)

quiz_html = """{% extends 'base.html' %}
{% block content %}
<div class="card glass-card p-4">
    <div class="d-flex justify-content-between mb-4">
        <h4 class="fw-bold">{{ topic.name }} Quiz</h4>
        <div class="fs-4 fw-bold text-danger"><i class="fas fa-clock"></i> <span id="timer">30</span>s</div>
    </div>
    <form method="POST">
        {% for q in questions %}
        <div class="mb-5 question-block" id="qblock_{{ loop.index }}" style="{% if not loop.first %}display:none;{% endif %}">
            <h5 class="fw-bold mb-3">{{ loop.index }}. {{ q.text }}</h5>
            <div class="row g-3">
                {% for opt, val in [('A', q.option_a), ('B', q.option_b), ('C', q.option_c), ('D', q.option_d)] %}
                <div class="col-md-6">
                    <label class="btn btn-outline-dark w-100 text-start p-3 rounded-3" style="cursor:pointer">
                        <input type="radio" name="q_{{ q.id }}" value="{{ opt }}" class="me-2"> {{ val }}
                    </label>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        <button type="submit" class="btn btn-premium w-100">Submit Quiz</button>
    </form>
</div>
{% endblock %}
"""
with open(os.path.join(user_templates, "quiz.html"), "w", encoding="utf-8") as f:
    f.write(quiz_html)

result_html = """{% extends 'base.html' %}
{% block content %}
<div class="card glass-card p-5 text-center">
    <h1 class="display-1 text-warning mb-3"><i class="fas fa-trophy"></i></h1>
    <h2 class="fw-bold mb-3">Quiz Completed!</h2>
    <h4 class="mb-4">Score: {{ attempt.score }} / {{ attempt.total_questions }}</h4>
    <a href="/dashboard" class="btn btn-premium">Back to Dashboard</a>
</div>
{% endblock %}
"""
with open(os.path.join(user_templates, "result.html"), "w", encoding="utf-8") as f:
    f.write(result_html)

# 6. LOGIN / REGISTER HTML
login_html = """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card glass-card p-4 mt-5">
            <h3 class="fw-bold text-center mb-4">Welcome Back</h3>
            <form method="POST">
                <div class="mb-3">
                    <label>Username</label>
                    <input type="text" name="username" class="form-control rounded-pill" required>
                </div>
                <div class="mb-4">
                    <label>Password</label>
                    <input type="password" name="password" class="form-control rounded-pill" required>
                </div>
                <button type="submit" class="btn btn-premium w-100 mb-3">Login</button>
                <div class="text-center">
                    <a href="/register" class="text-dark">Create new account</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(auth_templates, "login.html"), "w", encoding="utf-8") as f:
    f.write(login_html)

register_html = """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-7">
        <div class="card glass-card p-4 mt-3">
            <h3 class="fw-bold text-center mb-4">Create Account</h3>
            <form method="POST">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label>Full Name</label>
                        <input type="text" name="name" class="form-control rounded-pill" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Username</label>
                        <input type="text" name="username" class="form-control rounded-pill" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Email</label>
                        <input type="email" name="email" class="form-control rounded-pill" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Password</label>
                        <input type="password" name="password" class="form-control rounded-pill" required>
                    </div>
                    <div class="col-md-12 mb-3">
                        <label>Education Level</label>
                        <select name="education_level" class="form-select rounded-pill">
                            <option value="School">School</option>
                            <option value="Diploma">Diploma</option>
                            <option value="Graduation">Graduation</option>
                            <option value="Competitive Exam">Competitive Exam</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn btn-premium w-100 mt-3">Register</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(auth_templates, "register.html"), "w", encoding="utf-8") as f:
    f.write(register_html)

print("Scaffolding Complete!")
