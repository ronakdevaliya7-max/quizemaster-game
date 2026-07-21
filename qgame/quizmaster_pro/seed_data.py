import os
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Category, Question, Badge, StoreItem

def seed_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Admins and Users
        admin = User(username='admin', name='Administrator', password_hash=generate_password_hash('admin123', method='scrypt'), role='admin')
        user = User(username='user', name='Test Student', password_hash=generate_password_hash('user123', method='scrypt'), role='user')
        db.session.add_all([admin, user])
        
        # Store Items
        store_items = [
            StoreItem(name='Gold Ring', description='A beautiful shiny gold ring for your profile border.', cost=500, item_type='border', css_class='border-gold', icon='fas fa-ring text-warning'),
            StoreItem(name='Silver Ring', description='A sleek silver ring for your profile border.', cost=250, item_type='border', css_class='border-silver', icon='fas fa-ring text-secondary'),
            StoreItem(name='Diamond Ring', description='A shining diamond border.', cost=1000, item_type='border', css_class='border-diamond', icon='fas fa-gem text-info'),
            StoreItem(name='Ruby Ring', description='A glowing ruby border.', cost=800, item_type='border', css_class='border-ruby', icon='fas fa-fire text-danger'),
            StoreItem(name='Quiz Master', description='Show everyone who the real master is.', cost=1000, item_type='title', css_class='title-master', icon='fas fa-crown text-warning'),
            StoreItem(name='Pro Player', description='A title for the pros.', cost=500, item_type='title', css_class='title-pro', icon='fas fa-star text-info'),
            StoreItem(name='Legend', description='A legendary player.', cost=2000, item_type='title', css_class='title-legend', icon='fas fa-dragon text-danger'),
            StoreItem(name='Expert', description='An expert at quizzes.', cost=1500, item_type='title', css_class='title-expert', icon='fas fa-book-open text-primary'),
            StoreItem(name='Rookie', description='Just starting out.', cost=100, item_type='title', css_class='title-rookie', icon='fas fa-seedling text-success')
        ]
        db.session.add_all(store_items)
        
        # Badges
        badges = [
            Badge(name="First Blood", description="Take your first quiz", requirement_type="first_quiz", requirement_value=1),
            Badge(name="Perfect Score", description="Get 100% on a quiz", requirement_type="perfect_score", requirement_value=1),
            Badge(name="Centurion", description="Earn 100 points", requirement_type="points", requirement_value=100)
        ]
        db.session.bulk_save_objects(badges)
        
        # 10 Categories
        subjects = ['Python', 'Mathematics', 'General Knowledge', 'Science', 'History', 'Geography', 'Technology', 'Sports', 'Literature', 'Art']
        categories = []
        for s in subjects:
            c = Category(name=s, description=f'Test your skills in {s}.')
            categories.append(c)
        db.session.add_all(categories)
        db.session.commit()
        
        # Add 50 questions to each
        for c in categories:
            for i in range(1, 51):
                q = Question(
                    category_id=c.id,
                    text=f'{c.name} Question {i}: What is the correct answer?',
                    option_a='Option A (Correct)',
                    option_b='Option B',
                    option_c='Option C',
                    option_d='Option D',
                    correct_option='A',
                    difficulty='Easy'
                )
                db.session.add(q)
        
        db.session.commit()
        print("Database reverted and seeded with 10 subjects and 50 questions each.")

if __name__ == '__main__':
    seed_db()
