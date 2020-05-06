import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Chapter(SqlAlchemyBase):
    __tablename__ = 'chapters'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    manga_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("mangas.id"))
    manga = orm.relation('Manga')

    def to_dict(self):
        chapter = dict()
        chapter['id'] = self.id
        chapter['name'] = self.name
        chapter['content'] = self.content
        chapter['number'] = self.number
        chapter['manga_id'] = self.manga_id
        return chapter