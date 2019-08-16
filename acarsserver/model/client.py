from datetime import datetime


class Client:

    id = None
    ip = None
    last_seen = None
    is_online = None

    def __str__(self):
        return 'ID: {}, IP:{}, Last Seen:{}, Is Online: {}'.format(
            self.id,
            self.ip,
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.is_online
        )
