import json
import logging
import time

import fastapi
import pydantic
from common.utils import load_classifier, load_all_cpus
from common.iris_dto import IrisParameters, IrisType

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# model bring-up
clf = load_classifier('../models/model.pkl')

# REST server definition
app = fastapi.FastAPI()


@app.get('/model-info')
def model_info():
    return str(clf.get_params())


# inference method
@app.post('/iris-classifier')
def predict(X: IrisParameters, request: fastapi.Request) -> IrisType:
    logging.info(f"Processing request")
    time.sleep(10)
    # load_all_cpus(10)
    return IrisType(iris_type=clf.predict([X.to_list()])[0])
