from flask_restful import abort, Resource
from data import db_session
from data.genres import Genre
from flask import jsonify
from data import parsers
import os


def abort_if_genre_not_found(genre_id):  # Проверка на существование жанра с заданным id
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f"Genre {genre_id} not found")


def abort_if_genre_found(genre_id):  # Проверка на существование жанра с заданным id (обратная)
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)
    if genre:
        abort(404, message=f"Genre {genre_id} already exists")


class GenresResource(Resource):  # Ресурс жанра
    def get(self, genre_id):  # Обработчик запроса на получение конкретного жанра (с заданным id)
        abort_if_genre_not_found(genre_id)
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        return jsonify(
            {
                "genre": genre.to_dict()
            }
        )

    def delete(self, genre_id):  # Обработчик запроса на удаление конкретного жанра (с заданным id)
        abort_if_genre_not_found(genre_id)
        args = parsers.delete_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        for manga in genre.mangas:
            manga.genres.remove(genre)
        session.commit()
        session.delete(genre)
        session.commit()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/genres/' +
                            str(genre_id) + "_genre.jpg")
        os.remove(path)
        return jsonify({'success': 'OK'})

    def put(self, genre_id):  # Обработчик запроса на редактирование конкретного жанра (с заданным id)
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


class GenresListResource(Resource):  # Ресурс списка жанров
    def get(self):  # Обработчик запроса на получение всех жанров
        session = db_session.create_session()
        genres = session.query(Genre).all()
        return jsonify(
            {
                'genres': [item.to_dict() for item in genres]
            }
        )