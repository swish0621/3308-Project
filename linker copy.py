# -*- coding: utf-8 -*-
"""
Created on Fri May  9 20:02:22 2025

@author: kenji
"""

import pandas as pd
from get_ids import search_videos
from add_comments import add_comments
from calc_sentiment import calc_sentiment

import matplotlib.pyplot as plt

def main():
    topic = "Call of Duty" # Edit later to take these as param
    start_time = "2020-01-01T00:00:00Z"
    end_time = "2022-02-01T00:00:00Z"
    period = [0,1,0] # years, months, days
    vid_per_period = 10
    max_comments = 50
    
    print("Getting Video IDs...")
    periods, video_ids, titles = search_videos(topic, start_time, end_time, vid_per_period, period)

    df = pd.DataFrame({
        "period": periods,
        "video_id": video_ids,
        "title": titles
    })
    
    print("Getting Video Comments...")
    df = add_comments(df, max_comments)
    print(df[:20])
    num_comments = df.shape[0]
    
    print("Calculating Sentiment...")
    df = calc_sentiment(df)
    
    print(f"""Finished!
          Number of Comments: {num_comments}
          Number of Periods: {df.shape[0]}
          """)
          
          
    df.to_csv("output.csv", index=False)

if __name__ == "__main__":
    main()
    