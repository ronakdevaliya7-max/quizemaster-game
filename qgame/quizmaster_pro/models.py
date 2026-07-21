from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    
    # Profile Info
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    college = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(150), nullable=True)
    semester = db.Column(db.String(50), nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True, default='default.png')
    
    # Gamification
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    points = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    active_title_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=True)
    active_border_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=True)
    
    # Relationships
    attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)
    inventory = db.relationship('UserInventory', backref='user', lazy=True)
    
    active_title = db.relationship('StoreItem', foreign_keys=[active_title_id])
    active_border = db.relationship('StoreItem', foreign_keys=[active_border_id])

    def __init__(self, username, name, password_hash, role='user', age=None, gender=None, college=None, department=None, semester=None, profile_photo='default.png', xp=0, level=1, points=0, coins=0):
        self.username = username
        self.name = name
        self.password_hash = password_hash
        self.role = role
        self.age = age
        self.gender = gender
        self.college = college
        self.department = department
        self.semester = semester
        self.profile_photo = profile_photo
        self.xp = xp
        self.level = level
        self.points = points
        self.coins = coins

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    
    questions = db.relationship('Question', backref='category', lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship('QuizAttempt', backref='category', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, description=None, image_filename=None):
        self.name = name
        self.description = description
        self.image_filename = image_filename

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), default='Easy') # 'Easy', 'Medium', 'Hard'
    language = db.Column(db.String(10), default='en') # 'en', 'gu', 'hi'

    def __init__(self, category_id, text, option_a, option_b, option_c, option_d, correct_option, explanation=None, difficulty='Easy', language='en'):
        self.category_id = category_id
        self.text = text
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_option = correct_option
        self.explanation = explanation
        self.difficulty = difficulty
        self.language = language

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False) # In seconds
    date = db.Column(db.DateTime, default=datetime.utcnow)
    passed = db.Column(db.Boolean, default=False)
    
    certificate = db.relationship('Certificate', backref='attempt', uselist=False)

    def __init__(self, user_id, category_id, score, total_questions, time_taken, passed=False, date=None):
        self.user_id = user_id
        self.category_id = category_id
        self.score = score
        self.total_questions = total_questions
        self.time_taken = time_taken
        self.passed = passed
        if date:
            self.date = date
        else:
            self.date = datetime.utcnow()

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    certificate_id = db.Column(db.String(100), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, attempt_id, certificate_id, file_path, issue_date=None):
        self.user_id = user_id
        self.attempt_id = attempt_id
        self.certificate_id = certificate_id
        self.file_path = file_path
        if issue_date:
            self.issue_date = issue_date
        else:
            self.issue_date = datetime.utcnow()

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon_path = db.Column(db.String(255), nullable=False, default='default_badge.png')
    requirement_type = db.Column(db.String(50), nullable=False) # 'first_quiz', 'perfect_score', 'points', 'quizzes_completed'
    requirement_value = db.Column(db.Integer, nullable=False) # Example: 100 (for points) or 1 (for first quiz)

    def __init__(self, name, description, requirement_type, requirement_value, icon_path='default_badge.png'):
        self.name = name
        self.description = description
        self.requirement_type = requirement_type
        self.requirement_value = requirement_value
        self.icon_path = icon_path

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, badge_id, date_earned=None):
        self.user_id = user_id
        self.badge_id = badge_id
        if date_earned:
            self.date_earned = date_earned
        else:
            self.date_earned = datetime.utcnow()

class StoreItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(50), nullable=False) # 'title' or 'border'
    css_class = db.Column(db.String(255), nullable=True) 
    icon = db.Column(db.String(50), nullable=True) 

    def __init__(self, name, description, cost, item_type, css_class=None, icon=None):
        self.name = name
        self.description = description
        self.cost = cost
        self.item_type = item_type
        self.css_class = css_class
        self.icon = icon

class UserInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_item_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=False)
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    store_item = db.relationship('StoreItem')

    def __init__(self, user_id, store_item_id, acquired_at=None):
        self.user_id = user_id
        self.store_item_id = store_item_id
        if acquired_at:
            self.acquired_at = acquired_at
        else:
            self.acquired_at = datetime.utcnow()

