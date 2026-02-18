import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "postgres"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "password")
            )
            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None

    def log_game(self, player1_name, player2_name, winner_name):
        if not self.conn:
            print("No database connection. Game result not logged.")
            return

        try:
            cur = self.conn.cursor()
            query = """INSERT INTO tictactoe_games (player_01, player_02, game_status) VALUES (%s, %s, %s);"""
            
            game_status = f"Winner: {winner_name}"
            cur.execute(query, (player1_name, player2_name, game_status))
            self.conn.commit()
            cur.close()
            print("Game result logged successfully.")
        except Exception as e:
            print(f"Error logging game result: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
