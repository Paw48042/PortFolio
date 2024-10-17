from . import consumers 
from django.urls import re_path, path

websocket_urlpatterns = [
    path(r"ws/location/map/", consumers.LocationTrack.as_asgi()),
    re_path(r"ws/mission/join/(?P<number>\d+)/$", consumers.LocationTrack.as_asgi()),
]

