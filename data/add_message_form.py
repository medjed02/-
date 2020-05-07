from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed


class MessageForm(FlaskForm):
    name = StringField('Тема', default='Без темы')
    content = TextAreaField('Текст поста', validators=[DataRequired()])
    submit = SubmitField('Сохранить')