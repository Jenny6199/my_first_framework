from typing import List
from rhinoceros.urls import Url


class Rhinoceros:
    """This is the incoming point of this framework"""

    __slots__ = ('urls',)

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ, start_response):
        data = b'Hello World from Rhinoceros!\n'
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ])
        return iter([data])

    def _prepare_url(self, url: str):
        """
        method remove final symbol in url if it is '/'
        :param url:
        :return:
        """
        if url[-1] == '/':
            return url[:-1]
        return url
