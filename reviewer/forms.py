from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from reviewer.models import Game


class GameForm(FlaskForm):
    title = StringField("Tittle", validators=[DataRequired(), Length(min=3, max=100)])
    author = StringField("Author", validators=[DataRequired(), Length(min=5, max=100)])
    genre = StringField("Genre", validators=[DataRequired(), Length(min=5, max=20)])
    cover = FileField("Cover", validators=[FileAllowed(["jpg", "png"])])
    rating = IntegerField(
        "My rating", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    notes = TextAreaField("Notes", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Add")

    @staticmethod
    def validate_title(title):
        if Game.query.filter_by(title=title.data).first():
            raise ValidationError("This game already exist!")


class UpdateGame(FlaskForm):
    title = StringField("Tittle", validators=[DataRequired(), Length(min=5, max=100)])
    author = StringField("Author", validators=[DataRequired(), Length(min=5, max=100)])
    genre = StringField("Genre", validators=[DataRequired(), Length(min=5, max=100)])
    cover = FileField("Cover", validators=[FileAllowed(["jpg", "png"])])
    rating = IntegerField(
        "My rating", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=500)]
    )
    notes = TextAreaField("Notes", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Submit")
