from flask_restful import abort, Resource
from data import db_session
from data.mangas import Manga
from flask import jsonify


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


class MangasListResource(Resource):
    def get(self):
        session = db_session.create_session()
        mangas = session.query(Manga).all()
        return jsonify(
            {
                'mangas': [item.to_dict() for item in mangas]
            }
        )