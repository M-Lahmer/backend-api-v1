import os
from dotenv import load_dotenv

# charge le fichier .env à la racine du projet
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY")

SOCKETIO_CORS = os.getenv("SOCKETIO_CORS", "*")

# DEBUG TEMPORAIRE (à enlever plus tard)
print("🔎 Loaded MONGO_URI =", MONGO_URI)
