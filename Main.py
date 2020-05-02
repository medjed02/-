from flask import Flask, render_template
from data import db_session
from data.genres import Genre
from data.mangas import Manga
from data.chapters import Chapter


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/genre_page/<int:id>")
def genre_page(id):
    session = db_session.create_session()
    genre = session.query(Genre).filter(Genre.id == id).first()
    return render_template("genre_page.html", genre=genre, title=genre.name_of_genre)


@app.route("/manga_page/<int:id>")
def manga_page(id):
    session = db_session.create_session()
    manga = session.query(Manga).filter(Manga.id == id).first()
    return render_template("manga_page.html", manga=manga, title=manga.name)


@app.route("/chapter_page/<int:manga_id>/<int:chapter_id>/<int:page_number>")
def chapter_page(manga_id, chapter_id, page_number):
    session = db_session.create_session()
    manga = session.query(Manga).filter(Manga.id == manga_id).first()
    chapter = session.query(Chapter).filter(Chapter.id == chapter_id).first()
    return render_template("chapter_page.html", manga=manga, chapter=chapter,
                           page_number=page_number, title=chapter.name)


def main():
    db_session.global_init("db/mangeil.sqlite")
    app.run()


if __name__ == '__main__':
    main()