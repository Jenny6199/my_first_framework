import re
from typing import List, Type
from rhinoceros.exceptions import NotAllowed
from rhinoceros.urls import Url
from rhinoceros.view import View


class Rhinoceros:
    """This is the incoming point of this framework"""

    __slots__ = ('urls',)

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ, start_response):
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)()
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllowed
        raw_response = getattr(view, method)(None)
        response = raw_response.encode('utf-8')
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response)))
        ])
        return iter([response])

    def _prepare_url(self, url: str):
        """
        method remove final symbol in url if it is '/'
        :param url:
        :return:
        """
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            match = re.match(path.url, url)
            if match is not None:
                return path.view
