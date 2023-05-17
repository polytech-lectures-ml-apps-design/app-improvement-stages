import fastapi
import pydantic
from common.utils import load_classifier


# input validation
class IrisParameters(pydantic.BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    def to_list(self):
        return [self.sepal_length, self.sepal_width, self.petal_length, self.petal_width]


class IrisType(pydantic.BaseModel):
    iris_type: int


# model bring-up
clf = load_classifier('../models/model.pkl')

# REST server definition
app = fastapi.FastAPI()


# inference method
@app.post('/iris-classifier')
def predict(X: IrisParameters) -> IrisType:
    return IrisType(iris_type=clf.predict([X.to_list()])[0])
