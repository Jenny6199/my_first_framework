from rhinoceros.view import View


class Homepage(View):

    def get(self, request, *args, **kwargs):
        return 'Hello World form View'
