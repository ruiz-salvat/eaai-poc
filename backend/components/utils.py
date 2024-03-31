from authlib.oauth2.rfc6749 import grants
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator
from components.models import db_session, Token, User, Client, AuthorizationCode
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.integrations.sqla_oauth2 import create_query_client_func, create_save_token_func


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        client = request.client
        auth_code = AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id,
        )
        db_session.add(auth_code)
        db_session.commit()
        return auth_code

    def query_authorization_code(self, code, client):
        item = AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db_session.delete(authorization_code)
        db_session.commit()

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        return Token.query.filter_by(access_token=token_string).first()


require_oauth = ResourceProtector() # TODO move to app.py? is a decorator?
require_oauth.register_token_validator(MyBearerTokenValidator())


class CurrentServer():
    server = None
    
    @staticmethod
    def init(app):
        query_client = create_query_client_func(db_session, Client)
        save_token = create_save_token_func(db_session, Token)
        CurrentServer.server = AuthorizationServer(
            app, query_client=query_client, save_token=save_token
        )
        CurrentServer.server.register_grant(AuthorizationCodeGrant)