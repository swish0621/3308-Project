import os 
import praw
import prawcore
from prawcore import NotFound
import dotenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# load credentials 
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def search_keyword(word):   
    keyword = word
    data = []
    if (subreddit_exists(keyword.replace(" ", ""))): 
        subreddit=reddit.subreddit(keyword.replace(" ", ""))
        for submission in subreddit.hot(limit=5):
            data.append({
                "type": "submission",
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "date": datetime.fromtimestamp(submission.created_utc).isoformat()
            })
            submission.comments.replace_more(limit=0)
            for comment in list(submission.comments)[:10]:
                data.append({
                        "type": "comment",
                        "id": comment.id,
                        "parent_id": comment.parent_id,
                        "body": comment.body,
                        "score": comment.score,
                        "date": datetime.fromtimestamp(comment.created_utc).isoformat()
                })
        return data
    else:
        for submission in reddit.subreddit("gaming").new(limit=50):
            if keyword.lower() in submission.title.lower():
                data.append({
                    "type": "submission",
                    "id": submission.id,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "score": submission.score,
                    "date": datetime.fromtimestamp(submission.created_utc).isoformat()
                })
                submission.comments.replace_more(limit=0)
                for comment in list(submission.comments)[:10]:
                    data.append({
                        "type": "comment",
                        "id": comment.id,
                        "parent_id": comment.parent_id,
                        "body": comment.body,
                        "score": comment.score,
                        "date": datetime.fromtimestamp(comment.created_utc).isoformat()
                })
        return data

    
def subreddit_exists(name):
    try:
        reddit.subreddits.search_by_name(name, exact=True)
        return True
    except NotFound:
        return False
    