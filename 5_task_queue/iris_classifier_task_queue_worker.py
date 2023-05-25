import json
import logging
import time

from kafka import KafkaConsumer, KafkaProducer

from common.iris_dto import IrisParameters, IrisType, Result, Task, SignedResult
from common.utils import load_classifier

logging.basicConfig(encoding='utf-8', level=logging.INFO)


# model bring-up
clf = load_classifier('../models/model.pkl')

# setup worker
consumer = KafkaConsumer('tasks', group_id='task_consumer_group', bootstrap_servers='localhost:29092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

print(consumer.partitions_for_topic('tasks'))

producer = KafkaProducer(bootstrap_servers='localhost:29092',
                         value_serializer=lambda x: x.json().encode('utf-8'))

for in_msg in consumer:
    task = Task(**in_msg.value)
    logging.info(f"Received new task: {task}")

    time.sleep(10)
    # load_all_cpus(10)

    # inference
    iris_params = task.X
    y = clf.predict([iris_params.to_list()])

    # output interface
    out_msg = SignedResult(task_id=task.task_id, X=iris_params, y=IrisType(iris_type=y[0]))
    producer.send('results', out_msg)
    logging.info(f"Published {out_msg} to results (y) topic")
