from flask import Flask, jsonify
import pandas as pd
from youtube_pipeline.calc_sentiment import calc_sentiment
from igdb.igdb_api import igdb_api
from flask_cors import CORS
from mongodb.mongo import get_collection
import subprocess
import threading

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
    results = collection.find({"game": {"$regex": f"^{game.strip()}$", "$options": "i"}})
    resultsList = list(results)

    if not resultsList:
        def run_pipeline():
            subprocess.run(['python', '-m', 'youtube_pipeline.linker_copy', game])
        threading.Thread(target=run_pipeline).start()
        return jsonify({
            'message': 'No data found, loading data...',
            'sentiment_distribution': {"Positive": 0, "Negative": 0, "Neutral": 0},
            "total_comments": 0,
            "game": game,
            "source": source
            }), 202
                               
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    total = 0

    for doc in resultsList:
        avg = doc.get("average_sentiment")
        if avg is not None:
            if avg > 0.05:
                label = "Positive"
            elif avg < -0.05:
                label = "Negative"
            else:
                label = "Neutral"
            sentiments[label] += 1
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