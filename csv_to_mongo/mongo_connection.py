from pymongo import MongoClient
from cosntants import DB_URL, DB_NAME

def get_database(db_name=DB_NAME, uri=DB_URL):
    """
    Connect to MongoDB and return the specified database.
    
    Parameters:
    - db_name (str): Name of the database to use or create (default: "csv_database").
    - uri (str): MongoDB connection string (default: local MongoDB).
    
    Returns:
    - db: The MongoDB database object.
    """
    client = MongoClient(uri)  
    db = client[db_name]  
    return db
