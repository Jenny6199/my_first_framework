class Rhinoceros:
    """This is the incoming point of this framework"""
    def __call__(self, environ, start_response):
        data = b'Hello World from Rhinoceros!\n'
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ])
        return iter([data])
