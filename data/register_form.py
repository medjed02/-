from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('E-mail адрес', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired(),
                                                                    EqualTo("password",
                                                                            message="Пароли должны совпадать!")])
    submit = SubmitField('Регистрация')