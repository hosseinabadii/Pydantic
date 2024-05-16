import hashlib
import os
import re
from enum import IntFlag
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    SerializationInfo,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)
from typing_extensions import Self

os.system("clear")
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")


class Role(IntFlag):
    User = 0
    Author = 1
    Editor = 2
    Developer = 3
    Admin = 4
    SuperAdmin = 8


class User(BaseModel):
    name: str = Field(
        examples=["Arjan"],
    )
    email: EmailStr = Field(
        examples=["example@gamil.com"],
        description="This is email address of user",
        frozen=True,
    )
    password: SecretStr = Field(
        examples=["Password1234"],
        description="The password of the user",
        exclude=True,  # exclude this field from serialization
    )
    role: Role = Field(
        description="The role of the user",
        examples=[1, 2, 3, 4, 8],
        default=0,
        validate_default=True,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo) -> str:
        # print(info)
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contains only letters and be at least 2 characters long"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role, info: ValidationInfo) -> Role:
        # print(info)
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

    @model_validator(mode="after")
    def validate_user_post(self, v: Any) -> Self:
        if self.role == Role.Admin and self.name != "Arjan":
            raise ValueError("Only Arjan can be admin")
        return self

    @field_serializer("role", when_used="json")
    @classmethod
    def serialize_role(cls, v: Role) -> str:
        return v.name

    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info: SerializationInfo) -> dict[str, Any]:
        """Every parameters that we use in model_dump() method is accessable through info."""
        if not info.include and not info.exclude:
            return {"name": self.name, "role": self.role.name}
        return serializer(self)


def main() -> None:
    data = {
        "name": "Arjan",
        "email": "Ajran@gamil.com",
        "password": "Password123",
        "role": "Admin",
    }
    user = User.model_validate(data)
    if user:
        print(
            "The serializer that encodes all values to a dict:",
            dict(user),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dict, except (exclude=True) fields:",
            user.model_dump(),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dictionary with JSON-compatible data:",
            user.model_dump(mode="json"),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dictionary with JSON-compatible data, excluding the name:",
            user.model_dump(mode="json", exclude={"name"}),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a JSON string, excluding the name:",
            user.model_dump_json(indent=2, exclude={"name"}),
            sep="\n",
            end="\n\n",
        )


if __name__ == "__main__":
    main()
