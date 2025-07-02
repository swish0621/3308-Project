# -*- coding: utf-8 -*-
"""
Created on Fri May  9 19:26:41 2025

@author: kenji

Purpose: Grab Youtube IDs based on a topic and time period
"""

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_api_key(path="youtube_api.txt"):
    with open(path, "r") as file:
        return file.read().strip()
    
def calc_date(curr_date, period):
    """
    period input : [years, months, days]
    """
    dt = datetime.strptime(curr_date, "%Y-%m-%dT%H:%M:%SZ")
    delta = relativedelta(years=period[0], months=period[1], days=period[2])
    new_dt = dt + delta
    return new_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    

def search_videos(topic, start_time, end_time, max_results, period):
    API_key = load_api_key()

    if max_results > 50:
        print(f"Error: {max_results} videos per period exceeds Youtube API limit. Reducing to 50")
        max_results = 50

    lower_date = start_time
    upper_date = calc_date(lower_date, period)

    all_video_ids = []
    all_titles = []
    all_periods = [] 

    while lower_date < end_time:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": topic,
            "type": "video",
            "order": "date",
            "publishedAfter": lower_date,
            "publishedBefore": upper_date,
            "maxResults": max_results,
            "key": API_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            reason = data['error']['errors'][0].get('reason', 'No reason found')
            raise Exception(f"Error: {reason}")
            break

        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            all_video_ids.append(video_id)
            all_titles.append(title)
            all_periods.append(lower_date)

        lower_date = upper_date
        upper_date = calc_date(lower_date, period)
        if upper_date > end_time:
            upper_date = end_time

    # video IDs, titles, and periods
    return all_periods, all_video_ids, all_titles

"""
EXAMPLE 
topic = "tesla"
start_time = "2023-12-01T00:00:00Z"
end_time = "2024-01-01T00:00:00Z"
max_results = 10
video_ids, titles = search_videos(topic, start_time, end_time, max_results)
print(video_ids)
"""
