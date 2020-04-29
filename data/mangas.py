import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Manga(SqlAlchemyBase, SerializerMixin):
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

    chapters = orm.relation('Chapter', back_populates='manga')

    genres = orm.relation("Genre", secondary="mangas_to_genres", backref="mangass")

    def __repr__(self):
        return "<Manga> {} {}".format(str(self.id), self.name)