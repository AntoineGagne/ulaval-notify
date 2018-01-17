from collections import namedtuple
from threading import Lock

from .constants import API_URL, BASE_URL


Token = namedtuple(
    'Token',
    ['client_id', 'token', 'token_type', 'expiration_date']
)

UserDetails = namedtuple(
    'UserDetails', [
        'user_id',
        'email',
        'identification_number',
        'first_name',
        'last_name',
        'username',
        'change_number'
    ]
)


def create_token(token_details):
    return Token(
        client_id=token_details['idClient'],
        token=token_details['token'],
        token_type=token_details['typeToken'],
        expiration_date=token_details['dateExpiration']
    )


def create_user_details(user_details):
    return UserDetails(
        user_id=user_details['idUtilisateurMpo'],
        email=user_details['courrielPrincipal'],
        identification_number=user_details['nie'],
        first_name=user_details['prenom'],
        last_name=user_details['nom'],
        username=user_details['pseudonyme'],
        change_number=user_details['numeroChangement']
    )


class SessionManager:
    refresh_token_route = '{base_url}/auth/rafraichirtoken'.format(
        base_url=BASE_URL
    )

    refresh_session_route = '{api_url}/refreshsession'.format(
        api_url=API_URL
    )

    def __init__(self, session, cookie_name, cookie_content):
        self._session = session
        self.__lock = Lock()
        self._cookie_name = cookie_name
        self._update_cookies(cookie_content)
        self.token_details = create_token(cookie_content['detailsToken'])
        self.user_details = create_user_details(cookie_content['utilisateurMpo'])

    def _update_cookies(self, cookie_content):
        self.session.cookies.set(
            self._cookie_name,
            cookie_content,
            domain='monportail.ulaval.ca',
            path='/public/modules/mpo-client/services/securestorage/cookie/',
            secure=True
        )

    @property
    def session(self):
        with self.__lock:
            return self._session

    def refresh(self):
        self._refresh_session()
        response = self._refresh_token().json()
        self._update_cookies(response)
        self.token_details = create_token(response['detailsToken'])

    def _refresh_session(self):
        self._session.post(SessionManager.refresh_session_route)

    def _refresh_token(self):
        return self.session.post(
            SessionManager.refresh_token_route,
            headers={
                'Authorization': '{token_type} {token}'.format(
                    token_type=self.token_details.token_type,
                    token=self.token_details.token
                ),
                'Accept': 'application/json, text/plain, */*'
            }
        )
