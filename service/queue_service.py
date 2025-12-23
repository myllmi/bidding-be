import pika
import json

class QueueService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="domain_events",
            exchange_type="topic",
            durable=True
        )

    def publish_event(self, topic: str, payload: dict):
        self.channel.basic_publish(
            exchange="domain_events",
            routing_key=topic,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                content_type="application/json"
            )
        )
        # print(f"Published to {topic}")

    def close_connection(self):
        self.connection.close()

# publish_event("project.created", {"id": 1, "name": "Project A"})
# publish_event("resume.updated", {"id": 10, "owner": "John"})
# publish_event("tender.deleted", {"id": 99})

