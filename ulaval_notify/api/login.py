#! /usr/bin/env python

import re
import json

from .constants import BASE_URL, AUTHENTICATION_PAGE_URL, COOKIE_REGEX, OAUTH_API_URL


AUTHORIZATION = {}


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class LoginManager:
    def __init__(self, session):
        self.session = session

    def fetch_cookies(self, location_url):
        return self.session.get(location_url)

    def login(self, user, login_url):
        url = '{0}/my.policy'.format(login_url)
        parameters = user.__dict__.copy()
        parameters.update({'vhost': 'standard', 'rememberMe': '0'})
        response = self.session.post(url, params=parameters)
        match = re.search(COOKIE_REGEX, response.text)
        cookie_content = json.loads(json.loads(match.group('cookie_content')))
        AUTHORIZATION.update(cookie_content)
        self.session.cookies.set(
            match.group('cookie_name'),
            cookie_content,
            domain='monportail.ulaval.ca',
            path='/public/modules/mpo-client/services/securestorage/cookie/',
            secure=True
        )
