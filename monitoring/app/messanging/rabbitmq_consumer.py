"""
RabbitMQ consumer qui écoute l'exchange configuré et insère les documents dans MongoDB,
puis émet un event Socket.IO en temps réel.

Ce consumer tourne dans un thread (BlockingConnection + channel.start_consuming)
et utilise sio.start_background_task pour émettre l'event dans l'event loop async.
"""

import json
import threading
from datetime import datetime
import pika
from dateutil import parser as dateparser

from app.core.config import (
    RABBITMQ_HOST,
    RABBITMQ_EXCHANGE,
    RABBITMQ_QUEUE,
    RABBITMQ_ROUTING_KEY
)
from app.db.mongo import measurements_collection
from app.core.socket import sio

def parse_timestamp(ts_str):
    # accepte ISO8601 avec ou sans 'Z'
    try:
        return dateparser.parse(ts_str)
    except Exception:
        return datetime.utcnow()

def process_message(body):
    data = json.loads(body)
    device_id = data.get("device_id")
    ts = data.get("timestamp")
    payload = data.get("payload", {})

    timestamp = parse_timestamp(ts) if ts else datetime.utcnow()

    document = {
        "device_id": device_id,
        "timestamp": timestamp,
        "payload": payload
    }
    return document, data

def callback(ch, method, properties, body):
    try:
        document, raw = process_message(body)
        # Inserer en MongoDB (pymongo gère bien les datetime)
        measurements_collection.insert_one(document)

        # Emission Socket.IO en tâche de fond
        # Utilise room = device_id pour que les clients puissent s'abonner par device
        device_id = document.get("device_id")
        sio.start_background_task(
            sio.emit,
            "device_update",
            {
                "device_id": device_id,
                "timestamp": document["timestamp"].isoformat(),
                "payload": document["payload"]
            },
            room=device_id
        )

        # acknowledgement
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error processing message:", e)
        # En cas d'erreur on ack quand même (ou adapter selon stratégie)
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

    print("🟢 Monitoring RabbitMQ Consumer started, waiting for messages...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()

def start_consumer_thread():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
