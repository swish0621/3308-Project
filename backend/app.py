from flask import Flask, jsonify
import pandas as pd
from youtube_pipeline.calc_sentiment import calc_sentiment

app = Flask(__name__)

@app.route('/api/youtube/sentiment', methods=['GET'])
def get_youtube_sentiment():
    # example: load YouTube comments from a CSV (update path as needed)
    try:
        df = pd.read_csv('backend/youtube_pipeline/youtube_comments.csv')  # <-- Update if your file is elsewhere
        avg_df = calc_sentiment(df)
        return avg_df.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)