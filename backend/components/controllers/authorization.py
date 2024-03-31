from flask import request, session, render_template, redirect, Blueprint
from components.models import db_session, User, Client
from components.utils import CurrentServer
from werkzeug.security import gen_salt
import time


authorization_controller = Blueprint('AutorizationController', __name__, template_folder='controllers')


def current_user():  # TODO move to utils
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@authorization_controller.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()

    if request.method == 'GET':
        grant = CurrentServer.server.get_consent_grant(end_user=user)
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
    
    confirmed = request.form['confirm']
    if confirmed:
        return CurrentServer.server.create_authorization_response(grant_user=user)
    
    return CurrentServer.server.create_authorization_response(grant_user=None)


@authorization_controller.route('/logout')
def logout():
    del session['id']
    return redirect('/home')


@authorization_controller.route('/issue_token', methods=['POST'])
def issue_token():
    return CurrentServer.server.create_token_response()


@authorization_controller.route('/revoke_token', methods=['POST'])
def revoke_token():
    return CurrentServer.server.create_endpoint_response('revocation')


@authorization_controller.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db_session.add(user)
            db_session.commit()
        session['id'] = user.id
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/home')
    user = current_user()
    if user:
        clients = Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)


def split_by_crlf(s):  # TODO move to utils
    return [v for v in s.splitlines() if v]


@authorization_controller.route('/create_client', methods=['GET', 'POST'])
def create_client():
    user = current_user()
    if not user:
        return redirect('/home')
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db_session.add(client)
    db_session.commit()
    return redirect('/home')