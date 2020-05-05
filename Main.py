from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.genres import Genre
from data.users import User
from data.mangas import Manga
from data.chapters import Chapter
from data.register_form import RegisterForm
from data.login_form import LoginForm
from data.edit_user_info_form import EditUserInfoForm
from data.edit_user_password_form import EditUserPasswordForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from PIL import Image


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/", methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        session = db_session.create_session()
        dop = session.query(Genre).all()
        genres = []
        for i in range(0, len(dop), 2):
            genres.append([dop[i], dop[i + 1]])
        return render_template("main_page.html", dop=genres, title="Мангеил")
    elif request.method == 'POST':
        if request.form['input-search']:
            return redirect(f"/search/{request.form['input-search']}")
        else:
            return redirect("/")


@app.route('/register', methods=['POST', 'GET'])
def register():
    session = db_session.create_session()
    form = RegisterForm()
    if form.validate_on_submit():
        if session.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register_page.html', title='Регистрация',
                                   message="Пользователь с таким именем уже существует", form=form)
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register_page.html', title='Регистрация',
                                   message="Пользователь с таким e-mail уже существует", form=form)
        user = User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        if form.image.data != '':
            print(form.image.data, type(form.image.data))
            image_file = form.image.data
            image_filename = "static/img/" + str(user.id) + "_avatar" + '.jpg'
            image_file.save(os.path.join(image_filename))
            image_for_cut = Image.open(image_filename)
            width = image_for_cut.size[0]
            height = image_for_cut.size[1]
            if width > height:
                space = (width - height) // 2
                cut_image = image_for_cut.crop((space, 0, width - space, height))
            else:
                space = (height - width) // 2
                cut_image = image_for_cut.crop((0, space, width, height - space))
            cut_image.save(image_filename)
        else:
            image_filename = "/static/img/Hatsune_Miku.jpg"
        user.avatar = image_filename
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
                               message="Неправильный никнейм или пароль",
                               form=form)

    return render_template('login_page.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/user_page/<int:id>")
@login_required
def user_page(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    if not user:
        abort(404)
    return render_template("user_page.html", user=user, title=current_user.nickname)


@app.route('/edit_user_info/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_user_info(id):
    form = EditUserInfoForm()
    if request.method == "GET":
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            form.nickname.data = user.nickname
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.nickname == form.nickname.data, User.id != current_user.id).first():
            return render_template('edit_user_info_page.html', title='Редактирование профиля',
                                   message="Пользователь с таким именем уже существует", form=form)
        if session.query(User).filter(User.email == form.email.data, User.id != current_user.id).first():
            return render_template('edit_user_info_page.html', title='Редактирование профиля',
                                   message="Пользователь с таким e-mail уже существует", form=form)
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            user.nickname = form.nickname.data
            user.email = form.email.data
            session.commit()
            if form.image.data != '':
                image_file = form.image.data
                image_filename = "static/img/" + str(user.id) + "_avatar" + '.jpg'
                image_file.save(os.path.join(image_filename))
                image_for_cut = Image.open(image_filename)
                width = image_for_cut.size[0]
                height = image_for_cut.size[1]
                if width > height:
                    space = (width - height) // 2
                    cut_image = image_for_cut.crop((space, 0, width - space, height))
                else:
                    space = (height - width) // 2
                    cut_image = image_for_cut.crop((0, space, width, height - space))
                cut_image.save(image_filename)
            else:
                image_filename = user.avatar
            user.avatar = image_filename
            session.commit()
            return redirect('/user_page/' + str(user.id))
        else:
            abort(404)
    return render_template('edit_user_info_page.html', title='Редактирование профиля', form=form)


@app.route('/edit_user_password/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_user_password(id):
    form = EditUserPasswordForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            if user.check_password(form.password.data):
                user.set_password(form.new_password.data)
                session.add(user)
                session.commit()
                return redirect('/edit_user_info/' + str(user.id))
            else:
                return render_template('edit_user_password_form.html', message="Неправильный пароль", form=form)
        else:
            abort(404)
    return render_template('edit_user_password_form.html', title='Редактирование пароля', form=form)


@app.route("/genre_page/<int:id>", methods=['POST', 'GET'])
def genre_page(id):
    if request.method == "GET":
        session = db_session.create_session()
        genre = session.query(Genre).filter(Genre.id == id).first()
        if not genre:
            abort(404)                    
        return render_template("genre_page.html", genre=genre, title=genre.name_of_genre)
    elif request.method == 'POST':
        if request.form['input-search']:
            return redirect(f"/search/{request.form['input-search']}")
        else:
            return redirect(f"genre_page/{id}")


@app.route('/shaka_like_switch/<int:id>')
@login_required
def shaka_like_switch(id):
    session = db_session.create_session()
    manga = session.query(Manga).filter(Manga.id == id).first()
    user = session.query(User).filter(User.id == current_user.id).first()
    if not manga or not user:
        abort(404)
    if manga in user.mangas:
        user.mangas.remove(manga)
        manga.cnt_of_likes -= 1
    else:
        user.mangas.append(manga)
        manga.cnt_of_likes += 1
    session.commit()
    return redirect('/manga_page/' + str(id))
                            
                            
@app.route("/manga_page/<int:id>", methods=['POST', 'GET'])
def manga_page(id):
    if request.method == 'GET':
        session = db_session.create_session()
        manga = session.query(Manga).filter(Manga.id == id).first()
        if not manga:
            abort(404)
        if current_user.is_authenticated:
            user = session.query(User).filter(User.id == current_user.id).first()
            if not user:
                abort(404)
            else:
                user = ''
        return render_template("manga_page.html", manga=manga, title=manga.name, user=user)
    elif request.method == 'POST':
        if request.form['input-search']:
            return redirect(f"/search/{request.form['input-search']}")
        else:
            return redirect(f"/manga_page/{id}")


@app.route("/chapter_page/<int:manga_id>/<int:chapter_id>/<int:page_number>")
def chapter_page(manga_id, chapter_id, page_number):
    session = db_session.create_session()
    manga = session.query(Manga).filter(Manga.id == manga_id).first()
    chapter = session.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not manga or not chapter:
        abort(404)
    return render_template("chapter_page.html", manga=manga, chapter=chapter,
                           page_number=page_number, title=chapter.name)


@app.route("/search/<text>", methods=['POST', 'GET'])
def search_page(text):
    if request.method == 'GET':
        print(text)
        session = db_session.create_session()
        text = text.lower().capitalize()
        genres = session.query(Genre).filter(Genre.name_of_genre.like(f'%{text}%')).all()
        mangas = session.query(Manga).filter(Manga.name.like(f'%{text}%')).all()
        return render_template("search_page.html", mangas=mangas, genres=genres, title="Поиск")
    elif request.method == 'POST':
        if request.form['input-search']:
            return redirect(f"/search/{request.form['input-search']}")
        else:
            return redirect(f"/search/<text>")


def main():
    db_session.global_init("db/mangeil.sqlite")
    app.run(port=8080, host="127.0.0.1")


if __name__ == '__main__':
    main()