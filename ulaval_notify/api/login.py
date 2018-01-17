#! /usr/bin/env python

import re
import json

from collections import namedtuple

from .constants import (AUTHENTICATION_PAGE_URL,
                        COOKIE_REGEX,
                        LOCATION_URL)
from .session import SessionManager


User = namedtuple('User', ['username', 'password'])


def login(session, user):
    session.get(LOCATION_URL)
    url = '{0}/my.policy'.format(AUTHENTICATION_PAGE_URL)
    parameters = user._asdict()
    parameters.update({'vhost': 'standard', 'rememberMe': '0'})
    response = session.post(url, params=parameters)
    match = re.search(COOKIE_REGEX, response.text)
    cookie_content = json.loads(json.loads(match.group('cookie_content')))
    return SessionManager(session, match.group('cookie_name'), cookie_content)
