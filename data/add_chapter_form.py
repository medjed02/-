from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class AddChapterForm(FlaskForm):
    chapter_name = StringField('Название главы', validators=[DataRequired()])
    manga_name = StringField('Название манги', validators=[DataRequired()])
    number = IntegerField('Номер главы', validators=[DataRequired('Номер главы должен быть числом')])
    zip = FileField('Прикрепите zip-архив со старницами манги',
                    validators=[FileRequired(), FileAllowed(['zip'], 'Прикреплять можно только zip-архивы')])
    submit = SubmitField('Добавить главу')