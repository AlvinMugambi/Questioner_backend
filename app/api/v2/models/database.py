"""
    Initializes a connection to the db
"""
import os
import sys
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash


def init_db(db_url=None):
    """
        Initialize db connection
    """
    try:
        conn, cursor = connect_to_and_query_db()
        all_init_queries = drop_table_if_exists() + set_up_tables()
        i = 0
        while i != len(all_init_queries):
            query = all_init_queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        print("--"*50)
        conn.close()

    except Exception as error:
        print("\nQuery not executed : {} \n".format(error))


def set_up_tables():
    """
        Queries run to set up and create tables
    """
    users_table_query = """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR (24) NOT NULL UNIQUE,
        firstname VARCHAR (24) NOT NULL,
        lastname VARCHAR (24) NOT NULL,
        phone INTEGER NOT NULL,
        email VARCHAR (30) NOT NULL UNIQUE,
        password VARCHAR (128) NOT NULL,
        admin BOOLEAN
    )"""

    meetups_table_query = """
    CREATE TABLE meetups (
        meetup_id SERIAL PRIMARY KEY,
        topic VARCHAR (24) NOT NULL,
        meetup_date TIMESTAMP,
        meetup_location VARCHAR (24) NOT NULL,
        meetup_images VARCHAR (24) NOT NULL,
        meetup_tags VARCHAR (24) NOT NULL,
        created_at TIMESTAMP
    )"""

    questions_table_query = """
    CREATE TABLE questions (
        question_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        meetup_id INTEGER NOT NULL,
        title VARCHAR (50) NOT NULL,
        body VARCHAR (200) NOT NULL,
        votes INTEGER NOT NULL,
        comment VARCHAR,
        created_at TIMESTAMP
    )"""

    comments_table_query = """
    CREATE TABLE comments (
        comment_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        question_id INTEGER NOT NULL,
        title VARCHAR,
        body VARCHAR,
        comment VARCHAR
    )"""

    rsvps_table_query = """
    CREATE TABLE rsvps (
        rsvp_id SERIAL PRIMARY KEY,
        meetup_id INTEGER,
        user_id INTEGER,
        meetup_topic VARCHAR,
        rsvp VARCHAR
    )"""

    votes_table_query = """
    CREATE TABLE votes (
        user_id INTEGER,
        question_id INTEGER
    )"""

    tokens_table_query = """
    CREATE TABLE blacklist_tokens (
        token_id SERIAL PRIMARY KEY,
        token VARCHAR
    )"""

    password = generate_password_hash('ThaOG1234')
    create_admin_query = """
    INSERT INTO users(username, firstname, lastname, phone, email, password, admin) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}', '{}'
    )""".format('iamtheadmin', 'the', 'admin', '0706673461', 'adminog@gmail.com', password, True)

    return [users_table_query, meetups_table_query,
            questions_table_query, comments_table_query,
            rsvps_table_query, create_admin_query,
            votes_table_query, tokens_table_query]


def drop_table_if_exists():
    """
        Removes all tables on app restart
    """
    drop_users_table = """
    DROP TABLE IF EXISTS users"""

    drop_meetups_table = """
    DROP TABLE IF EXISTS meetups"""

    drop_questions_table = """
    DROP TABLE IF EXISTS questions"""

    drop_comments_table = """
    DROP TABLE IF EXISTS comments"""

    drop_rsvps_table = """
    DROP TABLE IF EXISTS rsvps"""

    drop_votes_table_ = """
    DROP TABLE IF EXISTS votes"""

    drop_blacklist_tokens_table_ = """
    DROP TABLE IF EXISTS blacklist_tokens"""

    return [drop_comments_table, drop_meetups_table,
            drop_questions_table, drop_users_table,
            drop_rsvps_table, drop_votes_table_,
            drop_blacklist_tokens_table_]


def connect_to_and_query_db(query=None, db_url=None):
    """
        Initiates a connection to the db and executes a query
    """
    conn = None
    cursor = None
    if db_url is None:
        db_url = os.getenv('DATABASE_URL')

    try:
        # connect to db
        conn = psycopg2.connect(db_url)
        print("\n\nConnected {}\n".format(conn.get_dsn_parameters()))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if query:
            # Execute query
            cursor.execute(query)
            # Commit changes
            conn.commit()

    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print("DB ERROR: {}".format(error))

    return conn, cursor


def query_db_no_return(query):
    """
        Handles INSERT queries
    """
    try:
        conn = connect_to_and_query_db(query)[0]
        # After successful INSERT query
        conn.close()
    except psycopg2.Error as error:
        sys.exit(1)


def select_from_db(query):
    """
        Handles SELECT queries
    """
    rows = None
    conn, cursor = connect_to_and_query_db(query)
    if conn:
        # Retrieve SELECT query results from db
        rows = cursor.fetchall()
        conn.close()

    return rows


if __name__ == '__main__':
    init_db()
    connect_to_and_query_db()
