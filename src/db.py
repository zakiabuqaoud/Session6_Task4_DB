
import pandas as pd
import sqlite3
import logging

# //////////////////// Stage 0 ////////////////////////

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
              join_platform TEXT );
      """)
    logging.info("Players Table is created:-")
    # Create openings Table
    conn.execute("""
          CREATE TABLE openings (
              opening_code TEXT PRIMARY KEY NOT NULL,
              opening_shortname TEXT NOT NULL,
              opening_fullname  TEXT NOT NULL);
    """)
    logging.info("openings Table is created:-")

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
         );
     """)
    logging.info("chess_games Table is created:-")
    print("Finish create_tables Method:-")



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
    logging.info("Indexes is added on columns:-")

def load_players(conn):
    df = pd.read_csv("../data/raw/player.csv")

    df['registered_year'] = df['registered_year'].where(pd.notna(df['registered_year']), None)
    df['email_verified'] = df['email_verified'].fillna(0).astype(int)
    df['total_games_registry'] = df['total_games_registry'].fillna(0).astype(int)

    df.to_sql('players', conn, if_exists='append', index=False)
    logging.info("Players Data is loaded to Database")

def load_openings(conn):
    df_chess_games = pd.read_csv("../data/raw/chess_games.csv")
    openings_df = df_chess_games[['opening_code', 'opening_fullname', 'opening_shortname',]].drop_duplicates(subset=['opening_code'])
    # clean openings
    openings_df = openings_df.where(pd.notna(openings_df), None)

    openings_df.to_sql('openings', conn, if_exists='append', index=False)
    logging.info("openings Data is loaded to Database")

def load_chess_games(conn):
    chess_games_df = pd.read_csv("../data/raw/chess_games.csv")
    chess_games_df['rated'] = chess_games_df['rated'].astype(int)
    chess_games_df['opening_moves'] = chess_games_df['opening_moves'].fillna(0).astype(int)

    chess_games_df.to_sql('games', conn, if_exists='append', index=False)
    logging.info("Games Data is loaded to Database")

# //////////////////// Stage 1 & 2 ////////////////////////

def solution_q1_q6(conn):
    #Q1: How many total games? How many are rated?
    conn.execute("""
        SELECT COUNT(*) AS TOTAL_GAMES,
        SUM(CASE WHEN rated = 1 THEN 1 ELSE 0 END)
        FROM chess_games;
    """)
    # Q2 List all distinct victory_status values and their counts.
    conn.execute("""
              SELECT victory_status,
               COUNT(*) AS game_count,
              FROM chess_games
              GROUP BY victory_status
              ORDER BY game_count DESC
          """)
    # Q3 The 10 games with the most turns. Show game_id, winner, turns.
    conn.execute("""
                 SELECT game_id, winner, turns FROM games
                 ORDER BY turns Desc
             """)
    # Q4 What is the win rate (%) for White, Black, and Draw across all games?
    # Q5 For each victory_status, what is the average and max number of turns? Sort highest avg first.
    # Q6 Which 5 opening_codes appear most frequently? Use HAVING to show only those with more than 500 games.

    # Q2 List all distinct victory_status values and their counts.
    conn.execute("""
           SELECT victory_status,
            COUNT(*) AS game_count,
           FROM chess_games
           GROUP BY victory_status
           ORDER BY game_count DESC
       """)
    # Q3 The 10 games with the most turns. Show game_id, winner, turns.
    conn.execute("""
              SELECT game_id, winner, turns FROM games
              ORDER BY turns Desc
          """)

# //////////////////// Stage 3 & 4 ////////////////////////
def solution_q7_q12(conn):
    # Q4 What is the win rate (%) for White, Black, and Draw across all games?
    # Q5 For each victory_status, what is the average and max number of turns? Sort highest avg first.
    # Q6 Which 5 opening_codes appear most frequently? Use HAVING to show only those with more than 500 games.
    # Q7 JOIN games to openings — find the 5 most played openings with their full name.
    # Q8 LEFT JOIN players to games: find players who have never appeared as white_id.
    # Q9  Using a CTE: compute total wins per player (as white). Return top 5.
    # Q10 UNION CTE: combine white wins and black wins into one 'player_wins' table. Who has the most total wins?
    # Q11 Window function: for each game, add a column showing what RANK each game holds for that white player by white_rating (highest rating = rank 1). Show top 10 rows.
    # Q12 LAG: show each game's white_rating and the previous game's white_rating for the same player. Filter to players with 5+ games.
    pass

def solution_five_query():
    pass

def main():
    # create Database
    conn = sqlite3.connect('chess.db')
    # setup logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
    # First Log
    log = logging.getLogger(__name__)
    # Stage 0
    create_tables(conn)
    add_indexes(conn)
    load_players(conn)
    load_openings(conn)
    load_chess_games(conn)

    # solution_q1_q6(conn)






main()



