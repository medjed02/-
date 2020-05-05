from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class EditUserPasswordForm(FlaskForm):
    password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    repeat_new_password = PasswordField('Повторите новый пароль',
                                        validators=[DataRequired(), EqualTo("new_password",
                                                                            message="Новые пароли должны совпадать!")])
    submit = SubmitField('Сохранить изменения')