import os
from app import app, db
from models import User, Category, Question, StoreItem
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database created.")
        
        # 1. Add Admin
        admin = User(
            username='admin',
            name='Administrator',
            password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin)
        
        # 2. Add Store Items
        items = [
            StoreItem(name="Novice Scholar", description="A title for beginners.", cost=100, item_type="title", css_class="text-gray-500 font-bold", icon="fas fa-star"),
            StoreItem(name="Quiz Master", description="A title for experts.", cost=500, item_type="title", css_class="text-yellow-500 font-bold", icon="fas fa-crown"),
            StoreItem(name="Gold Border", description="A shiny gold border for your profile.", cost=300, item_type="border", css_class="border-4 border-yellow-500", icon="fas fa-square"),
            StoreItem(name="Neon Border", description="A glowing neon border.", cost=600, item_type="border", css_class="border-4 border-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.8)]", icon="fas fa-square")
        ]
        db.session.add_all(items)
        
        # 3. Add Categories
        c1 = Category(name="General Knowledge", description="Test your general knowledge.", image_filename="gk.png")
        c2 = Category(name="Science", description="Test your science knowledge.", image_filename="science.png")
        db.session.add_all([c1, c2])
        db.session.commit()
        
        # 4. Add Questions
        # English
        q1_en = Question(category_id=c1.id, text="What is the capital of France?", option_a="Berlin", option_b="Madrid", option_c="Paris", option_d="Rome", correct_option="C", language="en")
        q2_en = Question(category_id=c2.id, text="What is the chemical symbol for water?", option_a="O2", option_b="H2O", option_c="CO2", option_d="HO", correct_option="B", language="en")
        
        # Gujarati
        q1_gu = Question(category_id=c1.id, text="ફ્રાન્સની રાજધાની કઈ છે?", option_a="બર્લિન", option_b="મેડ્રિડ", option_c="પેરિસ", option_d="રોમ", correct_option="C", language="gu")
        q2_gu = Question(category_id=c2.id, text="પાણીનું રાસાયણિક પ્રતીક શું છે?", option_a="O2", option_b="H2O", option_c="CO2", option_d="HO", correct_option="B", language="gu")
        
        # Hindi
        q1_hi = Question(category_id=c1.id, text="फ्रांस की राजधानी क्या है?", option_a="बर्लिन", option_b="मैड्रिड", option_c="पेरिस", option_d="रोम", correct_option="C", language="hi")
        q2_hi = Question(category_id=c2.id, text="पानी का रासायनिक प्रतीक क्या है?", option_a="O2", option_b="H2O", option_c="CO2", option_d="HO", correct_option="B", language="hi")
        
        db.session.add_all([q1_en, q2_en, q1_gu, q2_gu, q1_hi, q2_hi])
        db.session.commit()
        print("Database seeded with sample data in English, Gujarati, and Hindi.")

if __name__ == '__main__':
    init_db()
