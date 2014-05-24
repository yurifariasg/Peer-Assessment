from django.conf.urls import patterns, include, url
import app

urlpatterns = patterns('',
    # Place routes here
    url(r'^$', 'app.views.index'),
    url(r'^register$', 'app.views.register'),
)
