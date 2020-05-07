from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AddMangaForm(FlaskForm):  # Форма добавления манги
    name = StringField('Название манги', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    painter = StringField('Художник', validators=[DataRequired()])
    translate = StringField('Перевод', validators=[DataRequired()])
    date_of_release = IntegerField('Дата релиза', validators=[DataRequired('Дата релиза должна быть числом')])
    translators = StringField('Переводчики', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    genres = StringField('Жанры', validators=[DataRequired()])
    cover = FileField('Обложка',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Прикреплять можно только изображения')])
    submit = SubmitField('Добавить мангу')