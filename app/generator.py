import random
import json
import time
from datetime import datetime

def generate_message():
    return {
        "user": {
            "id": random.randint(1, 100),
            "name": random.choice(["Ilya", "Arya", "Putra", "Ahmad"])
        },
        "transaction": {
            "id": random.randint(1000, 9999),
            "amount": round(random.uniform(10.0, 500.0), 2),
            "items": [
                {"item_id": i, "price": round(random.uniform(1.0, 100.0), 2)}
                for i in range(random.randint(1, 3))
            ]
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    while True:
        msg = generate_message()
        print(json.dumps(msg))
        time.sleep(1)
