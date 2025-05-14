from pymongo import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

def connect_to_mongodb(db_name, collection_name):
    user = urllib.parse.quote_plus("juliana.cabrejo@urosario.edu.co")
    password = urllib.parse.quote_plus("Julienzo")
    uri = f"mongodb+srv://juliana.cabrejo:Mongo1234@ifmerjuli.7ev8g.mongodb.net/?retryWrites=true&w=majority&appName=ifmerJuli"
    
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection

