import sqlite3

# Create SQLite database
def init_db():
    conn = sqlite3.connect('dander.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            distance REAL
        )
    ''')  # Create table with a primary key
    conn.commit()
    conn.close()

# Store distance data
def store_distance(name, distance):
    with sqlite3.connect('dander.db') as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO users (name, distance) VALUES (?, ?)''', (name, distance))
        conn.commit()

# Retrieve distance data
def get_distance(name):
    with sqlite3.connect('dander.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT distance FROM users WHERE name=?''', (name,))
        result = c.fetchone()
        return result[0] if result else 0