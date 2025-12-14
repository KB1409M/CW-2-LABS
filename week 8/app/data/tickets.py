from app.data.db import connect_database

def insert_ticket(title, description, priority, status, created_at):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets (title, description, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, priority, status, created_at))
    conn.commit()
    conn.close()
