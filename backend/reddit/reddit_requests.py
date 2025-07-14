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

# create reddit instance 
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def search_keyword(word):   
    keyword = word
    data = []

    # if the keyword is listed as a subreddit search that subreddit
    if (subreddit_exists(keyword.replace(" ", ""))): 
        subreddit=reddit.subreddit(keyword.replace(" ", ""))
        for submission in subreddit.hot(limit=5):
            
            # add post info to data in json format 
            data.append({
                "type": "submission",
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "date": datetime.fromtimestamp(submission.created_utc).isoformat()
            })

            # expand comment tree 
            submission.comments.replace_more(limit=0)
            for comment in list(submission.comments)[:10]:
                # add comment info to data
                data.append({
                        "type": "comment",
                        "id": comment.id,
                        "parent_id": comment.parent_id,
                        "body": comment.body,
                        "score": comment.score,
                        "date": datetime.fromtimestamp(comment.created_utc).isoformat()
                })
        return data
    
    # if the subreddit doesnt exist check the gaming subreddit
    else:
        for submission in reddit.subreddit("gaming").new(limit=50):
            if keyword.lower() in submission.title.lower():

                # add post info to data in json format 
                data.append({
                    "type": "submission",
                    "id": submission.id,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "score": submission.score,
                    "date": datetime.fromtimestamp(submission.created_utc).isoformat()
                })

                # expand comment tree fully 
                submission.comments.replace_more(limit=0)
                for comment in list(submission.comments)[:10]:

                    # add comment info 
                    data.append({
                        "type": "comment",
                        "id": comment.id,
                        "parent_id": comment.parent_id,
                        "body": comment.body,
                        "score": comment.score,
                        "date": datetime.fromtimestamp(comment.created_utc).isoformat()
                })
        return data


# helper function to check if a subreddit exists
def subreddit_exists(name):
    try:
        reddit.subreddits.search_by_name(name, exact=True)
        return True
    except NotFound:
        return False
    