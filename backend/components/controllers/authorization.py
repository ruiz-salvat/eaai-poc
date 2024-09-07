from flask import request, session, render_template, redirect, Blueprint, jsonify, Response
from components.models import db_session, User, Client, AuthorizationCode
from components.oauth import CurrentServer, require_oauth
from components.utils import current_user, split_by_crlf
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token
from werkzeug.security import gen_salt
import time


authorization_controller = Blueprint('AutorizationController', __name__, template_folder='controllers')


@authorization_controller.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        print('\nusername:')
        print(username)
        print('---\n')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db_session.add(user)
            db_session.commit()
        session['id'] = user.id
        return jsonify({'user_id': session['id']})
    
    user = current_user()
    if user:
        clients = Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)


@authorization_controller.route('/create-client', methods=['GET', 'POST'])
def create_client():
    if 'User-Id' in request.headers: # TODO: refactor for reuse
        session['id'] = request.headers.get('User-Id')

    user = current_user()
    if not user:
            return Response(status=401)
    
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id
    )
    client_metadata = {}
    try:
        form = request.form
        print('\nform:', flush=True)
        print(form, flush=True)
        print(form.get('client_name'), flush=True)
    except:
        print('error at accessing form', flush=True)
    try:
        client_metadata = {
            "client_name": form.get('client_name'),
            "client_uri": form.get('client_uri'),
            "grant_types": split_by_crlf(form.get('grant_types')),
            "redirect_uris": split_by_crlf(form.get('redirect_uris')),
            "response_types": split_by_crlf(form.get('response_types')),
            "scope": form.get('scope'),
            "token_endpoint_auth_method": form.get('token_endpoint_auth_method')
        }
        print('\nclient metadata: ', flush=True)
        print(client_metadata, flush=True)
    except Exception as e:
        print('\nhmm\n', flush=True)
        print(e, flush=True)

    try:
        client.set_client_metadata(client_metadata)
        client.client_secret = gen_salt(48)
        print('\nAA\n', flush=True)
    except Exception as e:
        print('\nBB\n', flush=True)
        print(e, flush=True)
        return Response(status=400)
    
    try:
        db_session.add(client)
        db_session.commit()
    except Exception as e:
        print('\nAt except\n')
        print(e)
    
    return jsonify({'user_id': session['id'], 'client_id': client_id, 'client_secret': client.client_secret})


@authorization_controller.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if 'User-Id' in request.headers: # TODO: refactor for reuse
        session['id'] = request.headers.get('User-Id')

    user = current_user()
    if not user:
            return Response(status=401)
    print(f'user:\n{user.__dict__}', flush=True)
    if request.method == 'GET':
        try:
            grant = CurrentServer.server.get_consent_grant(end_user=user)
        except OAuth2Error as error:
            return error.error
        
        client = grant.client
        # scope = client.get_allowed_scope(grant.request.scope)
        
        # scopes = describe_scope(scope)
        return render_template(
            'authorize.html',
            grant=grant,
            user=user,
            client=client,
            # scopes=scopes,
        )
    
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

    if request.form['confirm']:
        CurrentServer.server.create_authorization_response(grant_user=user)
    else:
        CurrentServer.server.create_authorization_response(grant_user=None)

    authorization = AuthorizationCode.query.filter_by(user_id=user.id).order_by(AuthorizationCode.id.desc()).first()

    return jsonify({'authorization_code': authorization.code})


@authorization_controller.route('/issue-token', methods=['POST'])
def issue_token():
    return CurrentServer.server.create_token_response()


@authorization_controller.route('/revoke-token', methods=['POST'])
def revoke_token():
    return CurrentServer.server.create_endpoint_response('revocation')


@authorization_controller.route('/logout')
def logout():
    del session['id']
    return redirect('/home')


@authorization_controller.route('/api/me')
@require_oauth()
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)