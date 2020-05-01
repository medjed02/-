from flask import Flask, render_template
from data import db_session
from data.genres import Genre


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/genre_page/<int:id>")
def genre_page(id):
    session = db_session.create_session()
    genre = session.query(Genre).filter(Genre.id == id).first()
    return render_template("genre_page.html", genre=genre)


def main():
    db_session.global_init("db/mangeil.sqlite")
    app.run()


if __name__ == '__main__':
    main()