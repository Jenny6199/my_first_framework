import re
from typing import List, Type
from rhinoceros.exceptions import NotAllowed, NotFound
from rhinoceros.urls import Url
from rhinoceros.view import View
from rhinoceros.request import Request


class Rhinoceros:
    """This is the incoming point of this framework"""

    __slots__ = ('urls',)

    def __init__(self, urls: List[Url]):
        """
        Конструктор класса Rhinoceros
        :param urls: List[Url]
        """
        self.urls = urls

    def __call__(self, environ, start_response):
        """
        Функция вызываемая при обращении к классу
        :param environ: список переменных окружения
        :param start_response: начальный ответ
        :return: iter([response])
        """
        view = self._get_view(environ)
        request = self._get_request(environ)
        raw_response = self._get_response(environ, view, request)
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
        """
        Method for find match view for definitions in framework
        :param raw_url: string with query params
        :return: path.view
        """
        url = self._prepare_url(raw_url)
        for path in self.urls:
            match = re.match(path.url, url)
            if match is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ) -> View:
        """
        Method return view that it is equvivalen for query
        :param environ: environment
        :return: view
        """
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)()
        return view

    def _get_request(self, environ: dict):
        """
        Обрабатывает полученный запрос
        :param environ: переменные окружения
        :return: Request(environ)
        """
        return Request(environ)

    def _get_response(self, environ: dict, view: View, request: Request):
        """
        Метод подготавливает ответ
        :param environ: переменные окружения
        :param view: объект класса View
        :param request: объект класса Request
        :return: getattr(view, method)(None)
        """
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllowed
        return getattr(view, method)(None)
