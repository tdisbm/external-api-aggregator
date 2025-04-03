from pymongo import MongoClient
from pymongo.synchronous.database import Database

from app.config import MONGO_DB_NAME, MONGO_DB_URI


class CollectionAccessor:
    def __init__(self, database: Database):
        self._db = database

    def __getattr__(self, collection_name):
        if hasattr(self._db, collection_name):
            return self._db[collection_name]
        raise IllegalCollectionException(f'Collection {collection_name} does not exist')


class Session:
    def __init__(self):
        self.session = None

    def __enter__(self):
        """Start a session and begin a transaction."""
        self.session = client.start_session()
        self.session.start_transaction()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Handle commit, abort, and session cleanup."""
        if exc_type:
            print(f"Transaction failed due to: {exc_value}")
            self.session.abort_transaction()
        else:
            self.session.commit_transaction()
        self.session.end_session()


class IllegalCollectionException(Exception):
    pass


client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]
collections = CollectionAccessor(db)
