import psycopg2
import os

# PostgreSQL connection parameters
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "subh06",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def check_user(username, password):
    conn = get_db_connection()
    if not conn: return None
    try:
        c = conn.cursor()
        c.execute("SELECT firstname, gender FROM USERS WHERE username = %s AND password = %s", (username, password))
        data = c.fetchone()
        return data  # Returns (firstname, gender) or None
    finally:
        conn.close()

def register_user(fname, lname, username, password, gender):
    conn = get_db_connection()
    if not conn: return False
    try:
        c = conn.cursor()
        c.execute("INSERT INTO USERS (firstname, lastname, username, password, gender) VALUES (%s, %s, %s, %s, %s)",
                  (fname, lname, username, password, gender))
        c.execute("INSERT INTO LEADERBOARD (firstname, GamesWon, GamesLost, GamesTied, GamesPlayed, WiningRate) VALUES (%s, 0, 0, 0, 0, 0)",
                  (fname,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False
    finally:
        conn.close()

def update_leaderboard(username, user_won, comp_won, is_tie):
    conn = get_db_connection()
    if not conn: return
    try:
        c = conn.cursor()
        c.execute("SELECT GamesWon, GamesLost, GamesTied, GamesPlayed FROM LEADERBOARD WHERE firstname = %s", (username,))
        data = c.fetchone()
        if data:
            won, lost, tied, played = data
            if is_tie:
                tied += 1
            elif user_won > comp_won:
                won += 1
            else:
                lost += 1
            played += 1
            rate = round(won / played, 2) if played > 0 else 0
            
            c.execute("""
                UPDATE LEADERBOARD SET GamesWon = %s, GamesLost = %s, GamesTied = %s, GamesPlayed = %s, WiningRate = %s        
                WHERE firstname = %s""", (won, lost, tied, played, rate, username))
            conn.commit()
    finally:
        conn.close()

def get_leaderboard_data():
    conn = get_db_connection()
    if not conn: return []
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM LEADERBOARD ORDER BY GamesWon DESC")
        return c.fetchall()
    finally:
        conn.close()
