import re
from pydantic import BaseModel, field_validator


class User(BaseModel):
    username: str
    age: int
    email: str
    password: str

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 18:
            raise ValueError("User must be adult")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
            raise ValueError("Email is invalid")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password_length = len(value)
        if password_length < 8 or password_length > 16:
            raise ValueError("The password must be between 8 and 16 characters long")
        return value


# Valid User
valid_user = {
    'username': 'test_name',
    'age': 20,
    'email': 'name@test.gr',
    'password': '123456789'
}

# Invalid User
invalid_user = {
    'username': 'test_name',
    'age': 16,
    'email': 'name_test.gr',
    'password': '1234'
}

try:
    valid_result = User(**valid_user)
    print(valid_result)
    invalid_result = User(**invalid_user)
except ValueError as e:
    print(e.errors())
