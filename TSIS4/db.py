"""
db.py — PostgreSQL persistence layer for TSIS4 Snake game.
Uses psycopg2. Connection details come from config.py.
"""
import psycopg2
from config import DB_CONFIG


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create tables if they don't exist."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id           SERIAL PRIMARY KEY,
                    player_id    INTEGER   NOT NULL REFERENCES players(id),
                    score        INTEGER   NOT NULL,
                    level_reached INTEGER  NOT NULL,
                    played_at    TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()


def get_or_create_player(username: str) -> int:
    """Return the player's id, creating the row if needed."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            pid = cur.fetchone()[0]
        conn.commit()
    return pid


def save_result(username: str, score: int, level_reached: int):
    """Save a completed game session to the database."""
    pid = get_or_create_player(username)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) "
                "VALUES (%s, %s, %s)",
                (pid, score, level_reached)
            )
        conn.commit()


def get_personal_best(username: str) -> int | None:
    """Return the player's highest score ever, or None."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(gs.score)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s
            """, (username,))
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else None


def get_top10():
    """Return list of (rank, username, score, level, played_at) for top 10."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username,
                       gs.score,
                       gs.level_reached,
                       gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
    return [(i + 1, r[0], r[1], r[2], r[3]) for i, r in enumerate(rows)]