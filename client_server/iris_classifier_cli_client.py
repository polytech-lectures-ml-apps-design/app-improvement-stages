import requests

from common.utils import parse_input_string

# rest service config
url = "http://127.0.0.1:8000/iris-classifier"
headers = {'Content-Type': 'application/json'}

# inference; running the model
while True:
    # input interface
    user_input = input("Enter sepal length in cm, sepal width in cm, "
                       "petal length in cm, petal width in cm separated by commas or 'q' to quit: \n")
    if user_input == 'q':
        break

    X = [parse_input_string(user_input)]
    # client-side input validation
    if len(X[0]) != 4:
        print("Invalid input. Enter exactly 4 numbers. \n")
        continue

    # calling the model
    http_res = requests.Request('POST', url=url, headers=headers, data=X)
    y = http_res

    # output interface
    print(y)
