"""This module handles the login to monPortail API.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

import re
import json

from collections import namedtuple

from .constants import (AUTHENTICATION_PAGE_URL,
                        COOKIE_REGEX,
                        LOCATION_URL)
from .session import SessionManager


#: Immutable type to hold the user's *IDUL* and the *password*
User = namedtuple('User', ['username', 'password'])


def login(session, user):
    """Login to monPortail API as the specified user.

    :param session: The HTTP session to use for the requests
    :param user: The user's credentials (IDUL and password)
    :returns: A session manager that handles refreshing the token and can make
              authenticated requests to the API
    """
    session.get(LOCATION_URL)
    url = '{0}/my.policy'.format(AUTHENTICATION_PAGE_URL)
    parameters = user._asdict()
    parameters.update({'vhost': 'standard', 'rememberMe': '0'})
    response = session.post(url, params=parameters)
    match = re.search(COOKIE_REGEX, response.text)
    cookie_content = json.loads(json.loads(match.group('cookie_content')))
    return SessionManager(session, match.group('cookie_name'), cookie_content)
