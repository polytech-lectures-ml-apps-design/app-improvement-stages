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
python -m monolith_cli.iris_classifier_monolith_cli_app 1 2 3 4
```