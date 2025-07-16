from reddit.reddit_requests import search_keyword
from mongodb.mongo import get_collection, insert_mult_docs
from youtube_pipeline.calc_sentiment import calc_sentiment  # reuses existing sentiment code
import pandas as pd


def main():
    topic = "The Last of Us"
    print(f"Searching Reddit for: {topic}")

    reddit_data = search_keyword(topic)

    if not reddit_data:
        print("No data returned from Reddit.")
        return

    df = pd.DataFrame(reddit_data)

    # Apply sentiment analysis to comments
    comment_mask = df["type"] == "comment"
    if comment_mask.any():
        df_comments = df[comment_mask].copy()
        df_comments['date'] = pd.to_datetime(df_comments['date'])
        df_comments['period'] = df_comments['date'].dt.to_period('D')
        df_comments = df_comments.rename(columns={"body": "comment"})
        df_comments['video_id'] = None
        df_comments = calc_sentiment(df_comments)
        df.update(df_comments)  # merge sentiment columns back into full df

    # Add game/topic label
    df["game"] = topic

    # Insert into MongoDB
    reddit_collection = get_collection("RedditSamples")
    num_inserted = insert_mult_docs(reddit_collection, df.to_dict("records"))

    print(f"Inserted {num_inserted} Reddit records into MongoDB.")

if __name__ == "__main__":
    main()