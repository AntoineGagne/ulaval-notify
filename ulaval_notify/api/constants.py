API_URL = 'https://api.ulaval.ca/ul/auth/oauth/v2'

AUTHENTICATION_PAGE_URL = 'https://authentification.ulaval.ca'

BASE_URL = 'https://monportail.ulaval.ca'

LOCATION_URL = '{base_url}/auth/deleguer/?urlretour={base_url}/'.format(base_url=BASE_URL)

COOKIE_REGEX = r'serviceSecureStorage.setItem\((?P<cookie_name>"mpo.securite.contexteUtilisateur"), (?P<cookie_content>.+)\);'

NOTIFICATION_CALLBACKS_BY_PLATFORM_NAME = {
    'linux': send_linux_notification
}
