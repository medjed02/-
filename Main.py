from flask import Flask, render_template, redirect, request, abort, make_response
from data import db_session
from data.genres import Genre
from data.users import User
from data.messages import Message
from data.mangas import Manga
from data.add_message_form import MessageForm
from data.chapters import Chapter
from data.register_form import RegisterForm
from data.login_form import LoginForm
from data.edit_user_info_form import EditUserInfoForm
from data.edit_user_password_form import EditUserPasswordForm
from data.add_chapter_form import AddChapterForm
from data.add_manga_form import AddMangaForm
from data.add_genre_form import AddGenreForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource
from data import users_resource, genre_resource, mangas_resource, chapters_resource
from flask import jsonify
import datetime
import os
from PIL import Image
from zipfile import ZipFile  # Импортирование библиотек, объектов и пр.

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'  # Инициализация основных объектов


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/", methods=['POST', 'GET'])
def main_page():  # обработчик главной страницы
    if request.method == 'GET':
        session = db_session.create_session()
        dop = session.query(Genre).all()
        genres = []
        for i in range(0, len(dop), 2):
            if i + 1 == len(dop):
                dop[i].description = dop[i].description[:130] + '...'
                genres.append([dop[i]])
            else:
                dop[i].description = dop[i].description[:130] + '...'
                dop[i + 1].description = dop[i + 1].description[:130] + '...'
                genres.append([dop[i], dop[i + 1]])
        return render_template("main_page.html", dop=genres, title="Мангаил")


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
            image_file = form.image.data
            image_extension = image_file.filename[image_file.filename.rfind('.') + 1:]
            image_filename = "static/img/avatars/" + str(user.id) + "_avatar." + image_extension
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
            image_filename = "static/img/invariant/Hatsune_Miku.jpg"
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


@app.route("/user_page/<int:id>")  # Страница пользователя с его личной информацией
@login_required
def user_page(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    if not user:
        abort(404)
    return render_template("user_page.html", user=user, title=current_user.nickname)


@app.route('/edit_user_info/<int:id>', methods=['POST', 'GET'])  # Страница редактирования информации пользователя
@login_required
def edit_user_info(id):
    form = EditUserInfoForm()
    if request.method == "GET":  # Информация пользователся выводится для редактирования
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            form.nickname.data = user.nickname
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():  # Проверка информации
        session = db_session.create_session()
        if session.query(User).filter(User.nickname == form.nickname.data, User.id != current_user.id).first():
            return render_template('edit_user_info_page.html', title='Редактирование профиля',
                                   message="Пользователь с таким именем уже существует", form=form)
        if session.query(User).filter(User.email == form.email.data, User.id != current_user.id).first():
            return render_template('edit_user_info_page.html', title='Редактирование профиля',
                                   message="Пользователь с таким e-mail уже существует", form=form)
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:  # Запись информации
            user.nickname = form.nickname.data
            user.email = form.email.data
            session.commit()
            if form.image.data != '':  # Обработка аватарки
                image_file = form.image.data
                image_extension = image_file.filename[image_file.filename.rfind('.') + 1:]
                image_filename = "static/img/avatars/" + str(user.id) + "_avatar." + image_extension
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
def edit_user_password(id):  # Старница редактирования пароля
    form = EditUserPasswordForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:  # Проверка пользователя и пароля
            if user.check_password(form.password.data):
                user.set_password(form.new_password.data)  # Запись пароля
                session.add(user)
                session.commit()
                return redirect('/edit_user_info/' + str(user.id))
            else:
                return render_template('edit_user_password_form.html', message="Неправильный пароль", form=form)
        else:
            abort(404)
    return render_template('edit_user_password_form.html', title='Редактирование пароля', form=form)


@app.route('/add_chapter_page/<string:password>', methods=['POST', 'GET'])
def add_chapter_page(password):  # Старница добавления главы
    if password != 'DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin':
        abort(404)
    session = db_session.create_session()
    form = AddChapterForm()
    if form.validate_on_submit():  # Проверка информации
        manga = session.query(Manga).filter(Manga.name == form.manga_name.data).first()
        if not manga:
            return render_template('add_chpater_page.html', title='Добавление главы',
                                   message="Манги с таким названием не существует", form=form)
        if session.query(Chapter).filter(Chapter.number == form.number.data, Chapter.manga_id == manga.id).first():
            return render_template('add_chpater_page.html', title='Добавление главы',
                                   message="Глава с таким номером уже существует", form=form)
        if session.query(Chapter).filter(Chapter.name == form.chapter_name.data, Chapter.manga_id == manga.id).first():
            return render_template('add_chpater_page.html', title='Добавление главы',
                                   message="Глава с таким названием уже существует в этой манге", form=form)
        zip_file = form.zip.data
        zip_filename = "static/img/archive.zip"
        zip_file.save(os.path.join(zip_filename))
        with ZipFile(zip_filename, 'r') as piczip:
            pic_str = '%'.join(piczip.namelist())
        chapter = Chapter(  # Создание новой главы
            name=form.chapter_name.data,
            content=pic_str,
            number=form.number.data,
            manga_id=manga.id
        )
        session.add(chapter)
        manga.chapters.append(chapter)  # Добавление главы к манге
        session.commit()
        os.mkdir('static/img/' + str(manga.id) + '_manga/' + str(chapter.id) + '_chapter')  # Работа с архивом
        with ZipFile(zip_filename, 'r') as piczip:
            piczip.extractall('static/img/' + str(manga.id) + '_manga/' + str(chapter.id) + '_chapter')
        os.remove(zip_filename)
        return redirect("/add_chapter_page/DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin")
    return render_template('add_chpater_page.html', title='Добавление главы', form=form)


@app.route('/add_manga_page/<string:password>', methods=['POST', 'GET'])
def add_manga_page(password):  # Старница добавления манги
    if password != 'DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin':
        abort(404)
    session = db_session.create_session()
    form = AddMangaForm()
    if form.validate_on_submit():  # Проверка информации
        genres = str(form.genres.data).split(', ')
        for i in genres:
            if not session.query(Genre).filter(Genre.name_of_genre == i).first():
                return render_template('add_manga_page.html', title='Добавление манги',
                                       message="Вы указали несуществующий жанр", form=form)
        manga = Manga(  # Создание новой манги
            name=form.name.data,
            author=form.author.data,
            painter=form.painter.data,
            translate=form.translate.data,
            cnt_of_likes=0,
            date_of_release=form.date_of_release.data,
            translators=form.translators.data,
            description=form.description.data,
        )
        session.add(manga)
        session.commit()
        os.mkdir('static/img/' + str(manga.id) + '_manga')  # Создание папки манги и работа с обложкой
        image_file = form.cover.data
        image_extension = image_file.filename[image_file.filename.rfind('.') + 1:]
        image_filename = 'static/img/' + str(manga.id) + '_manga/' + str(manga.id) + '_manga.' + image_extension
        image_file.save(os.path.join(image_filename))
        manga.cover = '/' + image_filename
        for i in genres:  # Добавление жанров к манге
            genre = session.query(Genre).filter(Genre.name_of_genre == i).first()
            manga.genres.append(genre)
        session.commit()
        return redirect("/add_manga_page/DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin")
    return render_template('add_manga_page.html', title='Добавление манги', form=form)


@app.route('/add_genre_page/<string:password>', methods=['POST', 'GET'])
def add_genre_page(password):  # Страница добаления жанра
    if password != 'DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin':
        abort(404)
    session = db_session.create_session()
    form = AddGenreForm()
    if form.validate_on_submit():  # Проверка информации
        if session.query(Genre).filter(Genre.name_of_genre == form.name_of_genre.data).first():
            return render_template('add_genre_page.html', title='Добавление жанра',
                                   message="Такое имя жанра существует", form=form)
        genre = Genre(  # Создание новго жанра
            name_of_genre=form.name_of_genre.data,
            description=form.description.data,
        )
        session.add(genre)
        session.commit()
        image_file = form.cover.data  # Работа с иллюстрацией жанра
        image_extension = image_file.filename[image_file.filename.rfind('.') + 1:]
        image_filename = 'static/img/genres/' + str(genre.id) + '_genre.' + image_extension
        image_file.save(os.path.join(image_filename))
        genre.cover = '/' + image_filename
        session.commit()
        return redirect("/add_genre_page/DUK_Petyan_Kalinin_Mihail_Uryevich_Zamyatnin")
    return render_template('add_genre_page.html', title='Добавление жанра', form=form)


@app.route("/genre_page/<int:id>", methods=['POST', 'GET'])
def genre_page(id):  # Страница жанра
    if request.method == "GET":
        session = db_session.create_session()
        genre = session.query(Genre).filter(Genre.id == id).first()
        if not genre:
            abort(404)
        return render_template("genre_page.html", genre=genre, title=genre.name_of_genre)


@app.route('/shaka_like_switch/<int:id>')
@login_required
def shaka_like_switch(id):  # Установка и убирание лайка
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
def manga_page(id):  # Страница манги
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
        if user == '':
            flag = False
        else:
            flag = manga in user.mangas
        return render_template("manga_page.html", manga=manga, title=manga.name, user=user,
                               flag=flag)


@app.route("/chapter_page/<int:manga_id>/<int:chapter_id>/<int:page_number>")
def chapter_page(manga_id, chapter_id, page_number):  # Страница главы
    session = db_session.create_session()
    manga = session.query(Manga).filter(Manga.id == manga_id).first()
    chapter = session.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not manga or not chapter:
        abort(404)
    return render_template("chapter_page.html", manga=manga, chapter=chapter,
                           page_number=page_number, title=chapter.name)


@app.route("/search/<text>", methods=['POST', 'GET'])
def search_page(text):  # обработчик страницы поиска
    if request.method == 'GET':
        print(text)
        session = db_session.create_session()
        text = text.lower()
        a = session.query(Genre).all()
        genres = []
        mangas = []
        for genre in a:
            dop = genre.name_of_genre.lower()  # поиск результатов
            if dop in text or text in dop:
                genres.append(genre)
        a = session.query(Manga).all()
        for manga in a:
            dop = manga.name.lower()  # поиск результатов
            if dop in text or text in dop:
                mangas.append(manga)
        return render_template("search_page.html", mangas=mangas, genres=genres, title="Поиск")


@app.route("/handler", methods=['POST', 'GET'])
def handler():
    if request.method == "POST":
        if 'input-search' in request.form:
            if request.form['input-search']:
                return redirect(f"/search/{request.form['input-search']}")
            else:
                return redirect(f"/search/not_found")


@app.route("/forum", methods=['POST', 'GET'])
def forum():  # обработчик страницы поиска
    if request.method == 'GET':
        session = db_session.create_session()
        messages = session.query(Message).all()
        messages.reverse()
    if request.method == "POST":
        session = db_session.create_session()
        messages = session.query(Message).all()
        if "my_posts" in request.form:  # фильтрация по моим/всем постам
            if request.form["my_posts"]:
                id_dop = current_user.id
                messages = session.query(Message).filter(Message.user_id == id_dop).all()
        if request.form["new_or_old"]:  # фильтрация по новым/старым постам
            sort = request.form["new_or_old"]
            if sort == 'Сначала новые':
                messages.reverse()
        if request.form["interested_theme"]:  # фильтрация по теме
            theme = request.form["interested_theme"]
            a = messages[:]
            messages = []
            theme = theme.lower()
            for message in a:
                dop = message.name.lower()
                if theme in dop or dop in theme:
                    messages.append(message)
        if request.form["interested_author"]:  # фильтарция по автору
            author = request.form["interested_author"]
            a = messages[:]
            messages = []
            author = author.lower()
            for message in a:
                dop = message.user.nickname.lower()
                if author in dop or dop in author:
                    messages.append(message)
        if request.form["date1"]:  # фильтрация по дате
            date1 = request.form["date1"]
            a = messages[:]
            messages = []
            time1 = date1.split('-')
            time1.reverse()
            time1 = [int(i) for i in time1]
            for message in a:
                time2 = message.time.split()[0].split('.')
                time2 = [int(i) for i in time2]
                if time1[2] > time2[2]:
                    continue
                elif time2[2] > time1[2]:
                    messages.append(message)
                else:
                    if time1[1] > time2[1]:
                        continue
                    elif time2[1] > time1[1]:
                        messages.append(message)
                    else:
                        if time1[0] > time2[0]:
                            continue
                        else:
                            messages.append(message)
        if request.form["date2"]:  # фильтрация по дате
            date2 = request.form["date2"]
            a = messages[:]
            messages = []
            time1 = date2.split('-')
            time1.reverse()
            time1 = [int(i) for i in time1]
            for message in a:
                time2 = message.time.split()[0].split('.')
                time2 = [int(i) for i in time2]
                if time1[2] < time2[2]:
                    continue
                elif time2[2] < time1[2]:
                    messages.append(message)
                else:
                    if time1[1] < time2[1]:
                        continue
                    elif time2[1] < time1[1]:
                        messages.append(message)
                    else:
                        if time1[0] < time2[0]:
                            continue
                        else:
                            messages.append(message)
        if request.form['time1']:  # фильтрация по времени
            time1 = [int(i) for i in request.form['time1'].split(':')]
            time1 = time1[0] * 60 + time1[1]
            a = messages[:]
            messages = []
            for message in a:
                time2 = message.time.split()[1].split(':')
                time2 = int(time2[0]) * 60 + int(time2[1])
                if time1 > time2:
                    continue
                else:
                    messages.append(message)
        if request.form['time1']:  # фильтрация по времени
            time1 = [int(i) for i in request.form['time1'].split(':')]
            time1 = time1[0] * 60 + time1[1]
            a = messages[:]
            messages = []
            for message in a:
                time2 = message.time.split()[1].split(':')
                time2 = int(time2[0]) * 60 + int(time2[1])
                if time1 < time2:
                    continue
                else:
                    messages.append(message)

    return render_template("forum_page.html", messages=messages, title="Форум")


@app.route("/forum/add_post", methods=['POST', 'GET'])
def add_post():  # обработчик страницы добавления поста
    session = db_session.create_session()
    form = MessageForm()
    if form.validate_on_submit():
        time = datetime.datetime.now()
        if len(str(time.day)) == 1:
            day = '0' + str(time.day)
        else:
            day = time.day
        if len(str(time.month)) == 1:
            month = '0' + str(time.month)  # извлечение даты
        else:
            month = time.month
        if len(str(time.hour + 3)) == 1:
            hour = '0' + str(time.hour + 3)
        else:
            hour = time.hour + 3
        if len(str(time.minute)) == 1:
            minute = '0' + str(time.minute)
        else:
            minute = time.minute
        time = '.'.join([str(day), str(month), str(time.year)]) + ' ' + \
               ':'.join([str(hour), str(minute)])
        message = Message()  # извлечение всего остального
        message.name = form.name.data
        message.content = form.content.data
        message.user_id = current_user.id
        message.time = time
        session.add(message)
        session.commit()
        return redirect("/forum")
    else:
        return render_template('add_message.html', title='Добавление новости',
                               form=form, value_sumbit="Опубликовать")


@app.route("/forum/change_post/<int:id>", methods=['POST', 'GET'])
def change_post(id):  # обработчик страницы изменения поста
    form = MessageForm()
    if request.method == "GET":
        session = db_session.create_session()
        message = session.query(Message).filter(Message.id == id,
                                                Message.user == current_user).first()
        if message:
            form.name.data = message.name  # занесение данных в форму
            form.content.data = message.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        message = session.query(Message).filter(Message.id == id,
                                                Message.user == current_user).first()
        if message:
            message.name = form.name.data
            message.content = form.content.data
            session.commit()
            return redirect('/forum')
        else:
            abort(404)
    return render_template('add_message.html', title='Редактирование новости', form=form)


@app.route("/forum/delete_post/<int:id>", methods=['POST', 'GET'])
def delete_post(id):  # обработчик удаления поста
    session = db_session.create_session()
    message = session.query(Message).filter(Message.id == id,
                                            Message.user == current_user).first()
    if message:
        session.delete(message)
        session.commit()
    else:
        abort(404)
    return redirect('/forum')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():  # Добавление ресурсов для апи, инициализация базы данных и приложения
    api.add_resource(users_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/user/<int:user_id>')
    api.add_resource(genre_resource.GenresListResource, '/api/genres')
    api.add_resource(genre_resource.GenresResource, '/api/genre/<int:genre_id>')
    api.add_resource(mangas_resource.MangasListResource, '/api/mangas')
    api.add_resource(mangas_resource.MangasResource, '/api/manga/<int:manga_id>')
    api.add_resource(chapters_resource.ChaptersResource, '/api/chapter/<int:chapter_id>')
    db_session.global_init("db/mangeil.sqlite")
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()