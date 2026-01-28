from typing import List
from app.db.mongo import measurements_collection
from bson import json_util
from datetime import datetime

def get_device_data(device_id: str, limit: int = 100) -> List[dict]:
    """
    Récupère les documents pour device_id, triés par timestamp décroissant.
    Retourne une liste de dicts sérialisables.
    """
    cursor = measurements_collection.find({"device_id": device_id}).sort("timestamp", -1).limit(limit)
    results = []
    for doc in cursor:
        # Convertir ObjectId / datetime correctement en JSON-friendly dict
        doc["_id"] = str(doc.get("_id"))
        ts = doc.get("timestamp")
        if isinstance(ts, datetime):
            doc["timestamp"] = ts.isoformat()
        results.append(doc)
    return results
