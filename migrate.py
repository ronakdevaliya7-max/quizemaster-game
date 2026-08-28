import sys
import os
sys.path.append(r"d:\project\qgame\qgame")

from app import app, db
from sqlalchemy import create_engine, MetaData, text

sqlite_uri = 'sqlite:///d:/project/qgame/qgame/quizmaster.db'
pg_uri = 'postgresql://qdb_2ngq_user:VMyWIQN3JNKaOW43nwJG21RpOf5lyo5N@dpg-da6nbonavr4c739edgog-a.singapore-postgres.render.com/qdb_2ngq'

sqlite_engine = create_engine(sqlite_uri)
pg_engine = create_engine(pg_uri)

metadata = MetaData()
# reflect from SQLite
metadata.reflect(bind=sqlite_engine)

print("Creating tables in Postgres...")
db.metadata.create_all(bind=pg_engine)

print("Copying data...")
for table in metadata.sorted_tables:
    if table.name == 'alembic_version':
        continue
    print(f"Copying table {table.name}...")
    with sqlite_engine.connect() as sq_conn:
        rows = sq_conn.execute(table.select()).fetchall()
    
    if rows:
        with pg_engine.begin() as pg_conn:
            # try to convert to dicts
            dicts = []
            for row in rows:
                if hasattr(row, '_mapping'):
                    dicts.append(dict(row._mapping))
                elif hasattr(row._fields):
                    dicts.append(dict(zip(row._fields, row)))
                else:
                    # fallback
                    d = {}
                    for col in table.columns:
                        d[col.name] = getattr(row, col.name)
                    dicts.append(d)
            
            pg_conn.execute(table.insert(), dicts)
            
            # Reset the sequence for postgres if there's an id column
            if 'id' in table.columns and table.columns['id'].type.python_type == int:
                seq_name = f"{table.name}_id_seq"
                try:
                    pg_conn.execute(text(f"SELECT setval('{seq_name}', COALESCE((SELECT MAX(id)+1 FROM {table.name}), 1), false);"))
                except Exception as e:
                    print(f"Could not reset sequence for {table.name}: {e}")

print("Migration completed successfully!")
