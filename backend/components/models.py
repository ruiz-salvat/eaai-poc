from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


engine = create_engine('postgresql://root:pass@postgres:5432/postgres_groceries', echo = True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Model = declarative_base(name='Model')
Model.query = db_session.query_property()


def init_db():
    Model.metadata.create_all(bind=engine)


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    # other columns

    def get_user_id(self):
        return self.id
    

class Client(Model, OAuth2ClientMixin):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )
    user = relationship('User')


class Token(Model, OAuth2TokenMixin):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )
    user = relationship('User')


class AuthorizationCode(Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'authorization_codes'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )
    user = relationship('User')


class ApiKey(Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)