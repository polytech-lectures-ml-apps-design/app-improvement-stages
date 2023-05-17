import argparse
import os
import pickle


# model bring-up
model_pickle_path = os.path.join(os.path.dirname(__file__), '../models/model.pkl')
with open(model_pickle_path, 'rb') as p:
    clf = pickle.load(p)


# input interface
parser = argparse.ArgumentParser(description='Loads already prepared classifier for iris data, '
                                             'accepts input from CLI and predicts iris class on this '
                                             'input.')
parser.add_argument('X', type=float, nargs=4, help='Sepal length in cm, '
                                                   'Sepal width in cm, '
                                                   'Petal length in cm, '
                                                   'Petal width in cm.')
# input validation
args = parser.parse_args()
X = [args.X]

# inference, running the model
y = clf.predict(X)

# output interface
print(y)
