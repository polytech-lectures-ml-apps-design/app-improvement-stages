import json
import logging

from kafka import KafkaProducer, KafkaConsumer

from common.iris_dto import IrisParameters, Task, SignedResult
from common.utils import parse_input_string, generate_task_id

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# message queue connection
logging.info("establishing connection to kafka")
producer = KafkaProducer(bootstrap_servers='localhost:29092',
                         value_serializer=lambda x: x.json().encode('utf-8'))
consumer = KafkaConsumer('results', bootstrap_servers='localhost:29092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


while True:
    # input interface (user interaction)
    user_input = input("Enter sepal length in cm, sepal width in cm, "
                       "petal length in cm, petal width in cm separated by commas or 'q' to quit: \n")
    if user_input == 'q':
        break

    X = parse_input_string(user_input)
    # client-side input validation
    if len(X) != 4:
        print("Invalid input. Enter exactly 4 numbers. \n")
        continue

    # putting the task in the queue
    iris_parameters = IrisParameters(sepal_length=X[0],
                                     sepal_width=X[1],
                                     petal_length=X[2],
                                     petal_width=X[3])
    message = Task(task_id=generate_task_id(), X=iris_parameters)
    producer.send('tasks', message)
    logging.info(f"Published {message} to tasks (X) topic")

    # getting the result synchronously (we could also do smth else while waiting for result!!!)
    for result_msg in consumer:
        result = SignedResult(**result_msg.value)
        logging.info(f"Received result {result}")
        if result.task_id == message.task_id:
            print(f"Iris type: {result.y.iris_type}")
            break

    # output interface
    # THERE ISN'T ANY SO FAR
