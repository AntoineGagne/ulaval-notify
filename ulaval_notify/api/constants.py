"""This module contains the constants related to monPortail API.

:copyright: (c) 2018 by Antoine Gagné.
:license: MIT, see LICENSE for more details.
"""

#: The URL of monPortail API
API_URL = 'https://api.ulaval.ca/ul/auth/oauth/v2'

#: The authentication page URL
AUTHENTICATION_PAGE_URL = 'https://authentification.ulaval.ca'

#: The URL of the base website
BASE_URL = 'https://monportail.ulaval.ca'

#: The URL to set the needed cookies to log in
LOCATION_URL = '{base_url}/auth/deleguer/?urlretour={base_url}/'.format(
    base_url=BASE_URL
)

#: The regex that corresponds to the content of the cookie in the returned HTML
#: page
COOKIE_REGEX = (r'serviceSecureStorage.setItem\('
                r'(?P<cookie_name>"mpo.securite.contexteUtilisateur"),'
                r'(?P<cookie_content>.+)\);')
