from pydantic import BaseModel, field_validator


class UserProfile(BaseModel):
    username: str
    email: str
    age: int

    @field_validator("age")
    def check_age(cls, value):
        if value < 18:
            raise ValueError("Age must be 18 or above")
        return value


def main():
    data1 = {
        "username": "Ali",
        "email": "Ali@gmail.com",
        "age": 20,
    }
    user1 = UserProfile(**data1)
    print(user1)

    data2 = {
        "username": "Ali",
        "email": "Ali@gmail.com",
        "age": 10,
    }
    user2 = UserProfile(**data2)
    print(user2)


if __name__ == "__main__":
    main()
