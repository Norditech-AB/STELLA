from abc import ABC, abstractmethod
import os
import dotenv

from app.db.databases.mongodb import MongoDB

dotenv.load_dotenv()


class DatabaseFactory:
    @staticmethod
    def get_database():
        db_type = os.getenv('DATABASE')

        if db_type == 'mongodb':
            return MongoDB()
        # Add other database types here
        else:
            raise Exception(f"Unsupported database type: {db_type}")


db = DatabaseFactory.get_database()