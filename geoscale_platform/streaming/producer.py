import json
import time
from confluent_kafka import Producer

def main():
    p = Producer({"bootstrap.servers": "localhost:19092"})
    for i in range(100):
        event = {
            "event_id": i,
            "sensor_id": f"S{i % 8:02d}",
            "timestamp": time.time(),
            "magnitude": 0.5 + i/500,
        }
        p.produce(
            "ae-events",
            key=event["sensor_id"],
            value=json.dumps(event),
        )
        p.poll(0)
    p.flush()

if __name__ == "__main__":
    main()
