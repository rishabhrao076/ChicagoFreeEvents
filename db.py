import firebase_admin
from firebase_admin import db
from dotenv import load_dotenv
import os

load_dotenv()

cred_obj = firebase_admin.credentials.Certificate('dbcredentials.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':os.getenv("FIREBASE_DATABASE_URL")
	})

ref = db.reference("/")

def push_data_to_firebase(data, path):
    """
    Pushes data to Firebase Realtime Database.

    Args:
        data: The data to be pushed (dictionary).
        path: The path in the database where the data will be stored (string).
    """
    ref = db.reference(path)
    ref.push().set(data)

def update_data_in_firebase(data, path):
    """
    Updates data in Firebase Realtime Database.

    Args:
        data: The data to be updated (dictionary).
        path: The path in the database where the data will be updated (string).
    """
    ref = db.reference(path)
    
    # Update the data at the specified path
    ref.update(data)

def get_data_from_firebase(path):
    """
    Retrieves data from Firebase Realtime Database.

    Args:
        path: The path in the database from where the data will be retrieved (string).

    Returns:
        The retrieved data (dictionary).
    """
    ref = db.reference(path)
    
    # Get data from the specified path in the database
    data = ref.get()
    
    return data