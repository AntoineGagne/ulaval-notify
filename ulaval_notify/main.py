import getpass

import requests

from .api.login import LoginManager, User

def main():
    with requests.Session() as SESSION:
        REQUEST = LoginManager(SESSION)
        LOCATION_URL = '{0}/auth/deleguer/?urlretour={0}/'.format(BASE_URL)
        REQUEST.fetch_cookies(LOCATION_URL)

        USERNAME = input('Username: ')
        PASSWORD = getpass.getpass()
        REQUEST.login(User(USERNAME, PASSWORD),
                                 AUTHENTICATION_PAGE_URL)
        RESPONSE = REQUEST.session.post("https://monportail.ulaval.ca/auth/rafraichirtoken/", headers={'Authorization': AUTHORIZATION['detailsToken']['token'], 'Accept': 'application/json, text/plain, */*'})
        print(json.dumps(RESPONSE.json()))
