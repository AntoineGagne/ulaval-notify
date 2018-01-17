from notify2 import Notification
from requests import Request

from .constants import BASE_URL


NOTIFICATION_ROUTE = '{base_url}/communication/v1/messagesimportants'.format(
    base_url=BASE_URL
)

def check_notifications(session_manager, callback):
    request = Request(
        NOTIFICATION_ROUTE,
        params={
            'idutilisateurmpo': session_manager.user_details.user_id,
            'statutpublication': 'PUBLIE'
        }
    )
    response = session_manager.send(request.prepare())
    callback(response)



def send_linux_notification(notifications_details):
    notify2.init('ulaval-notify')
    notification = Notification(
        'New notifications',
        notifications_details['nombreTotalMessagesImportants'],
        kwargs.get('icon', '')
    )
    notification.show()
