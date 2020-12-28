"""
WSGI config for meiduo_mall project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 开发环境
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

# 线上生产环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.prod")

application = get_wsgi_application()
