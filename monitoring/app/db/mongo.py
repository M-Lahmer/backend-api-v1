from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DB

# Le client pymongo est thread-safe
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
measurements_collection = db["measurements"]
