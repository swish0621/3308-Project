# -*- coding: utf-8 -*-
"""
Created on Fri May  9 18:03:48 2025

@author: kenji

Get comments given youtube IDs
"""

import requests
import pandas as pd

def load_api_key(path="youtube_api.txt"):
    with open(path, "r") as file:
        return file.read().strip()



def get_comments(video_id, max_comments):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    api_key = load_api_key()
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": max_comments,
        "textFormat": "plainText"
    }
    response = requests.get(url, params=params)
    data = response.json()
    comments = [
        item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        for item in data.get("items", [])
    ]
    return comments
    
def add_comments(df, max_comments):
    rows = []
    for _, row in df.iterrows():
        video_id = row['video_id']
        title = row['title']
        period = row['period'] 
        try:
            comment_list = get_comments(video_id, max_comments)
            for comment in comment_list:
                rows.append({
                    'period': period,
                    'video_id': video_id,
                    'title': title,
                    'comment': comment
                })
        except Exception as e:
            print(f"Failed to get comments for video {video_id}: {e}")

    return pd.DataFrame(rows)