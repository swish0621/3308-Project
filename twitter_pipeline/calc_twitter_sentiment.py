# -*- coding: utf-8 -*-
"""
Created 6/25/25

author: nsawtelle

get sentiment of twitter replies
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

model_name = "AmaanP314/youtube-xlm-roberta-base-sentiment-multilingual"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def classify_sentiment(replies):

    inputs = tokenizer(
        replies,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )
    
    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=1)
    label_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
    return [label_mapping[p.item()] for p in predictions]


def extract_tweet_sentiment(df):

    sentiment_results = []
    
    grouped = df.groupby("period")
    for period, group in tqdm(grouped, desc="Classifying Twitter Sentiment by Period"):
        texts = group["reply_text"].tolist()
        if texts:
            sentiments = classify_sentiment(texts)
            for i, row in group.iterrows():
                sentiment_results.append({
                    "period": period,
                    "tweet_id": row["tweet_id"],
                    "title": row["title"],
                    "reply_text": row["reply_text"],
                    "sentiment": sentiments[i - group.index[0]]
                })

    return pd.DataFrame(sentiment_results)


def calc_sentiment(df):

    df = extract_tweet_sentiment(df)
    
    # Save full replies with sentiment to CSV
    df.to_csv("twitter_sentiment_classified.csv", index=False)
    
    # Convert sentiment to numerical scores
    score_map = {"Negative": -1, "Neutral": 0, "Positive": 1}
    df["sentiment_score"] = df["sentiment"].map(score_map)
    
    # Compute average sentiment per period
    avg_df = df.groupby("period")["sentiment_score"].mean().reset_index()
    avg_df.rename(columns={"sentiment_score": "average_sentiment"}, inplace=True)
    
    return avg_df


# main execution

if __name__ == "__main__":
    # Load replies from previous script
    replies_df = pd.read_csv("twitter_replies.csv")
    
    # Calculate sentiment and get average by period
    avg_sentiment_df = calc_sentiment(replies_df)
    
    # Save average sentiment to CSV
    avg_sentiment_df.to_csv("twitter_average_sentiment.csv", index=False)
    print("Saved twitter_average_sentiment.csv")