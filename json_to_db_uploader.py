from reviewer.models import Game
from reviewer import db
import json

with open("games.json", encoding="utf8") as f:
    books_json = json.load(f)
    for game in books_json:
        game = Game(
            author=game["author"],
            description=game["description"],
            genre=game["genre"],
            rating=game["rating"],
            title=game["title"],
            notes=game["notes"],
        )
        db.session.add(game)
        db.session.commit()
