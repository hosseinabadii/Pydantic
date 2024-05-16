import os
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated
from uuid import UUID

from api import get_data
from enums import Department
from pydantic import BaseModel, Field, field_validator

os.system("clear")


class Student(BaseModel):
    id: UUID
    name: str
    date_of_birth: date
    GPA: Annotated[float, Field(ge=0, le=4)]
    course: str | None
    department: Department
    fees_paid: bool

    @field_validator("date_of_birth")
    @classmethod
    def ensure_16_or_over(cls, v: date) -> date:
        sixteen_years_ago = date.today() - timedelta(days=16 * 365)
        if v > sixteen_years_ago:
            raise ValueError("Too young to enrol, sorry!")
        return v


def main(file_path: Path) -> None:
    data = get_data(file_path)
    for student in data:
        model = Student(**student)
        print(model)
        print("-" * 50)

    print("\n\nSerialization:")
    print(
        "The serializer that encodes all values to a dict:",
        dict(model),
        sep="\n",
        end="\n\n",
    )

    print(
        "The serializer that returns a dict, excluding the date_of_birth:",
        model.model_dump(exclude={"date_of_birth"}),
        sep="\n",
        end="\n\n",
    )

    print(
        "The serializer that returns a dictionary with JSON-compatible data:",
        model.model_dump(mode="json"),
        sep="\n",
        end="\n\n",
    )

    print(
        "The serializer that returns a dictionary with JSON-compatible data, including the name and GPA:",
        model.model_dump(mode="json", include={"name", "GPA"}),
        sep="\n",
        end="\n\n",
    )

    print(
        "The serializer that returns a JSON string, excluding the name:",
        model.model_dump_json(indent=2, exclude={"name"}),
        sep="\n",
        end="\n\n",
    )


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    main(BASE_DIR / "data/students_v1.json")
