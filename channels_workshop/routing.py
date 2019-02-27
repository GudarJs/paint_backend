from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from apps.paint.consumers import PaintConsumer


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter([
        path('ws/paint/<paint_name>/', PaintConsumer),
    ]),
})
