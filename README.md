# Application improvement stages

Collection of ML-enabled applications 
that consecutively improve upon each other
with a more elaborated and production-grade
architecture:

* jupyter notebook: model training
* monolith app (Python) with CLI; runs inference once
* monolith app processing user command line input sequentially
* first step to modularity: analytical REST service and CLI client

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