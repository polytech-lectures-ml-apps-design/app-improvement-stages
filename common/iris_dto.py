import pydantic


class IrisParameters(pydantic.BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    def to_list(self):
        return [self.sepal_length, self.sepal_width, self.petal_length, self.petal_width]


class IrisType(pydantic.BaseModel):
    iris_type: int
