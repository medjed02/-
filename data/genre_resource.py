from flask_restful import abort, Resource
from data import db_session
from data.genres import Genre
from flask import jsonify
from data import parsers


def abort_if_genre_not_found(genre_id):
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f"Genre {genre_id} not found")


def abort_if_genre_found(genre_id):
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)
    if genre:
        abort(404, message=f"Genre {genre_id} already exists")


class GenresResource(Resource):
    def get(self, genre_id):
        abort_if_genre_not_found(genre_id)
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        return jsonify(
            {
                "genre": genre.to_dict()
            }
        )

    def delete(self, genre_id):
        abort_if_genre_not_found(genre_id)
        args = parsers.genre_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        session.delete(genre)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, genre_id):
        abort_if_genre_not_found(genre_id)
        args = parsers.genre_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        for key in args:
            if key == "name_of_genre":
                genre.name = args[key]
            elif key == "description":
                genre.author = args[key]

        session.commit()
        return jsonify({'success': 'OK'})


class GenresListResource(Resource):
    def get(self):
        session = db_session.create_session()
        genres = session.query(Genre).all()
        return jsonify(
            {
                'genres': [item.to_dict() for item in genres]
            }
        )