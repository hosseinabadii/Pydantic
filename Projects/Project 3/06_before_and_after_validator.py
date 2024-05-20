import os
from typing import Any

from pydantic import BaseModel, field_validator

os.system("clear")


class Test(BaseModel):
    age: int

    @field_validator("age", mode="before")
    @classmethod
    def before_validator(cls, v: Any) -> Any:
        print("Calling before validator:")
        print(v, type(v), "\n------------")
        return v

    @field_validator("age")
    @classmethod
    def after_validator(cls, v: int) -> int:
        print("Calling after validator:")
        print(v, type(v), "\n------------")
        return v


def main():
    data_1 = {"age": "25"}
    try:
        model_1 = Test.model_validate(data_1)
        print(model_1)
    except ValueError as e:
        print(e)
    finally:
        print("-" * 50)

    data_2 = {"age": "aaa"}
    try:
        model_2 = Test.model_validate(data_2)
        print(model_2)
    except ValueError as e:
        print(e)
    finally:
        print("-" * 50)


if __name__ == "__main__":
    main()
