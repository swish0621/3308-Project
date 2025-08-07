from flask import Flask, jsonify
import pandas as pd
from youtube_pipeline.calc_sentiment import calc_sentiment
from igdb.igdb_api import igdb_api
from flask_cors import CORS
from mongodb.mongo import get_collection

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for debugging
app.register_blueprint(igdb_api)

@app.route('/api/youtube/sentiment', methods=['GET'])
def get_youtube_sentiment():
    # example: load YouTube comments from a CSV (update path as needed)
    try:
        df = pd.read_csv('backend/youtube_pipeline/youtube_comments.csv')  # <-- Update if your file is elsewhere
        avg_df = calc_sentiment(df)
        return avg_df.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/sentiment/<source>/<game>', methods=['GET'])
def get_sentiment(source, game):
    collection_name_map = {
        "reddit": "RedditSamples",
        "youtube": "YoutubeSamples"
    }

    collection_name = collection_name_map.get(source.lower())
    if not collection_name:
        return jsonify({'error': f'Unsupported Source: {source}'}), 400
    
    collection = get_collection(collection_name)
    results = collection.find({"game": game, "type": "comment"})
                               
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    total = 0

    for doc in results:
        sentiment = doc.get("sentiment")
        if sentiment in sentiments:
            sentiments[sentiment] += 1
            total += 1

    if total == 0:
        return jsonify({"message": "No sentiment data found", "data": {}}), 404
    
    for key in sentiments:
        sentiments[key] = round((sentiments[key] / total) * 100, 2)

    return jsonify({
        "game": game,
        "source": source,
        "total_comments": total,
        "sentiment_distribution": sentiments
    })
    

if __name__ == '__main__':
    app.run(debug=True)