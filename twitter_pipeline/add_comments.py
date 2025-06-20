import requests
import pandas as pd
import time

def load_bearer_token(path="twitter_bearer_token.txt"):
    with open(path, "r") as file:
        return file.read().strip()

def get_replies(tweet_id, max_results=10):
    """
    Retrieve recent replies (tweets in the same conversation) to the given tweet ID.
    
    Parameters:
    - tweet_id: The ID of the original tweet whose conversation replies we want.
    - max_results: The maximum number of replies to retrieve (up to 100 per request).
    
    Handles 429 (Too Many Requests) error by waiting and retrying.
    
    Returns:
    - A list of dictionaries, each containing reply text, author_id, and created_at timestamp.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    bearer_token = load_bearer_token()
    
    # query parameters
    params = {
        "query": f"conversation_id:{tweet_id}",
        "max_results": min(max_results, 100),
        "tweet.fields" : "author_id,conversation_id,created_at,text"
    }
    
    # authorization header
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    
    while True:
        # make 'get' request to twitter's API
        response = requests.get(url, headers=headers, params=params)
        
        # handle rate limiting by waiting before retrying
        if response.status_code == 429:
            print("Rate limit hit. Waiting 60 seconds before retrying...")
            time.sleep(60)
            continue
            
        # raise an error if another http error occurs
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} {response.text}")
        
        # json response and build list of replies
        data = response.json()
        replies = [
            {
                "reply_text": item["text"],
                "author_id": item["author_id"],
                "created_at": item["created_at"]
            }
            for item in data.get("data", [])
        ]
        return replies

def add_replies(df, max_results=10):
    """
    For each row in the input DataFrame (representing original tweets),
    retrieve replies and build a new DataFrame containing reply details.
    
    Parameters:
    - df: dataframe with columns 'tweet_id', 'title', and 'period'
    - max_results: Number of replies to attempt to retrieve per tweet
    
    Returns:
    - A dataframe containing period, tweet_id, title, reply_text, author_id, created_at
    """
    rows = []
    
    # iterate over each tweet in the input dataframe
    for _, row in df.iterrows():
        tweet_id = row["tweet_id"]
        title = row["title"]
        period = row["period"]
        try:
            # get replies for current tweet
            reply_list = get_replies(tweet_id, max_results)
            for reply in reply_list:
                rows.append({
                    "period": period,
                    "tweet_id": tweet_id,
                    "title": title,
                    "reply_text": reply["reply_text"],
                    "author_id": reply["author_id"],
                    "created_at": reply["created_at"]
                })
        except Exception as e:
                print(f"Failed to get replies for tweet {tweet_id}: {e}")
                
    # return the assembled dataframe
    return pd.DataFrame(rows)   

# example dataframe of tweets to process
df = pd.DataFrame([
    {
        "tweet_id": "1934268257021640845",  # actual tweet ID
        "title": "Example Post",
        "period": "2025-06"
    }
])

# get replies and build result dataframe
result_df = add_replies(df, max_results=10)

# show the result shape and first few rows
print(result_df.shape)
print(result_df.head())

# save to csv only if there are replies
if not result_df.empty:
    result_df.to_csv("twitter_replies.csv", index=False)
    print("Saved CSV successfully!")
else:
    print("No replies found. CSV not saved.")
    

# read back and display csv for verification if it was saved
pd.read_csv("twitter_replies.csv").head()