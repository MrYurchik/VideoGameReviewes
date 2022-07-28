import os
import secrets

from flask import (
    render_template,
    send_from_directory,
    request,
    flash,
    url_for,
    redirect,
    jsonify,
)
from sqlalchemy.exc import IntegrityError

from reviewer.forms import GameForm, UpdateGame
from PIL import Image
from reviewer.models import Game
from reviewer import app, db


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


def save_picture(cover):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(cover.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], picture_fn)

    output_size = (220, 340)
    i = Image.open(cover)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/create/", methods=("GET", "POST"))
def create():
    form = GameForm()
    if form.validate_on_submit():
        if form.cover.data:
            cover = save_picture(form.cover.data)
        else:
            cover = "default.jpg"
        title = form.title.data
        author = form.author.data
        genre = form.genre.data
        rating = int(form.rating.data)
        description = form.description.data
        notes = form.notes.data
        book = Game(
            title=title,
            author=author,
            genre=genre,
            rating=rating,
            cover=cover,
            description=description,
            notes=notes,
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("create.html", form=form)


@app.route("/<int:game_id>/edit/", methods=("GET", "POST"))
def edit(game_id):
    game = Game.query.get_or_404(game_id)
    form = UpdateGame()
    if form.validate_on_submit():
        if form.cover.data:
            cover = save_picture(form.cover.data)
        else:
            cover = game.cover
        game.title = form.title.data
        game.author = form.author.data
        game.genre = form.genre.data
        game.rating = int(form.rating.data)
        game.description = form.description.data
        game.notes = form.notes.data
        try:
            flash("Try to write to db")
            db.session.commit()
            return redirect(url_for("index"))
        except IntegrityError:
            db.session.rollback()
            flash("Error, this game already exist", "error")
            return render_template("edit.html", form=form)

    elif request.method == "GET":
        form.title.data = game.title
        form.author.data = game.author
        form.genre.data = game.genre
        form.rating.data = game.rating
        form.cover.data = game.cover
        form.description.data = game.description
        form.notes.data = game.notes

    return render_template("edit.html", form=form)


@app.post("/<int:game_id>/delete/")
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/export/")
def data():
    data = Game.query.all()
    return jsonify(data)
