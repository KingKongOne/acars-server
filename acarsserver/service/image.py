import json
import os
from urllib import request


class Image:

    URL_MEDIAWIKI = 'https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:{}_(aircraft)&gcmtype=file&redirects=1&prop=imageinfo&iiprop=url&format=json'

    @staticmethod
    def get_aircraft_image(aircraft):
        response = request.urlopen(Image.URL_MEDIAWIKI.format(aircraft))

        data = json.loads(response.read().decode('utf-8'))
        pages = data['query']['pages']

        return [elem for elem in pages.values()][0]['imageinfo'][0]['url']

    @staticmethod
    def exists(aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        return os.path.isfile('{}/../app/assets/aircrafts/{}.jpg'.format(path, aircraft.lower()))

    @staticmethod
    def download_aircraft_image(url, aircraft):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = '{}/../app/assets/aircrafts/{}.{}'.format(path, aircraft.lower(), url.split('.')[-1:][0])

        request.urlretrieve(url, filename)
