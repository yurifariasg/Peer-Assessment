from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import app

urlpatterns = patterns('',
    # Place routes here
    url(r'^register$', 'app.views.register'),
    url(r'^$', 'app.views.index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()


