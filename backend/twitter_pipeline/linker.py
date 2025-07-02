# -*- coding: utf-8 -*-
"""
Created on June 25, 2025

Adapted by: nsawtelle

End-to-end Twitter pipeline: search → replies → sentiment
"""

import pandas as pd
from get_ids import search_tweets    # formerly search_videos
from add_comments import add_replies    # formerly add_comments
from calc_sentiment import calc_sentiment

import matplotlib.pyplot as plt

def main():
    topic = '"Call of Duty"'  # quoted to treat as exact phrase
    start_time = "2025-06-20T00:00:00Z"  # Twitter: must be within last 7 days
    end_time = "2025-06-26T00:00:00Z"
    period = [0, 0, 2]  # every 2 days
    tweets_per_period = 5  # keep low to avoid rate limits
    replies_per_tweet = 10  # max replies per tweet

    print("Searching for Tweets...")
    periods, tweet_ids, texts = search_tweets(topic, start_time, end_time, tweets_per_period, period)

    df = pd.DataFrame({
        "period": periods,
        "tweet_id": tweet_ids,
        "title": texts  # rename "title" to "text" to match tweet body
    })

    print("Getting Replies to Tweets...")
    df = add_replies(df, max_results=replies_per_tweet)  # adds reply_text, created_at, etc.

    print(df.head(10))
    num_replies = df.shape[0]

    print("Calculating Sentiment...")
    sentiment_df = calc_sentiment(df)

    print(f"""Finished!
    Number of Replies: {num_replies}
    Number of Periods: {sentiment_df.shape[0]}
    """)

    df.to_csv("twitter_replies_with_sentiment.csv", index=False)
    sentiment_df.to_csv("twitter_avg_sentiment.csv", index=False)

if __name__ == "__main__":
    main()