import os
from typing import Annotated

from pydantic import AfterValidator, BaseModel

os.system("clear")


def validate_hash_tag(value: str) -> str:
    if not value.startswith("#"):
        raise ValueError("Hash tag must start with a '#'")
    return value


HashTagType = Annotated[str, AfterValidator(validate_hash_tag)]


class Test(BaseModel):
    hash_tag_1: HashTagType
    hash_tag_2: HashTagType


def main():
    data_1 = {
        "hash_tag_1": "#python",
        "hash_tag_2": "#programming",
    }
    try:
        model_1 = Test.model_validate(data_1)
        print(model_1)
    except ValueError as e:
        print(e)
    finally:
        print("-" * 50)

    data_2 = {
        "hash_tag_1": "python",
        "hash_tag_2": "programming",
    }
    try:
        model_2 = Test.model_validate(data_2)
        print(model_2)
    except ValueError as e:
        print(e)
    finally:
        print("-" * 50)


if __name__ == "__main__":
    main()
