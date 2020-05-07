from flask_restful import abort, Resource
from data import db_session
from data.users import User
from flask import jsonify


def abort_if_user_not_found(user_id):  # Проверка на существование пользователя с заданным id
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_user_found(user_id):  # Проверка на существование пользователя с заданным id (обратная)
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        abort(404, message=f"User {user_id} already exists")


class UsersResource(Resource):  # Ресурс пользователя
    def get(self, user_id):  # Обработчик запроса на получение конкретного пользователя (с заданным id)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                "user": user.to_dict()
            }
        )


class UsersListResource(Resource):  # Ресурс списка пользователей
    def get(self):  # Обработчик запроса на получение всех пользователей
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [item.to_dict() for item in users]
            }
        )