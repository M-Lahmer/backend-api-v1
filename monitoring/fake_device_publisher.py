"""
Simulateur simple : publie des messages sur l'exchange 'devices.events'
Utilise routing_key: device.<device_id>
"""

import pika
import json
import time
import random
from datetime import datetime

RABBITMQ_HOST = "localhost"
EXCHANGE = "devices.events"
ROUTING_KEY_TEMPLATE = "device.{}"

def make_message(device_id: str):
    return {
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 70.0), 2),
            "battery": random.randint(20, 100)
        }
    }

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    device_id = "device-001"
    print(f"Starting fake publisher for {device_id} -> exchange {EXCHANGE}")

    try:
        while True:
            msg = make_message(device_id)
            routing_key = ROUTING_KEY_TEMPLATE.format(device_id)
            channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key, body=json.dumps(msg))
            print(f"Sent: {msg}")
            time.sleep(7)
    except KeyboardInterrupt:
        print("Stopping publisher")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
