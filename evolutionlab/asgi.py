"""
ASGI config for evolutionlab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application


from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolutionlab.settings')

application = get_asgi_application()

from websocketapp.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
            "http": application,
            "websocket": URLRouter(websocket_urlpatterns) 
                       })
