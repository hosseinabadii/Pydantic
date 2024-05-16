import os
from typing import Any

from pydantic import BaseModel, EmailStr, model_validator
from typing_extensions import Self

os.system("clear")


class Owner(BaseModel):
    name: str
    email: EmailStr

    @model_validator(mode="before")
    @classmethod
    def check_sensitive_info_ommitted(cls, data: Any) -> Any:
        print("Calling model_validator mode='before'")
        if isinstance(data, dict):
            if "password" in data:
                raise ValueError("password should not be included in data.")
            if "card_number" in data:
                raise ValueError("card_number should not be included in data.")
        return data

    @model_validator(mode="after")
    def check_name_contains_space(self) -> Self:
        print("Calling model_validator mode='after'")
        if " " not in self.name:
            raise ValueError("Owner name must contain a space")
        return self


def main():
    owner_data1 = {
        "name": 123,
        "email": "john.doe@example.com",
        "password": "password123",
    }
    try:
        model1 = Owner.model_validate(owner_data1)
        print(model1)
    except ValueError as e:
        print(e)

    print("-" * 50)

    owner_data2 = {
        "name": 123,
        "email": "john.doe@example.com",
    }
    try:
        model2 = Owner.model_validate(owner_data2)
        print(model2)
    except ValueError as e:
        print(e)

    print("-" * 50)

    owner_data3 = {
        "name": "123",
        "email": "john.doe@example.com",
    }
    try:
        model3 = Owner.model_validate(owner_data3)
        print(model3)
    except ValueError as e:
        print(e)

    print("-" * 50)

    owner_data4 = {
        "name": "123 John",
        "email": "john.doe@example.com",
    }
    try:
        model4 = Owner.model_validate(owner_data4)
        print(model4)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
