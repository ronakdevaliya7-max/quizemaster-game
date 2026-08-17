import os
import sys

# Add qgame to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'qgame'))

from qgame.app import app
from qgame.models import db, User, QuizAttempt, Category
from qgame.utils.certificates import generate_certificate

with app.app_context():
    # get a user, attempt and category
    user = User.query.first()
    attempt = QuizAttempt.query.first()
    category = Category.query.first()
    
    try:
        cert_id, file_path = generate_certificate(user, attempt, category)
        print("Success! File:", file_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
