from typing import Annotated, Literal

from annotated_types import Gt
from pydantic import BaseModel


class Fruit(BaseModel):
    name: str
    color: Literal["red", "green"]
    weight: Annotated[float, Gt(10)]
    bazam: dict[str, list[tuple[int, bool, float]]]


def main():
    data1 = {
        "name": "Apple",
        "color": "red",
        "weight": 14.2,
        "bazam": {"foobar": [(1, True, 0.1)]},
    }
    fruit1 = Fruit(**data1)
    print(fruit1)

    data2 = {
        "name": "Apple",
        "color": "red",
        "weight": 4.2,
        "bazam": {"foobar": [(1, True, 0.1)]},
    }
    fruit2 = Fruit(**data2)
    print(fruit2)


if __name__ == "__main__":
    main()
