import os
import sys

base_dir = r"d:\project\qgame\qgame"
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from qgame.app import app, db
from sqlalchemy import text

def add_column(engine, table_name, column_name, column_type):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
            conn.commit()
            print(f"Added column {column_name} to {table_name}")
    except Exception as e:
        print(f"Column {column_name} might already exist or error: {e}")

with app.app_context():
    engine = db.engine
    
    # Question table new columns
    columns = [
        ("board", "VARCHAR(50)"),
        ("standard", "VARCHAR(50)"),
        ("stream", "VARCHAR(50)"),
        ("subject", "VARCHAR(100)"),
        ("chapter", "VARCHAR(100)"),
        ("topic", "VARCHAR(100)"),
        
        ("question_en", "TEXT"),
        ("question_gu", "TEXT"),
        ("question_hi", "TEXT"),
        
        ("option_a_en", "VARCHAR(255)"),
        ("option_b_en", "VARCHAR(255)"),
        ("option_c_en", "VARCHAR(255)"),
        ("option_d_en", "VARCHAR(255)"),
        
        ("option_a_gu", "VARCHAR(255)"),
        ("option_b_gu", "VARCHAR(255)"),
        ("option_c_gu", "VARCHAR(255)"),
        ("option_d_gu", "VARCHAR(255)"),
        
        ("option_a_hi", "VARCHAR(255)"),
        ("option_b_hi", "VARCHAR(255)"),
        ("option_c_hi", "VARCHAR(255)"),
        ("option_d_hi", "VARCHAR(255)"),
        
        ("explanation_en", "TEXT"),
        ("explanation_gu", "TEXT"),
        ("explanation_hi", "TEXT"),
        
        ("source", "VARCHAR(255)"),
        ("source_type", "VARCHAR(100)"),
        ("verified", "BOOLEAN DEFAULT 0"),
        ("created_at", "DATETIME")
    ]
    
    for col_name, col_type in columns:
        add_column(engine, "question", col_name, col_type)
        
    print("Schema update script completed.")
