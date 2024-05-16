import os

from pydantic import BaseModel, EmailStr, Field, HttpUrl, PositiveInt, field_validator

os.system("clear")


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Employee(BaseModel):
    name: str
    position: str
    email: EmailStr


class Owner(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("Owner name must contain a space")
        return v.title()


class Restaurant(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9-' ]+$")
    owner: Owner
    address: Address
    employees: list[Employee] = Field(min_length=2)
    number_of_seats: PositiveInt
    delivery: bool
    website: HttpUrl


restaurant_data = {
    "name": "Tasty Bites",
    "owner": {
        "name": "john doe",
        "email": "john.doe@example.com",
    },
    "address": {
        "street": "123, Flavor Street",
        "city": "Tastytown",
        "state": "TS",
        "zip_code": "12345",
    },
    "employees": [
        {
            "name": "Jane Doe",
            "position": "Chef",
            "email": "jane.doe@example.com",
        },
        {
            "name": "Mike Roe",
            "position": "waiter",
            "email": "mike.roe@example.com",
        },
    ],
    "number_of_seats": "50",
    "delivery": "True",
    "website": "https://tastybites.com",
}


def main():
    restaurant_instance = Restaurant.model_validate(restaurant_data)
    if restaurant_instance:
        print(
            "print the actual restaurant instance:",
            restaurant_instance,
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a JSON string:",
            restaurant_instance.model_dump_json(indent=4),
            sep="\n",
            end="\n\n",
        )


if __name__ == "__main__":
    main()
