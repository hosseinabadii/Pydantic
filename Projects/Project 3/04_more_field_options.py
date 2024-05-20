import os
from typing import Annotated

from pydantic import BaseModel, Field

os.system("clear")


# class User(BaseModel):
#     name: str = Field(min_length=3, max_length=10, alias="userName")
#     age: int = Field(gt=0, le=150, alias="userAge")
#     favorite_numbers: list[int] = Field(
#         min_length=2, max_length=10, alias="userFavoriteNumbers"
#     )


class User(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=10, alias="userName")]
    age: Annotated[int, Field(gt=0, le=150, alias="userAge")]
    favorite_numbers: Annotated[
        list[int], Field(min_length=2, max_length=5, alias="userFavoriteNumbers")
    ]


def main():
    user_data1 = {
        "userName": "al",
        "userAge": "200",
        "userFavoriteNumbers": [1],
    }
    try:
        model1 = User.model_validate(user_data1)
        print(model1)
    except ValueError as e:
        print(e)

    print("-" * 50)

    user_data2 = {
        "userName": "John Doe",
        "userAge": "30",
        "userFavoriteNumbers": [1, 2, 3],
    }
    try:
        model2 = User.model_validate(user_data2)
        print(model2)
        print(model2.model_dump())
        print(model2.model_dump(by_alias=True))
    except ValueError as e:
        print(e)

    print("-" * 50)

    user_data3 = {
        "userName": "John Doe",
        "userAge": "30",
        "userFavoriteNumbers": [1, 2, 3],
    }
    try:
        model3 = User.model_validate(user_data3, strict=True)
        print(model3)
        print(model3.model_dump())
        print(model3.model_dump(by_alias=True))
    except ValueError as e:
        print(e)

    print("-" * 50)

    user_data4 = {
        "userName": "John Doe",
        "userAge": 300,
        "userFavoriteNumbers": [1, 2, 3],
    }
    try:
        model4 = User.model_validate(user_data4, strict=True)
        print(model4)
        print(model4.model_dump())
        print(model4.model_dump(by_alias=True))
    except ValueError as e:
        print(e)

    print("-" * 50)

    user_data5 = {
        "userName": "John Doe",
        "userAge": 300,
        "userFavoriteNumbers": ["aaa", 2, 3, 4, 5],
    }
    try:
        model5 = User.model_validate(user_data5, strict=True)
        print(model5)
        print(model5.model_dump())
        print(model5.model_dump(by_alias=True))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
