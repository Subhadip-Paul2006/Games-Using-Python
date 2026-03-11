"""
╔══════════════════════════════════════════════════════╗
║       DATABASE MANAGER — Minesweeper Scores          ║
║  PostgreSQL backend for tracking high scores.        ║
║  Falls back gracefully if database is unavailable.   ║
╚══════════════════════════════════════════════════════╝

Requires:  pip install psycopg2-binary
"""

import datetime

# ── Optional psycopg2 import ────────────────────────────────────────────────
try:
    import psycopg2
    from psycopg2 import sql
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════
#  DATABASE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "user":     "postgres",
    "password": "subh06",
    "database": "minesweeper_db",
}


# ═══════════════════════════════════════════════════════════════════════════
#  DATABASE MANAGER CLASS
# ═══════════════════════════════════════════════════════════════════════════
class DatabaseManager:
    """
    Handles all PostgreSQL operations for the Minesweeper high-score system.

    Features:
      • Auto-creates the database and table on first run
      • Inserts scores (win or loss)
      • Retrieves best score per difficulty
      • Retrieves top N scores per difficulty
      • Gracefully degrades to no-op if PostgreSQL is unreachable

    Usage:
        db = DatabaseManager()
        if db.available:
            db.insert_score("Rahul", "Easy", 45, "Win")
            best = db.get_best_score("Easy")  # ("Rahul", 45, datetime)
    """

    def __init__(self):
        self.available = False    # Set to True only after successful connection
        self._conn = None
        self._cursor = None

        if not PSYCOPG2_AVAILABLE:
            print("[DB] psycopg2 not installed. Database features disabled.")
            return

        # Step 1: Ensure the database exists
        if not self._ensure_database_exists():
            return

        # Step 2: Connect to the minesweeper_db database
        if not self._connect():
            return

        # Step 3: Create the table (and index) if they don't exist
        if not self._create_table():
            return

        self.available = True
        print("[DB] Connected to PostgreSQL — high scores enabled.")

    # ─────────────────────────────────────────────────────────────────────────
    #  SETUP METHODS
    # ─────────────────────────────────────────────────────────────────────────

    def _ensure_database_exists(self) -> bool:
        """
        Connect to the default 'postgres' database and create
        'minesweeper_db' if it does not already exist.
        """
        try:
            # Connect to default 'postgres' database to run admin commands
            conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database="postgres",
            )
            conn.autocommit = True  # CREATE DATABASE cannot run inside a transaction
            cursor = conn.cursor()

            # Check if our database already exists
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (DB_CONFIG["database"],)
            )
            if cursor.fetchone() is None:
                # Database does not exist — create it
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(DB_CONFIG["database"])
                    )
                )
                print(f"[DB] Created database '{DB_CONFIG['database']}'.")
            else:
                print(f"[DB] Database '{DB_CONFIG['database']}' already exists.")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"[DB] Could not ensure database exists: {e}")
            return False

    def _connect(self) -> bool:
        """Open a persistent connection to the minesweeper_db database."""
        try:
            self._conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
            )
            self._conn.autocommit = True
            self._cursor = self._conn.cursor()
            return True
        except Exception as e:
            print(f"[DB] Connection failed: {e}")
            return False

    def _create_table(self) -> bool:
        """
        Create the high_scores table with:
          • CHECK constraint on difficulty
          • result column for Win/Loss tracking
          • Index on (difficulty, time_seconds) for fast lookups
        """
        try:
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS high_scores (
                    id           SERIAL PRIMARY KEY,
                    player_name  VARCHAR(100)  NOT NULL,
                    difficulty   VARCHAR(20)   NOT NULL
                                 CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
                    time_seconds INTEGER       NOT NULL,
                    result       VARCHAR(10)   NOT NULL DEFAULT 'Win'
                                 CHECK (result IN ('Win', 'Loss')),
                    played_at    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Index for fast best-score lookups by difficulty + time
            self._cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_difficulty_time
                ON high_scores(difficulty, time_seconds);
            """)

            print("[DB] Table 'high_scores' is ready.")
            return True

        except Exception as e:
            print(f"[DB] Failed to create table: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    #  SCORE OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────

    def insert_score(self, player_name: str, difficulty: str,
                     time_seconds: int, result: str = "Win") -> bool:
        """
        Insert a new score record.

        Args:
            player_name:  The player's display name.
            difficulty:   'Easy', 'Medium', or 'Hard'.
            time_seconds: Completion time in whole seconds.
            result:       'Win' or 'Loss'.

        Returns:
            True if inserted successfully, False otherwise.
        """
        if not self.available:
            return False
        try:
            self._cursor.execute(
                """
                INSERT INTO high_scores (player_name, difficulty, time_seconds, result)
                VALUES (%s, %s, %s, %s)
                """,
                (player_name, difficulty, time_seconds, result),
            )
            return True
        except Exception as e:
            print(f"[DB] Insert failed: {e}")
            return False

    def get_best_score(self, difficulty: str):
        """
        Retrieve the best (lowest time) winning score for a difficulty.

        Returns:
            A tuple (player_name, time_seconds, played_at) or None if no
            winning scores exist for this difficulty.
        """
        if not self.available:
            return None
        try:
            self._cursor.execute(
                """
                SELECT player_name, time_seconds, played_at
                FROM high_scores
                WHERE difficulty = %s AND result = 'Win'
                ORDER BY time_seconds ASC
                LIMIT 1
                """,
                (difficulty,),
            )
            row = self._cursor.fetchone()
            if row:
                return {
                    "player_name":  row[0],
                    "time_seconds": row[1],
                    "played_at":    row[2],
                }
            return None
        except Exception as e:
            print(f"[DB] Query failed: {e}")
            return None

    def get_top_scores(self, difficulty: str, limit: int = 5):
        """
        Retrieve the top N winning scores for a difficulty.

        Returns:
            A list of dicts with keys: player_name, time_seconds, played_at.
            Returns an empty list on failure.
        """
        if not self.available:
            return []
        try:
            self._cursor.execute(
                """
                SELECT player_name, time_seconds, played_at
                FROM high_scores
                WHERE difficulty = %s AND result = 'Win'
                ORDER BY time_seconds ASC
                LIMIT %s
                """,
                (difficulty, limit),
            )
            rows = self._cursor.fetchall()
            return [
                {
                    "player_name":  r[0],
                    "time_seconds": r[1],
                    "played_at":    r[2],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[DB] Query failed: {e}")
            return []

    def is_new_record(self, difficulty: str, time_seconds: int) -> bool:
        """
        Check if the given time would beat the current best score.

        Returns True if there is no existing record or the time is lower.
        """
        best = self.get_best_score(difficulty)
        if best is None:
            return True
        return time_seconds < best["time_seconds"]

    # ─────────────────────────────────────────────────────────────────────────
    #  UTILITY
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def format_time(seconds) -> str:
        """Format seconds as MM:SS string."""
        if seconds is None:
            return "–"
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"

    def close(self):
        """Close the database connection cleanly."""
        try:
            if self._cursor:
                self._cursor.close()
            if self._conn:
                self._conn.close()
            print("[DB] Connection closed.")
        except Exception:
            pass
