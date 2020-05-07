from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AddGenreForm(FlaskForm):  # Форма добавления жанра
    name_of_genre = StringField('Название жанра', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    cover = FileField('Обложка',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Прикреплять можно только изображения')])
    submit = SubmitField('Добавить жанр')