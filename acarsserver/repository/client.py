from datetime import datetime

from acarsserver.model.client import Client


class ClientRepository():

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def fetch_identical(self, client):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE ip = ?', (client.ip,))
        result = self.adapter.fetchone()

        client = None
        if result:
            client = Client()
            client.id = result[0]
            client.ip = result[1]
            client.last_seen = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')
            client.is_online = True if ((datetime.now() - client.last_seen).seconds / 60) <= 30 else False

        return client

    def update(self, client):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE clients SET last_seen = ? WHERE id = ?',
            (now, client.id)
        )

        self.adapter.connection.commit()
