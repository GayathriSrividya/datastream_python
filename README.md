# datastream_python

This repository is for data streaming and processing using pyspark, kafka, flink and druid.

config:
------
contains a json file with some queries to be performed on data.

data:
-----
The data folder contains compressed json file which has sunbird telemetry data.

src->kafka:
-----------
this folder has python scripts to create spark session, reading json file and pushing events into kafka.

kafka_producer.py:
    - creating instance for the python class Telemetry 
kafka_consumer.py
    - python script to read events from kafka topic (here "sb-telemetry")
telemetry_class.py
    - python class to create spark session and push events into kafka 

src->flink
----------
this folder has python script and dependencies to execute a flink job.

flink_transform.py
    -  python script to read events from kafka, apply some transformations on the datastream and push the events into kafka again.

src->druid
----------
this folder contains ingestion spec and native queries.

tests:
------
this folder contains unittest files to check functionality of python codes existing in src folder, and also contains json files with test scenarios.

tests->config:
-------------
this folder consists of json files which have different scenarios for the test cases

setting up github repository:
----------------------------
Before you start working on the project, create your own github repository and generate SSH, GPG keys for authentication. for more information, refer below:

https://docs.github.com/en/get-started/quickstart/create-a-repo

https://docs.github.com/en/authentication/connecting-to-github-with-ssh

https://docs.github.com/en/authentication/managing-commit-signature-verification


create python virtual environment in your linux system:
-------------------------------------------------------

Note: Python version (3.6, 3.7 or 3.8) is required for PyFlink. 

run python -V (if version is not displayed run sudo apt install python3)

after installing python, run "python -m venv my-project-env"

then virtual environment named my-project-env will be created.

run "source my-project-env/bin/activate" to activate

run "pip install requests" & "python -c "import requests"" only for the first time.

to close the virtual environment, type "deactivate"

project setup:
-------------
install required dependencies in requirements.txt file

"pip install -r requirements.txt"

create a new directory using "mkdir dir_name"

to navigate into directory use "cd path/to/dir_name"

create a new file (say python file) use "touch file.py"

to execute a python script, use command "python file.py" or "python path/to/file.py"

to create docker containers, type "docker compose up" in the terminal

refer https://docs.docker.com/engine/install/ubuntu/ for installation of docker


Generate test coverage:
-----------------------

type the following commands in the terminal to generate test coverage report

"coverage run -m unittest discover"

"coverage report"

"coverage html"