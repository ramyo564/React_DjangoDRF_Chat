"""
WSGI config for djchat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter

# from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djchat.settings')
django_application = get_asgi_application()

from . import urls # noqa isort: skip


# application = get_wsgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
