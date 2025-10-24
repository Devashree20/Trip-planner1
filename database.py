# database.py
from pymongo import MongoClient
from dotenv import dotenv_values
from datetime import datetime

config = dotenv_values(".env")

MONGO_URI = config.get("MONGODB_URI")
DB_NAME = config.get("MONGODB_DB", "trip_planner")
COLLECTION_NAME = config.get("MONGODB_COLLECTION", "itineraries")

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_itinerary(source, destination, itinerary_text):
    """Save generated itinerary to MongoDB."""
    record = {
        "source": source,
        "destination": destination,
        "itinerary": itinerary_text,
        "created_at": datetime.now().isoformat()
    }
    result = collection.insert_one(record)
    return str(result.inserted_id)

def get_all_itineraries():
    """Retrieve all stored itineraries."""
    itineraries = list(collection.find({}, {"_id": 0}))
    return itineraries

def get_itinerary_by_destination(destination):
    """Retrieve itineraries by destination."""
    return list(collection.find({"destination": {"$regex": destination, "$options": "i"}}, {"_id": 0}))
