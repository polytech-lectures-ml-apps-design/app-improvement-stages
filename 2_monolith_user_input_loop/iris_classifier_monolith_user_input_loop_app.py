from common.utils import parse_input_string, load_classifier

# model bring-up
clf = load_classifier('../models/model.pkl')

# inference; running the model
while True:
    # input interface
    user_input = input("Enter sepal length in cm, sepal width in cm, "
                       "petal length in cm, petal width in cm separated by commas or 'q' to quit: \n")
    if user_input == 'q':
        break

    X = [parse_input_string(user_input)]
    # input validation
    if len(X[0]) != 4:
        print("Invalid input. Enter exactly 4 numbers. \n")
        continue

    # calling the model
    y = clf.predict(X)

    # output interface
    print(y)
