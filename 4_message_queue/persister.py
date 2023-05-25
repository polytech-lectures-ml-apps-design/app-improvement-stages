import json
import logging

from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import Base, IrisPrediction

logging.basicConfig(encoding='utf-8', level=logging.INFO)


# setup worker
consumer = KafkaConsumer('results', bootstrap_servers='localhost:29092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# setup DB
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)

with Session(engine) as session:
    for msg in consumer:
        print(msg)
        new_iris_prediction = IrisPrediction(**msg.value['X'], **msg.value['y'])
        session.add(new_iris_prediction)
        session.commit()
