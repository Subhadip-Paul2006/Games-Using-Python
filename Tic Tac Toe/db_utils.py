"""
Database Utilities for Tic Tac Toe
Comprehensive testing and verification script
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "tictactoe_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        return conn
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def test_connection():
    """Test database connection"""
    print("=" * 50)
    print("1. Testing Database Connection")
    print("=" * 50)
    conn = get_connection()
    if conn:
        print("✓ Connection successful!")
        conn.close()
        return True
    else:
        print("✗ Connection failed!")
        return False

def check_table_structure():
    """Check if table exists and show its structure"""
    print("\n" + "=" * 50)
    print("2. Checking Table Structure")
    print("=" * 50)
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'tictactoe_games'
            );
            """)
        exists = cur.fetchone()[0]
        
        if not exists:
            print("✗ Table 'tictactoe_games' does NOT exist!")
            print("\nCreating table...")
            cur.execute("""
                CREATE TABLE tictactoe_games (
                    game_number SERIAL PRIMARY KEY,
                    player_01 VARCHAR(100) NOT NULL,
                    player_02 VARCHAR(100) NOT NULL,
                    game_status VARCHAR(100) NOT NULL,
                    game_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✓ Table created successfully!")
        else:
            print("✓ Table 'tictactoe_games' exists!")
        
        # Show table structure
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'tictactoe_games'
            ORDER BY ordinal_position;
        """)
        
        print("\nTable Structure:")
        print("-" * 50)
        for row in cur.fetchall():
            print(f"  {row[0]:<15} {row[1]:<20} NULL: {row[2]}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return False

def test_insert():
    """Test inserting a record"""
    print("\n" + "=" * 50)
    print("3. Testing Insert Operation")
    print("=" * 50)
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tictactoe_games (player_01, player_02, game_status)
            VALUES (%s, %s, %s)
            RETURNING game_number;
        """, ("TestPlayer1", "TestPlayer2", "Winner: TestPlayer1"))
        
        inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✓ Test record inserted successfully! (Game Number: {inserted_id})")
        return True
        
    except Exception as e:
        print(f"❌ Insert Error: {e}")
        conn.close()
        return False

def view_recent_games(limit=5):
    """View recent game logs"""
    print("\n" + "=" * 50)
    print(f"4. Recent Game Logs (Last {limit})")
    print("=" * 50)
    conn = get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT game_number, player_01, player_02, game_status, game_timeFROM tictactoe_gamesORDER BY game_time DESCLIMIT {limit};""")
        
        rows = cur.fetchall()
        if not rows:
            print("No games found in database.")
        else:
            print(f"\n{'#':<5} {'Player 1':<15} {'Player 2':<15} {'Status':<20} {'Date'}")
            print("-" * 85)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20} {row[4]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()

def delete_test_records():
    conn = get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""DELETE FROM tictactoe_games WHERE player_01 = 'TestPlayer1' AND player_02 = 'TestPlayer2';""")
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted > 0:
            print(f"\n✓ Cleaned up {deleted} test record(s)")
        
    except Exception as e:
        print(f"❌ Cleanup Error: {e}")
        conn.close()

if __name__ == "__main__":
    print("\n🎮 TIC TAC TOE - Database Utilities 🎮\n")
    
    if test_connection():
        check_table_structure()
        test_insert()
        view_recent_games()
        delete_test_records()
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50 + "\n")
