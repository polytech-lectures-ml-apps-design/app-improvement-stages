import os

import requests

from common.iris_dto import IrisParameters
from common.utils import parse_input_string

# rest service config
url = "http://127.0.0.1:8000/iris-classifier"
headers = {'Content-Type': 'application/json', 'Process-Id': f"{os.getpid()}"}

# inference; running the model
while True:
    # input interface
    user_input = input("Enter sepal length in cm, sepal width in cm, "
                       "petal length in cm, petal width in cm separated by commas or 'q' to quit: \n")
    if user_input == 'q':
        break

    X = parse_input_string(user_input)
    # client-side input validation
    if len(X) != 4:
        print("Invalid input. Enter exactly 4 numbers. \n")
        continue

    # calling the model
    http_res = requests.post(url=url, headers=headers, data=IrisParameters(sepal_length=X[0],
                                                                           sepal_width=X[1],
                                                                           petal_length=X[2],
                                                                           petal_width=X[3]).json())
    y = http_res.json()

    # output interface
    print(y)
