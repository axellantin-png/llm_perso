import sqlite3

DATABASE = "data/assistant.db"


def get_connection():

    return sqlite3.connect(DATABASE)