import os
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Category, Topic, LearningSection, Question, Badge

def recreate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # 1. Add Admin
        admin = User(
            username='admin',
            name='Administrator',
            password_hash=generate_password_hash('admin123', method='scrypt'),
            role='admin'
        )
        db.session.add(admin)
        
        # 2. Add Test User
        user = User(
            username='user',
            name='Test Student',
            password_hash=generate_password_hash('user123', method='scrypt'),
            role='user'
        )
        db.session.add(user)
        
        # 3. Add Badges
        badges = [
            Badge(name="First Blood", description="Take your first quiz", requirement_type="first_quiz", requirement_value=1),
            Badge(name="Perfect Score", description="Get 100% on a quiz", requirement_type="perfect_score", requirement_value=1),
            Badge(name="Centurion", description="Earn 100 points", requirement_type="points", requirement_value=100)
        ]
        db.session.bulk_save_objects(badges)
        
        # 4. Add Categories and Topics
        cat_python = Category(name='Python Programming', description='Master Python from scratch.')
        db.session.add(cat_python)
        db.session.commit()
        
        topic_vars = Topic(
            category_id=cat_python.id,
            title='Python Variables & Data Types',
            description='Learn the fundamental building blocks of Python data.',
            reading_time=8,
            difficulty='Beginner'
        )
        db.session.add(topic_vars)
        db.session.commit()
        
        # 5. Add Learning Sections
        sec1 = LearningSection(
            topic_id=topic_vars.id,
            title='Introduction to Variables',
            content_html='<p>Variables are containers for storing data values. In Python, a variable is created the moment you first assign a value to it.</p><pre><code>x = 5\ny = "Hello, World!"</code></pre>',
            order=1
        )
        sec2 = LearningSection(
            topic_id=topic_vars.id,
            title='Data Types',
            content_html='<p>Python has the following data types built-in by default:</p><ul><li><b>Text Type:</b> str</li><li><b>Numeric Types:</b> int, float, complex</li><li><b>Sequence Types:</b> list, tuple, range</li></ul><div class="note" style="padding:1rem;background:rgba(255,193,7,0.2);border-left:4px solid #ffc107;margin-top:10px;"><b>Remember:</b> Python is dynamically typed. You do not need to declare a type.</div>',
            order=2
        )
        db.session.add_all([sec1, sec2])
        
        # 6. Add Questions
        q1 = Question(
            topic_id=topic_vars.id,
            text='How do you create a variable with the numeric value 5?',
            option_a='x = 5', option_b='int x = 5', option_c='x = int(5)', option_d='Both A and C',
            correct_option='D'
        )
        q2 = Question(
            topic_id=topic_vars.id,
            text='Which of these is NOT a Python data type?',
            option_a='List', option_b='Dictionary', option_c='Float', option_d='Real',
            correct_option='D'
        )
        q3 = Question(
            topic_id=topic_vars.id,
            text='What is the correct file extension for Python files?',
            option_a='.pt', option_b='.pyt', option_c='.py', option_d='.python',
            correct_option='C'
        )
        db.session.add_all([q1, q2, q3])
        
        db.session.commit()
        print("Database recreated and seeded with LMS Data successfully!")

if __name__ == '__main__':
    recreate_db()
