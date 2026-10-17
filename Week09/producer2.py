import pika, json, time, random, ssl
from datetime import datetime

RABBITMQ_HOST = "amqp.iot.kmitl.co"
RABBITMQ_USER = "67070164"
RABBITMQ_PASS = "" # RabbitMQ Password

EXCHANGE_NAME = "amq.direct"
EXCHANGE_TYPE = "direct"

ROUTING_KEY = "every_3s"

credentials = pika.PlainCredentials(
    RABBITMQ_USER,
    RABBITMQ_PASS
)

parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=credentials,
    port=5671,
    virtual_host="67070164",
    ssl_options=pika.SSLOptions(
        ssl.create_default_context()
    )
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE_NAME,
    exchange_type=EXCHANGE_TYPE,
    durable=True
)

try:
    while True:
        data = {
            "timestamp": datetime.now().isoformat(),
            "producer_id": "P-02",
            "temperature": round(random.uniform(0, 100), 1)
        }
        message = json.dumps(data)
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=message,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2
            )
        )
        print(f"[SENDING] {message}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
finally:
    connection.close()
