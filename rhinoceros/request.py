from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict):
        pass

    def build_get_params_dict(self, raw_params: str):
        self.GET = parse_qs(raw_params)
