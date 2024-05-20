import os
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated, Any, Literal
from uuid import UUID

from api import get_data
from enums import Department
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing_extensions import Self

os.system("clear")


class Modules(BaseModel):
    id: int | UUID
    name: str
    professor: str
    credits: Literal[10, 20]
    registration_code: str


class Student(BaseModel):
    id: UUID
    name: str
    date_of_birth: date
    GPA: Annotated[float, Field(ge=0, le=4)]
    course: str | None
    department: Department
    fees_paid: bool
    modules: list[Modules] = []

    model_config = ConfigDict(
        use_enum_values=True,
        title="Students Model",
        extra="ignore",  # "forbid", "allow"
    )

    @field_validator("date_of_birth")
    @classmethod
    def ensure_16_or_over(cls, v: date) -> date:
        sixteen_years_ago = date.today() - timedelta(days=16 * 365)
        if v > sixteen_years_ago:
            raise ValueError("Too young to enrol, sorry!")
        return v

    @field_validator("modules")
    @classmethod
    def must_have_3_modules(cls, v: list[Modules]) -> list[Modules]:
        if v and len(v) != 3:
            raise ValueError("You must have 3 mudules.")
        return v

    @model_validator(mode="after")
    def validate_gpa_and_department(self, v: Any) -> Self:
        dept_science = self.department == Department.SCIENCE_AND_ENGINEERING.value
        if dept_science and not (self.GPA >= 3.0):
            raise ValueError("GPA not enough for S&E")
        return self


def main(file_path: Path) -> None:
    data = get_data(file_path)
    for student in data:
        try:
            model = Student.model_validate(student)
            print(model)
            print("-" * 50)
        except ValueError as e:
            print(e)

    print("-" * 50)
    print("Excluding nested fields: 'id' and 'registration_code'")
    excludes = {"id": True, "modules": {"__all__": {"registration_code"}}}
    print(model.model_dump(exclude=excludes))


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    main(BASE_DIR / "data/students_v2.json")
