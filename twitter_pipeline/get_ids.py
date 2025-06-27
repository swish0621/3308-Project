# -*- coding: utf-8 -*-
"""
Created 6/25/25

author: nsawtelle

Grab Twitter post IDs based on a topic and time period
"""

import time
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_bearer_token(path="twitter_bearer_token.txt"):
    with open(path, "r") as file:
        return file.read().strip()

def calc_date(curr_date, period):
    dt = datetime.strptime(curr_date, "%Y-%m-%dT%H:%M:%SZ")
    delta = relativedelta(years=period[0], months=period[1], days=period[2])
    new_dt = dt + delta
    return new_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def search_tweets(topic, start_time, end_time, max_results, period):
    bearer_token = load_bearer_token()

    if max_results > 10:
        print(f"Max allowed per period is 100. Reducing to 100.")
        max_results = 10

    all_tweet_ids = []
    all_texts = []
    all_periods = []

    lower_date = start_time
    upper_date = calc_date(lower_date, period)

    while lower_date < end_time:
        url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            "query": topic,
            "start_time": lower_date,
            "end_time": upper_date,
            "max_results": max_results,
            "tweet.fields": "created_at"
        }
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        reset_time = int(response.headers.get("x-rate-limit-reset", time.time() + 60))
        now = int(time.time())
        remaining = int(response.headers.get("x-rate-limit-remaining", 1))
        
        #if response.status_code == 429:
         #   print("Rate limit hit. Waiting 60 seconds before retrying...")
         #   time.sleep(60)
         #   continue
        if response.status_code == 429 or remaining == 0:
            wait_time = max(reset_time - now, 60)
            print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            continue
        elif response.status_code != 200:
            raise Exception(f"Twitter API error {response.status_code}: {response.text}")

        #if response.status_code != 200:
         #   raise Exception(f"Twitter API error {response.status_code}: {response.text}")

        for item in data.get("data", []):
            tweet_id = item["id"]
            text = item["text"]
            all_tweet_ids.append(tweet_id)
            all_texts.append(text)
            all_periods.append(lower_date)

        # Advance time window
        lower_date = upper_date
        upper_date = calc_date(lower_date, period)
        if upper_date > end_time:
            upper_date = end_time

    return all_periods, all_tweet_ids, all_texts


"""

# Example

topic = "The Last of Us"
start_time = "2025-06-25T00:00:00Z"  # Must be within past 7 days
end_time = "2025-06-26T00:00:00Z"
max_results = 10
period = [0, 0, 1]  # 2-day intervals

# Run the search
periods, tweet_ids, texts = search_tweets(topic, start_time, end_time, max_results, period)

# Convert to DataFrame
df = pd.DataFrame({
    "period": periods,
    "tweet_id": tweet_ids,
    "text": texts
})

# Display the first few results
print(df.head())

# Save to CSV
df.to_csv("last_of_us_tweets.csv", index=False)
print("Saved to last_of_us_tweets.csv")

"""