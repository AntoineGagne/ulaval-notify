from requests import Request
from pkg_resources import resource_filename

from .constants import BASE_URL


def create_request(session_manager):
    return Request(
        'GET',
        NotificationManager.notification_route,
        params={
            'idutilisateurmpo': session_manager.user_details.user_id,
            'statutpublication': 'PUBLIE'
        },
        headers={
            'Authorization': '{token_type} {token}'.format(
                token_type=session_manager.token_details.token_type,
                token=session_manager.token_details.token
            ),
            'Accept': 'application/json, text/plain, */*'
        }
    )


class NotificationManager:
    notification_route = '{base_url}/communication/v1/messagesimportants'.format(
        base_url=BASE_URL
    )

    def __init__(self, session_manager, callback, create_request):
        self._session_manager = session_manager
        self._callback = callback
        self._seen_notifications = set()
        self._create_request = create_request

    def check_notifications(self):
        response = self._session_manager.send(self._create_request(self._session_manager))
        if not response:
            return

        self._display_notifications(
            notification for notification
            in response.get('messagesImportants', ())
            if notification.get('idMessageImportant')
            not in self._seen_notifications
        )

    def _display_notifications(self, notifications):
        for notification in notifications:
            self._seen_notifications.add(
                notification.get('idMessageImportant')
            )
            self._callback(notification)


def send_linux_notification(notification):
    import notify2
    notify2.init('ulaval-notify')
    notification = notify2.Notification(
        'New notification',
        '{message}'.format(message=notification.get('messageHtml')),
        resource_filename('ulaval_notify', 'resources/images/ulaval-logo.png')
    )
    notification.show()


def find_appropriate_notification_callback(platform_name):
    notification_callbacks_by_platform_name = {
        'linux': send_linux_notification
    }

    notification_callback = send_linux_notification
    for platform, callback in notification_callbacks_by_platform_name.items():
        if platform_name.startswith(platform):
            notification_callback = callback

    return notification_callback
