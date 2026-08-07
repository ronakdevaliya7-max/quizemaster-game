import os
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
