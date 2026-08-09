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
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    
    # Educational Profile Fields
    education_level = db.Column(db.String(50), nullable=True)
    board = db.Column(db.String(50), nullable=True)
    standard = db.Column(db.String(50), nullable=True)
    stream = db.Column(db.String(50), nullable=True)
    course = db.Column(db.String(100), nullable=True)
    exam = db.Column(db.String(100), nullable=True)
    
    college = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(150), nullable=True)
    semester = db.Column(db.String(50), nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True, default='default.png')
    
    # Gamification
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    points = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    
    # Preferences
    language = db.Column(db.String(10), default='en')
    
    active_title_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=True)
    active_border_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=True)
    
    # Relationships
    attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)
    inventory = db.relationship('UserInventory', backref='user', lazy=True)
    
    active_title = db.relationship('StoreItem', foreign_keys=[active_title_id])
    active_border = db.relationship('StoreItem', foreign_keys=[active_border_id])

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    education_level = db.Column(db.String(50), nullable=True, index=True)
    board = db.Column(db.String(50), nullable=True, index=True)
    standard = db.Column(db.String(50), nullable=True, index=True)
    course = db.Column(db.String(50), nullable=True, index=True)

    image_filename = db.Column(db.String(255), nullable=True)
    
    questions = db.relationship('Question', backref='category', lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship('QuizAttempt', backref='category', lazy=True, cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True, index=True) # Optional now, for backward compatibility or special topics
    
    # Hierarchy Fields
    board = db.Column(db.String(50), nullable=True)
    standard = db.Column(db.String(50), nullable=True)
    stream = db.Column(db.String(50), nullable=True)
    subject = db.Column(db.String(100), nullable=True)
    chapter = db.Column(db.String(100), nullable=True)
    topic = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), default='Medium')
    
    # Multilingual Questions
    question_en = db.Column(db.Text, nullable=True)
    question_gu = db.Column(db.Text, nullable=True)
    question_hi = db.Column(db.Text, nullable=True)
    
    # Multilingual Options
    option_a_en = db.Column(db.String(255), nullable=True)
    option_b_en = db.Column(db.String(255), nullable=True)
    option_c_en = db.Column(db.String(255), nullable=True)
    option_d_en = db.Column(db.String(255), nullable=True)
    
    option_a_gu = db.Column(db.String(255), nullable=True)
    option_b_gu = db.Column(db.String(255), nullable=True)
    option_c_gu = db.Column(db.String(255), nullable=True)
    option_d_gu = db.Column(db.String(255), nullable=True)
    
    option_a_hi = db.Column(db.String(255), nullable=True)
    option_b_hi = db.Column(db.String(255), nullable=True)
    option_c_hi = db.Column(db.String(255), nullable=True)
    option_d_hi = db.Column(db.String(255), nullable=True)
    
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', or 'D'
    
    # Multilingual Explanations
    explanation_en = db.Column(db.Text, nullable=True)
    explanation_gu = db.Column(db.Text, nullable=True)
    explanation_hi = db.Column(db.Text, nullable=True)
    
    # Meta fields
    source = db.Column(db.String(255), nullable=True)
    source_type = db.Column(db.String(100), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Old legacy fields (for backward compatibility during migration)
    text = db.Column(db.Text, nullable=True)
    option_a = db.Column(db.String(255), nullable=True)
    option_b = db.Column(db.String(255), nullable=True)
    option_c = db.Column(db.String(255), nullable=True)
    option_d = db.Column(db.String(255), nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(10), default='en', index=True)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False) # In seconds
    date = db.Column(db.DateTime, default=datetime.utcnow)
    passed = db.Column(db.Boolean, default=False)
    
    certificate = db.relationship('Certificate', backref='attempt', uselist=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False, index=True)
    certificate_id = db.Column(db.String(100), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255), nullable=False)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon_path = db.Column(db.String(255), nullable=False, default='default_badge.png')
    requirement_type = db.Column(db.String(50), nullable=False) # 'first_quiz', 'perfect_score', 'points', 'quizzes_completed'
    requirement_value = db.Column(db.Integer, nullable=False) # Example: 100 (for points) or 1 (for first quiz)

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)

class StoreItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    board = db.Column(db.String(50), nullable=True)
    standard = db.Column(db.String(50), nullable=True)
    course = db.Column(db.String(50), nullable=True)

    cost = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(50), nullable=False) # 'title' or 'border'
    css_class = db.Column(db.String(255), nullable=True) 
    icon = db.Column(db.String(50), nullable=True) 

class UserInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_item_id = db.Column(db.Integer, db.ForeignKey('store_item.id'), nullable=False)
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    store_item = db.relationship('StoreItem')
