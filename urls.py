from rhinoceros.urls import Url
from view import Homepage

urlpatterns = [
    Url('^$', Homepage)
]
