
import pandas as pd
import sqlite3
import logging




# df_chess_games.to_sql('chess_games', conn, if_exists='append')
# df_players.to_sql('players', conn, if_exists='append')

def create_tables(conn):
    conn.execute("PRAGMA foreign_keys = ON")
    # drop tables Is Exist
    conn.execute("DROP TABLE IF EXISTS chess_games")
    conn.execute("DROP TABLE IF EXISTS openings")
    conn.execute("DROP TABLE IF EXISTS players")
    # Create Player Table
    conn.execute("""
          CREATE TABLE players (
              username     TEXT    PRIMARY KEY NOT NULL,
              display_name TEXT,
              country      TEXT,
              registered_year INTEGER,
              rating_registry  INTEGER,
              total_games_registry INTEGER DEFAULT 0,
              account_status TEXT,
              email_verified INTEGER DEFAULT 0,
              join_platform TEXT
          )
      """)

    # Create openings Table
    conn.execute("""
          CREATE TABLE openings (
              opening_code TEXT PRIMARY KEY NOT NULL,
              opening_shortname TEXT NOT NULL,
              opening_fullname  TEXT NOT NULL,          )
      """)

    # Create chess_games Table
    conn.execute("""
         CREATE TABLE chess_games (
             game_id        INTEGER PRIMARY KEY NOT NULL,
             white_id       TEXT    NOT NULL REFERENCES players(username),
             black_id       TEXT    NOT NULL REFERENCES players(username),
             winner         TEXT    NOT NULL CHECK(winner IN ('White', 'Black', 'Draw')),
             victory_status TEXT    NOT NULL CHECK(victory_status IN ('Mate', 'Resign', 'Out of Time', 'Draw')),
             turns INTEGER NOT NULL CHECK(turns >= 1),
             time_increment TEXT    NOT NULL,
             rated INTEGER NOT NULL CHECK(rated IN (0, 1)),
             opening_code  TEXT  NOT NULL REFERENCES openings(opening_code),
             white_rating   INTEGER NOT NULL,
             black_rating   INTEGER NOT NULL,
             moves          TEXT,
             opening_moves  INTEGER
         )
     """)

def add_indexes(conn):

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_white_id ON chess_games(white_id)",
        "CREATE INDEX IF NOT EXISTS idx_black_id ON chess_games(black_id)",
        "CREATE INDEX IF NOT EXISTS idx_openings_code ON openings(opening_code)",
        "CREATE INDEX IF NOT EXISTS idx_winner ON chess_games(winner)",
        "CREATE INDEX IF NOT EXISTS idx_players_country ON players(country)",
    ]

    for idx in indexes:
        conn.execute(idx)

def load_players(conn):
    df = pd.read_csv("../data/raw/player.csv")

    df['registered_year'] = df['registered_year'].where(pd.notna(df['registered_year']), None)
    df['email_verified'] = df['email_verified'].fillna(0).astype(int)
    df['total_games_registry'] = df['total_games_registry'].fillna(0).astype(int)

    df.to_sql('players', conn, if_exists='append', index=False)

def main():
    # create Database
    conn = sqlite3.connect('chess.db')
    # setup logging
    logging.basicConfig()
    # First Log
    log = logging.getLogger(__name__)





