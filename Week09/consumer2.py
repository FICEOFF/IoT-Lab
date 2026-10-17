import pika, json, ssl

RABBITMQ_HOST = "amqp.iot.kmitl.co"
RABBITMQ_USER = "67070164"
RABBITMQ_PASS = "" # RabbitMQ Password

EXCHANGE_NAME = "amq.direct"
EXCHANGE_TYPE = "direct"

QUEUE_NAME = "queue_50c"

ROUTING_KEY = ["every_2s", "every_3s"]

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

channel.queue_declare(
    queue=QUEUE_NAME,
    durable=True
)

for KEY in ROUTING_KEY:
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=KEY
    )

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        timestamp = data["timestamp"]
        producer_id = data["producer_id"]
        temperature = data["temperature"]
        if temperature > 50:
            print(f"[RECEIVE] {timestamp} | {producer_id} temperature: {temperature} °C")
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )
    except Exception as e:
        print(f"[ERROR] {e}: Message returned to queue")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )

channel.basic_qos(
    prefetch_count=1
)

channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=False
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n[QUIT] Stopping program...")
    channel.stop_consuming()
finally:
    connection.close()
