from flask import render_template, send_from_directory, request

from reviewer.models import Game
from reviewer import app


@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    games = Game.query.order_by(Game.created_at.desc()).paginate(page=page, per_page=4)
    return render_template("index.html", games=games)


@app.route("/uploads/<filename>")
def send_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/<int:game_id>/")
def game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template("games.html", game=game)


@app.route("/best/")
def best():
    page = request.args.get("page", 1, type=int)
    games = Game.query.filter(Game.rating > 4).paginate(page=page, per_page=4)
    return render_template("best.html", games=games)


@app.route("/thrillers/")
def thrillers():
    page = request.args.get("page", 1, type=int)
    games = Game.query.filter(Game.genre == "триллер").paginate(page=page, per_page=4)
    return render_template("thrillers.html", games=games)
