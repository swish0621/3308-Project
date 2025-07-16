from pymongo import MongoClient
import os
import dotenv
from dotenv import load_dotenv
import certifi

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://{username}:{password}@3308project.hvwxwa0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri,  tlsCAFile=certifi.where())

#   proposed general structure for DB looks like:
#   
#   Games
#       stores information about games 
#   RedditSamples
#       store data collected from reddit
#   YoutubeSamples
#       stores data collected from youtube
#   TwitterSamples 
#       stores data collected from twitter
#   TiktokSamples
#       stores data collected from tiktok
#   Sentiment
#       stores sentiments generated from a game

# Get collection from the media sentiment database
def get_collection(name):
    db = client["MediaSentiment"]
    return db[name]
    
# Insert multiple documents
def insert_mult_docs(collection, data_list):
    if data_list:
        result = collection.insert_many(data_list)
        return len(result.inserted_ids)
    return 0


# insert a new document to a collection 
def create_doc(collection, data):
    result = collection.insert_one(data)
    return result.inserted_id

# read a document within a collection
def read_doc(collection, query):
    return list(collection.find(query))

# update a document within a collection
def update_doc(collection, query, data):
    result = collection.update_many(query, {"$set": data})
    return result.modified_count

# delete a document within a collection
def delete_doc(collection, query):
    result = collection.delete_many(query)
    return result.deleted_count
