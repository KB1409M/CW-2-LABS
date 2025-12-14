from app.data.db import connect_database

def insert_dataset(name, description, source, created_at):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (name, description, source, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, description, source, created_at))
    conn.commit()
    conn.close()
