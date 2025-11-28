import pika
import json

RABBIT_HOST = "mq"

def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))

def publish_ai_request(mail_id: str, mail_text: str):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="ai_requests", durable=True)

    payload = {"mail_id": mail_id, "mail_text": mail_text}
    channel.basic_publish(
        exchange='',
        routing_key="ai_requests",
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()

def consume_ai_responses(callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="ai_responses", durable=True)

    channel.basic_consume(
        queue="ai_responses",
        on_message_callback=callback,
        auto_ack=True
    )

    print("[MAIN] Waiting for AI responses...")
    channel.start_consuming()

def consume_external_emails(callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="external_emails", durable=True)

    channel.basic_consume(
        queue="external_emails",
        on_message_callback=callback,
        auto_ack=True
    )

    print("[MAIN] Waiting for external emails...")
    channel.start_consuming()
