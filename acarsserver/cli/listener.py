#!/usr/bin/python

import socket
import sys

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.config import environment
from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.mapper.db.message import MessageDbMapper
from acarsserver.mapper.input.aircraft import AircraftInputMapper
from acarsserver.mapper.input.client import ClientInputMapper
from acarsserver.mapper.input.message import MessageInputMapper
from acarsserver.repository.aircraft import AircraftRepository
from acarsserver.repository.client import ClientRepository
from acarsserver.repository.message import MessageRepository
from acarsserver.service.image import ImageService
from acarsserver.service.logger import LoggerService

HOST = '' # all available interfaces
PORT = environment.listener_port

logger = LoggerService().get_instance()

# create udp socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.info('Socket created.')
except OSError as msg:
    logger.error('Failed to create socket. Error:' + msg)
    sys.exit()

# bind socket to local host and port
try:
    sock.bind((HOST, PORT))
except OSError as msg:
    logger.error('Bind failed. Error: ' + msg)
    sys.exit()

logger.info('Socket bind complete.')

adapter = SqliteAdapter.get_instance()

while True:
    try:
        # receive data from client
        request = sock.recvfrom(1024)
        data = request[0].decode().split(' ')
        address = request[1]
        ip = address[0]
        port = address[1]

        client = ClientInputMapper.map(ip)
        identical = ClientRepository(adapter).fetch_identical(client)
        if identical:
            ClientDbMapper(adapter).update(identical)
            client = identical
        else:
            ClientDbMapper(adapter).insert(client)
            client = ClientRepository(adapter).fetch_identical(client)

        aircraft = AircraftInputMapper.map(data[9].strip('.'))
        identical = AircraftRepository(adapter).fetch_identical(aircraft)
        if identical:
            aircraft = identical
        else:
            AircraftDbMapper(adapter).insert(aircraft)
            aircraft = AircraftRepository(adapter).fetch_identical(aircraft)

        msg = MessageInputMapper.map(data, aircraft, client)
        identical = MessageRepository(adapter).fetch_identical(msg)
        if identical:
            MessageDbMapper(adapter).update(identical, client)
            msg = identical
        else:
            MessageDbMapper(adapter).insert(msg, aircraft, client)
            msg = MessageRepository(adapter).fetch_identical(msg)

        ImageService(adapter, logger).handle(aircraft)

        logger.info('Message from client {}:{}\n{}'.format(ip, port, str(msg)))
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Exiting gracefully.')
        break

adapter.connection.close()

sock.close()
