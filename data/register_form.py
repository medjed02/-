from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('E-mail адрес', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired(),
                                                                    EqualTo("password",
                                                                            message="Пароли должны совпадать!")])
    image = FileField('Прикрепите аватарку (необязательно)',
                      validators=[FileAllowed(['jpg', 'png'], 'Прикреплять можно только изображения')], default='')
    submit = SubmitField('Регистрация')