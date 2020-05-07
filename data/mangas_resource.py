from flask_restful import abort, Resource
from data import db_session
from data.mangas import Manga
from flask import jsonify
from data import parsers


def abort_if_manga_not_found(manga_id):
    session = db_session.create_session()
    manga = session.query(Manga).get(manga_id)
    if not manga:
        abort(404, message=f"Manga {manga_id} not found")


def abort_if_manga_found(manga_id):
    session = db_session.create_session()
    manga = session.query(Manga).get(manga_id)
    if manga:
        abort(404, message=f"Manga {manga_id} already exists")


class MangasResource(Resource):
    def get(self, manga_id):
        abort_if_manga_not_found(manga_id)
        session = db_session.create_session()
        manga = session.query(Manga).get(manga_id)
        return jsonify(
            {
                "manga": manga.to_dict()
            }
        )

    def delete(self, manga_id):
        abort_if_manga_not_found(manga_id)
        args = parsers.genre_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        manga = session.query(Manga).get(manga_id)
        for genre in manga.genres:
            genre.mangas.remove(manga)
        session.delete(manga)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, manga_id):
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


class MangasListResource(Resource):
    def get(self):
        session = db_session.create_session()
        mangas = session.query(Manga).all()
        return jsonify(
            {
                'mangas': [item.to_dict() for item in mangas]
            }
        )