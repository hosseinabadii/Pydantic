import streamlit as st

from scraper import scrape_episodes

episodes = scrape_episodes()

st.title("Talk Python Episode Dashboard")
st.write("https://talkpython.fm/episodes/all")

min_date = min(episode.date for episode in episodes)
max_date = max(episode.date for episode in episodes)
title_filter = st.text_input("Filter by Title", "Python")
start_date = st.date_input("Start date", min_date, min_date, max_date, "start_date")
end_date = st.date_input("End date", max_date, min_date, max_date, "end_date")

show_episodes = st.button("Show Episodes")
if show_episodes:
    filtered_episodes = [
        ep
        for ep in episodes
        if (title_filter.lower() in ep.title.lower() if title_filter else True)
        and (start_date <= ep.date <= end_date)  # type: ignore
    ]
    st.success(f"{len(filtered_episodes)} episodes found!")
    for ep in filtered_episodes:
        st.write(f"**Title:** {ep.title}")
        st.write(f"**Date:** {ep.date}")
        st.write(f"**Link:** {ep.url}")
        st.write("---")
