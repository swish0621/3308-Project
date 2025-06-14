# -*- coding: utf-8 -*-
"""
Created on Sat May 10 18:28:41 2025

@author: kenji

get sentiment of each youtube comment
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

def classify_sentiment(comments):
    model_name = "AmaanP314/youtube-xlm-roberta-base-sentiment-multilingual"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    inputs = tokenizer(comments, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=1)
    label_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiments = [label_mapping[p.item()] for p in predictions]
    return sentiments



def extract_sentiment_scores(df):
    sentiment_results = []
    
    grouped = df.groupby("period")
    for period, group in tqdm(grouped, desc="Classifying Sentiment by Period"):
        comments = group["comment"].tolist()
        if comments:
            sentiments = classify_sentiment(comments)
            for i, row in group.iterrows():
                sentiment_results.append({
                    "period": period,
                    "video_id": row["video_id"],
                    "title": row["title"],
                    "comment": row["comment"],
                    "sentiment": sentiments[i - group.index[0]] 
                })

    return pd.DataFrame(sentiment_results)

def calc_sentiment(df):
    df = extract_sentiment_scores(df)
    df.to_csv("calc_semantics.csv", index=False)
    score_map = {"Negative": -1, "Neutral": 0, "Positive": 1} # map sentiments to integer value
    df["sentiment_score"] = df["sentiment"].map(score_map)

    # Get average score by period
    avg_df = df.groupby("period")["sentiment_score"].mean().reset_index()

    # The linker.py wants a different name
    avg_df.rename(columns={"sentiment_score": "average_sentiment"}, inplace=True)

    return avg_df
    
    
    