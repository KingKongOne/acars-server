from datetime import datetime

from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.model.message import Message


class MessageDbMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, msg, client):
        self.adapter.execute(
            'INSERT INTO messages (aircraft, flight, first_seen, last_seen, client_id) VALUES (?, ?, ?, ?, ?)',
            (msg.aircraft, msg.flight, msg.first_seen, msg.last_seen, client.id)
        )
        self.adapter.connection.commit()

    def fetch_all(self, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        # the actual query
        self.adapter.execute(
            'SELECT id, aircraft_id, flight, strftime("%Y-%m-%d %H:%M:%S", "first_seen", "localtime"), ' + \
            'strftime("%Y-%m-%d %H:%M:%S", "last_seen", "localtime"), client_id ' + \
            'FROM messages ' + \
            'ORDER BY {} {} LIMIT {}'
            .format(
                order[0],
                order[1],
                limit
            )
        )
        results = self.adapter.fetchall()

        # map to models
        messages = []
        for result in results:
            client = ClientDbMapper(self.adapter).fetch(result[5])
            msg = Message(result, client)

            messages.append(msg)

        return messages
