from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class EditUserInfoForm(FlaskForm):
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('E-mail адрес', validators=[DataRequired()])
    image = FileField('Прикрепите аватарку (необязательно)',
                      validators=[FileAllowed(['jpg', 'png'], 'Прикреплять можно только изображения')], default='')
    submit = SubmitField('Сохранить изменения')