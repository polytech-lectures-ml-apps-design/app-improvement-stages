# Application improvement stages

Collection of ML-enabled applications 
that consecutively improve upon each other
with a more elaborated and production-grade
architecture:

* jupyter notebook: model training
* monolith app (Python) with CLI; runs inference once
* monolith app processing user command line input sequentially
* first step to modularity: analytical REST service and CLI client
* decoupling via message queue
* load balancing with tasks queue

## How to run

Run all scripts as `python -m <package.name>`
as this will enable usage of relative paths to common utilities.
E.g.:
```bash
python -m 1_monolith_cli.iris_classifier_monolith_cli_app 1 2 3 4
```

### Monolith app with CLI

The app source code is in [1_monolith_cli](1_monolith_cli).

Run as:
```shell
python -m 1_monolith_cli.iris_classifier_monolith_cli_app <sepal_length> <sepal_width> <petal_length> <petal_width> 
```
I.e. the app accepts exactly 4 command line arguments.

### Monolith app processing user command line input sequentially

The app source code is in [2_monolith_user_input_loop](2_monolith_user_input_loop).

Run as:
```shell
python -m 2_monolith_user_input_loop.iris_classifier_monolith_user_input_loop_app 
```
and follow interactive prompt instructions.

### Client-server

Client is an interactive prompt client (like in [previous section](#monolith-app-processing-user-command-line-input-sequentially)).
The app source code is in [3_client_server](3_client_server).

Run server as:
```shell
uvicorn 3_client_server.iris_classifier_rest_server:app --reload 
```
Use `--reload` flag only for debugging.
Then start client as:
```shell
python -m 3_client_server.iris_classifier_cli_client_rest
```
and run it in interactive shell.

We will also use
```shell
uvicorn 3_client_server.iris_classifier_rest_server:app --limit-concurrency 2
```
with a CPU-bound version of server to illustrate that with 2 concurrent clients,
one of them will receive `503 Service Unavailable`
which brings of to the idea of using a message queue for tasks.

### Message queue

Kafka message queue is used.
Client (still operating via interactive prompt as previously) publishes tasks to the `tasks` 
topic in the message queue.
Server subscribes for the `tasks` topic and sequentially executes inference. 
Results are published to the `results` topic.
Results are also persisted in a simple SQLite DB.

The app source code is in [4_message_queue](4_message_queue).

First, bring up Apache Kafka with:
```shell
cd ./4_message_queue
docker compose up -d
```

Run worker as
```shell
python -m 4_message_queue.iris_classifier_mq_worker
```

Run CLI client as
```shell
python -m 4_message_queue.iris_classifier_cli_client_mq
```


### Task queue

Again, kafka message queue is used.
Client (still operating via interactive prompt as previously) publishes tasks to the `tasks` 
topic in the message queue and synchronously waits for the result in the `results` topic.
Workers subscribe for the `tasks` topic and sequentially executes inference. 
Results are published to the `results` topic.

The mechanism how clients understand which result is designated for them is as follows:
* the task contains not only the **X**, but also the task id (generated with UUID4)
* worker joins the task id to the result so that it can be linked and filtered out by the client

The load balancing as achieved by two things:
* setting multiple partitions for the `tasks` topic (in the script [kafka_setup.py](5_task_queue/kafka_setup.py))
* assigning all consumers (defined in workers) to the same consumer group
* check https://www.instaclustr.com/blog/a-beginners-guide-to-kafka-consumers/ for more details

The app source code is in [5_task_queue](5_task_queue).

First, bring up Apache Kafka with:
```shell
cd ./5_task_queue
docker compose up -d
```

Run multiple workers as
```shell
python -m 5_task_queue.iris_classifier_task_queue_worker
```

Run multiple CLI clients as
```shell
python -m 5_message_queue.iris_classifier_cli_client_task_queue
```
Send tasks simultaneously from multiple clients and check how they are distributed among workers.