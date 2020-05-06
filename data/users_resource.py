from flask_restful import abort, Resource
from data import db_session
from data.users import User
from flask import jsonify


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_user_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        abort(404, message=f"User {user_id} already exists")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                "user": user.to_dict()
            }
        )


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [item.to_dict() for item in users]
            }
        )