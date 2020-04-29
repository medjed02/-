import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)