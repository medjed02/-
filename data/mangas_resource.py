from flask_restful import abort, Resource
from data import db_session
from data.mangas import Manga
from flask import jsonify
from data import parsers
import shutil
import os


def abort_if_manga_not_found(manga_id):  # Проверка на существование манги с заданным id
    session = db_session.create_session()
    manga = session.query(Manga).get(manga_id)
    if not manga:
        abort(404, message=f"Manga {manga_id} not found")


def abort_if_manga_found(manga_id):  # Проверка на существование манги с заданным id (обратная)
    session = db_session.create_session()
    manga = session.query(Manga).get(manga_id)
    if manga:
        abort(404, message=f"Manga {manga_id} already exists")


class MangasResource(Resource):  # Ресурс манги
    def get(self, manga_id):  # Обработчик запроса на получение конкретной манги (с заданным id)
        abort_if_manga_not_found(manga_id)
        session = db_session.create_session()
        manga = session.query(Manga).get(manga_id)
        return jsonify(
            {
                "manga": manga.to_dict()
            }
        )

    def delete(self, manga_id):  # Обработчик запроса на удаление конкретной манги (с заданным id)
        abort_if_manga_not_found(manga_id)
        args = parsers.delete_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        manga = session.query(Manga).get(manga_id)
        for genre in manga.genres:
            genre.mangas.remove(manga)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/' + str(manga_id) + "_manga")
        shutil.rmtree(path)
        session.delete(manga)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, manga_id):  # Обработчик запроса на редактирование конкретной манги (с заданным id)
        abort_if_manga_not_found(manga_id)
        args = parsers.genre_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        manga = session.query(Manga).get(manga_id)
        for key in args:
            if key == "name":
                manga.name = args[key]
            elif key == "author":
                manga.author = args[key]
            elif key == "painter":
                manga.painter = args[key]
            elif key == "translate":
                manga.translate = args[key]
            elif key == "date_of_release":
                manga.date_of_release = args[key]
            elif key == "translators":
                manga.translators = args[key]
            elif key == "description":
                manga.description = args[key]

        session.commit()
        return jsonify({'success': 'OK'})


class MangasListResource(Resource):  # Класс списка манг
    def get(self):  # Обработчик запроса на получение всех манг
        session = db_session.create_session()
        mangas = session.query(Manga).all()
        return jsonify(
            {
                'mangas': [item.to_dict() for item in mangas]
            }
        )