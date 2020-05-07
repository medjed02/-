from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed


class MessageForm(FlaskForm):   # форма редактирования/добавления поста
    name = StringField('Тема', default='Без темы')
    content = TextAreaField('Текст поста', validators=[DataRequired()])
    image = FileField('Добавить изображение (необязательно)',
                      validators=[FileAllowed(['jpg', 'png'], 'Прикреплять можно только изображения')], default='')
    submit = SubmitField('Сохранить')