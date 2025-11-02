from django.urls import path

from .consumers import BaseConsumer

websocket_urlpatterns = [
    path("ws/base/", BaseConsumer.as_asgi()),
]

