import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


# Дополнительная таблица для отношения "многие ко многим" манг и жанров
association_table = sqlalchemy.Table('mangas_to_genres', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('mangass', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('mangas.id')),
                                     sqlalchemy.Column('genress', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('genres.id'))
                                     )


class Genre(SqlAlchemyBase):  # Класс жанра
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    mangas = orm.relation("Manga", secondary="mangas_to_genres", backref="genress")

    def __str__(self):
        return "<Genre> {} {}".format(str(self.id), self.name_of_genre)

    def to_dict(self):  # Функция преобразования нашего объекта в словарь (для API)
        genre = dict()
        genre['id'] = self.id
        genre['name_of_genre'] = self.name_of_genre
        genre['cover'] = self.cover
        genre['description'] = self.description
        genre['mangas'] = [str(item) for item in self.mangas]
        return genre