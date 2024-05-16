import os

from pydantic import BaseModel

os.system("clear")


class Food(BaseModel):
    name: str
    price: float
    ingredients: list[str] | None = None


class Restaurant(BaseModel):
    name: str
    location: str
    foods: list[Food]


data = {
    "name": "Tasty Bites",
    "location": "123, Flavor Street",
    "foods": [
        {
            "name": "Cheese Pizza",
            "price": "12.50",
            "ingredients": ["cheese", "Tomato Sauce", "Dough"],
        },
        {
            "name": "Veggie Burger",
            "price": "8.99",
        },
    ],
}


def main():
    restaurant_instance = Restaurant.model_validate(data)
    if restaurant_instance:
        print(
            "print the actual restaurant instance:",
            restaurant_instance,
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that encodes all values to a dict:",
            dict(restaurant_instance),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dict, except (exclude=True) fields:",
            restaurant_instance.model_dump(),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dictionary with JSON-compatible data:",
            restaurant_instance.model_dump(mode="json"),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a dictionary with JSON-compatible data, excluding the name:",
            restaurant_instance.model_dump(mode="json", exclude={"name"}),
            sep="\n",
            end="\n\n",
        )

        print(
            "The serializer that returns a JSON string, excluding the name:",
            restaurant_instance.model_dump_json(indent=2, exclude={"name"}),
            sep="\n",
            end="\n\n",
        )


if __name__ == "__main__":
    main()
