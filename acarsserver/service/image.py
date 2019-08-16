import json
import os
from urllib import request

from acarsserver.mapper.db.aircraft import AircraftDbMapper


class ImageService:

    MEDIAWIKI_URL = 'https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&' + \
        'gcmtitle=Category:{}_(aircraft)&gcmtype=file&redirects=1&prop=imageinfo&iiprop=url&format=json'
    adapter = None
    logger = None

    def __init__(self, adapter, logger):
        self.adapter = adapter
        self.logger = logger

    def handle(self, aircraft):
        # fetch the aircraft image if missing
        if not ImageService.exists(aircraft):
            self.logger.info('Downloading {} aircraft image.'.format(aircraft.registration))
            url = ImageService.get_url(aircraft)
            if url:
                filename = ImageService.download_image(url, aircraft)
                AircraftDbMapper(self.adapter).update(aircraft, filename)
                self.logger.info('Aircraft image downloaded.')
            else:
                self.logger.warning('Aircraft image URL could not be fetched.')

    @staticmethod
    def exists(aircraft):
        if not aircraft.image:
            return False

        path = os.path.dirname(os.path.realpath(__file__))
        return os.path.isfile('{}/../app/assets/img/aircrafts/{}'.format(path, aircraft.image))

    @staticmethod
    def get_url(aircraft):
        response = request.urlopen(ImageService.MEDIAWIKI_URL.format(aircraft.registration))

        data = json.loads(response.read().decode('utf-8'))
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']

            return [elem for elem in pages.values()][0]['imageinfo'][0]['url']

        return None

    @staticmethod
    def download_image(url, aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = '{}.{}'.format(aircraft.registration.lower(), url.split('.')[-1:][0].lower())
        filepath = '{}/../app/assets/img/aircrafts/{}'.format(path, filename)

        request.urlretrieve(url, filepath)

        return filename
