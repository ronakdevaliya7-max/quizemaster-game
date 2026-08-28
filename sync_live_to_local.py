import sys
import os
sys.path.append(r"d:\project\qgame\qgame")

from app import app, db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Database URIs
sqlite_uri = 'sqlite:///d:/project/qgame/qgame/quizmaster.db'
pg_uri = 'postgresql://qdb_2ngq_user:VMyWIQN3JNKaOW43nwJG21RpOf5lyo5N@dpg-da6nbonavr4c739edgog-a.singapore-postgres.render.com/qdb_2ngq'

sqlite_engine = create_engine(sqlite_uri)
pg_engine = create_engine(pg_uri)

# Create a session for Postgres
metadata = MetaData()
metadata.reflect(bind=pg_engine)
PgSession = sessionmaker(bind=pg_engine)
pg_session = PgSession()

# Set DB URI to SQLite before context
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri

# Create tables in SQLite and drop everything first
with app.app_context():
    print("Wiping local SQLite database completely...")
    db.drop_all()
    print("Recreating tables in local SQLite database...")
    db.create_all()

# Import the exact models that exist in models.py
from models import (
    User, Category, Question, QuizAttempt, Certificate, 
    Badge, UserBadge, StoreItem, UserInventory, 
    LiveSession, LiveParticipant
)

# Define migration order (parents first, then children to maintain foreign keys)
models = [
    Category,
    StoreItem,
    Badge,
    User,
    Question,
    QuizAttempt,
    Certificate,
    UserBadge,
    UserInventory,
    LiveSession,
    LiveParticipant
]

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri
    
    for model in models:
        print(f"Syncing {model.__name__} from live to local...")
        try:
            records = pg_session.query(model).all()
            count = 0
            for r in records:
                # Merge instance state into the local db session.
                # db.session.merge is used to ensure instance state is handled properly 
                # instead of direct add which causes conflicts.
                db.session.merge(r)
                count += 1
            db.session.commit()
            print(f" -> Migrated {count} records for {model.__name__}")
        except Exception as e:
            db.session.rollback()
            print(f" -> Failed to sync {model.__name__}: {e}")
            
    print("Reverse sync (Live -> Local) completed successfully!")
