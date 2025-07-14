from igdb.igdb_requests import search_game
from mongodb.mongo import get_collection, insert_mult_docs

def main():
    game_name = "The Last of Us"
    print(f"Searching IGDB for: {game_name}")

    try:
        results = search_game(game_name)
        if not results:
            print("No results found.")
            return

        # Add context or metadata
        for result in results:
            result["query"] = game_name
            result["source"] = "IGDB"

        # Insert into MongoDB
        games_collection = get_collection("Games")
        inserted = insert_mult_docs(games_collection, results)

        print(f"Inserted {inserted} IGDB records into MongoDB.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()