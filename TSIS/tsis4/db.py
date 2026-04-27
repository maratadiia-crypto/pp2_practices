import psycopg2


def connect():
    return psycopg2.connect(
        dbname="snake_db",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_player_id(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM players WHERE username = %s;",
        (username,)
    )

    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES(%s) RETURNING id;",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return player_id


def save_session(username, score, level):
    player_id = get_player_id(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO game_sessions(player_id, score, level)
        VALUES (%s, %s, %s);
        """,
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_personal_best(username):
    player_id = get_player_id(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COALESCE(MAX(score), 0)
        FROM game_sessions
        WHERE player_id = %s;
        """,
        (player_id,)
    )

    best = cur.fetchone()[0]

    cur.close()
    conn.close()

    return best


def get_leaderboard():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, MAX(g.score) AS best_score, MAX(g.level) AS best_level
        FROM players p
        JOIN game_sessions g ON p.id = g.player_id
        GROUP BY p.username
        ORDER BY best_score DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows