from flask_restful import abort, Resource
from data import db_session
from data.chapters import Chapter
from flask import jsonify
from data import parsers
import os
import shutil


def abort_if_chapter_not_found(chapter_id):
    session = db_session.create_session()
    chapter = session.query(Chapter).get(chapter_id)
    if not chapter:
        abort(404, message=f"Chapter {chapter_id} not found")


def abort_if_genre_found(chapter_id):
    session = db_session.create_session()
    chapter = session.query(Chapter).get(chapter_id)
    if chapter:
        abort(404, message=f"Chapter {chapter_id} already exists")


class ChaptersResource(Resource):
    def get(self, chapter_id):
        abort_if_chapter_not_found(chapter_id)
        session = db_session.create_session()
        chapter = session.query(Chapter).get(chapter_id)
        return jsonify(
            {
                "chapter": chapter.to_dict()
            }
        )

    def delete(self, chapter_id):
        abort_if_chapter_not_found(chapter_id)
        args = parsers.delete_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        chapter = session.query(Chapter).get(chapter_id)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/img/' +
                            str(chapter.manga_id) + "_manga/" + str(chapter_id) + "_chapter")
        shutil.rmtree(path)
        chapter.manga.chapters.remove(chapter)
        session.delete(chapter)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, chapter_id):
        abort_if_chapter_not_found(chapter_id)
        args = parsers.chapter_parser.parse_args()
        if args['apikey'] != "specialkey":
            return jsonify({'Access is denied': 'message'})
        session = db_session.create_session()
        chapter = session.query(Chapter).get(chapter_id)
        for key in args:
            if key == "name":
                chapter.name = args[key]
            elif key == "content":
                chapter.content = args[key]
            elif key == "number":
                chapter.number = args[key]

        session.commit()
        return jsonify({'success': 'OK'})