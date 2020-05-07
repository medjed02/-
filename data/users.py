import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


# Дополнительная таблица для отношения "многие ко многим" манг и пользователей
association_table = sqlalchemy.Table('mangas_to_users', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('mangas', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('mangas.id')),
                                     sqlalchemy.Column('users', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('users.id'))
                                     )


class User(SqlAlchemyBase, UserMixin, SerializerMixin):  # Класс пользователя
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True,
                              unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    mangas = orm.relation("Manga", secondary="mangas_to_users", backref="mangas")

    messages = orm.relation("Message", back_populates='user')

    def set_password(self, password):  # Функция установки пароля (с хэшированием)
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # Функция проверки пароля
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return "<User> {} {}".format(str(self.id), self.nickname)