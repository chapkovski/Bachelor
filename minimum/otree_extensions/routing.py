from django.urls import re_path
from .consumers import TaskConsumer
websocket_routes = [
    re_path(r'^tasktracker/(?P<player_id>[0-9]+)$', TaskConsumer),
]
