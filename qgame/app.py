import os
import urllib.request
import urllib.parse
import json
import html
import random
import time
from flask import Flask, render_template, redirect, url_for, flash, request, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from qgame.models import db, User, Category, Question, QuizAttempt, Certificate, Badge, UserBadge, StoreItem, UserInventory
from sqlalchemy.exc import IntegrityError
from qgame.utils.gamification import process_quiz_result
from qgame.utils.certificates import generate_certificate
from flask_babel import Babel, _
from deep_translator import GoogleTranslator
import json
import urllib.request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'offline_quiz_secret_key_123'
db_url = os.environ.get('DATABASE_URL', 'sqlite:///quizmaster.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'hi', 'gu']

db.init_app(app)

with app.app_context():
    db.create_all()

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

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
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
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        college = request.form.get('college')
        department = request.form.get('department')
        semester = request.form.get('semester')
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
            
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
            
        new_user = User(
            username=username,
            name=name,
            password_hash=generate_password_hash(password, method='scrypt'),
            age=age,
            gender=gender,
            college=college,
            department=department,
            semester=semester
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
        
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
    categories = Category.query.all()
    lang = session.get('lang', 'en')
    category_counts = {}
    for c in categories:
        category_counts[c.id] = Question.query.filter_by(category_id=c.id, language=lang).count()
    return render_template('user/dashboard.html', user=current_user, categories=categories, category_counts=category_counts)

@app.route('/quiz/<int:category_id>', methods=['GET'])
@login_required
def take_quiz(category_id):
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category.id, language=session.get('lang', 'en')).all()
    
    if not questions:
        flash("No questions available for this category yet.")
        return redirect(url_for('user_dashboard'))
        
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
    return render_template('user/result.html', attempt=attempt, percentage=percentage, cert=cert, review_data=review_data)

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
    
    response = send_from_directory(directory, filename)
    response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.age = request.form.get('age')
        current_user.gender = request.form.get('gender')
        current_user.college = request.form.get('college')
        current_user.department = request.form.get('department')
        current_user.semester = request.form.get('semester')
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
            
            # 2. Fetch 50 Questions
            category_map = {
                'General Knowledge': 9, 'Books': 10, 'Film': 11, 'Music': 12, 'Musicals & Theatres': 13,
                'Television': 14, 'Video Games': 15, 'Board Games': 16, 'Science & Nature': 17,
                'Computers': 18, 'Mathematics': 19, 'Mythology': 20, 'Sports': 21, 'Geography': 22,
                'History': 23, 'Politics': 24, 'Art': 25, 'Celebrities': 26, 'Animals': 27,
                'Vehicles': 28, 'Comics': 29, 'Gadgets': 30, 'Anime & Manga': 31, 'Cartoon & Animations': 32
            }
            tdb_id = category_map.get(name, 9)
            url = f"https://opentdb.com/api.php?amount=5&category={tdb_id}&type=multiple"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                data = json.loads(response.read())
                
                if data['response_code'] == 0:
                    for res in data['results']:
                        question_text = html.unescape(res['question'])
                        correct = html.unescape(res['correct_answer'])
                        incorrects = [html.unescape(ans) for ans in res['incorrect_answers']]
                        
                        all_opts = incorrects + [correct]
                        random.shuffle(all_opts)
                        correct_letter = chr(65 + all_opts.index(correct))
                        
                        # Add in all 3 languages
                        for lang in ['en', 'gu', 'hi']:
                            if lang == 'en':
                                q_text = question_text
                                opt_a = all_opts[0]
                                opt_b = all_opts[1]
                                opt_c = all_opts[2]
                                opt_d = all_opts[3]
                            else:
                                translator = GoogleTranslator(source='en', target=lang)
                                try:
                                    to_trans = [question_text, all_opts[0], all_opts[1], all_opts[2], all_opts[3]]
                                    translated = translator.translate_batch(to_trans)
                                    q_text = translated[0]
                                    opt_a = translated[1]
                                    opt_b = translated[2]
                                    opt_c = translated[3]
                                    opt_d = translated[4]
                                except Exception as e:
                                    print(f"Translation error: {e}")
                                    q_text = question_text
                                    opt_a = all_opts[0]
                                    opt_b = all_opts[1]
                                    opt_c = all_opts[2]
                                    opt_d = all_opts[3]

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
                    flash(f'Category "{name}" added with 50 questions in 3 languages!', 'success')
                else:
                    db.session.delete(cat)
                    db.session.commit()
                    flash(f'Failed to fetch questions from Trivia API for "{name}". The category was not added.', 'danger')
            except Exception as e:
                print(f"Error fetching questions: {e}")
                db.session.delete(cat)
                db.session.commit()
                flash(f'Error fetching questions for "{name}". The category was not added.', 'danger')
                
        return redirect(url_for('admin_categories'))
        
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

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
    flash(f'User {user_to_delete.name} has been deleted.', 'success')
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
