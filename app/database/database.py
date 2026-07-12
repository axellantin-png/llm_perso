import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("data").mkdir(exist_ok=True)

        self.database = "data/assistant.db"


    def get_connection(self):

        connection = sqlite3.connect(self.database)

        connection.row_factory = sqlite3.Row

        return connection
    
    def initialize(self):

        connection = self.get_connection()

        with open(
            "app/database/schema.sql",
            encoding="utf8"
        ) as file:

            connection.executescript(
                file.read()
            )

        connection.commit()

        connection.close()