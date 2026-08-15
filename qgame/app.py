import os
import sys
# Add parent directory to path so 'qgame' module can be imported when running app.py directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import urllib.request
import urllib.parse
import json
import html
import random
import time
from datetime import datetime
import threading
from flask import Flask, render_template, redirect, url_for, flash, request, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from qgame.models import db, User, Category, Question, QuizAttempt, Certificate, Badge, UserBadge, StoreItem, UserInventory, LiveSession, LiveParticipant
from sqlalchemy.exc import IntegrityError
from qgame.utils.gamification import process_quiz_result
from qgame.utils.certificates import generate_certificate
from flask_babel import Babel, _
from deep_translator import GoogleTranslator
import json
import urllib.request
import random

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'offline_quiz_secret_key_123'
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'quizmaster.db'))
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'hi', 'gu']

if db_url.startswith("sqlite"):
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Auto-upgrade schema for live database (ignores errors if columns exist)
    from sqlalchemy import text
    columns_to_add = [
        ("user", "name", "VARCHAR(100) DEFAULT 'User'"),
        ("user", "email", "VARCHAR(150)"),
        ("user", "mobile", "VARCHAR(20)"),
        ("user", "dob", "VARCHAR(50)"),
        ("user", "country", "VARCHAR(100)"),
        ("user", "state", "VARCHAR(100)"),
        ("user", "city", "VARCHAR(100)"),
        ("user", "age", "INTEGER"),
        ("user", "gender", "VARCHAR(20)"),
        ("user", "education_level", "VARCHAR(50)"),
        ("user", "board", "VARCHAR(50)"),
        ("user", "standard", "VARCHAR(50)"),
        ("user", "stream", "VARCHAR(50)"),
        ("user", "course", "VARCHAR(100)"),
        ("user", "exam", "VARCHAR(100)"),
        ("user", "college", "VARCHAR(150)"),
        ("user", "department", "VARCHAR(150)"),
        ("user", "semester", "VARCHAR(50)"),
        ("user", "profile_photo", "VARCHAR(255) DEFAULT 'default.png'"),
        ("user", "language", "VARCHAR(10) DEFAULT 'en'"),
        ("category", "education_level", "VARCHAR(50)"),
        ("category", "board", "VARCHAR(50)"),
        ("category", "standard", "VARCHAR(50)"),
        ("category", "course", "VARCHAR(50)"),
        ("store_item", "education_level", "VARCHAR(50)"),
        ("store_item", "board", "VARCHAR(50)"),
        ("store_item", "standard", "VARCHAR(50)"),
        ("store_item", "course", "VARCHAR(50)")
    ]
    for table, col, dtype in columns_to_add:
        try:
            db.session.execute(text(f'ALTER TABLE "{table}" ADD COLUMN {col} {dtype}'))
            db.session.commit()
            print(f"Added column {col} to {table}")
        except Exception as e:
            print(f"Error adding {col} to {table}: {e}")
            db.session.rollback()

    indexes_to_create = [
        "CREATE INDEX IF NOT EXISTS ix_category_education_level ON category (education_level)",
        "CREATE INDEX IF NOT EXISTS ix_category_board ON category (board)",
        "CREATE INDEX IF NOT EXISTS ix_category_standard ON category (standard)",
        "CREATE INDEX IF NOT EXISTS ix_category_course ON category (course)",
        "CREATE INDEX IF NOT EXISTS ix_question_category_id ON question (category_id)",
        "CREATE INDEX IF NOT EXISTS ix_question_language ON question (language)",
        "CREATE INDEX IF NOT EXISTS ix_quiz_attempt_user_id ON quiz_attempt (user_id)",
        "CREATE INDEX IF NOT EXISTS ix_quiz_attempt_category_id ON quiz_attempt (category_id)",
        "CREATE INDEX IF NOT EXISTS ix_certificate_user_id ON certificate (user_id)",
        "CREATE INDEX IF NOT EXISTS ix_certificate_attempt_id ON certificate (attempt_id)"
    ]
    for idx_query in indexes_to_create:
        try:
            db.session.execute(text(idx_query))
            db.session.commit()
        except Exception as e:
            print(f"Error creating index: {e}")
            db.session.rollback()

    admin = User.query.filter_by(username="admin").first()

    if not admin:
        admin = User(
            username="admin",
            name="Administrator",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

def get_locale():
    if current_user and current_user.is_authenticated:
        return current_user.language or 'en'
    return session.get('lang', request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'en')

babel = Babel(app, locale_selector=get_locale)

def get_category_icon(category_name):
    known = {
        'Python': ('fab fa-python', 'text-blue-500'),
        'General Knowledge': ('fas fa-brain', 'text-purple-500'),
        'Mathematics': ('fas fa-square-root-variable', 'text-pink-500'),
        'Science': ('fas fa-flask', 'text-green-500'),
        'History': ('fas fa-landmark', 'text-yellow-500'),
        'Geography': ('fas fa-globe-americas', 'text-cyan-500'),
        'Technology': ('fas fa-laptop-code', 'text-blue-500'),
        'Sports': ('fas fa-futbol', 'text-red-500'),
        'Literature': ('fas fa-book-open', 'text-green-500'),
        'Art': ('fas fa-palette', 'text-pink-500'),
    }
    if category_name in known:
        return known[category_name]
    
    icons = ['fas fa-gamepad', 'fas fa-rocket', 'fas fa-bolt', 'fas fa-star', 'fas fa-fire', 'fas fa-trophy', 'fas fa-crown', 'fas fa-lightbulb', 'fas fa-gem', 'fas fa-music', 'fas fa-film']
    colors = ['text-purple-500', 'text-red-500', 'text-blue-500', 'text-green-500', 'text-yellow-500', 'text-pink-500', 'text-cyan-500', 'text-orange-500']
    
    hash_val = sum(ord(c) for c in category_name)
    icon = icons[hash_val % len(icons)]
    color = colors[hash_val % len(colors)]
    return icon, color

app.jinja_env.globals.update(get_category_icon=get_category_icon)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/system_fix_db')
def system_fix_db():
    from sqlalchemy import text
    
    columns = [
        ("board", "VARCHAR(50)"),
        ("standard", "VARCHAR(50)"),
        ("stream", "VARCHAR(50)"),
        ("subject", "VARCHAR(100)"),
        ("chapter", "VARCHAR(100)"),
        ("topic", "VARCHAR(100)"),
        
        ("question_en", "TEXT"),
        ("question_gu", "TEXT"),
        ("question_hi", "TEXT"),
        
        ("option_a_en", "VARCHAR(255)"),
        ("option_b_en", "VARCHAR(255)"),
        ("option_c_en", "VARCHAR(255)"),
        ("option_d_en", "VARCHAR(255)"),
        
        ("option_a_gu", "VARCHAR(255)"),
        ("option_b_gu", "VARCHAR(255)"),
        ("option_c_gu", "VARCHAR(255)"),
        ("option_d_gu", "VARCHAR(255)"),
        
        ("option_a_hi", "VARCHAR(255)"),
        ("option_b_hi", "VARCHAR(255)"),
        ("option_c_hi", "VARCHAR(255)"),
        ("option_d_hi", "VARCHAR(255)"),
        
        ("explanation_en", "TEXT"),
        ("explanation_gu", "TEXT"),
        ("explanation_hi", "TEXT"),
        
        ("source", "VARCHAR(255)"),
        ("source_type", "VARCHAR(100)"),
        ("verified", "BOOLEAN DEFAULT FALSE"),
        ("created_at", "TIMESTAMP")
    ]
    
    output = "Fixing DB Schema...<br>"
    try:
        with db.engine.connect() as conn:
            for col_name, col_type in columns:
                try:
                    conn.execute(text(f"ALTER TABLE question ADD COLUMN {col_name} {col_type}"))
                    output += f"Added {col_name}<br>"
                except Exception as e:
                    output += f"Skipped {col_name} (already exists or error)<br>"
            conn.commit()
    except Exception as main_e:
        output += f"Main DB Error: {main_e}<br>"
        
    return output + "<br><b>Done! <a href='/admin'>Go to Admin</a></b>"

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
        if current_user.is_authenticated:
            current_user.language = lang
            db.session.commit()
    return redirect(request.referrer or url_for('index'))

# ----------------- AUTH ROUTES -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
            
        login_user(user, remember=remember)
        
        # Redirect to the page they were trying to access, if it exists
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
            
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
            
        return redirect(url_for('user_dashboard'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
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
        
        login_user(new_user)
        flash('Account created successfully! Welcome to your dashboard.')
        
        # Redirect to the page they were trying to access, if it exists
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
            
        return redirect(url_for('user_dashboard'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ----------------- USER ROUTES -----------------
@app.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    from sqlalchemy import or_
    
    query = Category.query
    profile_filter = None
    
    if current_user.education_level == 'School':
        profile_filter = (Category.education_level == 'School') & (Category.standard == current_user.standard) & (Category.board == current_user.board)
    elif current_user.education_level in ['Graduation', 'Diploma', 'Post Graduation']:
        profile_filter = (Category.education_level == current_user.education_level) & (Category.course == current_user.course)
        if current_user.semester and current_user.semester != 'None':
            profile_filter = profile_filter & (Category.standard == current_user.semester)
    elif current_user.education_level == 'Competitive Exam':
        profile_filter = (Category.education_level == 'Competitive Exam') & (Category.course == current_user.exam)
        
    if profile_filter is not None:
        categories = query.filter(or_(profile_filter, Category.education_level.is_(None), Category.education_level == '')).all()
    else:
        categories = query.filter(or_(Category.education_level.is_(None), Category.education_level == '')).all()
    
    # If no subjects are specifically matched, don't show random ones! 
    # Just show empty list so they know their specific profile has no subjects yet.
    # We will seed the DB to ensure there ARE subjects.
        
    category_counts = {}
    if categories:
        cat_ids = [c.id for c in categories]
        from sqlalchemy import func
        counts = db.session.query(Question.category_id, func.count(Question.id)).filter(Question.category_id.in_(cat_ids)).group_by(Question.category_id).all()
        for cat_id, count in counts:
            category_counts[cat_id] = count
    
    for c in categories:
        if c.id not in category_counts:
            category_counts[c.id] = 0
        
    user_quizzes = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.date.desc()).limit(5).all()
    user_inventory = [inv.store_item_id for inv in current_user.inventory]
    equipped_title = StoreItem.query.get(current_user.active_title_id) if current_user.active_title_id else None
    equipped_border = StoreItem.query.get(current_user.active_border_id) if current_user.active_border_id else None
    
    return render_template('user/dashboard.html', categories=categories, category_counts=category_counts, user_quizzes=user_quizzes, user=current_user, equipped_title=equipped_title, equipped_border=equipped_border)

@app.route('/quiz/<int:category_id>', methods=['GET'])
@login_required
def take_quiz(category_id):
    category = Category.query.get_or_404(category_id)
    lang = get_locale()
    questions = Question.query.filter_by(category_id=category.id, language=lang).all()
    
    if not questions:
        if lang != 'en':
            # Fallback to English questions
            en_questions = Question.query.filter_by(category_id=category.id, language='en').all()
            if not en_questions:
                flash(_("No questions available for this category yet."))
                return redirect(url_for('user_dashboard'))
            
            flash(_("Questions in your preferred language are not available yet. Showing English questions."))
            questions = en_questions
            
            # Translate in background (optional, simple thread)
            def translate_in_background(app_instance, cat_id, target_lang):
                with app_instance.app_context():
                    from deep_translator import GoogleTranslator
                    import random
                    qs = Question.query.filter_by(category_id=cat_id, language='en').all()
                    if not qs: return
                    random.shuffle(qs)
                    qs = qs[:10]
                    translator = GoogleTranslator(source='en', target=target_lang)
                    for eq in qs:
                        try:
                            # Check if already translated
                            exists = Question.query.filter_by(category_id=cat_id, text=eq.text, language=target_lang).first()
                            if exists: continue
                            to_trans = [eq.text, eq.option_a, eq.option_b, eq.option_c, eq.option_d]
                            t_text, t_a, t_b, t_c, t_d = translator.translate_batch(to_trans)
                            q = Question(
                                category_id=cat_id, text=t_text,
                                option_a=t_a, option_b=t_b, option_c=t_c, option_d=t_d,
                                correct_option=eq.correct_option, difficulty=eq.difficulty, language=target_lang
                            )
                            db.session.add(q)
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
            
            from threading import Thread
            Thread(target=translate_in_background, args=(app, category.id, lang)).start()
        else:
            flash(_("No questions available for this category yet."))
            return redirect(url_for('user_dashboard'))
            
    import random
    random.shuffle(questions)
    # Take up to 10 questions so that they are randomly chosen each time from the available pool
    questions = questions[:10]
    session[f'quiz_{category.id}_qids'] = [q.id for q in questions]
    
    return render_template('user/quiz.html', category=category, questions=questions)

@app.route('/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    category_id = int(request.form.get('category_id'))
    time_taken = int(request.form.get('time_taken', 0))
    
    category = Category.query.get_or_404(category_id)
    
    presented_qids = session.get(f'quiz_{category.id}_qids')
    if presented_qids:
        questions = Question.query.filter(Question.id.in_(presented_qids)).all()
    else:
        questions = Question.query.filter_by(category_id=category.id, language=session.get('lang', 'en')).all()
    
    score = 0
    total_questions = len(questions)
    review_data = []
    
    for q in questions:
        ans = request.form.get(f'q_{q.id}')
        is_correct = (ans == q.correct_option)
        if is_correct:
            score += 1
            
        user_ans_val = getattr(q, f"option_{ans.lower()}", "Not Answered") if ans else "Not Answered"
        review_data.append({
            'question': q.text,
            'user_ans': ans if ans else "-",
            'user_ans_text': user_ans_val,
            'correct_ans': q.correct_option,
            'correct_ans_text': getattr(q, f"option_{q.correct_option.lower()}", "Unknown"),
            'is_correct': is_correct,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d
        })
                
    session[f'review_{current_user.id}'] = review_data
    passed = (score / total_questions >= 0.7) if total_questions > 0 else False
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        category_id=category.id,
        score=score,
        total_questions=total_questions,
        time_taken=time_taken,
        passed=passed
    )
    
    db.session.add(attempt)
    db.session.commit()
    
    points, xp = process_quiz_result(current_user, attempt)
    # Certificate generation is now manual via an explicit option
    
    live_room_code = None
    participant_id = session.get('active_live_participant_id')
    if participant_id:
        participant = LiveParticipant.query.get(participant_id)
        if participant:
            participant.completed = True
            participant.score = score
            participant.questions_answered = total_questions
            participant.last_ping = datetime.utcnow()
            db.session.commit()
            
            # Get the room code
            live_session = LiveSession.query.get(participant.session_id)
            if live_session:
                live_room_code = live_session.room_code
                
        session.pop('active_live_session_id', None)
        session.pop('active_live_participant_id', None)
    
    if live_room_code:
        return redirect(url_for('quiz_result', attempt_id=attempt.id, live_room=live_room_code))
    return redirect(url_for('quiz_result', attempt_id=attempt.id))

@app.route('/quiz/result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('user_dashboard'))
        
    percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
    cert = Certificate.query.filter_by(attempt_id=attempt.id).first()
    review_data = session.get(f'review_{current_user.id}', [])
    live_room = request.args.get('live_room')
    
    return render_template('user/result.html', attempt=attempt, percentage=percentage, cert=cert, review_data=review_data, live_room=live_room)

@app.route('/certificate/generate/<int:attempt_id>', methods=['POST'])
@login_required
def generate_cert(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('user_dashboard'))
    
    if not attempt.passed:
        flash("You must pass the quiz to claim a certificate.")
        return redirect(url_for('quiz_result', attempt_id=attempt.id))
        
    cert = Certificate.query.filter_by(attempt_id=attempt.id).first()
    if not cert:
        category = Category.query.get(attempt.category_id)
        cert_id, file_path = generate_certificate(current_user, attempt, category)
        cert = Certificate(user_id=current_user.id, attempt_id=attempt.id, certificate_id=cert_id, file_path=file_path)
        db.session.add(cert)
        db.session.commit()
        flash("Certificate generated successfully!")
        
    return redirect(url_for('download_certificate', cert_id=cert.id))

@app.route('/certificate/download/<int:cert_id>')
@login_required
def download_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)
    if cert.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for('user_dashboard'))
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, 'static', 'certificates')
    filename = os.path.basename(cert.file_path)
    
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        # Regenerate if file is missing (e.g. after a deploy on ephemeral filesystem)
        attempt = QuizAttempt.query.get(cert.attempt_id)
        if attempt:
            category = Category.query.get(attempt.category_id)
            cert_id_new, file_path_new = generate_certificate(current_user, attempt, category)
            cert.certificate_id = cert_id_new
            cert.file_path = file_path_new
            db.session.commit()
            filename = os.path.basename(cert.file_path)
    
    response = send_from_directory(directory, filename)
    response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        age_str = request.form.get('age')
        current_user.age = int(age_str) if age_str and age_str.strip() else None
        current_user.gender = request.form.get('gender')
        current_user.email = request.form.get('email')
        current_user.mobile = request.form.get('mobile')
        current_user.dob = request.form.get('dob')
        current_user.country = request.form.get('country')
        current_user.state = request.form.get('state')
        current_user.city = request.form.get('city')
        
        ed_level = request.form.get('education_level')
        current_user.education_level = ed_level
        if ed_level == 'School':
            current_user.board = request.form.get('board')
            current_user.standard = request.form.get('standard')
            current_user.stream = request.form.get('stream')
        elif ed_level == 'Diploma':
            current_user.course = request.form.get('diploma_branch')
            current_user.semester = request.form.get('diploma_semester')
        elif ed_level == 'Graduation':
            current_user.college = request.form.get('university')
            current_user.course = request.form.get('grad_course')
            current_user.semester = request.form.get('grad_semester')
        elif ed_level == 'Post Graduation':
            current_user.course = request.form.get('pg_course')
            current_user.semester = request.form.get('pg_semester')
        elif ed_level == 'Competitive Exam':
            current_user.exam = request.form.get('exam')
            
        lang = request.form.get('language')
        if lang in app.config['BABEL_SUPPORTED_LOCALES']:
            current_user.language = lang
            session['lang'] = lang

        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))
    return render_template('user/profile.html', user=current_user)

@app.route('/leaderboard')
@login_required
def leaderboard():
    # Fetch top 10 users ranked by XP
    top_users = User.query.filter_by(role='user').order_by(User.xp.desc()).limit(10).all()
    return render_template('user/leaderboard.html', top_users=top_users, current_user=current_user)

# ----------------- ADMIN ROUTES -----------------
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    users_count = User.query.count()
    quizzes_count = QuizAttempt.query.count()
    certs_count = Certificate.query.count()
    questions_count = Question.query.filter_by(language='en').count()
    categories_count = Category.query.count()
    store_items_count = StoreItem.query.count()
    
    # Fetch recent activity
    recent_users = User.query.filter_by(role='user').order_by(User.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', user=current_user, users_count=users_count, quizzes_count=quizzes_count, certs_count=certs_count, questions_count=questions_count, categories_count=categories_count, store_items_count=store_items_count, recent_users=recent_users)




@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if name:
            cat = Category(name=name, description=description)
            db.session.add(cat)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash(f'Category "{name}" already exists!', 'danger')
                return redirect(url_for('admin_categories'))
            
            category_map = {
                'General Knowledge': 9, 'Books': 10, 'Film': 11, 'Music': 12, 'Musicals & Theatres': 13,
                'Television': 14, 'Video Games': 15, 'Board Games': 16, 'Science & Nature': 17,
                'Computers': 18, 'Mathematics': 19, 'Mythology': 20, 'Sports': 21, 'Geography': 22,
                'History': 23, 'Politics': 24, 'Art': 25, 'Celebrities': 26, 'Animals': 27,
                'Vehicles': 28, 'Comics': 29, 'Gadgets': 30, 'Anime & Manga': 31, 'Cartoon & Animations': 32
            }
            if name in category_map:
                tdb_id = category_map[name]
                
                def fetch_and_translate(app_instance, category_id, category_name, tdb_id):
                    with app_instance.app_context():
                        cat = Category.query.get(category_id)
                        if not cat: return
                        
                        data = None
                        amount = 10
                        import time
                        
                        def fetch_json_with_retry(url, max_retries=5):
                            import urllib.error
                            for attempt in range(max_retries):
                                try:
                                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                                    response = urllib.request.urlopen(req)
                                    return json.loads(response.read())
                                except urllib.error.HTTPError as e:
                                    if e.code == 429:
                                        print(f"Rate limited (429), waiting 6 seconds... (Attempt {attempt+1}/{max_retries})")
                                        time.sleep(6)
                                    else:
                                        print(f"HTTP Error {e.code}: {e.reason}")
                                        break
                                except Exception as e:
                                    print(f"API request failed: {e}")
                                    break
                            return None

                        count_url = f"https://opentdb.com/api_count.php?category={tdb_id}"
                        count_data = fetch_json_with_retry(count_url)
                        
                        if count_data:
                            easy_count = count_data.get('category_question_count', {}).get('total_easy_question_count', 0)
                            if easy_count > 0:
                                amounts_to_try = [min(50, easy_count)]
                                for a in [40, 30, 20, 10, 5]:
                                    if a < easy_count:
                                        amounts_to_try.append(a)
                                        
                                for amount in amounts_to_try:
                                    url = f"https://opentdb.com/api.php?amount={amount}&category={tdb_id}&type=multiple&difficulty=easy"
                                    data = fetch_json_with_retry(url)
                                    if data and data.get('response_code') == 0:
                                        break
                                    elif data and data.get('response_code') == 1:
                                        print(f"Code 1 for amount {amount}. Waiting 6s before trying lower amount...")
                                        time.sleep(6)
                                
                        if data and data.get('response_code') == 0:
                            try:
                                for res in data['results']:
                                    question_text = html.unescape(res['question'])
                                    correct = html.unescape(res['correct_answer'])
                                    incorrects = [html.unescape(ans) for ans in res['incorrect_answers']]
                                    
                                    all_opts = incorrects + [correct]
                                    random.shuffle(all_opts)
                                    correct_letter = chr(65 + all_opts.index(correct))
                                    
                                    for lang in ['en', 'gu', 'hi']:
                                        if lang == 'en':
                                            q_text, opt_a, opt_b, opt_c, opt_d = question_text, all_opts[0], all_opts[1], all_opts[2], all_opts[3]
                                        else:
                                            translator = GoogleTranslator(source='en', target=lang)
                                            try:
                                                to_trans = [question_text, all_opts[0], all_opts[1], all_opts[2], all_opts[3]]
                                                translated = translator.translate_batch(to_trans)
                                                q_text, opt_a, opt_b, opt_c, opt_d = translated
                                            except Exception as e:
                                                print(f"Translation error: {e}")
                                                q_text, opt_a, opt_b, opt_c, opt_d = question_text, all_opts[0], all_opts[1], all_opts[2], all_opts[3]
                                        
                                        q = Question(
                                            category_id=cat.id,
                                            text=q_text,
                                            option_a=opt_a,
                                            option_b=opt_b,
                                            option_c=opt_c,
                                            option_d=opt_d,
                                            correct_option=correct_letter,
                                            difficulty=res['difficulty'].capitalize(),
                                            language=lang
                                        )
                                        db.session.add(q)
                                db.session.commit()
                                print(f'Category "{category_name}" populated with questions successfully!')
                            except Exception as e:
                                print(f'Error saving questions for "{category_name}": {e}')
                        else:
                            print(f'Failed to fetch questions for "{category_name}". Deleting empty category.')
                            db.session.delete(cat)
                            db.session.commit()
                            
                # Run in background thread
                from threading import Thread
                thread = Thread(target=fetch_and_translate, args=(app, cat.id, name, tdb_id))
                thread.daemon = True
                thread.start()
                
                flash(f'Category "{name}" added! Questions are being fetched and translated in the background. Please wait a minute or two.', 'info')
            else:
                flash(f'Category "{name}" added successfully! You can now add questions manually from the Questions page.', 'success')
                
            return redirect(url_for('admin_categories'))
        
    import re
    categories_raw = Category.query.all()
    
    def sort_category(c):
        name = c.name or ''
        match = re.search(r'Std\s+(\d+)', name, re.IGNORECASE)
        if match:
            return (int(match.group(1)), name)
        return (float('inf'), name)
        
    categories = sorted(categories_raw, key=sort_category)
    
    category_counts = {}
    if categories:
        cat_ids = [c.id for c in categories]
        from sqlalchemy import func
        counts = db.session.query(Question.category_id, func.count(Question.id)).filter(Question.category_id.in_(cat_ids), Question.language == 'en').group_by(Question.category_id).all()
        for cat_id, count in counts:
            category_counts[cat_id] = count
            
    for c in categories:
        if c.id not in category_counts:
            category_counts[c.id] = 0
            
    return render_template('admin/categories.html', categories=categories, category_counts=category_counts)

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def admin_delete_category(category_id):
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'success')
    return redirect(url_for('admin_categories'))


@app.route('/admin/questions', methods=['GET', 'POST'])
@login_required
def admin_questions():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        text = request.form.get('text')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_option = request.form.get('correct_option')
        difficulty = request.form.get('difficulty')
        
        q = Question(category_id=category_id, text=text, option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, correct_option=correct_option, difficulty=difficulty)
        db.session.add(q)
        db.session.commit()
        flash('Question added.')
        return redirect(url_for('admin_questions'))
        
    category_id = request.args.get('category_id')
    if category_id:
        questions = Question.query.filter_by(category_id=category_id).all()
    else:
        questions = Question.query.all()
    categories = Category.query.all()
    return render_template('admin/questions.html', questions=questions, categories=categories)

@app.route('/admin/questions/delete/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    question_to_delete = Question.query.get_or_404(question_id)
    db.session.delete(question_to_delete)
    db.session.commit()
    flash('Question deleted successfully.', 'success')
    return redirect(url_for('admin_questions'))

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.role == 'admin':
        flash('Cannot delete an admin account.', 'danger')
        return redirect(url_for('admin_users'))
        
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'User deleted successfully.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    user_to_promote = User.query.get_or_404(user_id)
    if user_to_promote.role == 'admin':
        flash('User is already an admin.', 'danger')
    elif user_to_promote.role == 'teacher':
        user_to_promote.role = 'user'
        db.session.commit()
        flash(f'Removed teacher role from {user_to_promote.username}.', 'success')
    else:
        user_to_promote.role = 'teacher'
        db.session.commit()
        flash(f'Promoted {user_to_promote.username} to Teacher!', 'success')
        
    return redirect(url_for('admin_users'))

@app.route('/admin/quizzes')
@login_required
def admin_quizzes():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    quizzes = QuizAttempt.query.order_by(QuizAttempt.date.desc()).all()
    return render_template('admin/quizzes.html', quizzes=quizzes)

@app.route('/admin/certificates')
@login_required
def admin_certificates():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    certificates = Certificate.query.order_by(Certificate.issue_date.desc()).all()
    return render_template('admin/certificates.html', certificates=certificates)

@app.route('/admin/store', methods=['GET', 'POST'])
@login_required
def admin_store():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cost = int(request.form.get('cost', 100))
        item_type = request.form.get('item_type')
        css_class = request.form.get('css_class')
        icon = request.form.get('icon')
        
        new_item = StoreItem(name=name, description=description, cost=cost, item_type=item_type, css_class=css_class, icon=icon)
        db.session.add(new_item)
        db.session.commit()
        flash('Store item added successfully!', 'success')
        return redirect(url_for('admin_store'))
        
    items = StoreItem.query.all()
    return render_template('admin/store.html', items=items)


@app.route('/store')
@login_required
def store():
    items = StoreItem.query.all()
    user_inventory_ids = [inv.store_item_id for inv in current_user.inventory]
    return render_template('user/store.html', items=items, inventory=user_inventory_ids, user=current_user)

@app.route('/store/buy/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    item = StoreItem.query.get_or_404(item_id)
    user_inventory_ids = [inv.store_item_id for inv in current_user.inventory]
    
    if item.id in user_inventory_ids:
        flash('You already own this item.', 'warning')
        return redirect(url_for('store'))
        
    if current_user.coins >= item.cost:
        current_user.coins -= item.cost
        inv = UserInventory(user_id=current_user.id, store_item_id=item.id)
        db.session.add(inv)
        db.session.commit()
        flash(f'Successfully purchased {item.name}!', 'success')
    else:
        flash('Not enough coins!', 'danger')
        
    return redirect(url_for('store'))

@app.route('/store/equip/<int:item_id>', methods=['POST'])
@login_required
def equip_item(item_id):
    item = StoreItem.query.get_or_404(item_id)
    user_inventory_ids = [inv.store_item_id for inv in current_user.inventory]
    
    if item.id not in user_inventory_ids:
        flash('You do not own this item.', 'danger')
        return redirect(url_for('store'))
        
    if item.item_type == 'title':
        if current_user.active_title_id == item.id:
            current_user.active_title_id = None
            flash('Title unequipped.', 'info')
        else:
            current_user.active_title_id = item.id
            flash('Title equipped!', 'success')
            
    elif item.item_type == 'border':
        if current_user.active_border_id == item.id:
            current_user.active_border_id = None
            flash('Border unequipped.', 'info')
        else:
            current_user.active_border_id = item.id
            flash('Border equipped!', 'success')
            
    db.session.commit()
    return redirect(url_for('store'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('user_dashboard'))
        
    # Search for categories matching the query
    matching_categories = Category.query.filter(Category.name.ilike(f'%{query}%')).all()
    
    return render_template('user/search.html', query=query, categories=matching_categories)

@app.route('/admin/import_custom', methods=['POST'])
@login_required
def admin_import_custom():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    from flask import current_app
    app_instance = current_app._get_current_object()
    
    def seed_all_stds(app_obj):
        with app_obj.app_context():
            boards = ["GSEB"]
            general_subjects = ["Mathematics", "Science", "English", "Hindi", "Social Studies", "Gujarati"]
            science_subjects = ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Computer Science"]
            commerce_subjects = ["Accountancy", "Economics", "Business Administration", "Statistics", "English"]
            arts_subjects = ["History", "Geography", "Political Science", "Psychology", "Sociology", "English"]
            
            def seed_subjects(std_list, stream, subj_list):
                for board in boards:
                    for std in std_list:
                        for subj in subj_list:
                            name = f"Std {std} {subj}"
                            actual_stream = stream if std >= 11 else "None"
                            cat = Category.query.filter_by(name=name, standard=str(std)).first()
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
            
            seed_subjects(range(1, 11), "None", general_subjects)
            seed_subjects([11, 12], "Science", science_subjects)
            seed_subjects([11, 12], "Commerce", commerce_subjects)
            seed_subjects([11, 12], "Arts", arts_subjects)

    from threading import Thread
    thread = Thread(target=seed_all_stds, args=(app_instance,))
    thread.daemon = True
    thread.start()
    
    flash('Started adding all standard categories! Please refresh the page in a few seconds.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/import_culture', methods=['POST'])
@login_required
def admin_import_culture():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    import subprocess
    import sys
    import os
    
    script_path = os.path.join(basedir, '..', 'import_culture_quizzes.py')
    if os.path.exists(script_path):
        # Run the script in the background
        subprocess.Popen([sys.executable, script_path])
        flash('Started importing Ramayana, Mahabharata, and Hindu Gods quizzes! Please refresh the page in a few seconds.', 'success')
    else:
        flash('Could not find the import script.', 'error')
        
    return redirect(url_for('admin_categories'))



@app.route('/admin/ai_generator', methods=['GET', 'POST'])
@login_required
def admin_ai_generator():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        board = request.form.get('board')
        standard = request.form.get('standard')
        subject = request.form.get('subject')
        num_questions = int(request.form.get('num_questions', 10))
        
        if not board or not standard or not subject:
            flash('Board, Standard and Subject are required!', 'error')
            return redirect(url_for('admin_ai_generator'))
            
        try:
            from flask import current_app
            app_instance = current_app._get_current_object()
            
            def generate_bg(app_obj, b, st, sub, num):
                with app_obj.app_context():
                    try:
                        from qgame.utils.ai_generator import generate_questions_with_gemini
                        data = generate_questions_with_gemini(b, st, sub, num)
                        
                        for item in data:
                            q_en = item.get('question', {}).get('en')
                            if not q_en:
                                continue
                                
                            existing = Question.query.filter_by(
                                standard=str(item.get('standard')),
                                subject=item.get('subject'),
                                question_en=q_en
                            ).first()
                            
                            if existing:
                                continue
                                
                            cat_name = f"Std {item.get('standard')} {item.get('subject')}"
                            cat = Category.query.filter_by(name=cat_name).first()
                            if not cat:
                                cat = Category(name=cat_name, description=f"Imported {b} {cat_name}")
                                cat.education_level = 'School'
                                cat.board = item.get('board')
                                cat.standard = str(item.get('standard'))
                                cat.course = item.get('subject')
                                db.session.add(cat)
                                db.session.commit()
                                
                            q = Question(
                                category_id=cat.id,
                                board=item.get('board'),
                                standard=str(item.get('standard')),
                                stream=item.get('stream'),
                                subject=item.get('subject'),
                                chapter=item.get('chapter'),
                                topic=item.get('topic'),
                                difficulty=item.get('difficulty', 'Medium'),
                                
                                question_en=q_en,
                                question_gu=item.get('question', {}).get('gu'),
                                question_hi=item.get('question', {}).get('hi'),
                                
                                option_a_en=item.get('options', {}).get('en', ['', '', '', ''])[0],
                                option_b_en=item.get('options', {}).get('en', ['', '', '', ''])[1],
                                option_c_en=item.get('options', {}).get('en', ['', '', '', ''])[2],
                                option_d_en=item.get('options', {}).get('en', ['', '', '', ''])[3],
                                
                                option_a_gu=item.get('options', {}).get('gu', ['', '', '', ''])[0],
                                option_b_gu=item.get('options', {}).get('gu', ['', '', '', ''])[1],
                                option_c_gu=item.get('options', {}).get('gu', ['', '', '', ''])[2],
                                option_d_gu=item.get('options', {}).get('gu', ['', '', '', ''])[3],
                                
                                option_a_hi=item.get('options', {}).get('hi', ['', '', '', ''])[0],
                                option_b_hi=item.get('options', {}).get('hi', ['', '', '', ''])[1],
                                option_c_hi=item.get('options', {}).get('hi', ['', '', '', ''])[2],
                                option_d_hi=item.get('options', {}).get('hi', ['', '', '', ''])[3],
                                
                                correct_option=str(item.get('correct_option')),
                                
                                explanation_en=item.get('explanation', {}).get('en'),
                                explanation_gu=item.get('explanation', {}).get('gu'),
                                explanation_hi=item.get('explanation', {}).get('hi'),
                                
                                text=q_en,
                                option_a=item.get('options', {}).get('en', ['', '', '', ''])[0],
                                option_b=item.get('options', {}).get('en', ['', '', '', ''])[1],
                                option_c=item.get('options', {}).get('en', ['', '', '', ''])[2],
                                option_d=item.get('options', {}).get('en', ['', '', '', ''])[3],
                                explanation=item.get('explanation', {}).get('en'),
                                language='en',
                                
                                source=item.get('source'),
                                source_type=item.get('source_type', 'AI Generated'),
                                verified=item.get('verified', False)
                            )
                            db.session.add(q)
                            
                        db.session.commit()
                        print(f"Successfully generated and imported {num} questions for {sub}!")
                    except Exception as e:
                        print(f"AI Generation Error: {e}")
                        db.session.rollback()

            from threading import Thread
            thread = Thread(target=generate_bg, args=(app_instance, board, standard, subject, num_questions))
            thread.daemon = True
            thread.start()
            
            flash(f'AI has started generating {num_questions} questions for {subject} in the background! This may take 1-2 minutes. Please check the categories page later.', 'info')
            return redirect(url_for('admin_categories'))
            
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            
    return render_template('admin/ai_generator.html')

@app.route('/admin/migrate_db')
@login_required
def migrate_db_route():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    
    import sqlite3
    db_path = os.path.join(basedir, 'quizmaster.db')
    if not os.path.exists(db_path):
        flash('Local SQLite database not found!')
        return redirect(url_for('admin_dashboard'))
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Migrate Categories
        cursor.execute("SELECT id, name, description, image_filename, education_level, board, standard, course FROM category")
        sqlite_categories = cursor.fetchall()
        
        live_categories = {c.name: c for c in Category.query.all()}
        cat_id_mapping = {} 
        
        for row in sqlite_categories:
            sqlite_id, name, desc, img, ed_level, board, std, course = row
            if name not in live_categories:
                new_cat = Category(name=name, description=desc, image_filename=img)
                new_cat.education_level = ed_level
                new_cat.board = board
                new_cat.standard = std
                new_cat.course = course
                db.session.add(new_cat)
                db.session.commit()
                live_categories[name] = new_cat
            else:
                existing_cat = live_categories[name]
                
                # Force overwrite all metadata to ensure NO NULLs or mismatches
                existing_cat.education_level = ed_level
                existing_cat.board = board
                existing_cat.standard = std
                existing_cat.course = course
                db.session.commit()
                
            cat_id_mapping[sqlite_id] = live_categories[name].id
            
        # Migrate Questions
        cursor.execute("SELECT category_id, text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, language FROM question")
        sqlite_questions = cursor.fetchall()
        
        existing_qs = set((q.category_id, q.text, q.language) for q in Question.query.all())
        
        new_questions = []
        for row in sqlite_questions:
            cat_id, text, opt_a, opt_b, opt_c, opt_d, corr, expl, diff, lang = row
            live_cat_id = cat_id_mapping.get(cat_id)
            if live_cat_id:
                q_key = (live_cat_id, text, lang)
                if q_key not in existing_qs:
                    new_q = Question(
                        category_id=live_cat_id,
                        text=text,
                        option_a=opt_a, option_b=opt_b, option_c=opt_c, option_d=opt_d,
                        correct_option=corr, explanation=expl, difficulty=diff, language=lang
                    )
                    new_questions.append(new_q)
                    existing_qs.add(q_key)
                    
        if new_questions:
            db.session.bulk_save_objects(new_questions)
            db.session.commit()
            
        flash(f'Migration successful! Added {len(new_questions)} new questions from the local database.', 'success')
    except Exception as e:
        flash(f'Error during migration: {str(e)}', 'danger')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/debug_categories')
def debug_categories():
    categories = Category.query.all()
    out = "<h2>Live Database Categories:</h2>"
    for c in categories:
        out += f"{c.name} | Ed: {c.education_level} | Course: {c.course} | Std: {c.standard} | Board: {c.board}<br>"
    return out

@app.route('/admin/leaderboard_maker', methods=['GET', 'POST'])
@login_required
def admin_leaderboard_maker():
    if current_user.role != 'admin':
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
    
    generated_link = None
    if request.method == 'POST':
        standard = request.form.get('standard')
        if standard:
            generated_link = url_for('leaderboard_view', standard=standard, _external=True)
            flash('Leaderboard link generated successfully!', 'success')
            
    # Get distinct standards from users
    standards = db.session.query(User.standard).filter(User.standard.isnot(None)).distinct().all()
    standards = [s[0] for s in standards if s[0]]
    if not standards:
        standards = ['10', '11', '12'] # Default fallbacks
        
    return render_template('admin/leaderboard_maker.html', standards=standards, generated_link=generated_link)

@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():
    # Only allow admin or teacher roles
    if current_user.role not in ['admin', 'teacher']:
        flash('Unauthorized Access. Teacher role required.', 'danger')
        return redirect(url_for('index'))
    
    generated_quiz_link = None
    generated_leaderboard_link = None
    
    if request.method == 'POST':
        standard = request.form.get('standard')
        category_id = request.form.get('category_id')
        
        if standard and category_id:
            # Generate links
            generated_quiz_link = url_for('take_quiz', category_id=category_id, _external=True)
            generated_leaderboard_link = url_for('leaderboard_view', standard=standard, quiz_id=category_id, _external=True)
            flash('Links generated successfully!', 'success')
            
    # Get distinct standards from users and categories
    user_standards = [s[0] for s in db.session.query(User.standard).filter(User.standard.isnot(None)).distinct().all() if s[0]]
    cat_standards = [s[0] for s in db.session.query(Category.standard).filter(Category.standard.isnot(None)).distinct().all() if s[0]]
    standards = sorted(list(set(user_standards + cat_standards)))
    
    if not standards:
        standards = ['7', '8', '9', '10', '11', '12'] # Default fallbacks
        
    # Get all categories to pass to frontend for JS filtering
    categories = Category.query.all()
    categories_data = [{'id': c.id, 'name': c.name, 'standard': c.standard or 'All'} for c in categories]
        
    return render_template('teacher_dashboard.html', standards=standards, categories_json=json.dumps(categories_data), 
                           generated_quiz_link=generated_quiz_link, generated_leaderboard_link=generated_leaderboard_link,
                           active_sessions=LiveSession.query.filter_by(teacher_id=current_user.id, status='active').order_by(LiveSession.created_at.desc()).all())

import string
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/teacher/session/create', methods=['POST'])
@login_required
def create_live_session():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    category_id = request.form.get('category_id')
    if not category_id:
        return jsonify({'success': False, 'error': 'Category ID required'}), 400
        
    code = generate_room_code()
    while LiveSession.query.filter_by(room_code=code, status='active').first():
        code = generate_room_code()
        
    session = LiveSession(room_code=code, teacher_id=current_user.id, category_id=category_id)
    db.session.add(session)
    db.session.commit()
    
    return redirect(url_for('teacher_live_room', room_code=code))

@app.route('/teacher/session/<room_code>')
@login_required
def teacher_live_room(room_code):
    if current_user.role not in ['admin', 'teacher']:
        flash('Unauthorized Access.', 'danger')
        return redirect(url_for('index'))
        
    session = LiveSession.query.filter_by(room_code=room_code, status='active').order_by(LiveSession.id.desc()).first()
    if not session:
        session = LiveSession.query.filter_by(room_code=room_code).order_by(LiveSession.id.desc()).first_or_404()
        
    if session.teacher_id != current_user.id and current_user.role != 'admin':
        flash('Unauthorized Access.', 'danger')
        return redirect(url_for('index'))
        
    # Full URL for QR Code
    join_url = url_for('join_live_session', code=room_code, _external=True)
    return render_template('teacher/live_room.html', live_session=session, join_url=join_url)

@app.route('/teacher/session/delete/<room_code>', methods=['POST'])
@login_required
def delete_live_session(room_code):
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    session = LiveSession.query.filter_by(room_code=room_code, status='active').order_by(LiveSession.id.desc()).first()
    if not session:
        session = LiveSession.query.filter_by(room_code=room_code).order_by(LiveSession.id.desc()).first_or_404()
        
    if session.teacher_id != current_user.id and current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    db.session.delete(session)
    db.session.commit()
    
    flash('Live session deleted successfully.', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/api/session/status/<room_code>')
@login_required
def api_session_status(room_code):
    try:
        session = LiveSession.query.filter_by(room_code=room_code, status='active').order_by(LiveSession.id.desc()).first()
        if not session:
            # Fallback if somehow there's no active one but there is a completed one
            session = LiveSession.query.filter_by(room_code=room_code).order_by(LiveSession.id.desc()).first()
            
        if not session:
            return jsonify({'success': False, 'error': 'Session not found'})
            
        # EXPLICIT QUERY instead of session.participants
        participant_records = LiveParticipant.query.filter_by(session_id=session.id).all()
        
        participants = []
        for p in participant_records:
            participants.append({
                'user_id': p.user_id,
                'name': p.user.name if p.user else 'Student',
                'photo': p.user.profile_photo if p.user else 'default.png',
                'score': p.score or 0,
                'questions_answered': p.questions_answered or 0,
                'completed': p.completed,
                'last_ping': str(p.last_ping) if p.last_ping else None
            })
            
        return jsonify({
            'success': True,
            'status': session.status,
            'participants_count': len(participants),
            'session_id': session.id,
            'participants': sorted(participants, key=lambda x: (-x['score'], -x['questions_answered']))
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()})

@app.route('/join', methods=['GET', 'POST'])
def join_live_session():
    if not current_user.is_authenticated:
        flash('Please login to join a live quiz.')
        return redirect(url_for('login', next=request.url))
        
    code = request.args.get('code')
    if request.method == 'POST':
        code = request.form.get('room_code')
        
    if code:
        code = code.upper().strip()
        session = LiveSession.query.filter_by(room_code=code, status='active').first()
        if session:
            # Check if already joined
            participant = LiveParticipant.query.filter_by(session_id=session.id, user_id=current_user.id).first()
            if not participant:
                participant = LiveParticipant(session_id=session.id, user_id=current_user.id)
                db.session.add(participant)
                db.session.commit()
            
            # Store active session in Flask session so we can update it during quiz
            from flask import session as flask_session
            flask_session['active_live_session_id'] = session.id
            flask_session['active_live_participant_id'] = participant.id
            
            return redirect(url_for('take_quiz', category_id=session.category_id))
        else:
            flash('Invalid or inactive room code.', 'danger')
            
    return render_template('user/join.html', code=code)

@app.route('/live/board/<room_code>')
def live_board_user(room_code):
    session = LiveSession.query.filter_by(room_code=room_code, status='active').first()
    if not session:
        flash('Live session not found or ended.', 'danger')
        return redirect(url_for('join_live_session'))
    
    return render_template('user/live_board.html', live_session=session)

@app.route('/api/session/update_progress', methods=['POST'])
@login_required
def api_update_progress():
    from flask import session as flask_session
    participant_id = flask_session.get('active_live_participant_id')
    if not participant_id:
        return jsonify({'success': False})
        
    participant = LiveParticipant.query.get(participant_id)
    if participant:
        data = request.json
        participant.questions_answered = data.get('questions_answered', participant.questions_answered)
        participant.score = data.get('score', participant.score)
        participant.last_ping = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/leaderboard/<standard>')
@login_required
def leaderboard_view(standard):
    quiz_id = request.args.get('quiz_id')
    
    if quiz_id:
        # Fetch attempts for this specific quiz
        attempts = QuizAttempt.query.filter_by(category_id=quiz_id).all()
        
        # Get best score per user
        user_best = {}
        for att in attempts:
            if att.user_id not in user_best:
                user_best[att.user_id] = {'user': att.user, 'score': att.score, 'time': att.time_taken}
            else:
                if att.score > user_best[att.user_id]['score']:
                    user_best[att.user_id] = {'user': att.user, 'score': att.score, 'time': att.time_taken}
                elif att.score == user_best[att.user_id]['score'] and att.time_taken < user_best[att.user_id]['time']:
                    user_best[att.user_id] = {'user': att.user, 'score': att.score, 'time': att.time_taken}
                    
        # Sort by score desc, time asc
        sorted_attempts = sorted(user_best.values(), key=lambda x: (-x['score'], x['time']))[:10]
        
        # Create a list of dummy user objects for the template
        top_users = []
        class DummyUser:
            pass
        for item in sorted_attempts:
            u = item['user']
            du = DummyUser()
            du.name = u.name
            du.profile_photo = u.profile_photo
            du.points = item['score']  # Use quiz score instead of total points
            top_users.append(du)
            
    else:
        # Fallback to standard-based leaderboard using total points
        # Handle cases like "11 (Arts)" by extracting the number if needed, but let's just use exact match or basic fallback
        top_users = User.query.filter_by(standard=standard).order_by(User.points.desc(), User.xp.desc()).limit(10).all()
        # If no users found, try just the number
        if not top_users and " " in standard:
            base_std = standard.split(" ")[0]
            top_users = User.query.filter_by(standard=base_std).order_by(User.points.desc(), User.xp.desc()).limit(10).all()

    return render_template('leaderboard_view.html', users=top_users, standard=standard)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
