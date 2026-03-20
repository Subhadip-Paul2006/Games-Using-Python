import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="subh06",
        host="localhost",
        port="5432"
    )

def create():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS USERS(
    firstname text,
    lastname text,
    username text,
    password text,
    gender text
    )
    """)
    conn.commit()
    conn.close()
    print("USERS table created")

def LeaderboardCreate():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS LEADERBOARD(
    firstname text,
    GamesWon int,
    GamesLost int,
    GamesTied int,
    GamesPlayed int,
    WiningRate real
    )
    """)
    conn.commit()
    conn.close()
    print("LEADERBOARD table created")

create()
LeaderboardCreate()
