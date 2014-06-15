"""
WSGI config for peerassessment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import settings

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peerassessment.settings")

from app.job_manager import JobManager
JobManager.start()


if settings.HEROKU:
    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling
    application = Cling(get_wsgi_application())

else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
