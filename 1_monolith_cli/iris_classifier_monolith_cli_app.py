import argparse
from common.utils import load_classifier

# model bring-up
clf = load_classifier('../models/model.pkl')

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

# input data transformation
X = [args.X]

# inference, running the model
y = clf.predict(X)

# output interface
print(y)
