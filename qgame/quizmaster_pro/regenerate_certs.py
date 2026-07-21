from app import app, db
from models import Certificate, QuizAttempt, User, Category
from utils.certificates import generate_certificate
import os

def regenerate():
    with app.app_context():
        certs = Certificate.query.all()
        for c in certs:
            attempt = QuizAttempt.query.get(c.attempt_id)
            user = User.query.get(c.user_id)
            category = Category.query.get(attempt.category_id)
            
            # Generate new one
            cert_id, file_path = generate_certificate(user, attempt, category)
            
            # Update DB record
            c.certificate_id = cert_id
            c.file_path = file_path
            
        db.session.commit()
        print(f"Regenerated {len(certs)} certificates.")

if __name__ == '__main__':
    regenerate()
