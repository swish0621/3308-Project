from flask import Blueprint, request, jsonify
from igdb.igdb_requests import *

igdb_api = Blueprint('igdb_api', __name__)

@igdb_api.route('/api/igdb/game', methods=['GET'])
def get_igdb_game():
    print(f"IGDB endpoint called with name: {request.args.get('name')}")
    game_name = request.args.get('name')
    if not game_name:
        return jsonify({'error': 'Missing game name'}), 400
    try:
        results = search_game(game_name)
        if not results:
            print(f"IGDB: No results found for {game_name}")
            return jsonify({'error': 'No results found'}), 404
        return jsonify(results)
    except Exception as e:
        import traceback
        print(f"IGDB API error for {game_name}: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
