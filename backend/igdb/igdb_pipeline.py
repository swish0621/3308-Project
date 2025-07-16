from igdb.igdb_requests import search_game
from mongodb.mongo import * 
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage error")
        sys.exit()
    game_name = sys.argv[1]
    print(f"Searching IGDB for: {game_name}")

    try:
        results = search_game(game_name)
        if not results:
            print("No results found.")
            return

        # Add context or metadata if not exists
        games_collection = get_collection("Games")
        exists = read_doc(games_collection, {"query": game_name})
        if not (exists):
            for result in results:
                result["query"] = game_name
                result["source"] = "IGDB"

            # Insert into MongoDB
            inserted = insert_mult_docs(games_collection, results)
            print(f"Inserted {inserted} IGDB records into MongoDB.")

        else:
            print("Record already exists.")
    

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()