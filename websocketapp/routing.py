from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'celery/logs/$', consumers.CeleryLogConsumer),
    # re_path(r'ws/livec/$', consumers.Calculator.as_asgi()), 
    #  re_path(r"ws/celery_logs/$", consumers.CeleryLogConsumer.as_asgi()),
    #  re_path(r"ws/nginx_logs/$", consumers.NginxLogConsumer.as_asgi()),
     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
     re_path(r'^ws/sse/$', consumers.ServerSentEventsConsumer.as_asgi()),
]