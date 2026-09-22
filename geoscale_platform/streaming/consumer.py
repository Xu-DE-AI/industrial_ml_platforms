import json
import sqlite3
from confluent_kafka import Consumer

DB = "streaming/idempotency.db"

def seen(conn, event_id):
    return conn.execute(
        "select 1 from processed where event_id=?", (event_id,)
    ).fetchone() is not None

def mark(conn, event_id):
    conn.execute("insert or ignore into processed values (?)", (event_id,))
    conn.commit()

def main():
    conn = sqlite3.connect(DB)
    conn.execute("create table if not exists processed(event_id integer primary key)")

    c = Consumer({
        "bootstrap.servers": "localhost:19092",
        "group.id": "geoscale-risk",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    c.subscribe(["ae-events"])

    try:
        while True:
            msg = c.poll(1)
            if msg is None:
                continue
            if msg.error():
                print(msg.error())
                continue

            event = json.loads(msg.value())
            event_id = event["event_id"]

            if not seen(conn, event_id):
                # Side effect would happen here.
                print("process", event_id)
                mark(conn, event_id)
            else:
                print("duplicate ignored", event_id)

            c.commit(message=msg, asynchronous=False)
    except KeyboardInterrupt:
        pass
    finally:
        c.close()

if __name__ == "__main__":
    main()
