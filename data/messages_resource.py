from flask_restful import abort, Resource
from data import db_session
from data.messages import Message
from flask import jsonify


def abort_if_message_not_found(message_id):  # Проверка на существование поста с заданным id
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if not message:
        abort(404, message=f"Message {message_id} not found")


def abort_if_message_found(message_id):  # Проверка на существование поста с заданным id (обратная)
    session = db_session.create_session()
    message = session.query(Message).get(message_id)
    if message:
        abort(404, message=f"Message {message_id} already exists")


class MessagesResource(Resource):  # Ресурс поста
    def get(self, message_id):  # Обработчик запроса на получение конкретного поста (с заданным id)
        abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        return jsonify(
            {
                "message": message.to_dict()
            }
        )


class MessagesListResource(Resource):  # Ресурс списка постов
    def get(self):  # Обработчик запроса на получение всех постов
        session = db_session.create_session()
        messages = session.query(Message).all()
        return jsonify(
            {
                'messages': [item.to_dict() for item in messages]
            }
        )