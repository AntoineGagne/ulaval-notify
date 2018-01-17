import getpass

import requests

from .api.login import User, login


def main():
    with requests.Session() as session:
        username = input('Username: ')
        password = getpass.getpass()
        session_manager = login(
            session,
            User(username=username, password=password)
        )
        session_manager.refresh()
