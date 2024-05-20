from datetime import date

import requests
from bs4 import BeautifulSoup, Tag
from cachetools import TTLCache, cached
from loguru import logger
from pydantic import AnyHttpUrl, BaseModel

BASE_URL = "https://talkpython.fm"


class Episode(BaseModel):
    show_number: int
    date: date
    title: str
    url: AnyHttpUrl
    guests: str


@cached(TTLCache(maxsize=1000, ttl=24 * 3600))
def scrape_episodes() -> list[Episode]:
    url = "https://talkpython.fm/episodes/all1"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("There is a problem in connection")
        raise requests.exceptions.ConnectionError("There is a problem in connection")
    soup = BeautifulSoup(response.text, "html.parser")

    episodes = []
    rows = soup.select("tbody > tr")
    for row in rows:
        data = extract_episode_data(row)
        episodes.append(Episode.model_validate(data))
    return episodes


def extract_episode_data(row: Tag) -> dict:
    model_data = {}
    row_data = row.select("td")
    for i, td in enumerate(row_data):
        if i == 0:
            model_data["show_number"] = td.text.removeprefix("#")
        elif i == 1:
            model_data["date"] = td.text
        elif i == 2:
            link = td.find("a").attrs["href"]  # type: ignore
            model_data["url"] = BASE_URL + link
            model_data["title"] = td.text
        else:
            model_data["guests"] = td.text

    return model_data


def main():
    episodes = scrape_episodes()
    print(episodes[0])


if __name__ == "__main__":
    main()
