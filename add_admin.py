from qgame.app import app
from qgame.models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = "quize app"
    password = "quize886644"
    user = User.query.filter_by(username=username).first()
    if user:
        user.password_hash = generate_password_hash(password)
        user.role = 'admin'
        print("Updated existing user to admin with new password.")
    else:
        new_admin = User(
            username=username,
            password_hash=generate_password_hash(password),
            role='admin',
            name="Admin"
        )
        db.session.add(new_admin)
        print("Created new admin user.")
    db.session.commit()
