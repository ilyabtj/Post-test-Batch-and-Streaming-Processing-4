from kafka import KafkaProducer
import json
import time
from generator import generate_message

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "ilya_input"

if __name__ == "__main__":
    while True:
        msg = generate_message()
        producer.send(topic, value=msg)
        print("Sent:", msg)
        time.sleep(1)
