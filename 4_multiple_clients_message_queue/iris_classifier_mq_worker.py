import json
import logging
import time

from kafka import KafkaConsumer

from common.iris_dto import IrisParameters
from common.utils import load_classifier

logging.basicConfig(encoding='utf-8', level=logging.INFO)


# model bring-up
clf = load_classifier('../models/model.pkl')

# setup worker
consumer = KafkaConsumer('tasks', bootstrap_servers='localhost:29092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for msg in consumer:
    logging.info(f"Received new task; input value: {msg.value}")

    time.sleep(10)
    # load_all_cpus(10)

    # inference
    y = clf.predict([IrisParameters(**msg.value).to_list()])

    # output interface
    logging.info(f"Inference result: {y}")
