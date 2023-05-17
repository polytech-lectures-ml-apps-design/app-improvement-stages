import os
import pickle
import re


def parse_input_string(s):
    pattern = re.compile(r"(\d+(?:\.\d+)?)")
    return re.findall(pattern, s)


def load_classifier(model_pickle_path: str):
    model_pickle_path = os.path.join(os.path.dirname(__file__), model_pickle_path)
    with open(model_pickle_path, 'rb') as p:
        clf = pickle.load(p)
        return clf
