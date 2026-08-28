import sys
import os
sys.path.append(r"d:\project\qgame\qgame")

from app import app, db
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

sqlite_uri = 'sqlite:///d:/project/qgame/qgame/quizmaster.db'
pg_uri = 'postgresql://qdb_2ngq_user:VMyWIQN3JNKaOW43nwJG21RpOf5lyo5N@dpg-da6nbonavr4c739edgog-a.singapore-postgres.render.com/qdb_2ngq'

sqlite_engine = create_engine(sqlite_uri)
pg_engine = create_engine(pg_uri)

print("Creating tables in Postgres...")
# Force creation using the pg_engine
db.metadata.create_all(bind=pg_engine)

print("Reflecting SQLite...")
sqlite_metadata = MetaData()
sqlite_metadata.reflect(bind=sqlite_engine)

for table in sqlite_metadata.sorted_tables:
    if table.name == 'alembic_version':
        continue
    print(f"Copying table {table.name}...")
    with sqlite_engine.connect() as sq_conn:
        rows = sq_conn.execute(table.select()).mappings().all()
    
    if rows:
        # Convert to pure dicts
        dicts = [dict(r) for r in rows]
        with pg_engine.begin() as pg_conn:
            # Clear table first to avoid conflicts if rerunning
            pg_conn.execute(text(f'TRUNCATE TABLE "{table.name}" CASCADE'))
            
            # Insert data
            pg_conn.execute(table.insert(), dicts)
            
            # Reset sequence if id column exists
            if 'id' in table.columns and table.columns['id'].type.python_type == int:
                seq_name = f"{table.name}_id_seq"
                try:
                    pg_conn.execute(text(f'SELECT setval(\'"{seq_name}"\', COALESCE((SELECT MAX(id)+1 FROM "{table.name}"), 1), false);'))
                except Exception as e:
                    print(f"Sequence reset error for {table.name}: {e}")

print("Migration completed successfully!")
