from enum import IntFlag, auto
from typing import Any

from pydantic import BaseModel, EmailStr, Field, SecretStr, ValidationError


class Role(IntFlag):
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer


class User(BaseModel):
    name: str = Field(examples=["Arjan"])
    email: EmailStr = Field(
        examples=["example@gamil.com"],
        description="This is email address of user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password1234"],
        description="The password of the user",
    )
    role: Role = Field(
        default=None,
        description="The role of the user",
    )


def validate(data: dict[str, Any]) -> None:
    try:
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print("User is invalid")
        for idx, error in enumerate(e.errors(), 1):
            print(f"\nerror #{idx}:\n{error}")


def main() -> None:
    good_data = {
        "name": "Arjan",
        "email": "Ajran@gamil.com",
        "password": "Password123",
    }
    bad_data = {
        "email": "Ajrangamil.com",
        "password": "<bad data>",
    }

    validate(good_data)
    validate(bad_data)


if __name__ == "__main__":
    main()
