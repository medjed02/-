import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Manga(SqlAlchemyBase):  # Класс манги
    __tablename__ = 'mangas'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    painter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translate = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cnt_of_likes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date_of_release = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    translators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    chapters = orm.relation('Chapter', back_populates='manga')

    genres = orm.relation("Genre", secondary="mangas_to_genres", backref="mangass")

    def __str__(self):
        return "<Manga> {} {}".format(str(self.id), self.name)

    def to_dict(self):  # Функция преобразования нашего объекта в словарь (для API)
        manga = dict()
        manga['id'] = self.id
        manga['name'] = self.id
        manga['author'] = self.id
        manga['painter'] = self.id
        manga['translate'] = self.id
        manga['cnt_of_likes'] = self.id
        manga['date_of_release'] = self.id
        manga['translators'] = self.id
        manga['description'] = self.id
        manga['cover'] = self.id
        manga['genres'] = [str(item) for item in self.genres]
        manga['chapters'] = [item.to_dict() for item in self.chapters]
        return manga