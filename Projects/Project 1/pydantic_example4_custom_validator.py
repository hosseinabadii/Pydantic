import hashlib
import re
from enum import IntFlag, auto
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)

VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


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

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contains only letters and be at least 2 characters long"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError):
            raise ValueError(
                f"Role is invalid, please use one of the following: {', '.join(x.name for x in Role)}"
            )

    @model_validator(mode="before")
    @classmethod
    def validate_user(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "name" not in v or "password" not in v:
            raise ValueError("name and password are required")
        if v["name"].casefold() in v["password"].casefold():
            raise ValueError("Password cannot contain name")
        if not VALID_PASSWORD_REGEX.match(v["password"]):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 digit"
            )
        v["password"] = hashlib.sha256(v["password"].encode()).hexdigest()
        return v


def validate_data(data: dict[str, Any]) -> None:
    try:
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print("User is invalid")
        for idx, error in enumerate(e.errors(), 1):
            print(f"\nerror #{idx}:\n{error}")


def main() -> None:
    test_data = dict(
        good_data={
            "name": "Arjan",
            "email": "Ajran@gamil.com",
            "password": "Password123",
            "role": "Admin",
        },
        bad_role={
            "name": "Arjan",
            "email": "Ajran@gamil.com",
            "password": "Password123",
            "role": "Programmer",
        },
        bad_data={
            "name": "Arjan",
            "email": "bad email",
            "password": "bad password",
        },
        bad_name={
            "name": "<--Arjan-->",
            "email": "Ajran@gamil.com",
            "password": "Password123",
        },
        duplicate={
            "name": "Arjan",
            "email": "Ajran@gamil.com",
            "password": "Arjan123",
        },
        missing_data={
            "email": "Ajran@gamil.com",
            "password": "Password123",
        },
    )

    for example_name, data in test_data.items():
        print(f"{example_name}:\n")
        validate_data(data)
        print("=" * 50)


if __name__ == "__main__":
    main()
