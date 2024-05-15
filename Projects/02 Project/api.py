# import requests
import json
from pathlib import Path
from typing import Any

# url = "https://raw.githubusercontent.com/hosseinabadii/Pydantic/main/Projects/02%20Project/data/students_v1.json"


# def get_data(url: str = url) -> dict:
#     response = requests.get(url)
#     if not response.status_code == 200:
#         raise ConnectionError(f"connection error with {response.status_code} code!")
#     return response.json()


def get_data(file_path: Path) -> list[dict[str, Any]]:
    with open(file_path) as f:
        return json.load(f)
