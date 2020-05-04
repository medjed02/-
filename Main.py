from flask import Flask, render_template, redirect
from data import db_session
from data.genres import Genre
from data.users import User
from data.mangas import Manga
from data.chapters import Chapter
from data.register_form import RegisterForm
from data.login_form import LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def main_page():
    session = db_session.create_session()
    dop = session.query(Genre).all()
    genres = []
    for i in range(0, len(dop), 2):
        genres.append([dop[i], dop[i + 1]])
    return render_template("main_page.html", dop=genres, title="Мангеил")


@app.route('/register', methods=['POST', 'GET'])
def register():
    session = db_session.create_session()
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register_page.html', title='Регистрация',
                                   message="Пользователь с таким именем уже существует", form=form)
        user = User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user, remember=False)
        return redirect("/")
    return render_template('register_page.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_page.html',
                               message="Неправильный адрес почты или пароль",
                               form=form)
    return render_template('login_page.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
    app.run(port=8080, host="127.0.0.1")


if __name__ == '__main__':
    main()