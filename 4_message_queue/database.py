from sqlalchemy import Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IrisPrediction(Base):
    __tablename__ = "iris_prediction"

    id: Mapped[int] = mapped_column(primary_key=True)
    sepal_length: Mapped[float] = mapped_column(Float)
    sepal_width: Mapped[float] = mapped_column(Float)
    petal_length: Mapped[float] = mapped_column(Float)
    petal_width: Mapped[float] = mapped_column(Float)
    iris_type: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"IrisPrediction(id={self.id}, sepal_length={self.sepal_length}, sepal_width={self.sepal_width}," \
               f"petal_length={self.petal_length}, petal_width={self.petal_width}, iris_type={self.iris_type})"
