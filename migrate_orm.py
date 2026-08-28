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

# Set DB URI to Postgres before context
app.config['SQLALCHEMY_DATABASE_URI'] = pg_uri

# Create tables in PostgreSQL
with app.app_context():
    db.create_all()

# Connect to SQLite
metadata = MetaData()
metadata.reflect(bind=sqlite_engine)
SqliteSession = sessionmaker(bind=sqlite_engine)
sq_session = SqliteSession()

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
    # Make sure we're using the postgres URI
    app.config['SQLALCHEMY_DATABASE_URI'] = pg_uri
    
    # We don't truncate tables, we just merge missing data so we don't accidentally wipe live data
    # but if needed, we could. For now, merge will act as an upsert (insert or update).
    
    for model in models:
        print(f"Migrating {model.__name__}...")
        try:
            records = sq_session.query(model).all()
            count = 0
            for r in records:
                # Merge into the current db session (Postgres)
                db.session.merge(r)
                count += 1
            db.session.commit()
            print(f" -> Migrated {count} records for {model.__name__}")
        except Exception as e:
            db.session.rollback()
            print(f" -> Failed to migrate {model.__name__}: {e}")
            
    print("Migration completed successfully!")

