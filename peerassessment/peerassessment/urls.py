from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import app

urlpatterns = patterns('',
    # Common Ajax Endpoints
    url(r'^register$', 'app.views.ajax.register'),
    url(r'^login$', 'app.views.ajax.login_user'),
    url(r'^logout$', 'app.views.ajax.logout_user'),

    # Assignments Endpoints
    url(r'^assignment/create$', 'app.views.assignments.create'),
    url(r'^assignment/submit$', 'app.views.assignments.submit'),

    # HTML Endpoints
    url(r'^student/$', 'app.views.html.student_dashboard'),
    url(r'^professor/$', 'app.views.html.professor_dashboard'),
    url(r'^$', 'app.views.html.index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
