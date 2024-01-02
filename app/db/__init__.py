from abc import ABC, abstractmethod
import os
import dotenv

from app.db.databases.mongodb import MongoDB
from app.db.databases.sqlite import SQLite

dotenv.load_dotenv()


class DatabaseFactory:
    @staticmethod
    def get_database():
        db_type = os.getenv('DATABASE')

        if db_type == 'mongodb':
            return MongoDB()
        elif db_type == 'sqlite':
            return SQLite()
        else:
            raise Exception(f"Unsupported database type: {db_type}")


db = DatabaseFactory.get_database()
