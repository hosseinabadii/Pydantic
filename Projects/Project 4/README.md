# Talk Python Episode Dashboard

This project is a Python-based dashboard for scraping and searching episodes from the "Talk Python" website. The dashboard is built using Streamlit, allowing users to filter episodes based on their titles and dates.

## Features

- **Web Scraping**: Extracts episode information (titles and dates) from the "[Talk Python Episodes](https://talkpython.fm/episodes/all)" page.
- **Interactive Dashboard**: Built with Streamlit for easy interaction and filtering.
- **Filtering Options**: Filter episodes by title and date.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.10 +
- `pip` (Python package installer)

## Installation

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to the URL shown in the terminal, typically `http://localhost:8501`.

3. Use the web interface to filter episodes based on their title and date.

## Project Structure

- `app.py`: The main script for running the Streamlit dashboard.
- `scraper.py`: Contains the function for scraping the Talk Python episodes.
- `README.md`: This file.
- `requirements.txt`: Lists the Python packages required to run the project.
