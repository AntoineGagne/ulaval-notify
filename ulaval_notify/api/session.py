"""This module contains the code related to the session handling.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

from collections import namedtuple
from copy import copy
from threading import Lock, Timer

from requests import Request

from .constants import API_URL, BASE_URL


#: Immutable type that contains information about the session token
Token = namedtuple(
    'Token', [
        'client_id',
        'token',
        'token_type',
        'expiration_date'
    ]
)

#: Immutable type that contains information about the current user of the API
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


def refresh_periodically(interval, session_manager):
    """Refresh the session held by the session manager every given interval.

    :param interval: The number of time before refreshing the session
    :param session_manager: The session manager that will refresh the session
    """
    session_manager.refresh()
    timer = Timer(
        interval,
        refresh_periodically,
        args=(interval, session_manager)
    )
    timer.start()


def create_token(token_details):
    """Create a token based on the API response.

    :param token_details: The API response containing the token details
    :returns: The token details
    """
    return Token(
        client_id=token_details['idClient'],
        token=token_details['token'],
        token_type=token_details['typeToken'],
        expiration_date=token_details['dateExpiration']
    )


def create_user_details(user_details):
    """Create a type holding the user's details based on the API response.

    :param user_details: The API response containing the user's details
    :returns: The user details
    """
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
    """The session manager handles requests to the API related to the session.

    :param session: The API session
    :param cookie_name: The named of the cookie to set in the session
    :param cookie_content: The content of the cookie to set in the session
    """

    #: The route used to refresh the session token
    refresh_token_route = '{base_url}/auth/rafraichirtoken'.format(
        base_url=BASE_URL
    )

    #: The route used to refresh the session details
    refresh_session_route = '{api_url}/refreshsession'.format(
        api_url=API_URL
    )

    def __init__(self, session, cookie_name, cookie_content):
        """Create a new session manager."""
        self.__session = session
        self.__lock = Lock()
        self._cookie_name = cookie_name
        self._update_cookies(cookie_content)
        #: The details of the API session token
        self.token_details = create_token(cookie_content['detailsToken'])
        #: The details of the current user of the API
        self.user_details = create_user_details(cookie_content['utilisateurMpo'])

    def _update_cookies(self, cookie_content):
        with self.__lock:
            self.__session.cookies.set(
                self._cookie_name,
                cookie_content,
                domain='monportail.ulaval.ca',
                path='/public/modules/mpo-client/services/securestorage/cookie/',
                secure=True
            )

    @property
    def _session(self):
        return copy(self.__session)

    def send(self, request):
        """Send the given request with the current session.

        :param request: The request to send to the API
        :returns: The response of the API
        """
        response = None
        with self.__lock:
            request = self._add_authentication_header(request)
            response = self._session.send(
                self._session.prepare_request(request)
            )

        return response.json() if response else response

    def _add_authentication_header(self, request):
        request.headers['Authorization'] = '{token_type} {token}'.format(
            token_type=self.token_details.token_type,
            token=self.token_details.token
        )
        request.headers['Accept'] = 'application/json, text/plain, */*'

        return request

    def refresh(self):
        """Refresh the session."""
        self._refresh_session()
        response = self._refresh_token()
        self._update_cookies(response)
        self.token_details = create_token(response['detailsToken'])

    def _refresh_session(self):
        with self.__lock:
            self.__session.post(SessionManager.refresh_session_route)

    def _refresh_token(self):
        request = Request(
            'POST',
            SessionManager.refresh_token_route
        )

        return self.send(request)
